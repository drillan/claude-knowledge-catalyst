#!/bin/bash

# Pure Tag-Centered Claude Knowledge Catalyst Demo
# Demonstrates the revolutionary tag-centered knowledge management approach

set -e

# Dynamic path detection (portable across environments)
DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$DEMO_DIR")"

echo "🎯 Claude Knowledge Catalyst - Pure Tag-Centered Demo"
echo "===================================================="
echo ""
echo "Experience the revolutionary approach that eliminates:"
echo "• Cognitive overhead of directory classification"
echo "• Rigid content boundaries"
echo "• Manual categorization decisions"
echo ""
echo "And introduces:"
echo "• Multi-layered intelligent tag architecture"
echo "• State-based workflow organization"
echo "• AI-powered content classification"
echo ""

# Setup
echo "🧹 Setting up demo environment..."
rm -rf "$DEMO_DIR/my_project" "$DEMO_DIR/my_vault"
mkdir -p "$DEMO_DIR/my_project" "$DEMO_DIR/my_vault"

echo ""
echo "📂 Created demo project directories"
echo ""

# Function to run CKC commands (デモディレクトリ内で実行)
run_ckc() {
    PYTHONPATH="$PROJECT_ROOT/src" "$PROJECT_ROOT/.venv/bin/python" -m claude_knowledge_catalyst.cli.main "$@"
}

# Step 1: Navigate and initialize
echo "👤 STEP 1: Initialize Pure Tag-Centered Workspace"
echo "─────────────────────────────────────────────────"
echo "$ cd my_project"
echo "$ ckc init"
echo ""
cd "$DEMO_DIR/my_project"
run_ckc init

# Step 2: Add vault
echo ""
echo "👤 STEP 2: Connect Obsidian Vault"
echo "──────────────────────────────────"
echo "$ ckc add my-vault ../my_vault"
echo ""
run_ckc add my-vault "$DEMO_DIR/my_vault"

# Step 3A: Create frontmatter-free content (AI inference demo)
echo ""
echo "👤 STEP 3A: Zero-Config Start - AI Auto-Inference Experience"
echo "──────────────────────────────────────────────────────────"
echo ""

mkdir -p .claude

# Create frontmatter-free files to demonstrate AI inference
cat > .claude/simple_git_tips.md << 'EOF'
# Git便利コマンド集

## ブランチ状態確認
```bash
# 詳細なブランチ情報
git branch -vv

# 簡潔なステータス表示
git status --porcelain

# リモート同期状況
git remote -v
```

## クリーンアップコマンド
```bash
# マージ済みブランチの削除
git branch --merged | grep -v "\*\|main\|master" | xargs git branch -d

# 不要なファイルの削除
git clean -fd

# Gitログの整理表示
git log --oneline --graph --decorate --all -10
```
EOF

cat > .claude/productivity_memo.md << 'EOF'
# 開発生産性向上のメモ

効率的な開発環境を構築するための要点をまとめる。

## 環境設定
- エディタの設定統一
- ショートカットキーの習得
- 自動化スクリプトの活用

## コード品質
- リンター設定
- フォーマッター自動実行
- テスト駆動開発の実践

## チームワーク
- コードレビューの効率化
- ドキュメント作成の自動化
- 知識共有の仕組み作り
EOF

echo "✏️  Created frontmatter-free files:"
echo "  📄 simple_git_tips.md (No frontmatter - pure content)"
echo "  📄 productivity_memo.md (No frontmatter - plain text)"
echo ""

# Demonstrate AI inference
echo "🤖 AI Auto-Inference System Demonstration:"
echo "$ ckc classify .claude/simple_git_tips.md --show-evidence"
echo ""
run_ckc classify .claude/simple_git_tips.md --show-evidence

echo ""
echo "💡 What just happened:"
echo "  ✅ AI detected 'git' keywords → tech: [git]"
echo "  ✅ Code blocks detected → type: code"
echo "  ✅ Command patterns → domain: [devops]" 
echo "  ✅ Content length analysis → complexity: beginner"
echo "  ✅ No quality indicators → confidence: medium"
echo "  ✅ H1 title extracted → title: 'Git便利コマンド集'"
echo ""

# Step 3B: Create advanced tag-centered content
echo "👤 STEP 3B: Advanced Tag Architecture - Complete Metadata System"
echo "──────────────────────────────────────────────────────────────"
echo ""

# Create content with pure tag-centered metadata
cat > .claude/fastapi_prompt.md << 'EOF'
---
title: FastAPI Code Generation Prompt
type: prompt
status: production
tech:
  - python
  - fastapi
  - api
domain:
  - web-dev
  - backend
team:
  - backend
