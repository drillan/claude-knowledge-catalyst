#!/bin/bash

# Obsidian to CKC Pure Tag-Centered Migration Demo
# Demonstrates realistic migration from Obsidian vault to enhanced CKC system

set -e

# Dynamic path detection (portable across environments)
DEMO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$DEMO_DIR")"

echo "🎯 Claude Knowledge Catalyst - Obsidian Migration Demo"
echo "====================================================="
echo ""
echo "Experience the revolutionary enhancement of your Obsidian vault:"
echo "• Transform basic tags → 7-dimensional tag architecture"
echo "• Upgrade simple metadata → rich multi-layered system"
echo "• Enable AI-powered content classification and enhancement"
echo "• Unlock dynamic cross-dimensional knowledge discovery"
echo ""

# Function to run CKC commands (デモディレクトリ内で実行)
run_ckc() {
    PYTHONPATH="$PROJECT_ROOT/src" "$PROJECT_ROOT/.venv/bin/python" -m claude_knowledge_catalyst.cli.main "$@"
}

# Setup demo environment
echo "🧹 Setting up Obsidian migration demo environment..."
rm -rf "$DEMO_DIR/obsidian_vault" "$DEMO_DIR/enhanced_ckc_vault"
mkdir -p "$DEMO_DIR/obsidian_vault"

echo ""
echo "📂 Created demo directories:"
echo "  • obsidian_vault/ - Typical Obsidian vault with basic metadata"
echo "  • enhanced_ckc_vault/ - CKC enhanced vault (will be created)"
echo ""

# Step 1: Create realistic Obsidian vault structure
echo "👤 STEP 1: Creating Realistic Obsidian Vault Structure"
echo "────────────────────────────────────────────────────"
echo ""

cd "$DEMO_DIR/obsidian_vault"

# Create realistic Obsidian content with standard frontmatter
cat > API_Design_Principles.md << 'EOF'
---
title: API Design Principles
tags: [development, api, backend, documentation]
created: 2024-01-15
updated: 2024-01-20
author: Development Team
---

# API Design Principles

## Core Guidelines

### 1. RESTful Design
- Use standard HTTP methods (GET, POST, PUT, DELETE)
- Maintain stateless interactions
- Implement proper status codes

### 2. Consistent Naming
- Use kebab-case for endpoints
- Plural nouns for collections
- Clear, descriptive resource names

### 3. Error Handling
- Standardized error response format
- Meaningful error messages
- Proper HTTP status codes

### 4. Versioning Strategy
- URL versioning: `/api/v1/users`
- Backward compatibility maintenance
- Clear deprecation notices
EOF

cat > React_Performance_Tips.md << 'EOF'
---
title: React Performance Optimization
tags: [react, javascript, frontend, performance, optimization]
created: 2024-02-01
updated: 2024-02-10
author: Frontend Team
status: draft
---

# React Performance Optimization Tips

## Memoization Techniques

### React.memo
```jsx
const ExpensiveComponent = React.memo(({ data }) => {
  return <div>{data.map(item => <Item key={item.id} {...item} />)}</div>;
});
```

### useMemo Hook
```jsx
function DataProcessor({ items }) {
  const processedData = useMemo(() => {
    return items.filter(item => item.active)
                .sort((a, b) => a.priority - b.priority);
  }, [items]);
  
  return <DataList data={processedData} />;
}
```

### useCallback Hook
```jsx
function ParentComponent({ onItemClick }) {
  const handleClick = useCallback((itemId) => {
    onItemClick(itemId);
    analytics.track('item_clicked');
  }, [onItemClick]);
  
  return <ChildComponent onClick={handleClick} />;
}
```

## Code Splitting

### Lazy Loading
```jsx
const LazyComponent = lazy(() => import('./HeavyComponent'));

function App() {
  return (
    <Suspense fallback={<Loading />}>
      <LazyComponent />
    </Suspense>
  );
}
```
EOF

