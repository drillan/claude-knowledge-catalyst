"""File system watcher for monitoring .claude directory changes."""

import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

from .claude_md_processor import ClaudeMdProcessor
from .config import WatchConfig
from .metadata import MetadataManager


class KnowledgeFileEventHandler(FileSystemEventHandler):
    """Event handler for knowledge file changes."""

    def __init__(
        self,
        callback: Callable[[str, Path], None],
        watch_config: WatchConfig,
        metadata_manager: MetadataManager,
    ):
        """Initialize event handler.

        Args:
            callback: Function to call when files change (event_type, file_path)
            watch_config: Configuration for file watching
            metadata_manager: Manager for metadata operations
        """
        super().__init__()
        self.callback = callback
        self.watch_config = watch_config
        self.metadata_manager = metadata_manager
        self.debounce_cache: dict[str, float] = {}
        # Initialize CLAUDE.md processor
        self.claude_md_processor = ClaudeMdProcessor(
            sections_exclude=watch_config.claude_md_sections_exclude
        )

    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification events."""
        if not event.is_directory:
            self._handle_file_event("modified", Path(str(event.src_path)))

    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation events."""
        if not event.is_directory:
            self._handle_file_event("created", Path(str(event.src_path)))

    def on_deleted(self, event: FileSystemEvent) -> None:
        """Handle file deletion events."""
        if not event.is_directory:
            self._handle_file_event("deleted", Path(str(event.src_path)))

    def on_moved(self, event: FileSystemEvent) -> None:
        """Handle file move events."""
        if not event.is_directory and hasattr(event, "dest_path"):
            self._handle_file_event("moved", Path(str(event.dest_path)))

    def _handle_file_event(self, event_type: str, file_path: Path) -> None:
        """Handle file system events with debouncing."""
        if not self._should_process_file(file_path):
            return

        # Debouncing logic
        file_key = str(file_path)
        current_time = time.time()

        if file_key in self.debounce_cache:
            time_diff = current_time - self.debounce_cache[file_key]
            if time_diff < self.watch_config.debounce_seconds:
                return

        self.debounce_cache[file_key] = current_time

        # Process the event
        try:
            self.callback(event_type, file_path)
        except Exception as e:
            print(f"Error processing file event: {e}")  # noqa: T201

    def _should_process_file(self, file_path: Path) -> bool:
        """Check if file should be processed based on patterns."""
        file_str = str(file_path)

        # Check ignore patterns
        for pattern in self.watch_config.ignore_patterns:
            if pattern in file_str or file_path.match(pattern):
                return False

        # Check CLAUDE.md patterns if enabled
        if self.watch_config.include_claude_md:
            for pattern in self.watch_config.claude_md_patterns:
                if file_path.name == "CLAUDE.md" or file_path.match(pattern):
                    return True

        # Check file patterns
        for pattern in self.watch_config.file_patterns:
            if file_path.match(pattern):
                return True

        return False


