#!/bin/bash

# Multi-Project Pure Tag-Centered Demo for Claude Knowledge Catalyst
# Demonstrates team-based knowledge sharing with pure tag architecture

set -e

# Dynamic path detection (portable across environments)
DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$DEMO_DIR")"

echo "🎯 Claude Knowledge Catalyst - Multi-Project Tag-Centered Demo"
echo "============================================================="
echo ""
echo "Experience how multiple teams collaborate using:"
echo "• Pure tag-based knowledge organization"
echo "• Team-specific metadata and workflows"
echo "• Cross-team knowledge discovery"
echo "• State-based content lifecycle management"
echo ""

echo "🧹 Setting up multi-team demo environment..."
rm -rf "$DEMO_DIR/frontend_team" "$DEMO_DIR/backend_team" "$DEMO_DIR/shared_vault"
mkdir -p "$DEMO_DIR/frontend_team" "$DEMO_DIR/backend_team" "$DEMO_DIR/shared_vault"

echo ""
echo "📁 Created team environments:"
echo "  🎨 Frontend Team: React, TypeScript, UI/UX"
echo "  🔧 Backend Team: Python, AI/ML, APIs"
echo "  🏛️ Shared Vault: Cross-team knowledge repository"
echo ""

# Function to run CKC commands (デモディレクトリ内で実行)
run_ckc() {
    PYTHONPATH="$PROJECT_ROOT/src" "$PROJECT_ROOT/.venv/bin/python" -m claude_knowledge_catalyst.cli.main "$@"
}

# Frontend Team Setup
echo "👥 FRONTEND TEAM: Pure Tag-Centered Setup"
echo "─────────────────────────────────────────"
echo "$ cd frontend_team && ckc init"
cd "$DEMO_DIR/frontend_team"
run_ckc init

echo ""
echo "$ ckc add shared-vault ../shared_vault"
run_ckc add shared-vault "$DEMO_DIR/shared_vault"

echo ""
echo "💼 Creating Frontend Team tag-centered knowledge..."
mkdir -p .claude

# Frontend team content with pure tag architecture
cat > .claude/react_performance.md << 'EOF'
---
title: React Performance Optimization Patterns
type: code
status: production
tech:
  - react
  - typescript
  - javascript
domain:
  - web-dev
  - frontend
  - performance
team:
  - frontend
  - ui-ux
complexity: advanced
confidence: high
claude_model:
  - sonnet
  - sonnet-4
claude_feature:
  - code-generation
  - optimization
projects:
  - ui-framework
  - performance-toolkit
tags:
  - optimization
  - hooks
  - memoization
  - virtual-dom
---

# React Performance Optimization Patterns

## 1. Memoization Strategies

### React.memo for Component Memoization
```tsx
const ExpensiveComponent = React.memo(({ data, config }) => {
  const processedData = useMemo(() =>
    heavyProcessing(data), [data]);

  return <div>{processedData.map(item =>
    <Item key={item.id} {...item} />)}</div>;
});

// Custom comparison for complex props
const CustomMemoComponent = React.memo(
  ({ user, preferences }) => <UserProfile user={user} prefs={preferences} />,
  (prevProps, nextProps) =>
    prevProps.user.id === nextProps.user.id &&
    JSON.stringify(prevProps.preferences) === JSON.stringify(nextProps.preferences)
);
```

### useCallback and useMemo Optimization
```tsx
function ParentComponent({ items, onItemClick }) {
  // ✅ Memoize expensive calculations
  const expensiveValue = useMemo(() =>
    items.reduce((acc, item) => acc + item.value, 0), [items]);

  // ✅ Memoize event handlers to prevent child re-renders
  const handleItemClick = useCallback((itemId) => {
    onItemClick(itemId);
    analytics.track('item_clicked', { itemId });
  }, [onItemClick]);

  return (
    <div>
      <Summary total={expensiveValue} />
      {items.map(item =>
        <Item
          key={item.id}
          item={item}
          onClick={handleItemClick}
        />
      )}
    </div>
  );
}
```

