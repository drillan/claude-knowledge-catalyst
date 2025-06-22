# Pure Tag-Centered Knowledge Vault

Welcome to your revolutionary tag-centered knowledge management system! This vault eliminates complex directory hierarchies and relies on intelligent tagging for organization.

## Directory Structure (Minimal & State-Based)

```
📁 _system/          # System files (templates, scripts, configurations)
📁 _attachments/     # Binary files and attachments  
📁 inbox/            # Draft content and unprocessed files
📁 active/           # Currently relevant content
📁 archive/          # Deprecated or outdated content
📁 knowledge/        # Main knowledge repository (90% of content)
```

## Core Philosophy

### 🏷️ Tag-Centered Organization
- **No complex directory hierarchies** - content is organized by state, not type
- **Multi-layered tagging** - rich metadata through standardized tags
- **Dynamic views** - use Obsidian queries to create custom organization
- **Cognitive load reduction** - eliminate classification decisions

### 📊 State-Based Classification
- `draft` → `inbox/` - Work in progress, ideas, unprocessed content
- `tested`/`production` → `knowledge/` - Validated, reliable content
- `deprecated` → `archive/` - Outdated but historically valuable
- Active work → `active/` - Currently relevant projects and tasks

## Tag System

### Required Tags
- **type**: `prompt`, `code`, `concept`, `resource`
- **status**: `draft`, `tested`, `production`, `deprecated`

### Multi-Layered Categories
- **tech**: Technology stack (`python`, `react`, `docker`, etc.)
- **domain**: Knowledge domain (`web-dev`, `data-science`, `devops`, etc.)
- **team**: Team responsibility (`frontend`, `backend`, `ml`, etc.)
- **projects**: Associated projects (array)

### Quality Indicators
- **complexity**: `beginner`, `intermediate`, `advanced`, `expert`
- **confidence**: `low`, `medium`, `high`
- **success_rate**: 0-100 (for prompts and processes)

### Claude-Specific
- **claude_model**: `opus`, `sonnet`, `haiku`
- **claude_feature**: `code-generation`, `analysis`, `debugging`, etc.

## Quick Start

1. **Create content** in any directory (usually `inbox/` for drafts)
2. **Add tags** using the standardized system
3. **Use Obsidian queries** to organize and find content
4. **Let the system** automatically place files based on status

## Obsidian Queries

### All Production Code
```query
type:code status:production
```

### Python Web Development
```query
tech:python domain:web-dev
```

### High-Confidence Prompts
```query
type:prompt confidence:high success_rate:>80
```

## Templates

Use the templates in `_system/templates/` for consistent formatting:
- **Prompt Template**: For Claude prompts and interactions
- **Code Template**: For code snippets and scripts
- **Concept Template**: For knowledge documentation
- **Resource Template**: For curated resource lists

## Evolution

This system evolves with your needs:
- Add new tags organically
- Create custom queries for new workflows  
- Let content naturally flow between states
- Focus on creation, not organization

---
*Pure Tag-Centered System - Revolutionizing Knowledge Management*
