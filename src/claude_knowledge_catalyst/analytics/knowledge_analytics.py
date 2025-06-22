"""Knowledge analytics and insights for CKC."""

import json
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt

from ..core.config import CKCConfig
from ..core.metadata import KnowledgeMetadata, MetadataManager
from ..core.structure_validator import StructureHealthMonitor


class KnowledgeAnalytics:
    """Comprehensive knowledge analytics and insights."""

    def __init__(self, vault_path: Path, config: CKCConfig):
        self.vault_path = vault_path
        self.config = config
        self.metadata_manager = MetadataManager()
        self.health_monitor = StructureHealthMonitor(
            vault_path, config.hybrid_structure
        )

        # Analytics storage
        self.analytics_dir = vault_path / "Analytics"
        self.analytics_dir.mkdir(exist_ok=True)

        # Reports storage
        self.reports_dir = self.analytics_dir / "reports"
        self.reports_dir.mkdir(exist_ok=True)

        # Data cache
        self._cache = {}
        self._cache_timestamp = None

    def generate_comprehensive_report(self) -> dict[str, Any]:
        """Generate comprehensive analytics report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "vault_path": str(self.vault_path),
            "report_sections": {},
        }

        # Collect all knowledge items
        knowledge_items = self._collect_knowledge_items()

        # Generate report sections
        report["report_sections"]["overview"] = self._generate_overview(knowledge_items)
        report["report_sections"]["content_analysis"] = (
            self._analyze_content_distribution(knowledge_items)
        )
        report["report_sections"]["quality_metrics"] = self._analyze_quality_metrics(
            knowledge_items
        )
        report["report_sections"]["usage_patterns"] = self._analyze_usage_patterns(
            knowledge_items
        )
        report["report_sections"]["knowledge_evolution"] = (
            self._analyze_knowledge_evolution(knowledge_items)
        )
        report["report_sections"]["structure_health"] = self._analyze_structure_health()
        report["report_sections"]["recommendations"] = self._generate_recommendations(
            knowledge_items
        )

        # Save report
        self._save_report(report)

        return report

    def _collect_knowledge_items(self) -> list[tuple[Path, KnowledgeMetadata]]:
        """Collect all knowledge items with metadata."""
        # Check cache
        if self._cache_timestamp and datetime.now() - self._cache_timestamp < timedelta(
            hours=1
        ):
            return self._cache.get("knowledge_items", [])

        knowledge_items = []

        # Find all markdown files
        md_files = list(self.vault_path.rglob("*.md"))

        for md_file in md_files:
            if md_file.name == "README.md":
                continue

            try:
                metadata = self.metadata_manager.extract_metadata_from_file(md_file)
                knowledge_items.append((md_file, metadata))
            except Exception as e:
                print(f"Warning: Could not extract metadata from {md_file}: {e}")

        # Cache results
        self._cache["knowledge_items"] = knowledge_items
        self._cache_timestamp = datetime.now()

        return knowledge_items

    def _generate_overview(
        self, knowledge_items: list[tuple[Path, KnowledgeMetadata]]
    ) -> dict[str, Any]:
        """Generate overview statistics."""
        overview = {
            "total_files": len(knowledge_items),
            "content_distribution": defaultdict(int),
            "tag_distribution": Counter(),
            "status_distribution": Counter(),
            "quality_distribution": Counter(),
            "creation_timeline": defaultdict(int),
            "update_timeline": defaultdict(int),
        }

        for file_path, metadata in knowledge_items:
            # Content distribution by directory
            relative_path = file_path.relative_to(self.vault_path)
            main_dir = str(relative_path.parts[0]) if relative_path.parts else "root"
            overview["content_distribution"][main_dir] += 1

            # Tag distribution
            for tag in metadata.tags:
                overview["tag_distribution"][tag] += 1

            # Status and confidence (quality renamed to confidence in metadata model)
            overview["status_distribution"][metadata.status] += 1
            if metadata.confidence:
                overview["quality_distribution"][metadata.confidence] += 1

            # Timeline analysis
            created_month = metadata.created.strftime("%Y-%m")
            updated_month = metadata.updated.strftime("%Y-%m")
            overview["creation_timeline"][created_month] += 1
            overview["update_timeline"][updated_month] += 1

        # Convert defaultdicts to regular dicts for JSON serialization
        overview["content_distribution"] = dict(overview["content_distribution"])
        overview["creation_timeline"] = dict(overview["creation_timeline"])
        overview["update_timeline"] = dict(overview["update_timeline"])

        return overview

    def _analyze_content_distribution(
        self, knowledge_items: list[tuple[Path, KnowledgeMetadata]]
    ) -> dict[str, Any]:
        """Analyze content distribution and patterns."""
        analysis = {
            "category_distribution": Counter(),
            "complexity_distribution": Counter(),
            "success_rate_analysis": {
                "high_success": 0,  # >80%
                "medium_success": 0,  # 50-80%
                "low_success": 0,  # <50%
                "no_data": 0,
            },
            "content_maturity": {"experimental": 0, "developing": 0, "mature": 0},
            "knowledge_density": {},  # Files per directory
        }

        directory_files = defaultdict(int)

        for file_path, metadata in knowledge_items:
            # Content type analysis (pure tag system)
            if metadata.type:
                analysis["category_distribution"][metadata.type] += 1

            # Complexity analysis (if available)
            if metadata.complexity:
                analysis["complexity_distribution"][metadata.complexity] += 1

            # Success rate analysis
            if metadata.success_rate is not None:
                if metadata.success_rate > 80:
                    analysis["success_rate_analysis"]["high_success"] += 1
                elif metadata.success_rate >= 50:
                    analysis["success_rate_analysis"]["medium_success"] += 1
                else:
                    analysis["success_rate_analysis"]["low_success"] += 1
            else:
                analysis["success_rate_analysis"]["no_data"] += 1

            # Content maturity
            if metadata.status in ["draft", "experimental"]:
                analysis["content_maturity"]["experimental"] += 1
            elif metadata.status in ["testing", "review"]:
                analysis["content_maturity"]["developing"] += 1
            else:
                analysis["content_maturity"]["mature"] += 1

            # Knowledge density
            relative_path = file_path.relative_to(self.vault_path)
            main_dir = str(relative_path.parts[0]) if relative_path.parts else "root"
            directory_files[main_dir] += 1

        analysis["knowledge_density"] = dict(directory_files)

        return analysis

    def _analyze_quality_metrics(
        self, knowledge_items: list[tuple[Path, KnowledgeMetadata]]
    ) -> dict[str, Any]:
        """Analyze quality metrics and trends."""
        metrics = {
            "metadata_completeness": {
                "has_title": 0,
                "has_tags": 0,
                "has_category": 0,
                "has_purpose": 0,
                "has_quality_rating": 0,
                "complete_metadata": 0,
            },
            "content_quality_indicators": {
                "high_quality": 0,
                "medium_quality": 0,
                "low_quality": 0,
                "quality_unknown": 0,
            },
            "validation_metrics": {
                "files_with_success_rate": 0,
                "average_success_rate": 0,
                "confidence_distribution": Counter(),
            },
            "maintenance_metrics": {
                "recently_updated": 0,  # <30 days
                "needs_attention": 0,  # >180 days
                "stale_content": 0,  # >1 year
            },
        }

        total_files = len(knowledge_items)
        success_rates = []
        now = datetime.now()

        for file_path, metadata in knowledge_items:
            # Metadata completeness
            completeness = metrics["metadata_completeness"]

            if metadata.title and metadata.title != "Untitled":
                completeness["has_title"] += 1

            if metadata.tags:
                completeness["has_tags"] += 1

            if metadata.type:
                completeness["has_category"] += 1

            if metadata.purpose:
                completeness["has_purpose"] += 1

            if metadata.confidence:
                completeness["has_quality_rating"] += 1

            # Complete metadata (has most fields)
            complete_count = sum(
                [
                    bool(metadata.title and metadata.title != "Untitled"),
                    bool(metadata.tags),
                    bool(metadata.type),
                    bool(metadata.purpose),
                    bool(metadata.tech or metadata.domain),
                ]
            )

            if complete_count >= 4:
                completeness["complete_metadata"] += 1

            # Quality indicators (using confidence attribute)
            quality_indicators = metrics["content_quality_indicators"]
            if metadata.confidence:
                if metadata.confidence == "high":
                    quality_indicators["high_quality"] += 1
                elif metadata.confidence == "medium":
                    quality_indicators["medium_quality"] += 1
                elif metadata.confidence == "low":
                    quality_indicators["low_quality"] += 1
            else:
                quality_indicators["quality_unknown"] += 1

            # Validation metrics
            validation = metrics["validation_metrics"]
            if metadata.success_rate is not None:
                validation["files_with_success_rate"] += 1
                success_rates.append(metadata.success_rate)

            if metadata.confidence:
                validation["confidence_distribution"][metadata.confidence] += 1

            # Maintenance metrics
            maintenance = metrics["maintenance_metrics"]
            days_since_update = (now - metadata.updated).days

            if days_since_update <= 30:
                maintenance["recently_updated"] += 1
            elif days_since_update > 180:
                maintenance["needs_attention"] += 1

            if days_since_update > 365:
                maintenance["stale_content"] += 1

        # Calculate percentages
        if total_files > 0:
            completeness_keys = list(metrics["metadata_completeness"].keys())
            for key in completeness_keys:
                metrics["metadata_completeness"][f"{key}_percentage"] = (
                    metrics["metadata_completeness"][key] / total_files * 100
                )

        # Calculate average success rate
        if success_rates:
            metrics["validation_metrics"]["average_success_rate"] = sum(
                success_rates
            ) / len(success_rates)

        return metrics

    def _analyze_usage_patterns(
        self, knowledge_items: list[tuple[Path, KnowledgeMetadata]]
    ) -> dict[str, Any]:
        """Analyze usage patterns and trends."""
        patterns = {
            "creation_patterns": {
                "by_month": defaultdict(int),
                "by_day_of_week": defaultdict(int),
                "by_hour": defaultdict(int),
            },
            "update_patterns": {
                "by_month": defaultdict(int),
                "frequent_updaters": Counter(),  # Files updated most often
                "update_intervals": [],
            },
            "content_lifecycle": {
                "new_content": 0,  # <30 days
                "active_content": 0,  # 30-180 days
                "stable_content": 0,  # 180-365 days
                "archived_content": 0,  # >365 days
            },
            "collaboration_patterns": {"authors": Counter(), "projects": Counter()},
        }

        now = datetime.now()

        for file_path, metadata in knowledge_items:
            # Creation patterns
            created = metadata.created
            patterns["creation_patterns"]["by_month"][created.strftime("%Y-%m")] += 1
            patterns["creation_patterns"]["by_day_of_week"][created.strftime("%A")] += 1
            patterns["creation_patterns"]["by_hour"][created.hour] += 1

            # Update patterns
            updated = metadata.updated
            patterns["update_patterns"]["by_month"][updated.strftime("%Y-%m")] += 1

            # Update frequency (if we have version history)
            if metadata.version and metadata.version != "1.0":
                patterns["update_patterns"]["frequent_updaters"][str(file_path)] += 1

            # Update intervals
            update_interval = (updated - created).days
            if update_interval > 0:
                patterns["update_patterns"]["update_intervals"].append(update_interval)

            # Content lifecycle
            days_since_creation = (now - created).days
            if days_since_creation <= 30:
                patterns["content_lifecycle"]["new_content"] += 1
            elif days_since_creation <= 180:
                patterns["content_lifecycle"]["active_content"] += 1
            elif days_since_creation <= 365:
                patterns["content_lifecycle"]["stable_content"] += 1
            else:
                patterns["content_lifecycle"]["archived_content"] += 1

            # Collaboration patterns
            if metadata.author:
                patterns["collaboration_patterns"]["authors"][metadata.author] += 1

            for project in metadata.projects:
                patterns["collaboration_patterns"]["projects"][project] += 1

        # Convert defaultdicts to regular dicts
        patterns["creation_patterns"] = {
            k: dict(v) for k, v in patterns["creation_patterns"].items()
        }
        patterns["update_patterns"]["by_month"] = dict(
            patterns["update_patterns"]["by_month"]
        )

        return patterns

    def _analyze_knowledge_evolution(
        self, knowledge_items: list[tuple[Path, KnowledgeMetadata]]
    ) -> dict[str, Any]:
        """Analyze how knowledge evolves over time."""
        evolution = {
            "knowledge_growth": {
                "total_growth_rate": 0,
                "monthly_growth": defaultdict(int),
                "category_growth": defaultdict(lambda: defaultdict(int)),
            },
            "knowledge_maturation": {
                "status_transitions": Counter(),
                "quality_improvements": 0,
                "success_rate_trends": [],
            },
            "knowledge_connections": {
                "most_connected_topics": Counter(),
                "project_knowledge_map": defaultdict(list),
                "tag_relationships": defaultdict(set),
            },
        }

        # Sort by creation date for growth analysis
        sorted_items = sorted(knowledge_items, key=lambda x: x[1].created)

        # Calculate growth rates
        if sorted_items:
            first_date = sorted_items[0][1].created
            last_date = sorted_items[-1][1].created
            total_days = (last_date - first_date).days

            if total_days > 0:
                evolution["knowledge_growth"]["total_growth_rate"] = (
                    len(knowledge_items) / total_days
                )

        # Monthly growth and category distribution
        for file_path, metadata in sorted_items:
            month = metadata.created.strftime("%Y-%m")
            evolution["knowledge_growth"]["monthly_growth"][month] += 1

            if metadata.type:
                evolution["knowledge_growth"]["category_growth"][metadata.type][
                    month
                ] += 1

        # Knowledge connections and relationships
        for file_path, metadata in knowledge_items:
            # Tag relationships
            for i, tag1 in enumerate(metadata.tags):
                for tag2 in metadata.tags[i + 1 :]:
                    evolution["knowledge_connections"]["tag_relationships"][tag1].add(
                        tag2
                    )
                    evolution["knowledge_connections"]["tag_relationships"][tag2].add(
                        tag1
                    )

            # Project connections
            for project in metadata.projects:
                evolution["knowledge_connections"]["project_knowledge_map"][
                    project
                ].append(
                    {
                        "file": str(file_path),
                        "type": metadata.type,
                        "tags": metadata.tags,
                        "tech": metadata.tech,
                        "domain": metadata.domain,
                    }
                )

            # Most connected topics (by tag frequency)
            for tag in metadata.tags:
                evolution["knowledge_connections"]["most_connected_topics"][tag] += 1

        # Convert defaultdicts and sets for serialization
        evolution["knowledge_growth"]["monthly_growth"] = dict(
            evolution["knowledge_growth"]["monthly_growth"]
        )
        evolution["knowledge_growth"]["category_growth"] = {
            k: dict(v)
            for k, v in evolution["knowledge_growth"]["category_growth"].items()
        }
        evolution["knowledge_connections"]["project_knowledge_map"] = dict(
            evolution["knowledge_connections"]["project_knowledge_map"]
        )
        evolution["knowledge_connections"]["tag_relationships"] = {
            k: list(v)
            for k, v in evolution["knowledge_connections"]["tag_relationships"].items()
        }

        return evolution

    def _analyze_structure_health(self) -> dict[str, Any]:
        """Analyze structural health metrics."""
        health_result = self.health_monitor.run_health_check()
        trend_data = self.health_monitor.get_health_trend(days=30)

        return {
            "current_health": health_result.to_dict(),
            "health_trends": trend_data,
            "structure_recommendations": self._generate_structure_recommendations(
                health_result
            ),
        }

    def _generate_recommendations(
        self, knowledge_items: list[tuple[Path, KnowledgeMetadata]]
    ) -> list[dict[str, Any]]:
        """Generate actionable recommendations."""
        recommendations = []

        # Analyze current state
        total_files = len(knowledge_items)
        files_without_tags = sum(1 for _, m in knowledge_items if not m.tags)
        files_without_category = sum(1 for _, m in knowledge_items if not m.type)
        outdated_files = sum(
            1 for _, m in knowledge_items if (datetime.now() - m.updated).days > 180
        )

        # Generate specific recommendations
        if files_without_tags > total_files * 0.2:
            recommendations.append(
                {
                    "priority": "high",
                    "category": "metadata_quality",
                    "title": "Improve Tag Coverage",
                    "description": f"{files_without_tags} files lack tags. Add tags to improve discoverability.",
                    "action": "Review files without tags and add relevant tags",
                    "impact": "Improved content organization and searchability",
                }
            )

        if files_without_category > total_files * 0.3:
            recommendations.append(
                {
                    "priority": "medium",
                    "category": "metadata_quality",
                    "title": "Add Missing Categories",
                    "description": f"{files_without_category} files lack categories.",
                    "action": "Assign appropriate categories to uncategorized files",
                    "impact": "Better content classification and navigation",
                }
            )

        if outdated_files > total_files * 0.1:
            recommendations.append(
                {
                    "priority": "medium",
                    "category": "content_maintenance",
                    "title": "Review Outdated Content",
                    "description": f"{outdated_files} files haven't been updated in 6+ months.",
                    "action": "Review and update or archive outdated content",
                    "impact": "Maintain content relevance and accuracy",
                }
            )

        # Quality-based recommendations
        high_quality_files = sum(
            1 for _, m in knowledge_items if m.confidence == "high"
        )
        if high_quality_files < total_files * 0.3:
            recommendations.append(
                {
                    "priority": "low",
                    "category": "quality_improvement",
                    "title": "Promote High-Quality Content",
                    "description": "Consider promoting more content to high quality status.",
                    "action": "Review and upgrade quality ratings for mature content",
                    "impact": "Better identification of trusted knowledge",
                }
            )

        return recommendations

    def _generate_structure_recommendations(self, health_result) -> list[str]:
        """Generate structure-specific recommendations."""
        recommendations = []

        if not health_result.passed:
            recommendations.append(
                "Fix structural validation errors to improve vault health"
            )

        if health_result.warnings:
            recommendations.append("Address validation warnings for optimal structure")

        stats = health_result.statistics
        if stats.get("readme_files", 0) < stats.get("total_directories", 1):
            recommendations.append(
                "Add README files to directories for better navigation"
            )

        return recommendations

    def _save_report(self, report: dict[str, Any]):
        """Save analytics report."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"analytics_report_{timestamp}.json"

        try:
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        except Exception as e:
            print(f"Warning: Could not save analytics report: {e}")

    def generate_visualizations(self, report: dict[str, Any]) -> dict[str, Path]:
        """Generate visualization charts from analytics data."""
        visualizations = {}
        viz_dir = self.analytics_dir / "visualizations"
        viz_dir.mkdir(exist_ok=True)

        # Set style
        try:
            plt.style.use("seaborn-v0_8")
        except OSError:
            # Fallback if seaborn style not available
            plt.style.use("default")

        try:
            # Content distribution pie chart
            content_dist = report["report_sections"]["overview"]["content_distribution"]
            if content_dist:
                plt.figure(figsize=(10, 8))
                plt.pie(
                    content_dist.values(), labels=content_dist.keys(), autopct="%1.1f%%"
                )
                plt.title("Content Distribution by Directory")
                viz_path = viz_dir / "content_distribution.png"
                plt.savefig(viz_path, dpi=300, bbox_inches="tight")
                plt.close()
                visualizations["content_distribution"] = viz_path

            # Tag frequency bar chart
            tag_dist = report["report_sections"]["overview"]["tag_distribution"]
            if tag_dist:
                top_tags = dict(Counter(tag_dist).most_common(15))
                plt.figure(figsize=(12, 6))
                plt.bar(range(len(top_tags)), list(top_tags.values()))
                plt.xticks(range(len(top_tags)), list(top_tags.keys()), rotation=45)
                plt.title("Top 15 Most Used Tags")
                plt.ylabel("Frequency")
                viz_path = viz_dir / "tag_frequency.png"
                plt.savefig(viz_path, dpi=300, bbox_inches="tight")
                plt.close()
                visualizations["tag_frequency"] = viz_path

            # Knowledge growth timeline
            creation_timeline = report["report_sections"]["overview"][
                "creation_timeline"
            ]
            if creation_timeline:
                months = sorted(creation_timeline.keys())
                counts = [creation_timeline[month] for month in months]

                plt.figure(figsize=(12, 6))
                plt.plot(months, counts, marker="o")
                plt.title("Knowledge Creation Timeline")
                plt.xlabel("Month")
                plt.ylabel("Files Created")
                plt.xticks(rotation=45)
                viz_path = viz_dir / "knowledge_growth.png"
                plt.savefig(viz_path, dpi=300, bbox_inches="tight")
                plt.close()
                visualizations["knowledge_growth"] = viz_path

        except Exception as e:
            print(f"Warning: Could not generate visualizations: {e}")

        return visualizations


def generate_analytics_report(vault_path: Path, config: CKCConfig) -> dict[str, Any]:
    """Convenience function to generate analytics report."""
    analytics = KnowledgeAnalytics(vault_path, config)
    return analytics.generate_comprehensive_report()
