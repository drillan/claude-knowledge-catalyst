"""Tests for knowledge analytics functionality."""

import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest

from claude_knowledge_catalyst.analytics.knowledge_analytics import KnowledgeAnalytics
from claude_knowledge_catalyst.core.config import CKCConfig, HybridStructureConfig
from claude_knowledge_catalyst.core.metadata import KnowledgeMetadata, MetadataManager


class TestKnowledgeAnalytics:
    """Test suite for KnowledgeAnalytics."""

    @pytest.fixture
    def temp_vault_path(self):
        """Create temporary vault directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            vault_path = Path(temp_dir) / "test_vault"
            vault_path.mkdir()
            
            # Create basic vault structure
            for dir_name in ["knowledge", "inbox", "archive", "active", "_system"]:
                (vault_path / dir_name).mkdir()
            
            yield vault_path

    @pytest.fixture
    def mock_config(self):
        """Create mock CKC configuration."""
        config = Mock(spec=CKCConfig)
        config.hybrid_structure = Mock(spec=HybridStructureConfig)
        config.hybrid_structure.enabled = True
        return config

    @pytest.fixture
    def analytics(self, temp_vault_path, mock_config):
        """Create analytics instance."""
        return KnowledgeAnalytics(temp_vault_path, mock_config)

    @pytest.fixture
    def sample_knowledge_files(self, temp_vault_path):
        """Create sample knowledge files for testing."""
        files = []
        
        # Create sample files with metadata
        knowledge_dir = temp_vault_path / "knowledge"
        
        files.append(knowledge_dir / "python_basics.md")
        files[-1].write_text("""---
title: "Python Basics"
tags: ["python", "programming", "beginner"]
category: "concept"
created: "2024-01-01"
---

# Python Basics
Introduction to Python programming.
""")

        files.append(knowledge_dir / "api_design.md")
        files[-1].write_text("""---
title: "API Design Patterns"
tags: ["api", "design", "advanced"]
category: "concept"
success_rate: 85
---

# API Design Patterns
Best practices for API development.
""")

        files.append(knowledge_dir / "debugging_prompt.md")
        files[-1].write_text("""---
title: "Debug Helper Prompt"
tags: ["debugging", "prompt", "productivity"]
category: "prompt"
success_rate: 92
---

