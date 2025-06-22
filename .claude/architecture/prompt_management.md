---
author: null
category: concept
claude_feature:
- code-generation
- analysis
claude_model: []
complexity: advanced
confidence: high
created: 2025-06-19 00:00:00
domain:
- ai-ml
- automation
- data-science
- mobile
- security
- testing
project: claude-knowledge-catalyst
projects:
- claude-knowledge-catalyst
purpose: Auto-generated metadata for prompt_management
quality: high
status: draft
subcategory: Development_Patterns
success_rate: null
tags:
- architecture
- design
- structure
- system
team: []
tech:
- api
- aws
- git
- javascript
- python
- typescript
title: Prompt Management
type: prompt
updated: 2025-06-21 00:04:32.040182
version: '1.0'
---

# プロンプト記録・管理システム

## 概要

CKC のプロンプト管理システムは、Claude Code との開発プロセスで使用されるプロンプトを体系的に記録、分析、改善するためのコア機能です。単なる保存ではなく、**プロンプトエンジニアリングの知見蓄積と再利用促進**を目的とした統合システムです。

## システム設計思想

### 1. プロンプトライフサイクル管理
```
草稿作成 → 実行・テスト → 改善・最適化 → 本番運用 → アーカイブ
   ↓         ↓           ↓           ↓         ↓
 draft → experimental → tested → production → archived
```

### 2. 品質管理指標
- **成功率**: 期待する結果を得られた割合
- **効率性**: トークン使用量と結果品質のバランス
- **再利用性**: 他のコンテキストでの適用可能性
- **保守性**: 理解・修正のしやすさ

### 3. 知識資産化
- プロンプトパターンの体系化
- 成功事例のテンプレート化
- 失敗パターンの教訓抽出
- ドメイン特化知識の蓄積

## プロンプトメタデータ構造

### 基本情報
```yaml
---
title: "Python コードレビュー自動化プロンプト"
created: 2024-06-18T10:30:00+09:00
updated: 2024-06-18T15:45:00+09:00
version: "2.1"
category: prompt
subcategory: code_review

# Claude固有情報
model: sonnet
confidence: high
success_rate: 92
token_usage:
  input_tokens: 1200
  output_tokens: 800
  total_cost: 0.024

# 品質・パフォーマンス指標
quality: high
complexity: medium
effectiveness: high
reusability: high

# プロンプト分類
prompt_type: instruction  # instruction, conversation, system, template
domain: software_development
use_case: code_quality_assurance
target_audience: developers

# プロジェクト文脈
project: claude-knowledge-catalyst
purpose: Python コードの品質向上自動化
related_prompts:
  - python-bug-detection
  - code-optimization-suggestions
  - documentation-generation

# 実行履歴
execution_history:
  - date: 2024-06-15
    result: success
    feedback: "レビュー精度が高く、実用的な改善提案"
  - date: 2024-06-16
    result: partial_success
    feedback: "複雑な関数で詳細度不足"
    
# 改善ログ
improvement_log:
  - version: "1.0 → 1.1"
    change: "例外処理のレビュー観点を追加"
    reason: "セキュリティ問題の見落とし対策"
  - version: "1.1 → 2.0"
    change: "コンテキスト長の最適化"
    reason: "トークン使用量削減（30%改善）"

tags:
  - prompt
  - code_review
  - python
  - automation
  - claude/sonnet
  - production
---
```

### 特殊フィールド詳細

#### 1. プロンプト分類システム
```python
PROMPT_TYPES = {
    "instruction": "明確な指示・命令型",
    "conversation": "対話・インタラクティブ型", 
    "system": "システムメッセージ・設定型",
    "template": "再利用可能テンプレート型",
    "chain": "チェーン・連続実行型"
}

DOMAINS = {
    "software_development": "ソフトウェア開発",
    "data_analysis": "データ分析",
    "content_creation": "コンテンツ作成",
    "problem_solving": "問題解決",
    "research": "調査・研究",
    "automation": "自動化・効率化"
}
```

