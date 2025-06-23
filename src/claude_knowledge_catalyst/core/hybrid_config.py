"""Hybrid structure configuration for CKC."""

from enum import Enum

from pydantic import BaseModel, Field, field_validator


class DirectoryTier(str, Enum):
    """Directory tier classification."""

    SYSTEM = "system"  # _prefix directories
    CORE = "core"  # numbered directories
    AUXILIARY = "auxiliary"  # no prefix directories


class NumberingSystem(str, Enum):
    """Numbering system types."""

    SEQUENTIAL = "sequential"  # 00, 01, 02, 03...
    TEN_STEP = "ten_step"  # 00, 10, 20, 30...


class DirectoryClassification(BaseModel):
    """Directory classification information."""

    name: str = Field(..., description="Directory name")
    tier: DirectoryTier = Field(..., description="Directory tier")
    prefix: str | None = Field(None, description="Directory prefix")
    number: int | None = Field(None, description="Directory number")
    description: str = Field(..., description="Directory description")
    purpose: str = Field(..., description="Directory purpose")
    auto_organization: bool = Field(True, description="Enable auto organization")


class HybridStructureConfig(BaseModel):
    """Hybrid structure configuration."""

    # Core hybrid settings (always enabled in v2.0)
    enabled: bool = Field(True, description="Always enabled in modern CKC")
    numbering_system: NumberingSystem = Field(
        NumberingSystem.TEN_STEP, description="Modern 10-step numbering system"
    )
    structure_version: str = Field("hybrid_v1", description="Modern structure version")

    # Auto features (always enabled for modern workflow)
    auto_classification: bool = Field(True, description="Auto category classification")
    auto_enhancement: bool = Field(True, description="Auto metadata enhancement")
    structure_validation: bool = Field(True, description="Structure validation")

    # Custom structure definitions (optional)
    custom_structure: dict[str, dict[str, str]] | None = Field(
        None, description="Custom structure definitions"
    )
    custom_numbering: dict[str, int] | None = Field(
        None, description="Custom numbering assignments"
    )

    @field_validator("numbering_system")
    @classmethod
    def validate_numbering_system(cls, v: NumberingSystem) -> NumberingSystem:
        """Validate numbering system."""
        if not isinstance(v, NumberingSystem):
            if isinstance(v, str):
                try:
                    return NumberingSystem(v.lower())
                except ValueError:
                    raise ValueError(f"Invalid numbering system: {v}") from None
            raise ValueError(f"Invalid numbering system type: {type(v)}")
        return v

    def get_default_structure(self) -> dict[str, dict[str, str]]:
        """Get default structure based on numbering system."""
        if self.numbering_system == NumberingSystem.TEN_STEP:
            return self._get_ten_step_structure()
        else:
            return self._get_sequential_structure()

    def _get_ten_step_structure(self) -> dict[str, dict[str, str]]:
        """Get ten-step numbering structure."""
        return {
            "system_dirs": {
                "_templates": "テンプレートファイル集",
                "_attachments": "メディア・添付ファイル",
                "_scripts": "自動化スクリプト",
                "_docs": "システムドキュメント",
                "_commands": "スラッシュコマンド・自動化",
            },
            "core_dirs": {
                "00_Catalyst_Lab": "実験・プロトタイプ開発",
                "10_Projects": "アクティブプロジェクト管理",
                "20_Knowledge_Base": "構造化知識ベース",
                "30_Wisdom_Archive": "長期保管・成熟知識",
            },
            "auxiliary_dirs": {
                "Analytics": "分析・レポート",
                "Archive": "非アクティブアーカイブ",
                "Evolution_Log": "改善・進化の記録",
            },
        }

    def _get_sequential_structure(self) -> dict[str, dict[str, str]]:
        """Legacy sequential structure (deprecated in v2.0)."""
        # Legacy structure is no longer supported - return modern structure
        return self._get_ten_step_structure()

    def get_knowledge_base_structure(self) -> dict[str, dict[str, str]]:
        """Get Knowledge_Base detailed structure."""
        return {
            "20_Knowledge_Base": {
                "description": "構造化知識ベース",
                "subdirectories": {
                    "Prompts": {
                        "description": "プロンプト関連知識",
                        "subdirs": {
                            "Templates": "汎用プロンプトテンプレート",
                            "Best_Practices": "成功事例・ベストプラクティス",
                            "Improvement_Log": "プロンプト改善の記録",
                            "Domain_Specific": "領域特化プロンプト",
                        },
                    },
                    "Code_Snippets": {
                        "description": "コードスニペット集",
                        "subdirs": {
                            "Python": "Python関連",
                            "JavaScript": "JavaScript関連",
                            "TypeScript": "TypeScript関連",
                            "Shell": "シェルスクリプト",
                            "Other_Languages": "その他言語",
                        },
                    },
                    "Concepts": {
                        "description": "AI・LLM関連概念整理",
                        "subdirs": {
                            "AI_Fundamentals": "AI基礎概念",
                            "LLM_Architecture": "LLMアーキテクチャ",
                            "Development_Patterns": "開発パターン",
                            "Best_Practices": "業界ベストプラクティス",
                        },
                    },
                    "Resources": {
                        "description": "学習リソース・外部参考資料",
                        "subdirs": {
                            "Documentation": "公式ドキュメント",
                            "Tutorials": "チュートリアル",
                            "Research_Papers": "研究論文",
                            "Tools_And_Services": "ツール・サービス情報",
                        },
                    },
                },
            }
        }

    def classify_directory(self, dir_name: str) -> DirectoryClassification:
        """Classify a directory based on naming conventions."""
        if dir_name.startswith("_"):
            return DirectoryClassification(
                name=dir_name,
                tier=DirectoryTier.SYSTEM,
                prefix="_",
                number=None,
                description=f"System directory: {dir_name[1:]}",
                purpose="System management and automation",
            )

        # Check for numbered directories
        import re

        number_match = re.match(r"^(\d+)_(.+)$", dir_name)
        if number_match:
            number = int(number_match.group(1))
            name_part = number_match.group(2)

            return DirectoryClassification(
                name=dir_name,
                tier=DirectoryTier.CORE,
                prefix=f"{number:02d}_",
                number=number,
                description=f"Core workflow directory: {name_part}",
                purpose="Main knowledge organization",
            )

        # Auxiliary directory (no prefix)
        return DirectoryClassification(
            name=dir_name,
            tier=DirectoryTier.AUXILIARY,
            prefix=None,
            number=None,
            description=f"Auxiliary directory: {dir_name}",
            purpose="Supporting functionality",
        )


