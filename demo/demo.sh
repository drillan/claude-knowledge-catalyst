#!/bin/bash

# User-Friendly Claude Knowledge Catalyst Demo
# Shows the exact commands users would type in real scenarios

set -e

# Dynamic path detection (portable across environments)
DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$DEMO_DIR")"

echo "🎯 Claude Knowledge Catalyst - User Demo"
echo "========================================"
echo ""
echo "This demo shows the ACTUAL workflow users experience."
echo ""

# Setup
echo "🧹 Setting up demo project..."
rm -rf "$DEMO_DIR/my_project" "$DEMO_DIR/my_obsidian_vault"
mkdir -p "$DEMO_DIR/my_project" "$DEMO_DIR/my_obsidian_vault"

echo ""
echo "📂 Created demo project directory: my_project/"
echo "📂 Created vault directory: my_obsidian_vault/"
echo ""

# Step 1: User navigates to their project
echo "👤 USER ACTION: Navigate to project directory"
echo "$ cd my_project"
echo ""
cd "$DEMO_DIR/my_project"

# Function to run CKC commands (デモディレクトリ内で実行)
run_ckc() {
    # PYTHONPATH設定でCKCを利用可能にし、現在のディレクトリで実行
    PYTHONPATH="$PROJECT_ROOT/src" "$PROJECT_ROOT/.venv/bin/python" -m claude_knowledge_catalyst.cli.main "$@"
}

# Step 2: Initialize CKC  
echo "👤 USER ACTION: Initialize CKC with modern hybrid structure"
echo "$ ckc init"
echo ""
run_ckc init

# Step 3: Add vault
echo ""
echo "👤 USER ACTION: Add Obsidian vault as sync target"
echo "$ ckc add my-vault ../my_obsidian_vault"
echo ""
run_ckc add my-vault "$DEMO_DIR/my_obsidian_vault"

# Step 4: Create content
echo ""
echo "👤 USER ACTION: Create knowledge content"
echo "$ mkdir -p .claude"
echo "$ vim .claude/my_notes.md  # (creating files...)"
echo ""

mkdir -p .claude

# Simulate user-created content
cat > .claude/daily_standup_prompt.md << 'EOF'
---
title: "Daily Standup Prompt"
tags: ["prompt", "meetings"]
category: "prompt"
status: "production"
success_rate: 95
---

# Daily Standup Meeting Prompt

Please help me run an effective daily standup. Ask each team member:

1. What did you accomplish yesterday?
2. What will you work on today?
3. Are there any blockers or impediments?

Keep responses focused and under 2 minutes per person.
EOF

cat > .claude/git_utils.md << 'EOF'
---
title: "Git Utility Commands"
tags: ["code", "git", "utilities"]
category: "code"
status: "tested"
---

# Git Utility Commands

## Quick Status
```bash
# Show compact status
git status --porcelain

# Show branch info
git branch -vv
```

## Cleanup
```bash
# Remove merged branches
git branch --merged | grep -v "\*\|main\|master" | xargs git branch -d
```
EOF

cat > .claude/api_design_principles.md << 'EOF'
---
title: "API Design Principles"
tags: ["concept", "api", "design"]
category: "concept"
status: "validated"
---

# API Design Principles

## Core Principles

### 1. Consistency
- Use consistent naming conventions
- Maintain uniform response formats
- Apply standard HTTP status codes

### 2. Simplicity
- Keep endpoints intuitive
- Minimize required parameters
- Provide sensible defaults

### 3. Documentation
- Include comprehensive examples
- Document error responses
- Maintain up-to-date specs
EOF

echo "✏️  Created example content:"
echo "  - .claude/daily_standup_prompt.md (prompt category)"
echo "  - .claude/git_utils.md (code category)"
echo "  - .claude/api_design_principles.md (concept category)"
echo ""

# Step 5: Sync
echo "👤 USER ACTION: Sync content to vault"
echo "$ ckc sync"
echo ""
run_ckc sync

# Step 6: Check status
echo ""
echo "👤 USER ACTION: Check sync status"
echo "$ ckc status"
echo ""
run_ckc status

# Results
echo ""
echo "📊 RESULTS:"
echo "=========="
echo ""
echo "✅ Modern vault structure created with 10-step numbering:"
echo "📁 00_Catalyst_Lab/ - Experiments and prototypes"
echo "📁 10_Projects/ - Active project management"
echo "📁 20_Knowledge_Base/ - Structured knowledge (where files go)"
echo "📁 30_Wisdom_Archive/ - Long-term knowledge storage"
echo ""
echo "📝 Synced files organized by category:"
find "$DEMO_DIR/my_obsidian_vault/20_Knowledge_Base" -name "*.md" -not -name "README.md" | head -5 | sort

echo ""
echo "✅ Demo Complete!"
echo ""
echo "🎉 What just happened:"
echo "  1. ✅ Initialized CKC in project directory"  
echo "  2. ✅ Connected to Obsidian vault"
echo "  3. ✅ Created knowledge content"
echo "  4. ✅ Automatically synced and organized content"
echo ""
echo "🔍 Next steps for users:"
echo "  - Open vault in Obsidian: $DEMO_DIR/my_obsidian_vault"
echo "  - Continue adding content to .claude/ directory"
echo "  - Run 'ckc sync' to sync new content"
echo "  - Use 'ckc watch' for automatic syncing"
echo ""
echo "📁 Demo files location:"
echo "  - Project: $DEMO_DIR/my_project"
echo "  - Vault: $DEMO_DIR/my_obsidian_vault"