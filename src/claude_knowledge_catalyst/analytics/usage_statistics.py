"""Usage statistics and performance analysis for CKC."""

import json
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from ..core.config import CKCConfig


class UsageStatisticsCollector:
    """Collects and analyzes usage statistics for CKC."""

    def __init__(self, vault_path: Path, config: CKCConfig):
        self.vault_path = vault_path
        self.config = config

        # Statistics storage
        self.stats_dir = vault_path / ".ckc" / "statistics"
        self.stats_dir.mkdir(parents=True, exist_ok=True)

        # Usage tracking files
        self.usage_log_path = self.stats_dir / "usage_log.jsonl"
        self.performance_log_path = self.stats_dir / "performance_log.jsonl"
        self.interaction_log_path = self.stats_dir / "interaction_log.jsonl"

        # Cache
        self._stats_cache = {}
        self._cache_timestamp = None

    def track_operation(
        self, operation: str, duration: float, metadata: dict | None = None
    ) -> None:
        """Track a CKC operation with timing."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "duration_ms": round(duration * 1000, 2),
            "metadata": metadata or {},
        }

        self._append_to_log(self.usage_log_path, log_entry)

    def track_file_access(self, file_path: Path, access_type: str) -> None:
        """Track file access patterns."""
        # Try to make path relative to vault, fallback to absolute path
        try:
            relative_path = str(file_path.relative_to(self.vault_path))
        except ValueError:
            # File is not in vault, use absolute path
            relative_path = str(file_path)

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "file_path": relative_path,
            "access_type": access_type,  # read, write, sync, delete
            "file_size": file_path.stat().st_size if file_path.exists() else 0,
        }

        self._append_to_log(self.interaction_log_path, log_entry)

    def track_performance_metric(
        self, metric_name: str, value: float, context: dict | None = None
    ) -> None:
        """Track performance metrics."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "metric": metric_name,
            "value": value,
            "context": context or {},
        }

        self._append_to_log(self.performance_log_path, log_entry)

    def generate_usage_report(self, days: int = 30) -> dict[str, Any]:
        """Generate comprehensive usage statistics report."""
        cutoff_date = datetime.now() - timedelta(days=days)

        report = {
            "report_period": {
                "days": days,
                "start_date": cutoff_date.isoformat(),
                "end_date": datetime.now().isoformat(),
            },
            "operation_statistics": self._analyze_operations(cutoff_date),
            "file_access_patterns": self._analyze_file_access(cutoff_date),
            "performance_metrics": self._analyze_performance(cutoff_date),
            "user_behavior": self._analyze_user_behavior(cutoff_date),
            "system_health": self._analyze_system_health(cutoff_date),
            "recommendations": [],
        }

        # Generate recommendations based on analysis
        report["recommendations"] = self._generate_usage_recommendations(report)

        return report

    def _analyze_operations(self, cutoff_date: datetime) -> dict[str, Any]:
        """Analyze operation statistics."""
        operations = self._load_log_entries(self.usage_log_path, cutoff_date)

        analysis: dict[str, Any] = {
            "total_operations": len(operations),
            "operation_types": Counter(),
            "average_duration": {},
            "operation_frequency": defaultdict(int),
            "peak_usage_hours": defaultdict(int),
            "daily_activity": defaultdict(int),
        }

        total_durations = defaultdict(list)

        for op in operations:
            op_type = op["operation"]
            duration = op["duration_ms"]
            timestamp = datetime.fromisoformat(op["timestamp"])

            # Count operations
            analysis["operation_types"][op_type] += 1
            total_durations[op_type].append(duration)

            # Track timing patterns
            hour = timestamp.hour
            day = timestamp.strftime("%Y-%m-%d")
            analysis["peak_usage_hours"][hour] += 1
            analysis["daily_activity"][day] += 1

        # Calculate averages
        for op_type, durations in total_durations.items():
            analysis["average_duration"][op_type] = sum(durations) / len(durations)

        # Convert defaultdicts for JSON serialization
        analysis["operation_frequency"] = dict(analysis["operation_frequency"])
        analysis["peak_usage_hours"] = dict(analysis["peak_usage_hours"])
        analysis["daily_activity"] = dict(analysis["daily_activity"])

        return analysis

    def _analyze_file_access(self, cutoff_date: datetime) -> dict[str, Any]:
        """Analyze file access patterns."""
        accesses = self._load_log_entries(self.interaction_log_path, cutoff_date)

        access_types: Counter[str] = Counter()
        most_accessed_files: Counter[str] = Counter()
        directory_activity: Counter[str] = Counter()
        hourly_patterns: defaultdict[int, int] = defaultdict(int)
        daily_patterns: defaultdict[str, int] = defaultdict(int)
        by_type_and_hour: defaultdict[str, defaultdict[int, int]] = defaultdict(
            lambda: defaultdict(int)
        )
        file_size_distribution: dict[str, int] = {"small": 0, "medium": 0, "large": 0}

        analysis: dict[str, Any] = {
            "total_accesses": len(accesses),
            "access_types": access_types,
            "most_accessed_files": most_accessed_files,
            "file_size_distribution": file_size_distribution,
            "directory_activity": directory_activity,
            "access_patterns": {
                "hourly": hourly_patterns,
                "daily": daily_patterns,
                "by_type_and_hour": by_type_and_hour,
            },
        }

        for access in accesses:
            access_type = access["access_type"]
            file_path = access["file_path"]
            file_size = access.get("file_size", 0)
            timestamp = datetime.fromisoformat(access["timestamp"])

            # Count access types
            analysis["access_types"][access_type] += 1

            # Track most accessed files
            analysis["most_accessed_files"][file_path] += 1

            # File size distribution
            if file_size < 10000:  # < 10KB
                analysis["file_size_distribution"]["small"] += 1
            elif file_size < 100000:  # < 100KB
                analysis["file_size_distribution"]["medium"] += 1
            else:
                analysis["file_size_distribution"]["large"] += 1

            # Directory activity
            directory = str(Path(file_path).parent)
            analysis["directory_activity"][directory] += 1

            # Temporal patterns
            hour = timestamp.hour
            day = timestamp.strftime("%Y-%m-%d")
            analysis["access_patterns"]["hourly"][hour] += 1
            analysis["access_patterns"]["daily"][day] += 1
            analysis["access_patterns"]["by_type_and_hour"][access_type][hour] += 1

        # Convert for serialization
        analysis["access_patterns"]["hourly"] = dict(
            analysis["access_patterns"]["hourly"]
        )
        analysis["access_patterns"]["daily"] = dict(
            analysis["access_patterns"]["daily"]
        )
        analysis["access_patterns"]["by_type_and_hour"] = {
            k: dict(v)
            for k, v in analysis["access_patterns"]["by_type_and_hour"].items()
        }

        return analysis

    def _analyze_performance(self, cutoff_date: datetime) -> dict[str, Any]:
        """Analyze performance metrics."""
        metrics = self._load_log_entries(self.performance_log_path, cutoff_date)

        metric_types: Counter[str] = Counter()
        performance_trends: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
        metric_values: defaultdict[str, list[float]] = defaultdict(list)

        analysis: dict[str, Any] = {
            "metrics_collected": len(metrics),
            "metric_types": metric_types,
            "performance_trends": performance_trends,
            "performance_summary": {},
            "bottlenecks": [],
            "optimization_opportunities": [],
        }

        for metric in metrics:
            metric_name = metric["metric"]
            value = metric["value"]
            timestamp = datetime.fromisoformat(metric["timestamp"])

            analysis["metric_types"][metric_name] += 1
            metric_values[metric_name].append(value)

            # Track trends over time
            analysis["performance_trends"][metric_name].append(
                {"timestamp": timestamp.isoformat(), "value": value}
            )

        # Calculate performance summaries
        for metric_name, values in metric_values.items():
            if values:
                analysis["performance_summary"][metric_name] = {
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "count": len(values),
                }

                # Identify bottlenecks (values significantly above average)
                avg_value = sum(values) / len(values)
                max_value = max(values)
                if max_value > avg_value * 3:  # More than 3x average
                    analysis["bottlenecks"].append(
                        {
                            "metric": metric_name,
                            "average": avg_value,
                            "peak": max_value,
                            "severity": "high"
                            if max_value > avg_value * 5
                            else "medium",
                        }
                    )

        # Convert for serialization
        analysis["performance_trends"] = dict(analysis["performance_trends"])

        return analysis

    def _analyze_user_behavior(self, cutoff_date: datetime) -> dict[str, Any]:
        """Analyze user behavior patterns."""
        operations = self._load_log_entries(self.usage_log_path, cutoff_date)
        accesses = self._load_log_entries(self.interaction_log_path, cutoff_date)

        analysis = {
            "session_patterns": self._analyze_sessions(operations + accesses),
            "workflow_analysis": self._analyze_workflows(operations),
            "content_preferences": self._analyze_content_preferences(accesses),
            "productivity_metrics": self._calculate_productivity_metrics(
                operations, accesses
            ),
        }

        return analysis

    def _analyze_sessions(self, all_events: list[dict]) -> dict[str, Any]:
        """Analyze user session patterns."""
        if not all_events:
            return {"total_sessions": 0}

        # Sort events by timestamp
        sorted_events = sorted(
            all_events, key=lambda x: datetime.fromisoformat(x["timestamp"])
        )

        sessions = []
        current_session = [sorted_events[0]]
        session_gap_threshold = timedelta(minutes=30)  # 30 minutes gap = new session

        for i in range(1, len(sorted_events)):
            current_time = datetime.fromisoformat(sorted_events[i]["timestamp"])
            prev_time = datetime.fromisoformat(sorted_events[i - 1]["timestamp"])

            if current_time - prev_time > session_gap_threshold:
                # Start new session
                sessions.append(current_session)
                current_session = [sorted_events[i]]
            else:
                current_session.append(sorted_events[i])

        if current_session:
            sessions.append(current_session)

        # Analyze sessions
        session_durations = []
        session_activity_counts = []

        for session in sessions:
            if len(session) > 1:
                start_time = datetime.fromisoformat(session[0]["timestamp"])
                end_time = datetime.fromisoformat(session[-1]["timestamp"])
                duration = (end_time - start_time).total_seconds() / 60  # minutes
                session_durations.append(duration)

            session_activity_counts.append(len(session))

        return {
            "total_sessions": len(sessions),
            "average_session_duration_minutes": sum(session_durations)
            / len(session_durations)
            if session_durations
            else 0,
            "average_activities_per_session": sum(session_activity_counts)
            / len(session_activity_counts)
            if session_activity_counts
            else 0,
            "session_distribution": {
                "short": sum(1 for d in session_durations if d < 15),  # < 15 minutes
                "medium": sum(
                    1 for d in session_durations if 15 <= d < 60
                ),  # 15-60 minutes
                "long": sum(1 for d in session_durations if d >= 60),  # >= 60 minutes
            },
        }

    def _analyze_workflows(self, operations: list[dict]) -> dict[str, Any]:
        """Analyze common workflow patterns."""
        if not operations:
            return {"workflow_patterns": []}

        # Group operations by time windows
        workflows = []
        window_size = timedelta(minutes=10)  # 10-minute windows

        sorted_ops = sorted(
            operations, key=lambda x: datetime.fromisoformat(x["timestamp"])
        )
        current_window = [sorted_ops[0]]
        window_start = datetime.fromisoformat(sorted_ops[0]["timestamp"])

        for op in sorted_ops[1:]:
            op_time = datetime.fromisoformat(op["timestamp"])
            if op_time - window_start <= window_size:
                current_window.append(op)
            else:
                if len(current_window) > 1:
                    workflows.append(current_window)
                current_window = [op]
                window_start = op_time

        if len(current_window) > 1:
            workflows.append(current_window)

        # Analyze workflow patterns
        workflow_patterns = Counter()
        for workflow in workflows:
            pattern = " -> ".join(op["operation"] for op in workflow)
            workflow_patterns[pattern] += 1

        return {
            "workflow_patterns": dict(workflow_patterns.most_common(10)),
            "average_workflow_length": sum(len(w) for w in workflows) / len(workflows)
            if workflows
            else 0,
            "most_common_sequences": dict(workflow_patterns.most_common(5)),
        }

    def _analyze_content_preferences(self, accesses: list[dict]) -> dict[str, Any]:
        """Analyze content access preferences."""
        if not accesses:
            return {"content_preferences": {}}

        directory_preferences = Counter()
        file_type_preferences = Counter()

        for access in accesses:
            file_path = Path(access["file_path"])

            # Directory preferences
            directory = str(file_path.parent)
            directory_preferences[directory] += 1

            # File type preferences
            file_type = file_path.suffix.lower()
            file_type_preferences[file_type] += 1

        return {
            "preferred_directories": dict(directory_preferences.most_common(10)),
            "preferred_file_types": dict(file_type_preferences.most_common(10)),
            "access_diversity": len(
                directory_preferences
            ),  # Number of unique directories accessed
        }

    def _calculate_productivity_metrics(
        self, operations: list[dict], accesses: list[dict]
    ) -> dict[str, Any]:
        """Calculate productivity metrics."""
        all_events = operations + accesses
        if not all_events:
            return {"productivity_score": 0}

        # Sort by timestamp
        sorted_events = sorted(
            all_events, key=lambda x: datetime.fromisoformat(x["timestamp"])
        )

        # Calculate metrics
        total_time_span = (
            datetime.fromisoformat(sorted_events[-1]["timestamp"])
            - datetime.fromisoformat(sorted_events[0]["timestamp"])
        ).total_seconds() / 3600  # hours

        productivity_metrics = {
            "total_activities": len(all_events),
            "time_span_hours": total_time_span,
            "activities_per_hour": len(all_events) / total_time_span
            if total_time_span > 0
            else 0,
            "operation_efficiency": len(operations) / len(all_events)
            if all_events
            else 0,
            "productivity_score": self._calculate_productivity_score(
                operations, accesses
            ),
        }

        return productivity_metrics

    def _calculate_productivity_score(
        self, operations: list[dict], accesses: list[dict]
    ) -> float:
        """Calculate overall productivity score (0-100)."""
        if not operations and not accesses:
            return 0

        score: float = 0

        # Base score from activity volume
        total_activities = len(operations) + len(accesses)
        volume_score = min(20, total_activities / 10)  # Max 20 points for volume
        score += volume_score

        # Efficiency score (fewer long operations = better)
        if operations:
            avg_duration = sum(op["duration_ms"] for op in operations) / len(operations)
            efficiency_score = max(
                0, 20 - (avg_duration / 1000)
            )  # Max 20 points for efficiency
            score += efficiency_score

        # Consistency score (regular activity = better)
        if total_activities > 1:
            timestamps = [
                datetime.fromisoformat(event["timestamp"])
                for event in operations + accesses
            ]
            timestamps.sort()

            gaps = [
                (timestamps[i + 1] - timestamps[i]).total_seconds() / 3600
                for i in range(len(timestamps) - 1)
            ]

            avg_gap = sum(gaps) / len(gaps) if gaps else 0
            consistency_score = max(0, 20 - avg_gap)  # Max 20 points for consistency
            score += consistency_score

        # Diversity score (using different features = better)
        operation_types = {op["operation"] for op in operations}
        access_types = {acc["access_type"] for acc in accesses}
        diversity_score = min(
            20, (len(operation_types) + len(access_types)) * 2
        )  # Max 20 points
        score += diversity_score

        # Quality score (successful operations = better)
        # This would require error tracking, for now use base score
        quality_score = 20
        score += quality_score

        return min(100, score)

    def _analyze_system_health(self, cutoff_date: datetime) -> dict[str, Any]:
        """Analyze system health indicators."""
        performance_metrics = self._load_log_entries(
            self.performance_log_path, cutoff_date
        )

        health_indicators = {
            "error_rate": 0,  # Would need error tracking
            "average_response_time": 0,
            "resource_utilization": {},
            "system_stability": "stable",  # Would need more detailed monitoring
        }

        # Calculate average response times from performance metrics
        response_times = [
            m["value"]
            for m in performance_metrics
            if m["metric"] in ["operation_duration", "sync_time"]
        ]

        if response_times:
            health_indicators["average_response_time"] = sum(response_times) / len(
                response_times
            )

        return health_indicators

    def _generate_usage_recommendations(
        self, report: dict[str, Any]
    ) -> list[dict[str, str]]:
        """Generate recommendations based on usage analysis."""
        recommendations = []

        # Performance recommendations
        bottlenecks = report["performance_metrics"].get("bottlenecks", [])
        if bottlenecks:
            high_severity = [b for b in bottlenecks if b["severity"] == "high"]
            if high_severity:
                recommendations.append(
                    {
                        "priority": "high",
                        "category": "performance",
                        "title": "Address Performance Bottlenecks",
                        "description": (
                            f"Found {len(high_severity)} high-severity "
                            "performance issues"
                        ),
                        "action": "Optimize operations: "
                        + ", ".join(b["metric"] for b in high_severity[:3]),
                    }
                )

        # Usage pattern recommendations
        ops_stats = report["operation_statistics"]
        if ops_stats["total_operations"] > 0:
            avg_durations = ops_stats["average_duration"]
            slow_operations = [
                op for op, duration in avg_durations.items() if duration > 5000
            ]  # > 5 seconds

            if slow_operations:
                recommendations.append(
                    {
                        "priority": "medium",
                        "category": "efficiency",
                        "title": "Optimize Slow Operations",
                        "description": (
                            f"Operations taking >5s: {', '.join(slow_operations[:3])}"
                        ),
                        "action": (
                            "Review and optimize slow operations for better "
                            "user experience"
                        ),
                    }
                )

        # Productivity recommendations
        user_behavior = report.get("user_behavior", {})
        productivity = user_behavior.get("productivity_metrics", {})

        if productivity.get("productivity_score", 0) < 50:
            recommendations.append(
                {
                    "priority": "low",
                    "category": "productivity",
                    "title": "Improve Productivity Score",
                    "description": (
                        f"Current productivity score: "
                        f"{productivity.get('productivity_score', 0):.1f}/100"
                    ),
                    "action": (
                        "Consider workflow optimization and feature usage training"
                    ),
                }
            )

        return recommendations

    def _load_log_entries(self, log_path: Path, cutoff_date: datetime) -> list[dict]:
        """Load log entries since cutoff date."""
        entries = []

        if not log_path.exists():
            return entries

        try:
            with open(log_path, encoding="utf-8") as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        entry_time = datetime.fromisoformat(entry["timestamp"])
                        if entry_time >= cutoff_date:
                            entries.append(entry)
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
        except OSError:
            pass

        return entries

    def _append_to_log(self, log_path: Path, entry: dict) -> None:
        """Append entry to log file."""
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except OSError:
            pass  # Fail silently for logging

    def cleanup_old_logs(self, days_to_keep: int = 90) -> None:
        """Clean up old log entries."""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)

        for log_path in [
            self.usage_log_path,
            self.performance_log_path,
            self.interaction_log_path,
        ]:
            if not log_path.exists():
                continue

            # Read and filter entries
            recent_entries = []
            try:
                with open(log_path, encoding="utf-8") as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            entry_time = datetime.fromisoformat(entry["timestamp"])
                            if entry_time >= cutoff_date:
                                recent_entries.append(entry)
                        except (json.JSONDecodeError, KeyError, ValueError):
                            continue

                # Write back filtered entries
                with open(log_path, "w", encoding="utf-8") as f:
                    for entry in recent_entries:
                        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

            except OSError:
                pass


class PerformanceMonitor:
    """Context manager for tracking operation performance."""

    def __init__(
        self,
        collector: UsageStatisticsCollector,
        operation_name: str,
        metadata: dict | None = None,
    ):
        self.collector = collector
        self.operation_name = operation_name
        self.metadata = metadata or {}
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = time.time() - self.start_time
            self.collector.track_operation(self.operation_name, duration, self.metadata)


def create_usage_collector(
    vault_path: Path, config: CKCConfig
) -> UsageStatisticsCollector:
    """Convenience function to create usage statistics collector."""
    return UsageStatisticsCollector(vault_path, config)