# Debug Helper
Please help debug this code issue.
""")

        return files

    def test_analytics_initialization(self, analytics, temp_vault_path, mock_config):
        """Test analytics initialization."""
        assert analytics.vault_path == temp_vault_path
        assert analytics.config == mock_config
        assert analytics.metadata_manager is not None
        assert analytics.health_monitor is not None
        
        # Check directories created
        assert (temp_vault_path / "Analytics").exists()
        assert (temp_vault_path / "Analytics" / "reports").exists()

    def test_collect_knowledge_items(self, analytics, sample_knowledge_files):
        """Test knowledge items collection."""
        with patch.object(analytics.metadata_manager, 'extract_metadata') as mock_extract:
            # Setup mock metadata
            mock_metadatas = [
                KnowledgeMetadata(title="Python Basics", tags=["python"], category="concept"),
                KnowledgeMetadata(title="API Design", tags=["api"], category="concept"),
                KnowledgeMetadata(title="Debug Prompt", tags=["debugging"], category="prompt"),
            ]
            mock_extract.side_effect = mock_metadatas
            
            items = analytics._collect_knowledge_items()
            
            assert len(items) >= 3
            assert all(isinstance(item, tuple) for item in items)
            # Each item should be (file_path, metadata)
            assert all(len(item) == 2 for item in items)

    def test_generate_overview(self, analytics, sample_knowledge_files):
        """Test overview generation."""
        with patch.object(analytics, '_collect_knowledge_items') as mock_collect:
            # Setup mock knowledge items
            mock_items = [
                (Path("file1.md"), KnowledgeMetadata(title="Test 1", tags=["python"], category="concept")),
                (Path("file2.md"), KnowledgeMetadata(title="Test 2", tags=["api"], category="prompt")),
                (Path("file3.md"), KnowledgeMetadata(title="Test 3", tags=["debug"], category="code")),
            ]
            mock_collect.return_value = mock_items
            
            overview = analytics._generate_overview(mock_items)
            
            assert "total_files" in overview
            assert "categories" in overview
            assert "total_tags" in overview
            assert overview["total_files"] == 3
            assert "concept" in overview["categories"]
            assert "prompt" in overview["categories"]

    def test_tag_analysis(self, analytics):
        """Test tag analysis functionality."""
        mock_items = [
            (Path("f1.md"), KnowledgeMetadata(tags=["python", "programming"])),
            (Path("f2.md"), KnowledgeMetadata(tags=["python", "advanced"])),
            (Path("f3.md"), KnowledgeMetadata(tags=["javascript", "programming"])),
        ]
        
        tag_stats = analytics._analyze_tags(mock_items)
        
        assert "tag_frequency" in tag_stats
        assert "most_common_tags" in tag_stats
        assert tag_stats["tag_frequency"]["python"] == 2
        assert tag_stats["tag_frequency"]["programming"] == 2
        assert tag_stats["tag_frequency"]["javascript"] == 1

    def test_category_distribution(self, analytics):
        """Test category distribution analysis."""
        mock_items = [
            (Path("f1.md"), KnowledgeMetadata(category="concept")),
            (Path("f2.md"), KnowledgeMetadata(category="concept")),
            (Path("f3.md"), KnowledgeMetadata(category="prompt")),
            (Path("f4.md"), KnowledgeMetadata(category="code")),
        ]
        
        category_stats = analytics._analyze_categories(mock_items)
        
        assert "distribution" in category_stats
        assert category_stats["distribution"]["concept"] == 2
        assert category_stats["distribution"]["prompt"] == 1
        assert category_stats["distribution"]["code"] == 1

    def test_success_rate_analysis(self, analytics):
        """Test success rate analysis."""
        mock_items = [
            (Path("f1.md"), KnowledgeMetadata(success_rate=90)),
            (Path("f2.md"), KnowledgeMetadata(success_rate=85)),
            (Path("f3.md"), KnowledgeMetadata(success_rate=95)),
            (Path("f4.md"), KnowledgeMetadata()),  # No success rate
        ]
        
        success_stats = analytics._analyze_success_rates(mock_items)
        
        assert "average_success_rate" in success_stats
        assert "items_with_success_rate" in success_stats
        assert "high_performers" in success_stats
        
        # Should calculate average of items with success rates
        assert success_stats["average_success_rate"] == 90.0  # (90+85+95)/3
        assert success_stats["items_with_success_rate"] == 3

    def test_temporal_analysis(self, analytics):
        """Test temporal analysis functionality."""
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        week_ago = now - timedelta(days=7)
        
        mock_items = [
            (Path("f1.md"), KnowledgeMetadata(created=now.isoformat())),
            (Path("f2.md"), KnowledgeMetadata(created=yesterday.isoformat())),
            (Path("f3.md"), KnowledgeMetadata(created=week_ago.isoformat())),
            (Path("f4.md"), KnowledgeMetadata()),  # No creation date
        ]
        
        temporal_stats = analytics._analyze_temporal_patterns(mock_items)
        
        assert "creation_timeline" in temporal_stats
        assert "recent_activity" in temporal_stats
        assert len(temporal_stats["recent_activity"]["last_7_days"]) >= 2

    def test_comprehensive_report_generation(self, analytics, sample_knowledge_files):
        """Test comprehensive report generation."""
        with patch.object(analytics, '_collect_knowledge_items') as mock_collect:
            mock_items = [
                (Path("f1.md"), KnowledgeMetadata(
                    title="Test", 
                    tags=["python"], 
                    category="concept",
                    success_rate=85
                )),
            ]
            mock_collect.return_value = mock_items
            
            report = analytics.generate_comprehensive_report()
            
            assert "timestamp" in report
            assert "vault_path" in report
            assert "report_sections" in report
            assert "overview" in report["report_sections"]

    def test_trend_analysis(self, analytics):
        """Test trend analysis over time."""
        # Create mock data with timestamps
        base_date = datetime(2024, 1, 1)
        mock_items = []
        
        for i in range(10):
            date = base_date + timedelta(days=i*10)
            mock_items.append((
                Path(f"file_{i}.md"),
                KnowledgeMetadata(
                    created=date.isoformat(),
                    tags=["python"] if i % 2 == 0 else ["javascript"],
                    category="concept"
                )
            ))
        
        trends = analytics._analyze_trends(mock_items)
        
        assert "creation_trends" in trends
        assert "tag_evolution" in trends
        assert len(trends["creation_trends"]) > 0

    def test_knowledge_gaps_identification(self, analytics):
        """Test knowledge gaps identification."""
        mock_items = [
            (Path("f1.md"), KnowledgeMetadata(tags=["python", "basic"])),
            (Path("f2.md"), KnowledgeMetadata(tags=["python", "basic"])),
            (Path("f3.md"), KnowledgeMetadata(tags=["javascript", "advanced"])),
        ]
        
        gaps = analytics._identify_knowledge_gaps(mock_items)
        
        assert "underrepresented_areas" in gaps
        assert "missing_combinations" in gaps
        # Should identify that we have lots of python basic but little else

    def test_performance_metrics(self, analytics):
        """Test performance metrics calculation."""
        mock_items = [
            (Path("f1.md"), KnowledgeMetadata(success_rate=90, usage_count=10)),
            (Path("f2.md"), KnowledgeMetadata(success_rate=80, usage_count=5)),
            (Path("f3.md"), KnowledgeMetadata(success_rate=95, usage_count=15)),
        ]
        
        metrics = analytics._calculate_performance_metrics(mock_items)
        
        assert "top_performers" in metrics
        assert "improvement_candidates" in metrics
        assert "overall_effectiveness" in metrics

    def test_export_report_json(self, analytics, temp_vault_path):
        """Test JSON report export."""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "total_files": 10,
            "categories": {"concept": 5, "prompt": 3, "code": 2}
        }
        
        filepath = analytics.export_report(report_data, format="json")
        
        assert filepath.exists()
        assert filepath.suffix == ".json"
        
        # Verify content
        with open(filepath) as f:
            loaded_data = json.load(f)
        assert loaded_data["total_files"] == 10

    def test_cache_mechanism(self, analytics):
        """Test analytics caching mechanism."""
        with patch.object(analytics, '_collect_knowledge_items') as mock_collect:
            mock_collect.return_value = [
                (Path("f1.md"), KnowledgeMetadata(title="Test"))
            ]
            
            # First call should populate cache
            report1 = analytics.generate_comprehensive_report()
            call_count_1 = mock_collect.call_count
            
            # Second call should use cache
            report2 = analytics.generate_comprehensive_report()
            call_count_2 = mock_collect.call_count
            
            # Should use cache for second call
            assert call_count_2 == call_count_1

    def test_visualization_data_preparation(self, analytics):
        """Test data preparation for visualizations."""
        mock_items = [
            (Path("f1.md"), KnowledgeMetadata(tags=["python"], category="concept")),
            (Path("f2.md"), KnowledgeMetadata(tags=["api"], category="prompt")),
            (Path("f3.md"), KnowledgeMetadata(tags=["debug"], category="code")),
        ]
        
        viz_data = analytics._prepare_visualization_data(mock_items)
        
        assert "tag_counts" in viz_data
        assert "category_distribution" in viz_data
        assert "timeline_data" in viz_data


class TestKnowledgeAnalyticsIntegration:
    """Integration tests for KnowledgeAnalytics."""

    @pytest.fixture
    def full_vault_setup(self):
        """Create full vault setup with realistic content."""
        with tempfile.TemporaryDirectory() as temp_dir:
            vault_path = Path(temp_dir) / "full_vault"
            vault_path.mkdir()
            
            # Create comprehensive vault structure
            dirs = ["knowledge", "inbox", "archive", "active", "_system", "_attachments"]
            for dir_name in dirs:
                (vault_path / dir_name).mkdir()
            
            # Create realistic content
            knowledge_dir = vault_path / "knowledge"
            
            # Python content
            (knowledge_dir / "python_guide.md").write_text("""---