class KnowledgeWatcher:
    """File system watcher for knowledge files."""

    def __init__(
        self,
        watch_config: WatchConfig,
        metadata_manager: MetadataManager,
        sync_callback: Callable[[str, Path], None] | None = None,
    ):
        """Initialize knowledge watcher.

        Args:
            watch_config: Configuration for file watching
            metadata_manager: Manager for metadata operations
            sync_callback: Callback function for sync operations
        """
        self.watch_config = watch_config
        self.metadata_manager = metadata_manager
        self.sync_callback = sync_callback or self._default_sync_callback
        self.observer = Observer()
        self.event_handler = KnowledgeFileEventHandler(
            self._handle_file_change,
            watch_config,
            metadata_manager,
        )
        # Initialize CLAUDE.md processor
        self.claude_md_processor = ClaudeMdProcessor(
            sections_exclude=watch_config.claude_md_sections_exclude
        )
        self.is_running = False
        self.watched_paths: set[Path] = set()

    def start(self) -> None:
        """Start watching for file changes."""
        if self.is_running:
            return

        # Add watch paths
        for watch_path in self.watch_config.watch_paths:
            self.add_watch_path(watch_path)

        self.observer.start()
        self.is_running = True
        print(f"Started watching {len(self.watched_paths)} paths")

    def stop(self) -> None:
        """Stop watching for file changes."""
        if not self.is_running:
            return

        self.observer.stop()
        self.observer.join()
        self.is_running = False
        print("Stopped file watching")

    def add_watch_path(self, path: Path) -> bool:
        """Add a path to watch.

        Args:
            path: Path to start watching

        Returns:
            True if path was added, False if already watched or invalid
        """
        if not path.exists():
            print(f"Warning: Watch path does not exist: {path}")
            return False

        if not path.is_dir():
            print(f"Warning: Watch path is not a directory: {path}")
            return False

        if path in self.watched_paths:
            return False

        self.observer.schedule(self.event_handler, str(path), recursive=True)
        self.watched_paths.add(path)
        print(f"Added watch path: {path}")
        return True

    def remove_watch_path(self, path: Path) -> bool:
        """Remove a path from watching.

        Args:
            path: Path to stop watching

        Returns:
            True if path was removed, False if not found
        """
        if path not in self.watched_paths:
            return False

        # Note: watchdog doesn't provide a direct way to remove specific paths
        # In practice, you would need to recreate the observer
        self.watched_paths.discard(path)
        print(f"Removed watch path: {path}")
        return True

    def _handle_file_change(self, event_type: str, file_path: Path) -> None:
        """Handle file change events."""
        print(f"File {event_type}: {file_path}")

        # Update metadata for existing files
        if event_type in ["modified", "created"] and file_path.exists():
            try:
                self._update_file_metadata(file_path)
            except Exception as e:
                print(f"Error updating metadata for {file_path}: {e}")

        # Trigger sync callback
        self.sync_callback(event_type, file_path)

    def _update_file_metadata(self, file_path: Path) -> None:
        """Update metadata for a file."""
        if file_path.suffix.lower() not in [".md", ".txt"]:
            return

        try:
            # Check if this is a CLAUDE.md file
            is_claude_md = (
                file_path.name == "CLAUDE.md" and self.watch_config.include_claude_md
            )

            if is_claude_md:
                # Use specialized CLAUDE.md metadata
                claude_metadata = self.claude_md_processor.get_metadata_for_claude_md(
                    file_path
                )
                # Extract standard metadata and merge
                metadata = self.metadata_manager.extract_metadata_from_file(file_path)

                # Update timestamp
                from datetime import datetime

                metadata.updated = datetime.now()

                # Add CLAUDE.md specific metadata
                for key, value in claude_metadata.items():
                    setattr(metadata, key, value)

            else:
                # Extract current metadata for regular files
                metadata = self.metadata_manager.extract_metadata_from_file(file_path)

                # Update timestamp
                from datetime import datetime

                metadata.updated = datetime.now()

            # Update metadata in file
            self.metadata_manager.update_file_metadata(file_path, metadata)

        except Exception as e:
            print(f"Error updating metadata for {file_path}: {e}")

    def _default_sync_callback(self, event_type: str, file_path: Path) -> None:
        """Default sync callback that just logs events."""
        print(f"Sync trigger: {event_type} - {file_path}")

    def scan_existing_files(self) -> list[Path]:
        """Scan existing files in watch paths."""
        existing_files = []

        for watch_path in self.watch_config.watch_paths:
            if not watch_path.exists():
                continue

            for pattern in self.watch_config.file_patterns:
                files = list(watch_path.rglob(pattern))
                existing_files.extend(files)

        return existing_files

    def process_existing_files(self) -> None:
        """Process all existing files to initialize metadata."""
        existing_files = self.scan_existing_files()

        print(f"Processing {len(existing_files)} existing files...")

        for file_path in existing_files:
            try:
                self._update_file_metadata(file_path)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        print("Finished processing existing files")

    def get_status(self) -> dict[str, Any]:
        """Get current watcher status."""
        return {
            "is_running": self.is_running,
            "watched_paths": [str(path) for path in self.watched_paths],
            "file_patterns": self.watch_config.file_patterns,
            "ignore_patterns": self.watch_config.ignore_patterns,
            "debounce_seconds": self.watch_config.debounce_seconds,
        }

    def __enter__(self) -> "KnowledgeWatcher":
        """Context manager entry."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        """Context manager exit."""
        self.stop()


class WatcherManager:
    """Manager for multiple watchers."""

    def __init__(self) -> None:
        """Initialize watcher manager."""
        self.watchers: dict[str, KnowledgeWatcher] = {}

    def add_watcher(self, name: str, watcher: KnowledgeWatcher) -> None:
        """Add a watcher with a name."""
        if name in self.watchers:
            self.watchers[name].stop()

        self.watchers[name] = watcher

    def remove_watcher(self, name: str) -> bool:
        """Remove a watcher by name."""
        if name not in self.watchers:
            return False

        self.watchers[name].stop()
        del self.watchers[name]
        return True

    def start_all(self) -> None:
        """Start all watchers."""
        for watcher in self.watchers.values():
            watcher.start()

    def stop_all(self) -> None:
        """Stop all watchers."""
        for watcher in self.watchers.values():
            watcher.stop()

    def get_status(self) -> dict[str, dict[str, Any]]:
        """Get status of all watchers."""
        return {name: watcher.get_status() for name, watcher in self.watchers.items()}