## 2. Code Splitting and Lazy Loading
```tsx
// Route-based code splitting
const Dashboard = lazy(() => import('./Dashboard'));
const UserProfile = lazy(() => import('./UserProfile'));

function App() {
  return (
    <Router>
      <Suspense fallback={<LoadingSpinner />}>
        <Routes>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/profile" element={<UserProfile />} />
        </Routes>
      </Suspense>
    </Router>
  );
}

// Component-based lazy loading
const HeavyChart = lazy(() =>
  import('./HeavyChart').then(module => ({ default: module.HeavyChart }))
);
```
EOF

cat > .claude/design_system_prompt.md << 'EOF'
---
title: Design System Component Generator
type: prompt
status: production
tech:
  - react
  - typescript
  - css
  - storybook
domain:
  - web-dev
  - frontend
  - design-systems
team:
  - frontend
  - ui-ux
  - design
complexity: intermediate
confidence: high
claude_model:
  - sonnet
  - sonnet-4
claude_feature:
  - code-generation
  - design
success_rate: 88
projects:
  - design-system
  - component-library
tags:
  - components
  - accessibility
  - tokens
  - storybook
---

# Design System Component Generator

Generate a production-ready React component for our design system with:

## Requirements
- TypeScript with strict typing
- Accessibility compliance (WCAG 2.1 AA)
- Design token integration
- Responsive behavior
- Storybook stories
- Jest unit tests

## Component Structure
```
ComponentName/
├── index.ts                 # Public exports
├── ComponentName.tsx        # Main component
├── ComponentName.module.css # Styles
├── ComponentName.stories.tsx # Storybook stories
├── ComponentName.test.tsx   # Unit tests
└── types.ts                # Type definitions
```

## Implementation Guidelines
- Use CSS modules for styling
- Implement proper focus management
- Support both controlled and uncontrolled modes
- Include comprehensive prop documentation
- Follow our naming conventions
- Add proper error boundaries where needed

## Testing Requirements
- Unit tests for all interactive behaviors
- Accessibility tests with jest-axe
- Visual regression tests in Storybook
- Cross-browser compatibility tests

Generate the complete component implementation.
EOF

# Backend Team Setup
echo ""
echo "👥 BACKEND TEAM: Pure Tag-Centered Setup"
echo "────────────────────────────────────────"
echo "$ cd backend_team && ckc init"
cd "$DEMO_DIR/backend_team"
run_ckc init

echo ""
echo "$ ckc add shared-vault ../shared_vault"
run_ckc add shared-vault "$DEMO_DIR/shared_vault"

echo ""
echo "🔬 Creating Backend/ML Team tag-centered knowledge..."
mkdir -p .claude

cat > .claude/async_api_patterns.md << 'EOF'
---
title: Async Python API Architecture
type: code
status: production
tech:
  - python
  - fastapi
  - asyncio
  - postgresql
domain:
  - web-dev
  - backend
  - api-design
team:
  - backend
  - fullstack
complexity: advanced
confidence: high
claude_model:
  - sonnet
  - sonnet-4
claude_feature:
  - code-generation
  - architecture
projects:
  - api-platform
  - microservices
tags:
  - async
  - performance
  - scalability
  - database
---

# Async Python API Architecture Patterns

## 1. High-Performance Database Operations

### Connection Pool Management
```python
import asyncio
import asyncpg
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Any

class DatabaseManager:
    def __init__(self, database_url: str, min_size: int = 10, max_size: int = 20):
        self.database_url = database_url
        self.min_size = min_size
        self.max_size = max_size
        self._pool: asyncpg.Pool = None

    async def initialize(self):
        """Initialize connection pool on startup."""
        self._pool = await asyncpg.create_pool(
            self.database_url,
            min_size=self.min_size,
            max_size=self.max_size,
            command_timeout=60,
            server_settings={
                'jit': 'off',  # Disable JIT for faster connection
                'application_name': 'fastapi_app',
            }
        )

    @asynccontextmanager
    async def acquire(self) -> AsyncGenerator[asyncpg.Connection, None]:
        """Context manager for acquiring database connections."""
        async with self._pool.acquire() as connection:
            yield connection

    async def close(self):
        """Close all connections in the pool."""
        if self._pool:
            await self._pool.close()

# Usage in FastAPI
db_manager = DatabaseManager("postgresql://...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await db_manager.initialize()
    yield
    # Shutdown
    await db_manager.close()

app = FastAPI(lifespan=lifespan)
```