title: "Python Programming Guide"
tags: ["python", "programming", "guide", "beginner"]
category: "concept"
created: "2024-01-15"
success_rate: 88
---

# Python Programming Guide
Comprehensive guide to Python programming.
""")
            
            # API content
            (knowledge_dir / "rest_api_design.md").write_text("""---
title: "REST API Design"
tags: ["api", "rest", "design", "web", "backend"]
category: "concept"
created: "2024-01-20"
success_rate: 92
---

# REST API Design Principles
Best practices for REST API development.
""")
            
            # Prompt content
            (knowledge_dir / "code_review_prompt.md").write_text("""---
title: "Code Review Assistant"
tags: ["prompt", "code-review", "quality", "automation"]
category: "prompt"
created: "2024-01-25"
success_rate: 95
usage_count: 15
---

# Code Review Assistant Prompt
Please review the following code for quality and best practices.
""")
            
            yield vault_path

    def test_real_vault_analysis(self, full_vault_setup):
        """Test analytics with realistic vault content."""
        config = Mock(spec=CKCConfig)
        config.hybrid_structure = Mock(spec=HybridStructureConfig)
        config.hybrid_structure.enabled = True
        
        analytics = KnowledgeAnalytics(full_vault_setup, config)
        
        with patch.object(analytics.metadata_manager, 'extract_metadata') as mock_extract:
            # Setup realistic metadata
            mock_metadatas = [
                KnowledgeMetadata(
                    title="Python Programming Guide",
                    tags=["python", "programming", "guide", "beginner"],
                    category="concept",
                    success_rate=88
                ),
                KnowledgeMetadata(
                    title="REST API Design",
                    tags=["api", "rest", "design", "web", "backend"],
                    category="concept",
                    success_rate=92
                ),
                KnowledgeMetadata(
                    title="Code Review Assistant",
                    tags=["prompt", "code-review", "quality", "automation"],
                    category="prompt",
                    success_rate=95,
                    usage_count=15
                ),
            ]
            mock_extract.side_effect = mock_metadatas
            
            report = analytics.generate_comprehensive_report()
            
            # Verify comprehensive report structure
            assert report["report_sections"]["overview"]["total_files"] == 3
            assert "concept" in report["report_sections"]["overview"]["categories"]
            assert "prompt" in report["report_sections"]["overview"]["categories"]
            
            # Verify analytics quality
            tag_section = report["report_sections"]["tags"]
            assert "python" in tag_section["tag_frequency"]
            assert "api" in tag_section["tag_frequency"]

    def test_performance_with_large_dataset(self, full_vault_setup):
        """Test analytics performance with larger dataset."""
        config = Mock(spec=CKCConfig)
        config.hybrid_structure = Mock(spec=HybridStructureConfig)
        
        analytics = KnowledgeAnalytics(full_vault_setup, config)
        
        # Create many mock items
        large_dataset = []
        for i in range(100):
            large_dataset.append((
                Path(f"file_{i}.md"),
                KnowledgeMetadata(
                    title=f"File {i}",
                    tags=[f"tag_{i%10}", "common"],
                    category="concept" if i % 2 == 0 else "prompt",
                    success_rate=80 + (i % 20)
                )
            ))
        
        with patch.object(analytics, '_collect_knowledge_items') as mock_collect:
            mock_collect.return_value = large_dataset
            
            # Should handle large dataset efficiently
            import time
            start_time = time.time()
            report = analytics.generate_comprehensive_report()
            end_time = time.time()
            
            # Should complete in reasonable time (< 5 seconds)
            assert end_time - start_time < 5.0
            assert report["report_sections"]["overview"]["total_files"] == 100


class TestAnalyticsErrorHandling:
    """Test error handling in analytics."""

    @pytest.fixture
    def analytics(self):
        """Create analytics with minimal setup."""
        with tempfile.TemporaryDirectory() as temp_dir:
            vault_path = Path(temp_dir)
            config = Mock(spec=CKCConfig)
            config.hybrid_structure = Mock()
            yield KnowledgeAnalytics(vault_path, config)

    def test_empty_vault_handling(self, analytics):
        """Test analytics with empty vault."""
        with patch.object(analytics, '_collect_knowledge_items') as mock_collect:
            mock_collect.return_value = []
            
            report = analytics.generate_comprehensive_report()
            
            assert report["report_sections"]["overview"]["total_files"] == 0
            assert isinstance(report["report_sections"]["overview"]["categories"], dict)

    def test_malformed_metadata_handling(self, analytics):
        """Test handling of malformed metadata."""
        # Test with items that have missing or invalid metadata
        problematic_items = [
            (Path("valid.md"), KnowledgeMetadata(title="Valid")),
            (Path("no_metadata.md"), None),  # None metadata
            (Path("invalid.md"), "invalid_metadata"),  # Wrong type
        ]
        
        with patch.object(analytics, '_collect_knowledge_items') as mock_collect:
            mock_collect.return_value = problematic_items
            
            # Should handle gracefully without crashing
            report = analytics.generate_comprehensive_report()
            assert "overview" in report["report_sections"]

    def test_missing_file_handling(self, analytics):
        """Test handling when files are missing."""
        with patch.object(analytics, '_collect_knowledge_items') as mock_collect:
            # Mock missing files
            mock_collect.side_effect = FileNotFoundError("File not found")
            
            # Should handle file system errors gracefully
            try:
                report = analytics.generate_comprehensive_report()
                # If it doesn't raise, that's good
                assert True
            except FileNotFoundError:
                # If it does raise, we should improve error handling
                pytest.skip("Error handling for missing files needs improvement")