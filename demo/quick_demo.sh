#!/bin/bash

# Quick Demo for Claude Knowledge Catalyst
# Fast demonstration of core CKC features for developers
set -e

# Dynamic path detection (portable across environments)
DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$DEMO_DIR")"

echo "⚡ Claude Knowledge Catalyst - Quick Demo"
echo "========================================"
echo ""
echo "Fast demo of core features for developers and testing."
echo ""

# Cleanup and setup
echo "🧹 Setting up demo environment..."
rm -rf "$DEMO_DIR/quick_test" "$DEMO_DIR/test_vault"
mkdir -p "$DEMO_DIR/quick_test" "$DEMO_DIR/test_vault"

cd "$DEMO_DIR/quick_test"

# Function to run CKC commands (デモディレクトリ内で実行)
run_ckc() {
    # PYTHONPATH設定でCKCを利用可能にし、現在のディレクトリで実行
    PYTHONPATH="$PROJECT_ROOT/src" "$PROJECT_ROOT/.venv/bin/python" -m claude_knowledge_catalyst.cli.main "$@"
}

echo "📝 Initializing CKC project..."
run_ckc init

echo "🔗 Adding vault sync target..."
run_ckc add test-vault "$DEMO_DIR/test_vault"

echo "📄 Creating sample content (diverse categories for classification demo)..."
mkdir -p .claude

# Sample prompt (Best Practices category)
cat > .claude/sample_prompt.md << 'EOF'
---
title: "Documentation Writer Prompt"
tags: ["prompt", "documentation"]
category: "prompt"
status: "production"
success_rate: 95
author: "Development Team"
purpose: "Generate comprehensive technical documentation"
---

# Documentation Writer Prompt

Create comprehensive technical documentation for the given code or feature. Include:

1. **Overview** - What it does and why it's useful
2. **Usage** - How to use it with examples
3. **API Reference** - Parameters, return values, exceptions
4. **Best Practices** - Common patterns and gotchas

Write in clear, professional language suitable for developers.
EOF

# Sample code snippet (Python category)
cat > .claude/utility_code.md << 'EOF'
---
title: "String Processing Utilities"
tags: ["code", "python", "utilities"]
category: "code"
status: "production"
author: "Backend Team"
purpose: "Reusable text processing functions"
---

# String Processing Utilities

## Text Cleaning
```python
import re
from typing import Optional

def clean_text(text: str) -> str:
    """Remove extra whitespace and normalize text."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    # Remove special characters
    text = re.sub(r'[^\w\s-]', '', text)
    return text.lower()

def extract_keywords(text: str, max_words: int = 10) -> list[str]:
    """Extract key words from text."""
    cleaned = clean_text(text)
    words = cleaned.split()
    return words[:max_words]
```
EOF

# Sample concept note (Development Practices category)
cat > .claude/knowledge_management_concept.md << 'EOF'
---
title: "Modern Knowledge Management Principles"
tags: ["concept", "knowledge_management", "development", "practices"]
category: "concept"
status: "validated"
author: "Architecture Team"
purpose: "Document knowledge management best practices"
---

# Modern Knowledge Management Principles

## Core Philosophy
Effective knowledge management balances structure with flexibility, enabling teams to capture and share insights efficiently.

## Key Components
1. **10-step numbering system** (00, 10, 20, 30) for scalable organization
2. **Category-first classification** for intuitive discovery
3. **Metadata-driven automation** for reduced manual overhead
4. **Shared knowledge prioritization** over project silos

## Implementation Benefits
- **Scalability**: Grows with team size and knowledge base
- **Consistency**: Maintains organization across projects
- **Discoverability**: Easy to find relevant information
- **Automation**: Reduces manual categorization effort
EOF

echo "🔄 Running sync..."
run_ckc sync

echo "📊 Showing results..."
echo ""
echo "Generated vault structure:"
find "$DEMO_DIR/test_vault" -name "*.md" | head -10 | sort

echo ""
echo "📁 Vault directory structure:"
tree "$DEMO_DIR/test_vault" -I 'README.md' | head -15 || find "$DEMO_DIR/test_vault" -type d | sort

echo ""
echo "📈 Status check:"
run_ckc status

echo ""
echo "✅ Quick demo complete!"
echo ""
echo "🎯 What was demonstrated:"
echo "  ✅ 10-step numbering system (00, 10, 20, 30)"
echo "  ✅ Category-first classification"
echo "  ✅ Shared knowledge organization"
echo "  ✅ Automated file placement"
echo ""
echo "📂 Demo files location:"
echo "  - Source: $DEMO_DIR/quick_test"
echo "  - Vault: $DEMO_DIR/test_vault"
echo ""
echo "🔍 Explore the organized vault at: $DEMO_DIR/test_vault"