### Optimized Query Patterns
```python
from typing import List, Optional
import asyncpg

class UserRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager

    async def get_users_with_stats(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Fetch users with aggregated statistics in single query."""
        query = """
        SELECT
            u.id, u.name, u.email, u.created_at,
            COUNT(p.id) as post_count,
            AVG(p.rating) as avg_rating,
            MAX(p.created_at) as last_post_date
        FROM users u
        LEFT JOIN posts p ON u.id = p.user_id
        WHERE u.active = true
        GROUP BY u.id, u.name, u.email, u.created_at
        ORDER BY u.created_at DESC
        LIMIT $1
        """

        async with self.db.acquire() as conn:
            rows = await conn.fetch(query, limit)
            return [dict(row) for row in rows]

    async def bulk_update_users(self, updates: List[Dict[str, Any]]) -> int:
        """Efficient bulk update using UNNEST."""
        if not updates:
            return 0

        user_ids = [update['id'] for update in updates]
        names = [update['name'] for update in updates]
        emails = [update['email'] for update in updates]

        query = """
        UPDATE users SET
            name = data.name,
            email = data.email,
            updated_at = NOW()
        FROM (
            SELECT * FROM UNNEST($1::int[], $2::text[], $3::text[])
            AS t(id, name, email)
        ) AS data
        WHERE users.id = data.id
        """

        async with self.db.acquire() as conn:
            result = await conn.execute(query, user_ids, names, emails)
            return int(result.split()[-1])  # Extract affected row count
```

## 2. Advanced Async Patterns

### Concurrent Processing with Semaphores
```python
import asyncio
from typing import List, Callable, TypeVar, Awaitable

T = TypeVar('T')

class ConcurrentProcessor:
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def process_batch(
        self,
        items: List[T],
        processor: Callable[[T], Awaitable[Any]],
        batch_size: int = 100
    ) -> List[Any]:
        """Process items in controlled batches with concurrency limits."""
        results = []

        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            batch_tasks = [
                self._process_with_semaphore(item, processor)
                for item in batch
            ]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            results.extend(batch_results)

        return results

    async def _process_with_semaphore(self, item: T, processor: Callable[[T], Awaitable[Any]]):
        async with self.semaphore:
            return await processor(item)

# Usage example
async def process_user_data(user_id: int) -> Dict[str, Any]:
    """Example processor function."""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/api/users/{user_id}/data")
        return response.json()

processor = ConcurrentProcessor(max_concurrent=20)
user_ids = list(range(1, 1000))
results = await processor.process_batch(user_ids, process_user_data)
```
EOF

cat > .claude/ml_pipeline_concept.md << 'EOF'
---
title: ML Pipeline Architecture for Production
type: concept
status: production
tech:
  - python
  - pytorch
  - mlflow
  - docker
  - kubernetes
domain:
  - machine-learning
  - mlops
  - data-science
team:
  - ml-research
  - backend
  - devops
complexity: expert
confidence: high
claude_feature:
  - analysis
  - architecture
projects:
  - ml-platform
  - ai-services
tags:
  - mlops
  - pipelines
  - monitoring
  - deployment
---

# ML Pipeline Architecture for Production

## 1. Pipeline Components Architecture

### Core Pipeline Structure
```
ML Pipeline:
├── Data Ingestion     # Batch/Stream data collection
├── Data Validation    # Schema validation, drift detection
├── Feature Engineering # Transform, encode, scale
├── Model Training     # Experiment tracking, hyperparameter tuning
├── Model Validation   # A/B testing, performance metrics
├── Model Deployment   # Containerization, serving
└── Monitoring        # Performance, drift, feedback loops
```

### Design Principles
- **Reproducibility**: Version control for data, code, and models
- **Scalability**: Horizontal scaling for training and inference
- **Observability**: Comprehensive logging and monitoring
- **Fault Tolerance**: Graceful degradation and recovery
- **Security**: Data privacy and model protection

## 2. Implementation Architecture

