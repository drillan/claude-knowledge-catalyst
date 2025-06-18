#!/bin/bash

# Multi-Project Demo for Claude Knowledge Catalyst
# Demonstrates how multiple projects can share a single Obsidian vault
set -e

# Dynamic path detection (portable across environments)
DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$DEMO_DIR")"

echo "🎯 Claude Knowledge Catalyst - Multi-Project Demo"
echo "================================================="
echo ""
echo "This demo shows how multiple development projects can share"
echo "a single knowledge vault with automatic organization."
echo ""

echo "🧹 Cleaning up previous demo runs..."
rm -rf "$DEMO_DIR/frontend_team" "$DEMO_DIR/backend_team" "$DEMO_DIR/shared_vault"
mkdir -p "$DEMO_DIR/frontend_team" "$DEMO_DIR/backend_team" "$DEMO_DIR/shared_vault"

echo ""
echo "📁 Created demo environment:"
echo "  - Frontend Team: React, UI/UX, design systems"
echo "  - Backend Team: Python, AI/ML, data processing" 
echo "  - Shared Vault: Common knowledge repository"
echo ""

# Function to run CKC commands (デモディレクトリ内で実行)
run_ckc() {
    # PYTHONPATH設定でCKCを利用可能にし、現在のディレクトリで実行
    PYTHONPATH="$PROJECT_ROOT/src" "$PROJECT_ROOT/.venv/bin/python" -m claude_knowledge_catalyst.cli.main "$@"
}

# Frontend Team setup
echo "👥 FRONTEND TEAM: React & UI Development"
echo "$ cd frontend_team && ckc init"
cd "$DEMO_DIR/frontend_team"
run_ckc init

echo ""
echo "$ ckc add shared-vault ../shared_vault"
run_ckc add shared-vault "$DEMO_DIR/shared_vault"

echo ""
echo "💼 Creating Frontend Team knowledge content..."
mkdir -p .claude

# Create project configuration for explicit identification
cat > .claude/project.yaml << 'EOF'
project_name: "Frontend-Team"
description: "Frontend development team - React, UI/UX, design systems"
team_type: "frontend"
tech_stack: ["react", "typescript", "css", "figma"]
EOF

cat > .claude/react_best_practices.md << 'EOF'
---
title: "React Component Best Practices"
project: "Frontend-Team"
tags: ["code", "react", "frontend"]
category: "code"
status: "production"
author: "Frontend Team Lead"
---

# React Component Best Practices

## Component Structure
```jsx
// ✅ Good: Functional component with hooks
const UserProfile = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchUser(userId).then(setUser).finally(() => setLoading(false));
  }, [userId]);
  
  if (loading) return <Spinner />;
  if (!user) return <ErrorMessage />;
  
  return <div className="user-profile">{user.name}</div>;
};
```

## Performance Tips
- Use React.memo for expensive components
- Optimize re-renders with useMemo and useCallback
- Split large components into smaller ones
EOF

cat > .claude/ui_design_review.md << 'EOF'
---
title: "UI Design Review Prompt"
project: "Frontend-Team"
tags: ["prompt", "design", "review", "accessibility"]
category: "prompt"
status: "tested"
success_rate: 90
author: "UX Team Lead"
purpose: "Standardize UI design review process for accessibility and consistency"
---

# UI Design Review Prompt

Please review this UI design for:

1. **Accessibility compliance** (WCAG 2.1 AA)
2. **Mobile responsiveness**
3. **User experience flow**
4. **Visual hierarchy and readability**
5. **Brand consistency**

Provide specific recommendations with examples.
EOF

echo ""
echo "👥 BACKEND TEAM: Python & AI/ML Research"
echo "$ cd backend_team && ckc init"
cd "$DEMO_DIR/backend_team"
run_ckc init

echo ""
echo "$ ckc add shared-vault ../shared_vault"
run_ckc add shared-vault "$DEMO_DIR/shared_vault"

echo ""
echo "🔬 Creating Backend/ML Team knowledge content..."
mkdir -p .claude

# Create project configuration for Backend team
cat > .claude/project.yaml << 'EOF'
project_name: "Backend-Team"
description: "Backend development & ML research team - Python, AI/ML, data processing"
team_type: "backend"
tech_stack: ["python", "pytorch", "fastapi", "postgresql", "docker"]
research_areas: ["llm", "nlp", "machine_learning", "architecture"]
EOF

cat > .claude/llm_architecture_notes.md << 'EOF'
---
title: "LLM Architecture Analysis"
project: "Backend-Team"
tags: ["concept", "ai", "architecture", "research"]
category: "concept"
status: "validated"
author: "ML Research Team"
purpose: "Document latest trends in LLM architecture for team knowledge sharing"
related_projects: ["AI-Infrastructure", "NLP-Pipeline"]
---