cat > Python_Async_Patterns.md << 'EOF'
---
title: Python Async Programming Patterns
tags: [python, async, backend, programming, patterns]
created: 2024-01-25
author: Backend Team
projects: [api-development]
---

# Python Async Programming Patterns

## Basic Async/Await

```python
import asyncio
import aiohttp

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    data = await fetch_data('https://api.example.com/data')
    print(data)

asyncio.run(main())
```

## Concurrent Processing

```python
async def process_urls(urls):
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

# Process multiple URLs concurrently
urls = ['https://api1.com', 'https://api2.com', 'https://api3.com']
results = await process_urls(urls)
```

## Error Handling

```python
async def safe_fetch(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {'error': f'HTTP {response.status}'}
    except asyncio.TimeoutError:
        return {'error': 'Request timeout'}
    except Exception as e:
        return {'error': str(e)}
```
EOF

# Create .claude directory structure first
mkdir -p .claude/code

cat > .claude/code/python_snippets.md << 'EOF'
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
EOF

cat > Machine_Learning_Pipeline.md << 'EOF'
---
title: ML Pipeline Best Practices
tags: [machine-learning, mlops, python, data-science, pipeline]
created: 2024-02-05
author: Data Science Team
project: ml-platform
status: published
---

# Machine Learning Pipeline Best Practices

## Pipeline Structure

### 1. Data Ingestion
- Automated data collection
- Data validation and quality checks
- Version control for datasets

### 2. Feature Engineering
- Reproducible transformations
- Feature store integration
- Automated feature selection

### 3. Model Training
- Experiment tracking with MLflow
- Hyperparameter optimization
- Cross-validation strategies

### 4. Model Evaluation
- Multiple evaluation metrics
- A/B testing framework
- Performance monitoring

### 5. Deployment
- Containerized model serving
- Blue-green deployment
- Rollback capabilities

## Implementation Example

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Create ML pipeline
ml_pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100))
])

# Train pipeline
ml_pipeline.fit(X_train, y_train)

# Make predictions
predictions = ml_pipeline.predict(X_test)
```
EOF

cat > DevOps_Automation.md << 'EOF'
---
title: DevOps Automation Strategies
tags: [devops, automation, ci-cd, infrastructure, deployment]
created: 2024-01-30
author: DevOps Team
project: infrastructure
---

# DevOps Automation Strategies

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest tests/
      - name: Deploy to staging
        if: github.ref == 'refs/heads/develop'
        run: |
          ./deploy-staging.sh
```

## Infrastructure as Code

### Terraform Configuration
```hcl
resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1d0"
  instance_type = "t2.micro"
  
  tags = {
    Name = "WebServer"
    Environment = "production"
  }
}
```

## Monitoring and Alerting

- Prometheus for metrics collection
- Grafana for visualization
- PagerDuty for incident management
- ELK stack for log aggregation
EOF

cat > Code_Review_Checklist.md << 'EOF'
---
title: Code Review Checklist
tags: [code-review, quality, best-practices, guidelines]
created: 2024-02-12
author: Engineering Team
---

# Code Review Checklist

## Functionality
- [ ] Code accomplishes what it's supposed to do
- [ ] Logic is correct and handles edge cases
- [ ] No obvious bugs or logical errors

## Code Quality
- [ ] Code is readable and well-structured
- [ ] Follows project coding standards
- [ ] Appropriate comments and documentation
- [ ] No code duplication

## Security
- [ ] No hardcoded secrets or credentials
- [ ] Input validation is properly implemented
- [ ] Authorization checks are in place
- [ ] SQL injection prevention measures

## Performance
- [ ] No unnecessary database queries
- [ ] Efficient algorithms and data structures
- [ ] Memory usage is reasonable
- [ ] Caching is used where appropriate

## Testing
- [ ] Unit tests cover new functionality
- [ ] Integration tests are updated
- [ ] Test cases cover edge scenarios
- [ ] All tests pass

## Documentation
- [ ] README updated if necessary
- [ ] API documentation is current
- [ ] Inline comments explain complex logic
EOF