### Data Pipeline with Quality Gates
```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import pandas as pd
from great_expectations import DataContext

@dataclass
class DataQualityReport:
    passed: bool
    metrics: Dict[str, float]
    issues: List[str]
    confidence_score: float

class DataQualityGate:
    def __init__(self, expectations_suite: str):
        self.context = DataContext()
        self.suite_name = expectations_suite

    async def validate_data(self, data: pd.DataFrame) -> DataQualityReport:
        """Validate data quality before pipeline processing."""
        batch = self.context.get_batch(
            {"dataset": data, "datasource": "pandas_datasource"},
            expectation_suite_name=self.suite_name
        )

        results = self.context.run_validation_operator(
            "action_list_operator", assets_to_validate=[batch]
        )

        validation_result = results.list_validation_results()[0]

        return DataQualityReport(
            passed=validation_result.success,
            metrics=self._extract_metrics(validation_result),
            issues=self._extract_issues(validation_result),
            confidence_score=self._calculate_confidence(validation_result)
        )
```

### Model Training with Experiment Tracking
```python
import mlflow
import mlflow.pytorch
from mlflow.tracking import MlflowClient
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

class ExperimentTracker:
    def __init__(self, experiment_name: str):
        mlflow.set_experiment(experiment_name)
        self.client = MlflowClient()

    async def train_model_with_tracking(
        self,
        model: nn.Module,
        train_loader: DataLoader,
        val_loader: DataLoader,
        config: Dict[str, Any]
    ) -> str:
        """Train model with comprehensive experiment tracking."""

        with mlflow.start_run() as run:
            # Log hyperparameters
            mlflow.log_params(config)

            # Log model architecture
            mlflow.log_text(str(model), "model_architecture.txt")

            optimizer = torch.optim.Adam(model.parameters(), lr=config['learning_rate'])
            criterion = nn.CrossEntropyLoss()

            best_val_accuracy = 0.0

            for epoch in range(config['num_epochs']):
                # Training phase
                train_loss, train_acc = await self._train_epoch(
                    model, train_loader, optimizer, criterion
                )

                # Validation phase
                val_loss, val_acc = await self._validate_epoch(
                    model, val_loader, criterion
                )

                # Log metrics
                mlflow.log_metrics({
                    "train_loss": train_loss,
                    "train_accuracy": train_acc,
                    "val_loss": val_loss,
                    "val_accuracy": val_acc
                }, step=epoch)

                # Save best model
                if val_acc > best_val_accuracy:
                    best_val_accuracy = val_acc
                    mlflow.pytorch.log_model(
                        model,
                        "best_model",
                        registered_model_name=config['model_name']
                    )

            # Log final metrics
            mlflow.log_metric("best_val_accuracy", best_val_accuracy)

            return run.info.run_id
```

## 3. Production Deployment Strategy

### Model Serving Architecture
- **A/B Testing**: Gradual rollout with traffic splitting
- **Shadow Deployment**: Parallel testing without affecting users
- **Canary Releases**: Progressive deployment with monitoring
- **Rollback Capability**: Instant reversion to previous versions

### Monitoring and Alerting
- **Data Drift Detection**: Statistical tests for input distribution changes
- **Model Performance**: Real-time accuracy, latency, throughput metrics
- **Business Metrics**: Impact on key performance indicators
- **Infrastructure**: Resource utilization, error rates, availability

### Continuous Learning Loop
1. **Feedback Collection**: User interactions, expert annotations
2. **Performance Analysis**: Model degradation detection
3. **Retraining Triggers**: Automated decision for model updates
4. **Validation Pipeline**: Comprehensive testing before deployment
EOF

# Synchronization with project identification
echo ""
echo "🔄 MULTI-TEAM SYNCHRONIZATION"
echo "═════════════════════════════"
echo ""

echo "📤 Frontend Team Knowledge Sync"
echo "$ ckc sync --project Frontend-Team"
cd "$DEMO_DIR/frontend_team"
run_ckc sync --project Frontend-Team

echo ""
echo "📤 Backend Team Knowledge Sync"
echo "$ ckc sync --project Backend-Team"
cd "$DEMO_DIR/backend_team"
run_ckc sync --project Backend-Team