class NumberManagerConfig(BaseModel):
    """Number manager configuration."""

    system_type: NumberingSystem = Field(
        NumberingSystem.TEN_STEP, description="Numbering system type"
    )
    base_numbers: list[int] = Field(
        default_factory=lambda: [0, 10, 20, 30],
        description="Base numbers for ten-step system",
    )
    step_size: int = Field(10, description="Step size between numbers")
    max_number: int = Field(990, description="Maximum allowed number")

    def get_next_available_number(self, after: int) -> int:
        """Get next available number after specified number."""
        if self.system_type == NumberingSystem.SEQUENTIAL:
            return after + 1

        # Ten-step system
        if after in self.base_numbers:
            index = self.base_numbers.index(after)
            if index < len(self.base_numbers) - 1:
                # Return midpoint between current and next base number
                next_base = self.base_numbers[index + 1]
                return after + (next_base - after) // 2
            else:
                # Return next step after last base number
                return after + self.step_size
        else:
            # For non-base numbers, just add step size
            return min(after + self.step_size, self.max_number)

    def can_insert_between(self, before: int, after: int) -> bool:
        """Check if number can be inserted between two numbers."""
        if self.system_type == NumberingSystem.SEQUENTIAL:
            return (after - before) > 1

        # Ten-step system allows insertion if gap >= step_size
        return (after - before) >= self.step_size

    def suggest_number_for_category(self, category: str) -> int:
        """Suggest number for category based on common patterns."""
        category_mapping = {
            "experimental": 0,
            "catalyst": 0,
            "lab": 0,
            "projects": 10,
            "active": 10,
            "knowledge": 20,
            "base": 20,
            "wisdom": 30,
            "archive": 30,
            "mature": 30,
        }

        category_lower = category.lower()
        for key, number in category_mapping.items():
            if key in category_lower:
                return number

        # Default to first available number
        return self.base_numbers[0] if self.base_numbers else 0
