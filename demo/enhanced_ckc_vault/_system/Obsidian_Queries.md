# Obsidian Queries for Pure Tag-Centered System

This document contains pre-built queries for organizing and discovering content in the tag-centered system.

## Content Discovery

### By Type
```query
type:prompt
```
```query  
type:code
```
```query
type:concept
```
```query
type:resource
```

### By Status  
```query
status:draft
```
```query
status:production
```
```query
status:deprecated
```

### By Technology
```query
tech:python
```
```query
tech:javascript
```
```query
tech:react
```

### By Domain
```query
domain:web-dev
```
```query
domain:data-science
```
```query
domain:devops
```

## Quality Filters

### High-Quality Content
```query
confidence:high status:production
```

### Expert-Level Content
```query
complexity:advanced OR complexity:expert
```

### Successful Prompts
```query
type:prompt success_rate:>80
```

## Team Views

### Frontend Resources
```query
team:frontend
```

### Backend Code
```query
team:backend type:code
```

### ML Research
```query
team:ml domain:machine-learning
```

## Project Views

### Active Projects
```query
status:production projects:*
```

### Project-Specific Content
```query
projects:"ProjectName"
```

## Advanced Combinations

### Production Python Code for Web Development
```query
type:code tech:python domain:web-dev status:production
```

### High-Confidence Debugging Prompts
```query
type:prompt claude_feature:debugging confidence:high
```

### Beginner-Friendly Frontend Resources
```query
team:frontend complexity:beginner type:resource
```

## Dynamic Views

### Recently Updated
```query
updated:>2024-01-01
```

### Needs Review (Draft Status)
```query
status:draft created:<-30d
```

### Deprecated Content (Cleanup Candidates)
```query
status:deprecated updated:<-180d
```

---
*Pure Tag-Centered System Query Reference*