echo "✏️ Created realistic Obsidian vault content:"
echo "  📄 API_Design_Principles.md - Basic development tags"
echo "  📄 React_Performance_Tips.md - Frontend optimization notes"
echo "  📄 Python_Async_Patterns.md - Backend programming patterns"
echo "  📄 Machine_Learning_Pipeline.md - ML best practices"
echo "  📄 DevOps_Automation.md - Infrastructure automation"
echo "  📄 Code_Review_Checklist.md - Quality assurance guidelines"
echo ""

# Initialize CKC project for migration
echo "👤 STEP 2: Initialize CKC Project for Migration"
echo "───────────────────────────────────────────────"
echo "$ mkdir ckc_project && cd ckc_project"
echo "$ ckc init"
echo ""
mkdir -p "$DEMO_DIR/ckc_project"
cd "$DEMO_DIR/ckc_project"
run_ckc init

# Step 3: Connect vault and preview migration
echo ""
echo "$ ckc add enhanced-vault ../enhanced_ckc_vault"
run_ckc add enhanced-vault "../enhanced_ckc_vault"

echo ""
echo "👤 STEP 3: Preview Obsidian to CKC Enhancement"
echo "─────────────────────────────────────────────"
echo "$ ckc migrate --source ../obsidian_vault --target ../enhanced_ckc_vault --dry-run"
echo ""
run_ckc migrate --source "../obsidian_vault" --target "../enhanced_ckc_vault" --dry-run

# Wait for user confirmation to continue
echo ""
echo "🤔 The dry-run shows how basic Obsidian metadata will be enhanced."
echo "   Ready to perform the actual migration? [Press Enter to continue]"
read -r

# Step 4: Perform actual migration
echo ""
echo "👤 STEP 4: Perform Obsidian to CKC Enhancement Migration"
echo "─────────────────────────────────────────────────────────"
echo "$ ckc migrate --source ../obsidian_vault --target ../enhanced_ckc_vault"
echo ""
run_ckc migrate --source "../obsidian_vault" --target "../enhanced_ckc_vault"

# Step 5: Explore the migration results
echo ""
echo "📊 STEP 5: Exploring Migration Enhancement Results"
echo "─────────────────────────────────────────────────"
echo ""

# Show new directory structure
echo "🏗️ Enhanced CKC Vault Structure:"
if [ -d "../enhanced_ckc_vault" ]; then
    echo "├── _system/          # Templates and configuration"
    echo "├── _attachments/     # Media files"
    echo "├── inbox/            # Unprocessed content (status: draft)"
    echo "├── active/           # Working content (status: tested)"
    echo "├── archive/          # Deprecated content"
    echo "└── knowledge/        # Mature content (90% of files)"
    echo ""
    
    echo "📁 Generated Structure:"
    find "../enhanced_ckc_vault" -type d -name "*" | head -8 | sort
    echo ""
fi

# Show specific directories
for dir in "_system" "inbox" "active" "archive" "knowledge"; do
    if [ -d "../enhanced_ckc_vault/$dir" ]; then
        echo "📁 $dir/:"
        ls -la "../enhanced_ckc_vault/$dir" | grep -E "\.(md|yaml)$" | head -3 || echo "  (no files or empty)"
        echo ""
    fi
done

# Step 6: Compare before and after metadata
echo "🏷️ STEP 6: Before vs After Metadata Comparison"
echo "─────────────────────────────────────────────────"
echo ""

# Show original Obsidian metadata
echo "📊 BEFORE (Original Obsidian):"
echo "────────────────────────────────"
original_file=$(find "../obsidian_vault" -name "*.md" -type f | head -1)
if [ -n "$original_file" ]; then
    echo "📄 $(basename "$original_file"):"
    sed -n '/^---$/,/^---$/p' "$original_file" | head -10
    echo ""
fi

