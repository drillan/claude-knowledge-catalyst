---
author: null
category: code
claude_feature:
- debugging
claude_model: []
complexity: intermediate
confidence: medium
created: 2025-06-20 17:21:02.385881
domain:
- data-science
- mobile
projects:
- claude-knowledge-catalyst
purpose: null
status: draft
success_rate: null
tags:
- python
- utilities
team: []
tech:
- api
- javascript
- python
- typescript
title: Python Utility Snippets
type: code
updated: 2025-06-20 17:21:02.385884
version: '1.0'
---

# Python Utility Snippets

## File Operations
```python
import json
from pathlib import Path

def read_json_file(file_path):
    """Safely read JSON file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {file_path}: {e}")
        return None
```

## Data Processing
```python
from collections import defaultdict

def group_by_key(items, key_func):
    """Group items by a key function."""
    groups = defaultdict(list)
    for item in items:
        groups[key_func(item)].append(item)
    return dict(groups)
```