#### 2. パフォーマンス指標
```yaml
performance_metrics:
  success_rate: 92          # 成功率（%）
  avg_token_usage: 2000     # 平均トークン使用量
  response_quality: 4.5     # 応答品質（1-5）
  execution_time: 12.3      # 平均実行時間（秒）
  cost_efficiency: 0.95     # コスト効率性（1.0が最適）
```

#### 3. 実行履歴管理
```python
class PromptExecution(BaseModel):
    execution_id: str
    timestamp: datetime
    model_used: str
    input_tokens: int
    output_tokens: int
    execution_time: float
    result_status: str  # success, partial_success, failure
    quality_score: float
    user_feedback: str | None
    context_hash: str  # 実行コンテキストの識別
```

## テンプレートシステム

### 1. プロンプトテンプレート構造

#### 基本テンプレート
```jinja2
{# templates/prompt.md #}
---
title: "{{ title }}"
created: {{ now() }}
updated: {{ now() }}
version: "1.0"
category: prompt
subcategory: {{ subcategory | default('general') }}
model: {{ model | default('sonnet') }}
prompt_type: {{ prompt_type | default('instruction') }}
domain: {{ domain }}
project: {{ project }}
tags:
  - prompt
  {% for tag in additional_tags -%}
  - {{ tag }}
  {% endfor %}
---

# {{ title }}

## 目的
{{ purpose }}

## 使用モデル
- **推奨モデル**: {{ model | default('Claude Sonnet') }}
- **最小要件**: {{ min_model | default('Claude Haiku') }}

## プロンプト本体

```
{{ prompt_content }}
```

## 実行例

### 入力例
```
{{ input_example }}
```

### 期待出力例
```
{{ expected_output }}
```

## 改善履歴
{% if improvement_log %}
{% for entry in improvement_log %}
- **{{ entry.version }}**: {{ entry.change }} ({{ entry.reason }})
{% endfor %}
{% endif %}

## 関連プロンプト
{% if related_prompts %}
{% for prompt in related_prompts %}
- [[{{ prompt }}]]
{% endfor %}
{% endif %}

## 注意事項
{{ notes | default('特になし') }}
```

#### 特殊用途テンプレート

**コードレビュープロンプト**:
```jinja2
{# templates/code_review_prompt.md #}
---
title: "{{ language }} コードレビュープロンプト"
prompt_type: instruction
domain: software_development
subcategory: code_review
---

# {{ language }} コードレビュー自動化

## レビュー観点
{% for aspect in review_aspects %}
- {{ aspect }}
{% endfor %}

## プロンプト
```
あなたは経験豊富な{{ language }}開発者です。以下のコードを以下の観点でレビューしてください：

{% for aspect in review_aspects %}
{{ loop.index }}. {{ aspect }}
{% endfor %}

コード:
```{{ language }}
{CODE_HERE}
```

各観点について、具体的な改善提案と理由を示してください。
```
```

### 2. 動的テンプレート生成

```python
class PromptTemplateManager:
    def __init__(self, template_dir: Path):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.env.globals.update({
            'now': datetime.now,
            'uuid4': lambda: str(uuid.uuid4()),
        })
    
    def create_prompt_from_template(
        self, 
        template_name: str, 
        context: dict[str, Any]
    ) -> str:
        template = self.env.get_template(f"{template_name}.md")
        return template.render(**context)
    
    def create_specialized_prompt(
        self,
        prompt_type: str,
        domain: str,
        **kwargs
    ) -> str:
        """特殊化されたプロンプトの生成"""
        template_key = f"{prompt_type}_{domain}"
        if template_key in self.specialized_templates:
            return self.specialized_templates[template_key].render(**kwargs)
        return self.create_prompt_from_template("generic_prompt", kwargs)
```

## プロンプト品質管理

