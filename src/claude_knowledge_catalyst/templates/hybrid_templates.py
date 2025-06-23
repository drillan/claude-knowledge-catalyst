"""Hybrid structure-aware template system for CKC."""

from datetime import datetime
from pathlib import Path
from typing import Any

from ..core.config import CKCConfig
from ..core.hybrid_config import DirectoryTier, HybridStructureConfig
from .manager import TemplateManager


class HybridTemplateManager(TemplateManager):
    """Template manager with hybrid structure awareness."""

    def __init__(self, template_path: Path, hybrid_config: HybridStructureConfig):
        super().__init__(template_path)
        self.hybrid_config = hybrid_config

        # Hybrid-specific templates
        self.hybrid_templates = {
            "catalyst_experiment": self._create_catalyst_experiment_template,
            "project_kickoff": self._create_project_kickoff_template,
            "knowledge_article": self._create_knowledge_article_template,
            "wisdom_distillation": self._create_wisdom_distillation_template,
            "prompt_template": self._create_prompt_template,
            "code_snippet": self._create_code_snippet_template,
            "concept_explanation": self._create_concept_explanation_template,
            "resource_catalog": self._create_resource_catalog_template,
            "structure_readme": self._create_structure_readme_template,
        }

    def get_template_for_directory(self, directory_path: str) -> str:
        """Get appropriate template based on target directory."""

        # Parse directory to understand tier and purpose
        dir_parts = directory_path.split("/")
        main_dir = dir_parts[0] if dir_parts else ""

        classification = self.hybrid_config.classify_directory(main_dir)

        # Select template based on directory classification
        if classification.tier == DirectoryTier.SYSTEM:
            if "_templates" in main_dir:
                return "template_meta"
            elif "_scripts" in main_dir:
                return "script_documentation"
            else:
                return "system_documentation"

        elif classification.tier == DirectoryTier.CORE:
            if main_dir.startswith("00_"):  # Catalyst Lab
                return "catalyst_experiment"
            elif main_dir.startswith("10_"):  # Projects
                return "project_kickoff"
            elif main_dir.startswith("20_"):  # Knowledge Base
                return self._get_knowledge_base_template(directory_path)
            elif main_dir.startswith("30_"):  # Wisdom Archive
                return "wisdom_distillation"

        elif classification.tier == DirectoryTier.AUXILIARY:
            if "Analytics" in main_dir:
                return "analytics_report"
            elif "Archive" in main_dir:
                return "archived_content"
            elif "Evolution_Log" in main_dir:
                return "evolution_entry"

        # Default to basic template
        return "basic_markdown"

    def _get_knowledge_base_template(self, directory_path: str) -> str:
        """Get specific template for Knowledge Base subdirectories."""
        if "Prompts" in directory_path:
            return "prompt_template"
        elif "Code_Snippets" in directory_path:
            return "code_snippet"
        elif "Concepts" in directory_path:
            return "concept_explanation"
        elif "Resources" in directory_path:
            return "resource_catalog"
        else:
            return "knowledge_article"

    def create_file_from_template(
        self, template_name: str, target_path: Path, context: dict[str, Any]
    ) -> bool:
        """Create file from template with hybrid-aware context."""

        # Enhance context with hybrid structure information
        enhanced_context = self._enhance_context_for_hybrid(context, target_path)

        # Check if it's a hybrid-specific template
        if template_name in self.hybrid_templates:
            template_content = self.hybrid_templates[template_name](enhanced_context)
        else:
            # Use base template manager
            template_content = self.get_template_content(
                template_name, enhanced_context
            )

        # Write to file
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(template_content, encoding="utf-8")
            return True
        except Exception as e:
            print(f"Error creating file from template: {e}")
            return False

    def _enhance_context_for_hybrid(
        self, context: dict[str, Any], target_path: Path
    ) -> dict[str, Any]:
        """Enhance context with hybrid structure information."""
        enhanced = dict(context)

        # Add path analysis
        relative_path = str(target_path.relative_to(target_path.anchor))
        path_parts = relative_path.split("/")

        if len(path_parts) > 0:
            main_dir = path_parts[0]
            classification = self.hybrid_config.classify_directory(main_dir)

            enhanced.update(
                {
                    "directory_tier": classification.tier.value,
                    "directory_purpose": classification.purpose,
                    "directory_number": classification.number,
                    "directory_prefix": classification.prefix,
                    "main_directory": main_dir,
                    "subdirectory_path": "/".join(path_parts[1:])
                    if len(path_parts) > 1
                    else "",
                    "numbering_system": self.hybrid_config.numbering_system.value,
                    "structure_version": self.hybrid_config.structure_version,
                }
            )

        # Add current date/time
        now = datetime.now()
        enhanced.update(
            {
                "current_date": now.strftime("%Y-%m-%d"),
                "current_datetime": now.isoformat(),
                "current_timestamp": now.strftime("%Y%m%d_%H%M%S"),
            }
        )

        return enhanced

    def _create_catalyst_experiment_template(self, context: dict[str, Any]) -> str:
        """Create template for Catalyst Lab experiments."""
        return f"""---
title: "{context.get("title", "New Experiment")}"
created: "{context["current_datetime"]}"
updated: "{context["current_datetime"]}"
version: "1.0"
category: "experiment"
status: "draft"
tags: ["catalyst", "experiment", "prototype"]
confidence: "low"
success_rate: null
purpose: "Experimental exploration and rapid prototyping"
related_projects: []
quality: "experimental"
author: "{context.get("author", "Unknown")}"
---

# {context.get("title", "New Experiment")}

## 🧪 Experiment Overview

**Hypothesis**: {context.get("hypothesis", "State your hypothesis here")}

**Expected Outcome**: {context.get("expected_outcome", "Describe what you expect to learn or achieve")}

## 🎯 Objective

{context.get("objective", "Clearly define the objective of this experiment")}

## 🔬 Methodology

### Approach
{context.get("methodology", "Describe your experimental approach")}

### Variables
- **Independent**: 
- **Dependent**: 
- **Controls**: 

## 📊 Data Collection

### Metrics to Track
- 
- 
- 

### Collection Method
{context.get("collection_method", "How will you collect and measure data?")}

## 🚀 Implementation

### Step 1: Setup
{context.get("step1", "Describe initial setup")}

### Step 2: Execution
{context.get("step2", "Describe execution phase")}

### Step 3: Analysis
{context.get("step3", "Describe analysis phase")}

## 📈 Results

*Document results as experiment progresses*

### Observations
- 

### Data
- 

### Insights
- 

## 🎯 Conclusions

*To be filled after experiment completion*

### Success Criteria Met
- [ ] 
- [ ] 
- [ ] 

### Key Learnings
- 

### Next Steps
- 

### Promotion Candidates
*Mark items ready for promotion to 10_Projects*
- [ ] 
- [ ] 

---

**Experiment Status**: In Progress | Completed | Abandoned  
**Last Updated**: {context["current_date"]}  
**Directory**: {context.get("main_directory", "00_Catalyst_Lab")}  
**Structure**: {context.get("numbering_system", "ten_step")} system
"""

    def _create_project_kickoff_template(self, context: dict[str, Any]) -> str:
        """Create template for project kickoff."""
        return f"""---
title: "{context.get("title", "New Project")}"
created: "{context["current_datetime"]}"
updated: "{context["current_datetime"]}"
version: "1.0"
category: "project"
status: "planning"
tags: ["project", "active", "planning"]
purpose: "Active project management and execution"
related_projects: []
quality: "high"
author: "{context.get("author", "Unknown")}"
project_phase: "kickoff"
priority: "{context.get("priority", "medium")}"
deadline: "{context.get("deadline", "TBD")}"
---

# {context.get("title", "New Project")}

## 📋 Project Overview

**Start Date**: {context["current_date"]}  
**Target Completion**: {context.get("deadline", "TBD")}  
**Priority**: {context.get("priority", "Medium")}  
**Phase**: Planning

## 🎯 Project Goals

### Primary Objective
{context.get("primary_objective", "Define the main goal of this project")}

### Success Criteria
- [ ] {context.get("success_criteria_1", "Define measurable success criterion 1")}
- [ ] {context.get("success_criteria_2", "Define measurable success criterion 2")}
- [ ] {context.get("success_criteria_3", "Define measurable success criterion 3")}

## 👥 Stakeholders

### Project Team
- **Project Lead**: {context.get("project_lead", "TBD")}
- **Team Members**: {context.get("team_members", "TBD")}

### External Stakeholders
- {context.get("stakeholders", "List key stakeholders")}

## 📊 Project Scope

### In Scope
- {context.get("in_scope", "What is included in this project")}

### Out of Scope
- {context.get("out_of_scope", "What is explicitly excluded")}

### Dependencies
- {context.get("dependencies", "External dependencies and prerequisites")}

## 🗓️ Timeline & Milestones

### Phase 1: Planning
- **Duration**: {context.get("phase1_duration", "1-2 weeks")}
- **Deliverables**: Project plan, requirements, resource allocation

### Phase 2: Implementation
- **Duration**: {context.get("phase2_duration", "TBD")}
- **Deliverables**: {context.get("phase2_deliverables", "Core implementation")}

### Phase 3: Testing & Refinement
- **Duration**: {context.get("phase3_duration", "TBD")}
- **Deliverables**: {context.get("phase3_deliverables", "Tested and refined solution")}

### Phase 4: Delivery
- **Duration**: {context.get("phase4_duration", "TBD")}
- **Deliverables**: {context.get("phase4_deliverables", "Final delivery and documentation")}

## 🔧 Technical Approach

### Architecture
{context.get("architecture", "Describe technical architecture and approach")}

### Technology Stack
- {context.get("tech_stack", "List key technologies")}

### Integration Points
- {context.get("integrations", "External systems and APIs")}

## ⚠️ Risk Management

### High-Risk Items
- **Risk**: {context.get("risk1", "Identify key risk")}
  - **Mitigation**: {context.get("mitigation1", "How to mitigate this risk")}

### Medium-Risk Items
- **Risk**: {context.get("risk2", "Identify medium risk")}
  - **Mitigation**: {context.get("mitigation2", "Mitigation strategy")}

## 📈 Success Metrics

### Quantitative Metrics
- {context.get("quantitative_metrics", "Measurable KPIs")}

### Qualitative Metrics
- {context.get("qualitative_metrics", "Quality measures")}

## 📚 Resources & References

### Knowledge Base Links
- [[20_Knowledge_Base/Concepts/]] - Related concepts
- [[20_Knowledge_Base/Code_Snippets/]] - Reusable code
- [[20_Knowledge_Base/Resources/]] - External references

### Tools & Platforms
- {context.get("tools", "Development and project management tools")}

---

**Project Status**: Planning | In Progress | Testing | Complete | On Hold  
**Last Updated**: {context["current_date"]}  
**Directory**: {context.get("main_directory", "10_Projects")}  
**Next Review**: {context.get("next_review", "TBD")}
"""

    def _create_knowledge_article_template(self, context: dict[str, Any]) -> str:
        """Create template for Knowledge Base articles."""
        return f"""---
title: "{context.get("title", "Knowledge Article")}"
created: "{context["current_datetime"]}"
updated: "{context["current_datetime"]}"
version: "1.0"
category: "knowledge"
status: "draft"
tags: ["knowledge", "documentation"]
purpose: "Structured knowledge preservation and sharing"
related_projects: []
quality: "high"
author: "{context.get("author", "Unknown")}"
knowledge_type: "{context.get("knowledge_type", "general")}"
complexity: "{context.get("complexity", "intermediate")}"
---

# {context.get("title", "Knowledge Article")}

## 📋 Overview

**Knowledge Type**: {context.get("knowledge_type", "General")}  
**Complexity Level**: {context.get("complexity", "Intermediate")}  
**Last Verified**: {context["current_date"]}

## 🎯 Key Concepts

### Core Principle
{context.get("core_principle", "Explain the fundamental concept or principle")}

### Related Concepts
- [[Related Concept 1]]
- [[Related Concept 2]]
- [[Related Concept 3]]

## 📚 Detailed Explanation

### Background
{context.get("background", "Provide context and background information")}

### How It Works
{context.get("how_it_works", "Explain the mechanism or process")}

### Key Components
1. **Component 1**: {context.get("component1", "Description")}
2. **Component 2**: {context.get("component2", "Description")}
3. **Component 3**: {context.get("component3", "Description")}

## 💡 Practical Application

### Use Cases
- **Use Case 1**: {context.get("use_case1", "When and how to apply this knowledge")}
- **Use Case 2**: {context.get("use_case2", "Alternative application scenario")}

### Best Practices
- {context.get("best_practice1", "Recommended approach or pattern")}
- {context.get("best_practice2", "Additional best practice")}

### Common Pitfalls
- {context.get("pitfall1", "What to avoid and why")}
- {context.get("pitfall2", "Additional pitfall to watch for")}

## 🔗 Implementation

### Code Examples
{
            context.get(
                "code_example",
                '''```python
# Example implementation
def example_function():
    pass
```''',
            )
        }

### Configuration
{context.get("configuration", "Any configuration or setup requirements")}

## 📊 Performance & Considerations

### Performance Characteristics
- {context.get("performance", "Performance implications and characteristics")}

### Trade-offs
- **Pros**: {context.get("pros", "Advantages and benefits")}
- **Cons**: {context.get("cons", "Limitations and drawbacks")}

### Alternatives
- **Alternative 1**: {context.get("alternative1", "Other approaches to consider")}
- **Alternative 2**: {context.get("alternative2", "Additional alternatives")}

## 🧪 Testing & Validation

### Verification Methods
- {context.get("verification", "How to test or verify the concept")}

### Quality Metrics
- {context.get("quality_metrics", "How to measure success or quality")}

## 📖 Further Reading

### Internal References
- [[20_Knowledge_Base/Concepts/]] - Related concepts
- [[20_Knowledge_Base/Resources/]] - Additional resources

### External Resources
- {context.get("external_resources", "Books, articles, documentation links")}

---

**Knowledge Status**: Draft | Reviewed | Validated | Expert-Level  
**Last Updated**: {context["current_date"]}  
**Directory**: {context.get("main_directory", "20_Knowledge_Base")}  
**Verification Due**: {context.get("verification_due", "TBD")}
"""

    def _create_wisdom_distillation_template(self, context: dict[str, Any]) -> str:
        """Create template for Wisdom Archive distillation."""
        return f"""---
title: "{context.get("title", "Wisdom Distillation")}"
created: "{context["current_datetime"]}"
updated: "{context["current_datetime"]}"
version: "1.0"
category: "wisdom"
status: "curated"
tags: ["wisdom", "distilled", "long-term"]
purpose: "Long-term knowledge preservation and wisdom distillation"
related_projects: []
quality: "expert"
author: "{context.get("author", "Unknown")}"
maturity_level: "mature"
impact_scope: "{context.get("impact_scope", "high")}"
---

# {context.get("title", "Wisdom Distillation")}

## 🏆 Wisdom Summary

**Maturity Level**: Mature  
**Impact Scope**: {context.get("impact_scope", "High")}  
**Distillation Date**: {context["current_date"]}  
**Source Period**: {context.get("source_period", "Last 6 months")}

## 💎 Core Wisdom

### Essential Insight
{context.get("essential_insight", "The most important insight or lesson learned")}

### Universal Principles
1. **Principle 1**: {context.get("principle1", "Fundamental principle that applies broadly")}
2. **Principle 2**: {context.get("principle2", "Secondary but important principle")}
3. **Principle 3**: {context.get("principle3", "Supporting principle")}

## 🎯 Strategic Value

### Decision Framework
{context.get("decision_framework", "How this wisdom guides future decisions")}

### Risk Mitigation
- **Major Risk**: {context.get("major_risk", "Key risk this wisdom helps avoid")}
- **Prevention Strategy**: {context.get("prevention_strategy", "How to prevent this risk")}

### Opportunity Recognition
- **Pattern**: {context.get("opportunity_pattern", "Patterns that indicate opportunities")}
- **Action**: {context.get("opportunity_action", "How to capitalize on these patterns")}

## 📈 Evolution Journey

### Origin Story
{context.get("origin_story", "How this wisdom was discovered or developed")}

### Key Milestones
- **Milestone 1**: {context.get("milestone1", "First major breakthrough or realization")}
- **Milestone 2**: {context.get("milestone2", "Refinement or validation")}
- **Milestone 3**: {context.get("milestone3", "Maturation and broad application")}

### Learning Curve
{context.get("learning_curve", "How understanding evolved over time")}

## 🔍 Evidence Base

### Successful Applications
1. **Case 1**: {context.get("case1", "Specific example where this wisdom proved valuable")}
2. **Case 2**: {context.get("case2", "Additional validation case")}
3. **Case 3**: {context.get("case3", "Third example of successful application")}

### Quantitative Evidence
- **Metric 1**: {context.get("metric1", "Measurable improvement or result")}
- **Metric 2**: {context.get("metric2", "Additional quantitative evidence")}

### Qualitative Indicators
- {context.get("qualitative1", "Subjective but important indicator")}
- {context.get("qualitative2", "Additional qualitative evidence")}

## 🚀 Implementation Wisdom

### Getting Started
{context.get("getting_started", "How to begin applying this wisdom")}

### Advanced Application
{context.get("advanced_application", "How experts can leverage this wisdom")}

### Integration Strategies
- **Strategy 1**: {context.get("integration1", "How to integrate with existing processes")}
- **Strategy 2**: {context.get("integration2", "Alternative integration approach")}

## ⚠️ Wisdom Boundaries

### Context Limitations
{context.get("context_limitations", "Where this wisdom does not apply")}

### Failure Modes
- **Mode 1**: {context.get("failure_mode1", "How this wisdom can be misapplied")}
- **Mode 2**: {context.get("failure_mode2", "Additional failure pattern")}

### Evolution Indicators
{context.get("evolution_indicators", "Signs that this wisdom needs updating")}

## 🔮 Future Implications

### Trend Alignment
{context.get("trend_alignment", "How this wisdom aligns with future trends")}

### Adaptation Strategies
{context.get("adaptation_strategies", "How to adapt this wisdom as conditions change")}

### Legacy Planning
{context.get("legacy_planning", "How to preserve and transfer this wisdom")}

## 📚 Source Materials

### Original Sources
- [[00_Catalyst_Lab/]] - Experimental origins
- [[10_Projects/]] - Practical applications
- [[20_Knowledge_Base/]] - Theoretical foundation

### Key Contributors
- {context.get("contributors", "People who contributed to this wisdom")}

---

**Wisdom Status**: Distilled | Validated | Canonical | Transcendent  
**Last Updated**: {context["current_date"]}  
**Directory**: {context.get("main_directory", "30_Wisdom_Archive")}  
**Next Review**: {context.get("next_review", "Annual")}
"""

    def _create_structure_readme_template(self, context: dict[str, Any]) -> str:
        """Create template for directory README files."""
        directory_name = context.get("directory_name", "Directory")
        tier = context.get("directory_tier", "unknown")

        # Tier-specific emojis and content
        tier_emoji = {"system": "⚙️", "core": "📂", "auxiliary": "📋"}.get(tier, "📁")

        return f"""# {tier_emoji} {directory_name}

## 📋 概要
{context.get("description", f"{directory_name} ディレクトリの説明")}

## 🎯 目的
{context.get("purpose", "このディレクトリの目的と使用方法")}

## 📊 分類情報
- **層**: {tier.title()}
- **プレフィックス**: {context.get("directory_prefix", "なし")}
- **番号**: {context.get("directory_number", "なし")}
- **自動整理**: {context.get("auto_organization", "有効")}

## 📝 使用方法
{context.get("usage_guide", f"このディレクトリは{tier}層に分類されており、{context.get('purpose', '知識管理')}に使用されます。")}

## 📁 構造
{context.get("structure_info", "```" + chr(10) + "(ディレクトリ構造をここに記述)" + chr(10) + "```")}

## 🔗 関連リンク
{context.get("related_links", "- [[関連ディレクトリ1]]" + chr(10) + "- [[関連ディレクトリ2]]")}

---
*このREADMEは自動生成されました - {context.get("main_directory", directory_name)}*  
*最終更新: {context["current_date"]}*  
*構造バージョン: {context.get("structure_version", "hybrid_v1")}*
"""

    def get_available_templates(self) -> dict[str, str]:
        """Get list of available templates with descriptions."""
        base_templates = super().get_available_templates()

        hybrid_templates = {
            "catalyst_experiment": "実験・プロトタイプ用テンプレート (Catalyst Lab)",
            "project_kickoff": "プロジェクト開始用テンプレート (Projects)",
            "knowledge_article": "知識記事用テンプレート (Knowledge Base)",
            "wisdom_distillation": "知恵の蒸留用テンプレート (Wisdom Archive)",
            "prompt_template": "プロンプトテンプレート",
            "code_snippet": "コードスニペット用テンプレート",
            "concept_explanation": "概念説明用テンプレート",
            "resource_catalog": "リソースカタログ用テンプレート",
            "structure_readme": "ディレクトリREADME用テンプレート",
        }

        return {**base_templates, **hybrid_templates}


def create_hybrid_template_manager(config: CKCConfig) -> HybridTemplateManager:
    """Create hybrid template manager from configuration."""
    return HybridTemplateManager(config.template_path, config.hybrid_structure)