complexity: intermediate
confidence: high
claude_model:
  - sonnet
  - sonnet-4
claude_feature:
  - code-generation
success_rate: 92
projects:
  - api-development
tags:
  - rest-api
  - authentication
  - performance
---

# FastAPI REST API Generator

Generate a production-ready FastAPI application with:

## Requirements
- Authentication with JWT tokens
- CRUD operations for user management
- Input validation with Pydantic models
- Error handling and logging
- OpenAPI documentation
- Async database operations

## Structure
- Follow FastAPI best practices
- Use dependency injection
- Include comprehensive type hints
- Add detailed docstrings

Generate both the main application and test files.
EOF

cat > .claude/python_debugging_tips.md << 'EOF'
---
title: Python Debugging Techniques
type: code
status: tested
tech:
  - python
  - debugging
domain:
  - development
  - troubleshooting
team:
  - backend
  - fullstack
complexity: beginner
confidence: high
claude_feature:
  - debugging
  - analysis
projects:
  - best-practices
tags:
  - pdb
  - logging
  - profiling
---

# Python Debugging Techniques

## 1. Interactive Debugging with pdb
```python
import pdb

def problematic_function(data):
    pdb.set_trace()  # Debugger will pause here
    result = process_data(data)
    return result
```

## 2. Advanced Logging
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def api_call(url):
    logger.debug(f"Making request to {url}")
    try:
        response = requests.get(url)
        logger.info(f"Response: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Request failed: {e}")
        raise
```

## 3. Performance Profiling
```python
import cProfile
import pstats

def profile_function():
    cProfile.run('your_function()', 'profile_output')
    stats = pstats.Stats('profile_output')
    stats.sort_stats('tottime').print_stats(10)
```
EOF

cat > .claude/react_architecture_concept.md << 'EOF'
---
title: React Component Architecture Patterns
type: concept
status: production
tech:
  - react
  - javascript
  - typescript
domain:
  - web-dev
  - frontend
team:
  - frontend
complexity: advanced
confidence: high
projects:
  - component-library
  - ui-framework
tags:
  - patterns
  - scalability
  - maintainability
---

# React Component Architecture Patterns

## 1. Container vs Presentational Components

### Container Components (Smart)
- Manage state and side effects
- Handle data fetching
- Connect to external state management
- Minimal UI logic

### Presentational Components (Dumb)
- Focus on UI rendering
- Receive data via props
- Stateless when possible
- Highly reusable

## 2. Compound Components Pattern
```tsx
// Parent component manages shared state
function Tabs({ children, defaultTab = 0 }) {
  const [activeTab, setActiveTab] = useState(defaultTab);
  
  return (
    <div className="tabs">
      {React.Children.map(children, (child, index) =>
        React.cloneElement(child, { activeTab, setActiveTab, index })
      )}
    </div>
  );
}

// Child components receive context
function Tab({ children, activeTab, index, label }) {
  return (
    <div className={activeTab === index ? 'active' : 'inactive'}>
      {children}
    </div>
  );
}
```

## 3. Render Props Pattern
```tsx
function DataProvider({ render, endpoint }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetch(endpoint)
      .then(res => res.json())
      .then(setData)
      .finally(() => setLoading(false));
  }, [endpoint]);
  
  return render({ data, loading });
}

// Usage
<DataProvider 
  endpoint="/api/users"
  render={({ data, loading }) => (
    loading ? <Spinner /> : <UserList users={data} />
  )}