### 1. 自動品質評価

```python
class PromptQualityAssessor:
    def __init__(self):
        self.metrics = {
            'clarity': self._assess_clarity,
            'specificity': self._assess_specificity,
            'completeness': self._assess_completeness,
            'efficiency': self._assess_efficiency
        }
    
    def assess_prompt_quality(self, prompt_content: str) -> dict[str, float]:
        """プロンプト品質の多次元評価"""
        results = {}
        for metric_name, assessor in self.metrics.items():
            results[metric_name] = assessor(prompt_content)
        
        results['overall_score'] = sum(results.values()) / len(results)
        return results
    
    def _assess_clarity(self, content: str) -> float:
        """明確性の評価 (0.0-1.0)"""
        # 文構造の複雑さ、曖昧な表現の検出
        # 実装: 自然言語処理による分析
        pass
    
    def _assess_specificity(self, content: str) -> float:
        """具体性の評価 (0.0-1.0)"""
        # 具体的な指示の割合、例の有無
        pass
```

### 2. 成功率追跡システム

```python
class PromptSuccessTracker:
    def __init__(self, storage: PromptExecutionStorage):
        self.storage = storage
    
    def record_execution(
        self,
        prompt_id: str,
        execution_result: PromptExecution
    ) -> None:
        """プロンプト実行結果の記録"""
        self.storage.save_execution(prompt_id, execution_result)
        self._update_success_metrics(prompt_id)
    
    def get_success_analytics(self, prompt_id: str) -> dict[str, Any]:
        """成功率分析の取得"""
        executions = self.storage.get_executions(prompt_id)
        
        return {
            'total_executions': len(executions),
            'success_count': len([e for e in executions if e.result_status == 'success']),
            'success_rate': self._calculate_success_rate(executions),
            'avg_quality_score': self._calculate_avg_quality(executions),
            'trend': self._analyze_trend(executions),
            'performance_by_model': self._group_by_model(executions)
        }
```

### 3. A/Bテスト機能

```python
class PromptABTester:
    def __init__(self):
        self.active_tests = {}
    
    def create_ab_test(
        self,
        test_name: str,
        prompt_a: str,
        prompt_b: str,
        success_criteria: dict[str, Any]
    ) -> str:
        """A/Bテストの作成と開始"""
        test_id = str(uuid.uuid4())
        self.active_tests[test_id] = {
            'name': test_name,
            'prompts': {'A': prompt_a, 'B': prompt_b},
            'criteria': success_criteria,
            'results': {'A': [], 'B': []},
            'created': datetime.now()
        }
        return test_id
    
    def analyze_test_results(self, test_id: str) -> dict[str, Any]:
        """テスト結果の統計分析"""
        test = self.active_tests[test_id]
        return {
            'winner': self._determine_winner(test),
            'confidence_level': self._calculate_confidence(test),
            'detailed_metrics': self._detailed_analysis(test)
        }
```

## プロンプト改善ワークフロー

### 1. 改善提案システム

```python
class PromptImprovementSuggester:
    def __init__(self, ai_assistant: AIAssistant):
        self.ai = ai_assistant
        self.improvement_patterns = self._load_improvement_patterns()
    
    def suggest_improvements(
        self,
        prompt_content: str,
        execution_history: list[PromptExecution]
    ) -> list[ImprovementSuggestion]:
        """実行履歴に基づく改善提案"""
        
        # 1. パフォーマンス分析
        performance_issues = self._analyze_performance_issues(execution_history)
        
        # 2. パターンマッチング
        pattern_suggestions = self._match_improvement_patterns(
            prompt_content, performance_issues
        )
        
        # 3. AI支援改善提案
        ai_suggestions = self.ai.generate_improvement_suggestions(
            prompt_content, execution_history
        )
        
        return self._merge_and_rank_suggestions(
            pattern_suggestions + ai_suggestions
        )
```

### 2. バージョン管理

