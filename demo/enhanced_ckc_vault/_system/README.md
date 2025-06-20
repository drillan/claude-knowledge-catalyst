# _system

System files (templates, configurations)

## Purpose

This directory is part of the pure tag-centered system's minimal structure. Content is organized by **state** rather than **type**.

## Content Guidelines

### What belongs here:
System files, templates, configurations, and documentation

### Tagging Strategy:
- Ensure `status: draft` is set correctly
- Use rich multi-layered tags for discoverability
- Focus on `tech`, `domain`, and `team` tags

## Obsidian Queries

### Content in this directory:
```query
path:"_system/"
```

### By content type:
```query
path:"_system/" type:prompt
path:"_system/" type:code  
path:"_system/" type:concept
```

## Workflow

Files naturally flow between directories as their status changes:
- `inbox/` → `knowledge/` (when validated)
- `knowledge/` → `archive/` (when deprecated)
- `active/` ↔ other directories (based on current relevance)

---
*Generated with Pure Tag-Centered System*