# Show enhanced CKC metadata
echo "📊 AFTER (CKC Enhanced):"
echo "───────────────────────────"
migrated_file=$(find "../enhanced_ckc_vault/knowledge" -name "*.md" -type f | head -1)
if [ -n "$migrated_file" ]; then
    echo "📄 $(basename "$migrated_file"):"
    sed -n '/^---$/,/^---$/p' "$migrated_file" | head -20
    echo ""
fi

# Step 7: Show enhanced templates and features
echo "📝 STEP 7: Enhanced CKC Templates and Features"
echo "─────────────────────────────────────────────"
echo ""

template_dir="../enhanced_ckc_vault/_system/templates"
if [ -d "$template_dir" ]; then
    echo "📁 Enhanced templates created in _system/templates/:"
    ls -la "$template_dir"/*.md 2>/dev/null | while read line; do
        filename=$(echo "$line" | awk '{print $NF}')
        echo "  📄 $(basename "$filename")"
    done
    echo ""
    
    # Show a sample enhanced template
    if [ -f "$template_dir/prompt_template.md" ]; then
        echo "📄 Sample Enhanced Template (prompt_template.md):"
        echo "─────────────────────────────────────────────────"
        head -20 "$template_dir/prompt_template.md"
        echo "  ... (showing enhanced metadata fields)"
        echo ""
    fi
fi

# Step 8: Show migration report
echo "📋 STEP 8: Migration Enhancement Report"
echo "─────────────────────────────────────"
echo ""

if [ -f "../enhanced_ckc_vault/migration_report.md" ]; then
    echo "📄 Migration Enhancement Summary:"
    echo "──────────────────────────────────"
    head -15 "../enhanced_ckc_vault/migration_report.md"
    echo ""
fi

# Step 9: Demonstrate enhancement benefits
echo "🔍 STEP 9: Obsidian vs CKC Enhancement Benefits"
echo "─────────────────────────────────────────────"
echo ""

echo "📊 BEFORE (Standard Obsidian):"
echo "─────────────────────────────────"
echo "tags: [development, api, backend, documentation]"
echo "created: 2024-01-15"
echo "author: Development Team"
echo ""
echo "❌ Limitations of basic Obsidian tagging:"
echo "  • Flat tag structure - no hierarchical organization"
echo "  • No semantic categorization (type, domain, team)"
echo "  • Missing workflow states (draft, tested, production)"
echo "  • No AI-enhanced metadata inference"
echo "  • Limited cross-dimensional discovery"
echo ""

echo "📊 AFTER (CKC Enhanced Multi-Dimensional):"
echo "─────────────────────────────────────────────"
echo "type: concept                    # Content nature classification"
echo "status: production              # Workflow lifecycle state"
echo "tech: [api, rest, graphql]       # Technology stack tags"
echo "domain: [web-dev, backend]       # Application domain areas"
echo "team: [backend, fullstack]       # Team ownership/relevance"
echo "complexity: intermediate         # Skill level requirement"
echo "confidence: high                 # Content reliability score"
echo "projects: [api-platform]         # Associated project links"
echo "claude_feature: [analysis, docs] # Claude AI capabilities"
echo "tags: [design-patterns, scale]   # Evolutionary free-form tags"
echo ""
echo "✅ Benefits of CKC enhanced system:"
echo "  • 7-dimensional tag architecture for precise classification"
echo "  • State-based workflow organization (inbox→active→knowledge)"
echo "  • AI-powered metadata inference and enhancement"
echo "  • Cross-team knowledge discovery and collaboration"
echo "  • Dynamic Obsidian query generation for complex searches"
echo "  • Scalable organization that grows with your knowledge"
echo ""

# Step 10: Advanced discovery examples
echo "🔍 STEP 10: Advanced CKC Discovery Examples"
echo "──────────────────────────────────────────"
echo ""

echo "With CKC's enhanced tag system, powerful queries become possible:"
echo ""
echo "📋 Example Advanced Obsidian Queries:"
echo ""
echo "1. Production-ready backend patterns:"
echo '   ```dataview'
echo '   TABLE tech, complexity, confidence, success_rate'
echo '   FROM #backend'
echo '   WHERE status = "production" AND confidence = "high"'
echo '   SORT confidence DESC, complexity ASC'
echo '   ```'
echo ""
echo "2. Cross-team technology knowledge:"
echo '   ```query'
echo '   (team:frontend OR team:backend) AND tech:python'
echo '   AND status:production'
echo '   ```'
echo ""
echo "3. ML pipeline resources by complexity:"
echo '   ```dataview'
echo '   LIST domain, projects, claude_feature'
echo '   FROM #machine-learning'
echo '   WHERE complexity IN ["intermediate", "advanced"]'
echo '   GROUP BY complexity'
echo '   ```'
echo ""
echo "4. High-success prompts for automation:"
echo '   ```dataview'
echo '   TABLE title, success_rate, claude_model, updated'
echo '   FROM #automation AND type = "prompt"'
echo '   WHERE success_rate > 80'
echo '   SORT success_rate DESC'
echo '   ```'
echo ""

# Final summary
echo "✅ DEMO COMPLETE: Obsidian to CKC Enhancement Revolution"
echo "════════════════════════════════════════════════════════"
echo ""
echo "🎉 Revolutionary Enhancement Achieved:"
echo "  ✅ Transformed basic Obsidian tags → 7-dimensional tag architecture"
echo "  ✅ Enhanced simple metadata → rich multi-layered system"
echo "  ✅ Upgraded flat organization → state-based workflow"
echo "  ✅ Added AI-powered content classification and enhancement"
echo "  ✅ Generated advanced Obsidian templates and queries"
echo "  ✅ Enabled cross-dimensional knowledge discovery"
echo ""
echo "🔍 Key Enhancement Benefits:"
echo "  • 🏷️ Multi-Dimensional Tags: tech + domain + team + status + complexity"
echo "  • 🤖 AI Enhancement: Automatic metadata inference and suggestions"
echo "  • 📊 Workflow States: Clear content lifecycle (draft→tested→production)"
echo "  • 🔍 Advanced Discovery: Complex queries across multiple dimensions"
echo "  • 👥 Team Collaboration: Clear ownership and knowledge sharing"
echo "  • 📈 Scalable Growth: Tag system evolves with your knowledge base"
echo ""
echo "🏷️ CKC 7-Dimensional Tag Architecture:"
echo "  • type: Content nature (prompt, code, concept, resource)"
echo "  • tech: Technology stack (python, react, fastapi, kubernetes, ...)"
echo "  • domain: Application areas (web-dev, machine-learning, devops, ...)"
echo "  • team: Team ownership (backend, frontend, ml-research, devops)"
echo "  • status: Lifecycle state (draft, tested, production, deprecated)"
echo "  • complexity: Skill level (beginner, intermediate, advanced, expert)"
echo "  • confidence: Content reliability (low, medium, high)"
echo "  • projects: Associated projects and initiatives"
echo "  • claude_feature: AI capabilities (analysis, code-generation, debugging)"
echo ""
echo "📁 Demo artifacts:"
echo "  • Original Obsidian: $DEMO_DIR/obsidian_vault/"
echo "  • CKC Enhanced: $DEMO_DIR/enhanced_ckc_vault/"
echo "  • Migration Report: $DEMO_DIR/enhanced_ckc_vault/migration_report.md"
echo "  • CKC Project: $DEMO_DIR/ckc_project/"
echo ""
echo "🚀 Next steps:"
echo "  1. Open enhanced_ckc_vault in Obsidian"
echo "  2. Try the advanced queries in knowledge/ README"
echo "  3. Use the enhanced templates in _system/templates/"
echo "  4. Experience 7-dimensional knowledge discovery!"
echo "  5. Set up 'ckc watch' for continuous enhancement"
echo ""
echo "💡 Welcome to enhanced knowledge management!"
echo "   Your Obsidian vault, supercharged with AI-powered multi-dimensional organization!"