# LLM Architecture Analysis

## Current Trends in 2024

### Mixture of Experts (MoE)
- Sparse activation patterns improve efficiency
- Conditional computation based on input type
- Reduced inference costs for large models

### Context Length Extensions
- Techniques like RoPE (Rotary Position Embedding)
- Memory-efficient attention mechanisms
- Long-context applications (100K+ tokens)

### Multi-modal Integration
- Vision-language models (GPT-4V, Claude-3)
- Audio processing capabilities
- Unified embedding spaces
EOF

cat > .claude/async_python_patterns.md << 'EOF'
---
title: "Async Python Patterns"
project: "Backend-Team"
tags: ["code", "python", "async", "performance"]
category: "code"
status: "production"
author: "Backend Architecture Team"
purpose: "Best practices for async Python development in high-performance applications"
model: "claude-sonnet"
success_rate: 95
---

# Async Python Patterns

## Database Operations
```python
import asyncio
import aiopg

async def fetch_user_data(user_ids):
    """Fetch multiple users concurrently."""
    async with aiopg.create_pool(DATABASE_URL) as pool:
        tasks = [
            fetch_single_user(pool, user_id) 
            for user_id in user_ids
        ]
        return await asyncio.gather(*tasks)

async def fetch_single_user(pool, user_id):
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
            return await cur.fetchone()
```

## Error Handling
```python
async def robust_api_call(session, url, retries=3):
    """API call with exponential backoff."""
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.json()
        except asyncio.TimeoutError:
            if attempt == retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)
```
EOF

echo ""
echo "🔄 SYNCHRONIZATION PHASE"
echo "========================"
echo ""
echo "🎯 Demonstrating project identification methods:"
echo "  1. Explicit CLI parameter (--project) ← 使用"
echo "  2. Project metadata in frontmatter"  
echo "  3. Auto-detection from .claude/project.yaml ← バックアップ"

echo ""
echo "📤 Frontend Team: Explicit project identification"
echo "$ ckc sync --project Frontend-Team"
cd "$DEMO_DIR/frontend_team"
run_ckc sync --project Frontend-Team

echo ""
echo "📤 Backend Team: Explicit project identification" 
echo "$ ckc sync --project Backend-Team"
cd "$DEMO_DIR/backend_team"
run_ckc sync --project Backend-Team

echo ""
echo "📊 RESULTS SUMMARY"
echo "=================="
echo ""
echo "✅ Multi-project knowledge sharing demonstrated!"
echo ""
echo "🧪 PROJECT MANAGEMENT FEATURES DEMO"
echo "===================================="

echo ""
echo "📋 Listing all discovered projects:"
echo "$ ckc project list"
run_ckc project list

echo ""
echo "👀 Frontend team files:"
echo "$ ckc project files Frontend-Team"
run_ckc project files Frontend-Team

echo ""
echo "📊 Backend team statistics:"
echo "$ ckc project stats Backend-Team"
run_ckc project stats Backend-Team

echo ""
echo "📁 Shared vault project structure:"
find "$DEMO_DIR/shared_vault/10_Projects" -name "*.md" 2>/dev/null | sort | head -10 || echo "  (Files will appear after sync)"

echo ""
echo "🎯 Advanced features demonstrated:"
echo "  ✅ Multi-team development workflow"
echo "  ✅ Automatic project detection from .claude/project.yaml"
echo "  ✅ Team-specific file organization in 10_Projects/"
echo "  ✅ Cross-team knowledge sharing in 20_Knowledge_Base/"
echo "  ✅ Rich metadata (author, purpose, related_projects)"
echo "  ✅ Team statistics and file management"
echo ""
echo "📂 Team directories:"
echo "  - Frontend Team: $DEMO_DIR/frontend_team"
echo "  - Backend Team:  $DEMO_DIR/backend_team"
echo "  - Shared Vault:  $DEMO_DIR/shared_vault"
echo ""
echo "🔍 Next steps for teams:"
echo "  - Open shared vault in Obsidian: $DEMO_DIR/shared_vault"
echo "  - View team-specific content in 10_Projects/ and shared knowledge in 20_Knowledge_Base/"
echo "  - Use 'ckc project list' to see all teams"
echo "  - Use 'ckc project stats <team>' for team insights"
echo "  - Continue adding knowledge with team metadata"
echo "  - Set up 'ckc watch' for automatic synchronization"
echo ""
echo "💡 Project identification methods:"
echo "  1. Explicit: ckc sync --project \"TeamName\""
echo "  2. Configuration: .claude/project.yaml"
echo "  3. Metadata: project field in frontmatter"
echo "  4. Auto-detection: Git repo name or project structure"