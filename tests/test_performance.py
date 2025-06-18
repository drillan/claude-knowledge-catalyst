"""Performance tests for Claude Knowledge Catalyst."""

import time
import tempfile
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
import pytest

from src.claude_knowledge_catalyst.core.config import CKCConfig
from src.claude_knowledge_catalyst.core.metadata import MetadataManager
from src.claude_knowledge_catalyst.sync.hybrid_manager import HybridObsidianVaultManager
from src.claude_knowledge_catalyst.analytics.knowledge_analytics import KnowledgeAnalytics
from src.claude_knowledge_catalyst.automation.structure_automation import AutomatedStructureManager


class TestPerformance:
    """Performance tests for CKC components."""
    
    @pytest.fixture
    def performance_setup(self):
        """Setup for performance tests."""
        temp_dir = tempfile.mkdtemp()
        vault_path = Path(temp_dir) / "vault"
        project_path = Path(temp_dir) / "project"
        vault_path.mkdir()
        project_path.mkdir()
        
        # Mock Path.cwd() to avoid "No such file or directory" errors during testing
        with patch('pathlib.Path.cwd', return_value=project_path):
            config = CKCConfig()
        config.hybrid_structure.enabled = True
        config.project_root = project_path
        
        yield {
            "vault_path": vault_path,
            "project_path": project_path,
            "config": config
        }
        
        shutil.rmtree(temp_dir)
    
    def test_vault_initialization_performance(self, performance_setup):
        """Test vault initialization performance."""
        setup = performance_setup
        metadata_manager = MetadataManager()
        vault_manager = HybridObsidianVaultManager(
            setup["vault_path"], 
            metadata_manager, 
            setup["config"]
        )
        
        # Measure initialization time
        start_time = time.time()
        success = vault_manager.initialize_vault()
        init_duration = time.time() - start_time
        
        assert success, "Vault initialization should succeed"
        assert init_duration < 5.0, f"Vault initialization took {init_duration:.2f}s, should be under 5s"
        
        # Verify all directories were created
        expected_dirs = [
            "_templates", "_attachments", "_scripts",
            "00_Catalyst_Lab", "10_Projects", "20_Knowledge_Base", "30_Wisdom_Archive"
        ]
        
        for dir_name in expected_dirs:
            assert (setup["vault_path"] / dir_name).exists(), f"Directory {dir_name} should exist"
    
    def test_file_sync_performance(self, performance_setup):
        """Test file synchronization performance."""
        setup = performance_setup
        metadata_manager = MetadataManager()
        vault_manager = HybridObsidianVaultManager(
            setup["vault_path"], 
            metadata_manager, 
            setup["config"]
        )
        
        vault_manager.initialize_vault()
        
        # Create test files
        test_files = []
        for i in range(100):
            file_path = setup["project_path"] / f"test_{i:03d}.md"
            content = f"""---
title: "Performance Test File {i}"
tags: ["test", "performance", "batch-{i//10}"]
category: "{['prompt', 'code', 'concept'][i % 3]}"
---

# Performance Test File {i}

This is test content for performance evaluation.

## Section 1
Content with details and examples for file {i}.

```python
def test_function_{i}():
    return f"Result from function {i}"
```

## Notes
Additional content to make files substantial.
"""
            file_path.write_text(content)
            test_files.append(file_path)
        
        # Measure sync performance
        start_time = time.time()
        sync_results = []
        
        for file_path in test_files:
            result = vault_manager.sync_file(file_path)
            sync_results.append(result)
        
        sync_duration = time.time() - start_time
        
        assert all(sync_results), "All files should sync successfully"
        assert sync_duration < 30, f"Sync of 100 files took {sync_duration:.2f}s, should be under 30s"
        
        # Calculate per-file performance
        per_file_time = sync_duration / len(test_files)
        assert per_file_time < 0.3, f"Per-file sync time {per_file_time:.3f}s should be under 0.3s"
    
    def test_concurrent_sync_performance(self, performance_setup):
        """Test concurrent file synchronization performance."""
        setup = performance_setup
        metadata_manager = MetadataManager()
        vault_manager = HybridObsidianVaultManager(
            setup["vault_path"], 
            metadata_manager, 
            setup["config"]
        )
        
        vault_manager.initialize_vault()
        
        # Create test files
        test_files = []
        for i in range(50):
            file_path = setup["project_path"] / f"concurrent_test_{i:03d}.md"
            content = f"""---
title: "Concurrent Test File {i}"
tags: ["concurrent", "test", "perf"]
category: "prompt"
---

# Concurrent Test File {i}

Test content for concurrent processing.
"""
            file_path.write_text(content)
            test_files.append(file_path)
        
        def sync_file(file_path):
            """Sync single file."""
            return vault_manager.sync_file(file_path)
        
        # Measure concurrent sync performance
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(sync_file, test_files))
        
        concurrent_duration = time.time() - start_time
        
        assert all(results), "All concurrent syncs should succeed"
        assert concurrent_duration < 20, f"Concurrent sync took {concurrent_duration:.2f}s, should be under 20s"
        
        # Should be faster than sequential for this workload
        # Note: This is a rough estimate, actual performance depends on system
        expected_sequential_time = len(test_files) * 0.1  # Rough estimate
        efficiency = expected_sequential_time / concurrent_duration
        assert efficiency > 0.5, f"Concurrent efficiency {efficiency:.2f} should be reasonable"
    
    def test_analytics_performance(self, performance_setup):
        """Test analytics generation performance."""
        setup = performance_setup
        
        # Setup vault with substantial content
        metadata_manager = MetadataManager()
        vault_manager = HybridObsidianVaultManager(
            setup["vault_path"], 
            metadata_manager, 
            setup["config"]
        )
        vault_manager.initialize_vault()
        
        # Create diverse content
        categories = ["prompt", "code", "concept", "project_log", "experiment", "resource"]
        for i in range(200):  # Create 200 files for analytics
            category = categories[i % len(categories)]
            dir_mapping = {
                "prompt": "20_Knowledge_Base/Prompts",
                "code": "20_Knowledge_Base/Code_Snippets", 
                "concept": "20_Knowledge_Base/Concepts",
                "project_log": "10_Projects",
                "experiment": "00_Catalyst_Lab",
                "resource": "20_Knowledge_Base/Resources"
            }
            
            target_dir = setup["vault_path"] / dir_mapping[category]
            target_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = target_dir / f"{category}_test_{i:03d}.md"
            content = f"""---
title: "{category.title()} Test {i}"
tags: ["{category}", "test", "analytics", "batch-{i//20}"]
category: "{category}"
status: "{['draft', 'review', 'published'][i % 3]}"
quality: "{['low', 'medium', 'high'][i % 3]}"
success_rate: {60 + (i % 40)}
---

# {category.title()} Test {i}

This is test content for analytics performance testing.

## Details
Content with various elements for comprehensive analysis.

{'```python' if category == 'code' else ''}
{'def test_function():' if category == 'code' else ''}
{'    return "test"' if category == 'code' else ''}
{'```' if category == 'code' else ''}

## Notes
Additional content to test analytics processing.
"""
            file_path.write_text(content)
        
        # Measure analytics performance
        analytics = KnowledgeAnalytics(setup["vault_path"], setup["config"])
        
        start_time = time.time()
        report = analytics.generate_comprehensive_report()
        analytics_duration = time.time() - start_time
        
        assert report["report_sections"]["overview"]["total_files"] >= 200, "Should analyze all files"
        assert analytics_duration < 15, f"Analytics took {analytics_duration:.2f}s, should be under 15s"
        
        # Test analytics sections exist and have data
        sections = report["report_sections"]
        assert sections["overview"]["total_files"] > 0
        assert len(sections["content_analysis"]["category_distribution"]) > 0
        assert len(sections["quality_metrics"]["metadata_completeness"]) > 0
    
    def test_automation_performance(self, performance_setup):
        """Test automation system performance."""
        setup = performance_setup
        
        # Setup vault with content that needs maintenance
        metadata_manager = MetadataManager()
        vault_manager = HybridObsidianVaultManager(
            setup["vault_path"], 
            metadata_manager, 
            setup["config"]
        )
        vault_manager.initialize_vault()
        
        # Create files with various issues for automation to fix
        for i in range(100):
            file_path = setup["vault_path"] / "20_Knowledge_Base" / f"maintenance_test_{i:03d}.md"
            
            # Create files with deliberate issues
            issues = ["missing_title", "no_tags", "no_category", "outdated"]
            issue_type = issues[i % len(issues)]
            
            if issue_type == "missing_title":
                content = f"""---
tags: ["test", "maintenance"]
category: "test"
---

# File {i}
Content without proper title.
"""
            elif issue_type == "no_tags":
                content = f"""---
title: "Test File {i}"
category: "test"
---

# Test File {i}
Content without tags.
"""
            elif issue_type == "no_category":
                content = f"""---
title: "Test File {i}"
tags: ["test", "maintenance"]
---

# Test File {i}
Content without category.
"""
            else:  # outdated
                content = f"""---
title: "Test File {i}"
tags: ["test", "maintenance", "old"]
category: "test"
created: "2020-01-01T00:00:00"
updated: "2020-01-01T00:00:00"
---

# Test File {i}
Outdated content.
"""
            
            file_path.write_text(content)
        
        # Measure automation performance
        automation_manager = AutomatedStructureManager(setup["vault_path"], setup["config"])
        
        start_time = time.time()
        result = automation_manager.run_automated_maintenance()
        automation_duration = time.time() - start_time
        
        assert "error" not in result, "Automation should complete without errors"
        assert automation_duration < 10, f"Automation took {automation_duration:.2f}s, should be under 10s"
        
        # Check that maintenance tasks were completed
        tasks_completed = result.get("tasks_completed", [])
        assert len(tasks_completed) > 0, "Should complete some maintenance tasks"
        
        # Check performance metrics
        performance = result.get("performance", {})
        assert "duration_seconds" in performance
        assert performance["duration_seconds"] == pytest.approx(automation_duration, rel=0.1)
    
    def test_metadata_enhancement_performance(self, performance_setup):
        """Test metadata enhancement performance."""
        setup = performance_setup
        
        from src.claude_knowledge_catalyst.automation.metadata_enhancer import AdvancedMetadataEnhancer
        
        enhancer = AdvancedMetadataEnhancer(setup["config"])
        
        # Create test files for enhancement
        test_files = []
        for i in range(50):
            file_path = setup["vault_path"] / f"enhance_test_{i:03d}.md"
            content = f"""---
title: "Enhancement Test {i}"
tags: ["test"]
---

# Enhancement Test {i}

This is test content for metadata enhancement performance testing.
The content includes various elements like code examples, technical terms,
and different complexity levels to test the enhancement algorithms.

## Technical Section
Here we discuss APIs, algorithms, and optimization techniques.
This should trigger technical term detection and complexity assessment.

```python
def example_function():
    # This is a code example
    return "test result"
```

## Testing Notes
- Performance testing
- Metadata enhancement
- Quality assessment
- Success rate evaluation

The content quality should be assessed as medium to high based on
structure, completeness, and technical depth.
"""
            file_path.write_text(content)
            test_files.append(file_path)
        
        # Measure enhancement performance
        start_time = time.time()
        enhanced_files = []
        
        for file_path in test_files:
            enhanced_metadata = enhancer.enhance_metadata(file_path)
            enhanced_files.append((file_path, enhanced_metadata))
        
        enhancement_duration = time.time() - start_time
        
        assert len(enhanced_files) == len(test_files), "Should enhance all files"
        assert enhancement_duration < 20, f"Enhancement took {enhancement_duration:.2f}s, should be under 20s"
        
        # Verify enhancement quality
        for file_path, metadata in enhanced_files[:5]:  # Check first 5 files
            assert metadata.title is not None
            assert len(metadata.tags) > 1  # Should have added tags
            assert hasattr(metadata, 'complexity')  # Should have complexity assessment
    
    def test_memory_usage_under_load(self, performance_setup):
        """Test memory usage with large datasets."""
        import psutil
        import os
        
        setup = performance_setup
        process = psutil.Process(os.getpid())
        
        # Get baseline memory usage
        baseline_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Setup and process large dataset
        metadata_manager = MetadataManager()
        vault_manager = HybridObsidianVaultManager(
            setup["vault_path"], 
            metadata_manager, 
            setup["config"]
        )
        vault_manager.initialize_vault()
        
        # Create and process many files
        for i in range(500):  # Process 500 files
            file_path = setup["project_path"] / f"memory_test_{i:03d}.md"
            content = f"""---
title: "Memory Test File {i}"
tags: ["memory", "test", "large-dataset"]
category: "test"
---

# Memory Test File {i}

This is test content for memory usage evaluation.
{' '.join([f'Word{j}' for j in range(100)])}

## Large Content Section
{'This is repeated content to increase file size. ' * 50}

## Code Section
```python
def memory_test_function_{i}():
    data = [{{'key': f'value{{j}}'}} for j in range(100)]
    return data
```
"""
            file_path.write_text(content)
            
            # Sync file and check memory periodically
            vault_manager.sync_file(file_path)
            
            if i % 100 == 0:  # Check every 100 files
                current_memory = process.memory_info().rss / 1024 / 1024  # MB
                memory_increase = current_memory - baseline_memory
                
                # Memory should not grow excessively
                assert memory_increase < 500, f"Memory usage increased by {memory_increase:.1f}MB after {i} files"
        
        # Final memory check
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        total_increase = final_memory - baseline_memory
        
        # Total memory increase should be reasonable
        assert total_increase < 1000, f"Total memory increase {total_increase:.1f}MB should be under 1GB"
    
    def test_large_vault_analytics_performance(self, performance_setup):
        """Test analytics performance with large vault."""
        setup = performance_setup
        
        # Create large vault structure
        metadata_manager = MetadataManager()
        vault_manager = HybridObsidianVaultManager(
            setup["vault_path"], 
            metadata_manager, 
            setup["config"]
        )
        vault_manager.initialize_vault()
        
        # Create many directories and files
        base_dirs = [
            "20_Knowledge_Base/Prompts",
            "20_Knowledge_Base/Code_Snippets", 
            "20_Knowledge_Base/Concepts",
            "10_Projects",
            "00_Catalyst_Lab"
        ]
        
        total_files = 0
        for dir_name in base_dirs:
            dir_path = setup["vault_path"] / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories
            for sub_i in range(5):
                sub_dir = dir_path / f"subdir_{sub_i}"
                sub_dir.mkdir(exist_ok=True)
                
                # Create files in subdirectory
                for file_i in range(20):  # 20 files per subdirectory
                    file_path = sub_dir / f"file_{file_i:03d}.md"
                    content = f"""---
title: "Large Vault Test {total_files}"
tags: ["large-vault", "test", "subdir-{sub_i}", "dir-{dir_name.split('/')[-1]}"]
category: "{['prompt', 'code', 'concept', 'project_log', 'experiment'][total_files % 5]}"
status: "{['draft', 'review', 'published'][total_files % 3]}"
---

# Large Vault Test {total_files}

Content for large vault analytics testing.
File {file_i} in subdirectory {sub_i} of {dir_name}.
"""
                    file_path.write_text(content)
                    total_files += 1
        
        # Test analytics on large vault
        analytics = KnowledgeAnalytics(setup["vault_path"], setup["config"])
        
        start_time = time.time()
        report = analytics.generate_comprehensive_report()
        analytics_duration = time.time() - start_time
        
        assert report["report_sections"]["overview"]["total_files"] >= total_files * 0.9, "Should analyze most files"
        assert analytics_duration < 30, f"Large vault analytics took {analytics_duration:.2f}s, should be under 30s"
        
        # Verify report completeness
        sections = report["report_sections"]
        assert len(sections["content_analysis"]["category_distribution"]) > 0
        assert len(sections["overview"]["tag_distribution"]) > 0
        assert sections["overview"]["total_files"] > 400  # Should have processed many files


if __name__ == "__main__":
    pytest.main([__file__, "-v"])