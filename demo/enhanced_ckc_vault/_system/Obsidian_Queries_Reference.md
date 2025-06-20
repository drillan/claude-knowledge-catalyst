# Obsidian Queries for Pure Tag-Centered System

This document contains optimized queries for the revolutionary tag-centered knowledge management system.

## How to Use

1. **Search Box**: Copy any query below into Obsidian's search box
2. **Query Block**: Use in code blocks with 'query' language
3. **Dataview**: Some queries include Dataview syntax for advanced tables

## Query Categories

### Content Discovery

#### All Prompts
```query
type:prompt
```

#### All Code
```query
type:code
```

#### All Concepts
```query
type:concept
```

#### All Resources
```query
type:resource
```

### Quality Filters

#### High-Quality Content
```query
status:production confidence:high
```

#### Successful Prompts
```query
type:prompt success_rate:>=80
```

#### Expert-Level Content
```query
complexity:expert status:production
```

#### Beginner-Friendly
```query
complexity:beginner confidence:high -status:deprecated
```

### Technology Focus

#### Python Resources
```query
tech:python sort:updated:desc
```

#### JavaScript Content
```query
tech:javascript
```

#### React Development
```query
tech:react domain:web-dev
```

#### Docker & DevOps
```query
tech:docker tech:kubernetes
```

### Team Views

#### Frontend Team
```query
domain:web-dev team:frontend -status:deprecated
```

#### Backend Resources
```query
team:backend -status:deprecated
```

#### ML Research
```query
team:ml team:research domain:machine-learning
```

#### DevOps Tools
```query
team:devops (type:code OR type:resource)
```

### Status & Workflow

#### Production Ready
```query
status:production
```

#### Needs Review
```query
status:draft
```

#### Recent Updates
```query
updated:>2024-01-01 sort:updated:desc limit:20
```

#### Cleanup Candidates
```query
status:draft updated:>2023-01-01 sort:updated:asc
```

### Claude-Specific

#### Code Generation
```query
claude_feature:code-generation -status:deprecated sort:success_rate:desc
```

#### Analysis & Review
```query
claude_feature:analysis claude_feature:code-review
```

#### Debugging Help
```query
claude_feature:debugging confidence:high
```

#### Sonnet Optimized
```query
claude_model:sonnet
```

## Advanced Examples

### Multi-Technology Web Development
```query
tech:react tech:typescript tech:nodejs domain:web-dev status:production
```

### High-Impact Research Content
```query
type:concept (complexity:advanced OR complexity:expert) confidence:high domain:machine-learning domain:research
```

### Recently Active Projects
```query
updated:>2024-06-01 -status:deprecated sort:updated:desc limit:10
```

## Dataview Queries

### Technology Distribution Table
```dataview
TABLE file.name as Name, type, status, tech, domain, projects
WHERE status = "production" AND confidence = "high"
```

### Team Productivity Dashboard
```dataview
TABLE file.name as Name, type, status, tech, domain, projects
WHERE status != "deprecated"
SORT updated desc
```

## Custom Query Builder

Use the `ObsidianQueryBuilder` class to create custom queries:

```python
from claude_knowledge_catalyst.obsidian.query_builder import ObsidianQueryBuilder

# Build custom query
query = (ObsidianQueryBuilder()
         .type('prompt')
         .tech(['python', 'fastapi'])
         .confidence('high')
         .success_rate(85)
         .sort_by('updated', False)
         .build())
```

---
*Generated with Pure Tag-Centered Query System*