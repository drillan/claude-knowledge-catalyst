# knowledge

Main knowledge repository (status: tested/production)

## Purpose

This directory is part of the pure tag-centered system's minimal structure. Content is organized by **state** rather than **type**.

## Content Guidelines

### What belongs here:
Validated, tested, and production-ready content

### Tagging Strategy:
- Ensure `status: tested or production` is set correctly
- Use rich multi-layered tags for discoverability
- Focus on `tech`, `domain`, and `team` tags

## Obsidian Queries

### Content in this directory:
```query
path:"knowledge/"
```

### By content type:
```query
path:"knowledge/" type:prompt
path:"knowledge/" type:code  
path:"knowledge/" type:concept
```

## Workflow

Files naturally flow between directories as their status changes:
- `inbox/` → `knowledge/` (when validated)
- `knowledge/` → `archive/` (when deprecated)
- `active/` ↔ other directories (based on current relevance)

---
*Generated with Pure Tag-Centered System*