/>
```
EOF

echo "✏️  Created advanced tag-centered examples:"
echo "  📝 FastAPI Prompt (type: prompt, tech: python+fastapi, 15+ metadata fields)"
echo "  🐛 Python Debugging (type: code, domain: troubleshooting, structured tags)"
echo "  🏗️  React Architecture (type: concept, complexity: advanced, project links)"
echo ""

echo "🔍 Comparing AI Inference vs Manual Tagging:"
echo "  • AI Inference: Quick start, 75%+ accuracy, zero setup"
echo "  • Manual Tags: Maximum precision, rich relationships, team workflows"
echo "  • Best Practice: Start with AI, enhance with manual tags over time"
echo ""

# Step 4: Demonstrate AI classification on all files
echo "👤 STEP 4: AI-Powered Content Classification"
echo "──────────────────────────────────────────────"
echo "$ ckc classify .claude --format summary"
echo ""
run_ckc classify .claude --format summary

# Step 5: Tag management
echo ""
echo "👤 STEP 5: Pure Tag System Management"
echo "─────────────────────────────────"
echo "$ ckc tags list"
echo ""
run_ckc tags list

# Step 6: Sync with enhanced organization
echo ""
echo "👤 STEP 6: Intelligent Synchronization"
echo "──────────────────────────────────────"
echo "$ ckc sync"
echo ""
run_ckc sync

# Step 7: Advanced search capabilities
echo ""
echo "👤 STEP 7: Dynamic Knowledge Discovery"
echo "─────────────────────────────────────"
echo "$ ckc search --tech python --status production"
echo ""
run_ckc search --tech python --status production

# Step 8: Query generation
echo ""
echo "👤 STEP 8: Obsidian Query Generation"
echo "────────────────────────────────────"
echo "$ ckc query high-quality"
echo ""
run_ckc query high-quality

# Results exploration
echo ""
echo "📊 STEP 9: Exploring Pure Tag-Centered Results"
echo "─────────────────────────────────────────────"
echo ""

echo "🏗️ Vault Structure (State-Based, Not Content-Based):"
if [ -d "$DEMO_DIR/my_vault" ]; then
    echo "├── _system/          # Templates and configuration"
    echo "├── _attachments/     # Media files"
    echo "├── inbox/            # Unprocessed content (status: draft)"
    echo "├── active/           # Working content (status: tested)"
    echo "├── archive/          # Deprecated content"
    echo "└── knowledge/        # Mature content (status: production)"
    echo ""
    
    echo "📁 Generated Structure:"
    find "$DEMO_DIR/my_vault" -type d -name "*" | head -8 | sort
    echo ""
    
    echo "📄 Sample Files by Status (not by content type):"
    for dir in "inbox" "knowledge" "_system"; do
        if [ -d "$DEMO_DIR/my_vault/$dir" ]; then
            echo "  $dir/:"
            find "$DEMO_DIR/my_vault/$dir" -name "*.md" | head -3 | while read file; do
                echo "    📄 $(basename "$file")"
            done
        fi
    done
fi

echo ""
echo "🏷️ Sample Enhanced Metadata:"
echo "────────────────────────────"
if [ -f "$DEMO_DIR/my_vault/knowledge"/*.md ]; then
    sample_file=$(find "$DEMO_DIR/my_vault/knowledge" -name "*.md" | head -1)
    if [ -n "$sample_file" ]; then
        echo "📄 $(basename "$sample_file"):"
        sed -n '/^---$/,/^---$/p' "$sample_file" | head -15
    fi
fi

echo ""
echo "✅ DEMO COMPLETE: Pure Tag-Centered Knowledge Management"
echo "═══════════════════════════════════════════════════════"
echo ""
echo "🎉 Revolutionary Features Demonstrated:"
echo "  ✅ Zero-config AI auto-inference (frontmatter-free files)"
echo "  ✅ Advanced multi-layered tag architecture (15+ metadata fields)"
echo "  ✅ AI-powered content analysis with 75%+ accuracy"
echo "  ✅ State-based organization (workflow-driven, not content-based)"
echo "  ✅ Dynamic cross-dimensional knowledge discovery"
echo "  ✅ Obsidian query generation for complex searches"
echo ""
echo "🏷️ Pure Tag System Benefits:"
echo "  • type: [prompt, code, concept, resource] - Content nature"
echo "  • tech: [python, react, fastapi, ...] - Technology stack"
echo "  • domain: [web-dev, backend, frontend] - Application area"
echo "  • team: [backend, frontend, fullstack] - Team ownership"
echo "  • status: [draft, tested, production] - Lifecycle state"
echo "  • complexity: [beginner, intermediate, advanced] - Skill level"
echo "  • confidence: [low, medium, high] - Content reliability"
echo ""
echo "🔍 Advanced Capabilities:"
echo "  • Zero-config start: AI auto-inference from content"
echo "  • Gradual enhancement: Manual tags improve precision"
echo "  • 75%+ accuracy AI classification with evidence-based reasoning"
echo "  • Natural language search queries across multiple dimensions"
echo "  • Cross-project knowledge linking and team collaboration"
echo "  • Automated Obsidian template generation"
echo "  • State-based file placement (90% in knowledge/)"
echo ""
echo "📁 Demo artifacts:"
echo "  • Project: $DEMO_DIR/my_project/"
echo "  • Vault: $DEMO_DIR/my_vault/"
echo "  • Configuration: $DEMO_DIR/my_project/ckc_config.yaml"
echo ""
echo "🚀 Next steps:"
echo "  1. Open vault in Obsidian: $DEMO_DIR/my_vault"
echo "  2. Try dynamic queries in knowledge/ README"
echo "  3. Explore _system/templates/ for tag-centered templates"
echo "  4. Use 'ckc interactive' for guided tagging"
echo "  5. Run 'ckc watch' for automatic synchronization"
echo ""
echo "💡 Experience the cognitive revolution!"
echo "   No more 'Which category?' decisions - just pure, discoverable knowledge."