# Demonstrate cross-team discovery
echo ""
echo "🔍 CROSS-TEAM KNOWLEDGE DISCOVERY"
echo "═════════════════════════════════"
echo ""

echo "📋 All Projects in Shared Vault:"
echo "$ ckc project list"
run_ckc project list

echo ""
echo "🎨 Frontend Team Content:"
echo "$ ckc search --team frontend --format summary"
run_ckc search --team frontend --format summary

echo ""
echo "🔧 Backend Team Content:"
echo "$ ckc search --team backend --format summary"
run_ckc search --team backend --format summary

echo ""
echo "🔍 Cross-Team Technology Search:"
echo "$ ckc search --tech typescript --team any"
run_ckc search --tech typescript || echo "  (No TypeScript content from Backend team, as expected)"

echo ""
echo "📊 VAULT ORGANIZATION ANALYSIS"
echo "══════════════════════════════"
echo ""

if [ -d "$DEMO_DIR/shared_vault" ]; then
    echo "🏗️ Pure Tag-Centered Vault Structure:"
    echo "├── _system/          # Templates and configuration"
    echo "├── _attachments/     # Shared media resources"
    echo "├── inbox/            # Unprocessed content (status: draft)"
    echo "├── active/           # Working content (status: tested)"
    echo "├── archive/          # Deprecated content"
    echo "└── knowledge/        # Mature content (status: production)"
    echo ""

    echo "📁 Actual Generated Structure:"
    find "$DEMO_DIR/shared_vault" -type d | head -10 | sort
    echo ""

    echo "📄 Content Distribution by Workflow State:"
    for dir in "knowledge" "active" "inbox" "_system"; do
        if [ -d "$DEMO_DIR/shared_vault/$dir" ]; then
            count=$(find "$DEMO_DIR/shared_vault/$dir" -name "*.md" 2>/dev/null | wc -l)
            echo "  $dir/: $count files"
        fi
    done
fi

echo ""
echo "✅ MULTI-TEAM DEMO COMPLETE"
echo "═══════════════════════════"
echo ""
echo "🎉 Revolutionary Team Collaboration Features:"
echo "  ✅ Pure tag-based team identification (no directory silos)"
echo "  ✅ Cross-team knowledge discovery through multi-dimensional tags"
echo "  ✅ State-based content lifecycle (draft→tested→production)"
echo "  ✅ Team-specific metadata and ownership tracking"
echo "  ✅ Technology and domain-based content organization"
echo "  ✅ Unified vault with intelligent content placement"
echo ""
echo "🏷️ Multi-Team Tag Architecture:"
echo "  • team: [frontend, backend, fullstack, ml-research, devops]"
echo "  • tech: [react, python, typescript, pytorch, fastapi, ...]"
echo "  • domain: [web-dev, machine-learning, api-design, ...]"
echo "  • complexity: [beginner, intermediate, advanced, expert]"
echo "  • projects: [ui-framework, ml-platform, api-services, ...]"
echo "  • status: [draft, tested, production, deprecated]"
echo ""
echo "🔍 Cross-Team Discovery Examples:"
echo "  • Find all React content: #tech/react"
echo "  • Advanced backend patterns: #team/backend AND #complexity/advanced"
echo "  • Cross-team API knowledge: #domain/api-design"
echo "  • Production-ready patterns: #status/production AND #confidence/high"
echo ""
echo "📁 Demo artifacts:"
echo "  • Frontend Team: $DEMO_DIR/frontend_team/"
echo "  • Backend Team: $DEMO_DIR/backend_team/"
echo "  • Shared Vault: $DEMO_DIR/shared_vault/"
echo ""
echo "🚀 Next steps for teams:"
echo "  1. Open shared vault in Obsidian: $DEMO_DIR/shared_vault"
echo "  2. Explore team-specific content with tag queries"
echo "  3. Use cross-team discovery for knowledge sharing"
echo "  4. Set up 'ckc watch' in each team directory"
echo "  5. Experience seamless multi-team collaboration!"
echo ""
echo "💡 The future of team knowledge management:"
echo "   No silos, no boundaries - just intelligent, discoverable knowledge!"
