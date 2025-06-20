---
title: Python Utility Snippets
category: code
tags: ["python", "utilities"]
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