```python
class PromptVersionManager:
    def __init__(self, storage: PromptStorage):
        self.storage = storage
    
    def create_new_version(
        self,
        prompt_id: str,
        updated_content: str,
        change_description: str,
        change_reason: str
    ) -> str:
        """新バージョンの作成"""
        current_version = self.storage.get_latest_version(prompt_id)
        new_version = self._increment_version(current_version.version)
        
        version_entry = PromptVersion(
            prompt_id=prompt_id,
            version=new_version,
            content=updated_content,
            change_description=change_description,
            change_reason=change_reason,
            created=datetime.now(),
            parent_version=current_version.version
        )
        
        self.storage.save_version(version_entry)
        return new_version
    
    def compare_versions(
        self, 
        prompt_id: str, 
        version_a: str, 
        version_b: str
    ) -> VersionComparison:
        """バージョン間の詳細比較"""
        # 差分表示、性能比較、改善点分析
        pass
```

## プロンプトライブラリ

### 1. カテゴリ別組織化

```
prompts/
├── development/
│   ├── code_review/
│   │   ├── python_code_review.md
│   │   ├── javascript_code_review.md
│   │   └── security_review.md
│   ├── documentation/
│   │   ├── api_documentation.md
│   │   └── readme_generation.md
│   └── testing/
│       ├── unit_test_generation.md
│       └── integration_test_scenarios.md
├── analysis/
│   ├── data_analysis/
│   │   ├── statistical_analysis.md
│   │   └── data_visualization.md
│   └── log_analysis/
│       └── error_pattern_detection.md
└── automation/
    ├── workflow_automation.md
    └── report_generation.md
```

### 2. 検索・発見システム

```python
class PromptDiscoveryEngine:
    def __init__(self, index: PromptIndex):
        self.index = index
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def semantic_search(self, query: str, limit: int = 10) -> list[PromptMatch]:
        """セマンティック検索による関連プロンプト発見"""
        query_embedding = self.embedding_model.encode(query)
        matches = self.index.similarity_search(query_embedding, limit)
        return matches
    
    def recommend_prompts(
        self, 
        current_context: dict[str, Any]
    ) -> list[PromptRecommendation]:
        """コンテキストベースのプロンプト推奨"""
        # プロジェクト、ドメイン、過去の使用履歴に基づく推奨
        pass
```

## パフォーマンス監視

### 1. リアルタイム監視

```python
class PromptPerformanceMonitor:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager()
    
    def monitor_execution(self, execution: PromptExecution) -> None:
        """実行時監視とアラート"""
        # 成功率低下の検出
        if self._detect_performance_degradation(execution):
            self.alert_manager.send_alert(
                f"プロンプト性能低下: {execution.prompt_id}"
            )
        
        # 異常なトークン使用量の検出
        if self._detect_unusual_token_usage(execution):
            self.alert_manager.send_alert(
                f"異常なトークン使用: {execution.prompt_id}"
            )
```

### 2. 分析レポート

```python
class PromptAnalyticsReporter:
    def generate_monthly_report(self, month: str) -> PromptReport:
        """月次プロンプト活用レポート"""
        return PromptReport(
            most_used_prompts=self._get_most_used_prompts(month),
            highest_performing_prompts=self._get_top_performers(month),
            improvement_opportunities=self._identify_improvement_opportunities(month),
            cost_analysis=self._analyze_costs(month),
            roi_metrics=self._calculate_roi(month)
        )
```

## 統合とワークフロー

### Claude Code との統合
- **自動記録**: 実行されたプロンプトの自動保存
- **コンテキスト保持**: プロジェクト情報とファイル文脈の自動関連付け
- **改善フィードバック**: 実行結果に基づく改善提案

### Obsidian 連携
- **双方向リンク**: 関連プロンプト間の自動リンク生成
- **タグ同期**: プロンプトタグとObsidianタグの統合
- **可視化**: プロンプト関係図の自動生成