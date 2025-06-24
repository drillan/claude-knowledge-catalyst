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
- testing
- web-dev
project: claude-knowledge-catalyst
projects:
- claude-knowledge-catalyst
purpose: Auto-generated metadata for classification_obsidian
quality: high
status: draft
subcategory: Development_Patterns
success_rate: null
tags:
- architecture
- design
- ff6b6b
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
title: Classification Obsidian
type: prompt
updated: 2025-06-21 00:04:32.043003
version: '1.0'
---

# 分類システムとObsidian統合

## 概要

CKC の分類システムは、知識の**自然進化**と**段階的構造化**を支援する核心機能です。カオスから秩序への知識進化プロセスを自動化し、Obsidian との deep integration により、パワフルな知識管理エコシステムを構築します。

## 設計哲学：ハイブリッド構造システム

### 1. 10-Step Numbering System

```
00_Catalyst_Lab      # 実験・アイデア孵化の場
10_Projects          # アクティブプロジェクト管理
20_Knowledge_Base    # 体系化された知見
30_Wisdom_Archive    # 高品質な知識資産
_templates           # システムテンプレート
Analytics            # 知見の活用状況分析
Archive              # 古い・非推奨の知見
```

この数字システムにより、**知識の成熟度**と**アクセス頻度**を視覚的に表現し、自然なワークフローを実現します。

### 2. 知識進化ステージ

```
Raw Ideas → Structured Insights → Validated Knowledge → Wisdom Assets
   (00)         (10-20)              (20-30)            (30+)

├─ 00_Catalyst_Lab/
│  ├─ brainstorming/         # 未加工アイデア
│  ├─ experiments/           # 実験的取り組み
│  └─ rapid_prototypes/      # 迅速プロトタイピング
│
├─ 10_Projects/
│  ├─ active/                # 進行中プロジェクト
│  ├─ planning/              # 計画段階
│  └─ review/                # レビュー・評価段階
│
├─ 20_Knowledge_Base/
│  ├─ Prompts/              # プロンプト知見
│  ├─ Code_Snippets/        # コードパターン
│  ├─ Concepts/             # 概念・理論
│  └─ Resources/            # 学習リソース
│
└─ 30_Wisdom_Archive/
   ├─ Best_Practices/       # ベストプラクティス集
   ├─ Lessons_Learned/      # 教訓と反省
   └─ Strategic_Insights/   # 戦略的知見
```

## ObsidianVaultManager 詳細

### 1. 初期化とボルト構造

```python
class ObsidianVaultManager:
    def __init__(self, vault_path: Path, metadata_manager: MetadataManager):
        self.vault_path = Path(vault_path)
        self.metadata_manager = metadata_manager

        # ハイブリッド構造定義
        self.vault_structure = {
            "00_Catalyst_Lab": "実験・アイデア孵化の場",
            "10_Projects": "アクティブプロジェクト管理",
            "20_Knowledge_Base": "体系化された知見",
            "20_Knowledge_Base/Prompts": "プロンプト関連",
            "20_Knowledge_Base/Prompts/Templates": "汎用プロンプトテンプレート",
            "20_Knowledge_Base/Prompts/Best_Practices": "成功事例とベストプラクティス",
            "20_Knowledge_Base/Prompts/Improvement_Log": "プロンプト改善の記録",
            "20_Knowledge_Base/Code_Snippets": "再利用可能なコードスニペット",
            "20_Knowledge_Base/Code_Snippets/Python": "Python関連",
            "20_Knowledge_Base/Code_Snippets/JavaScript": "JavaScript関連",
            "20_Knowledge_Base/Code_Snippets/Bash": "Bash/Shell関連",
            "20_Knowledge_Base/Code_Snippets/Other_Languages": "その他言語",
            "20_Knowledge_Base/Concepts": "AI・LLM関連の概念整理",
            "20_Knowledge_Base/Concepts/API_Design": "API設計原則",
            "20_Knowledge_Base/Concepts/Software_Architecture": "ソフトウェア設計",
            "20_Knowledge_Base/Concepts/Development_Practices": "開発手法",
            "20_Knowledge_Base/Resources": "学習リソースと外部参考資料",
            "30_Wisdom_Archive": "高品質な知識資産",
            "_templates": "システムテンプレート",
            "Analytics": "知見の活用状況分析",
            "Archive": "古い・非推奨の知見",
        }
```

### 2. インテリジェント分類システム

```python
class IntelligentClassifier:
    def __init__(self, metadata_manager: MetadataManager):
        self.metadata_manager = metadata_manager
        self.classification_rules = self._load_classification_rules()

    def determine_optimal_location(
        self,
        metadata: KnowledgeMetadata,
        content: str
    ) -> Path:
        """最適配置場所の決定"""

        # 1. 成熟度ベース分類
        maturity_level = self._assess_content_maturity(metadata, content)
        base_dir = self._get_base_directory(maturity_level)

        # 2. コンテンツタイプ分類
        content_type = self._classify_content_type(metadata, content)
        subdirectory = self._get_subdirectory(content_type)

        # 3. 技術スタック分類（該当する場合）
        tech_stack = self._identify_tech_stack(metadata, content)
        if tech_stack:
            subdirectory = subdirectory / tech_stack

        return base_dir / subdirectory

    def _assess_content_maturity(
        self,
        metadata: KnowledgeMetadata,
        content: str
    ) -> str:
        """コンテンツ成熟度の評価"""

        # 実行履歴による成熟度判定
        if metadata.success_rate and metadata.success_rate >= 90:
            return "30_wisdom"  # 高い成功率 = 成熟した知見
        elif metadata.status == "production":
            return "20_knowledge"  # 本番運用 = 体系化された知見
        elif metadata.status in ["tested", "experimental"]:
            return "10_projects"  # テスト済み = プロジェクト段階
        else:
            return "00_catalyst"  # ドラフト = 実験段階

    def _classify_content_type(
        self,
        metadata: KnowledgeMetadata,
        content: str
    ) -> str:
        """コンテンツタイプの分類"""

        # メタデータのカテゴリ優先
        if metadata.category:
            category_mapping = {
                "prompt": "Prompts",
                "code": "Code_Snippets",
                "concept": "Concepts",
                "resource": "Resources",
                "project_log": "Project_Logs"
            }
            return category_mapping.get(metadata.category, "General")

        # コンテンツ解析による分類
        if "```" in content:  # コードブロックの存在
            return "Code_Snippets"
        elif any(keyword in content.lower() for keyword in ["claude", "prompt", "ai"]):
            return "Prompts"
        elif any(keyword in content.lower() for keyword in ["concept", "theory", "principle"]):
            return "Concepts"
        else:
            return "General"
```

### 3. 高度なフロントマター強化

```python
class ObsidianFrontmatterEnhancer:
    def __init__(self):
        self.obsidian_specific_fields = {
            'aliases': 'ファイルの別名リスト',
            'cssclass': 'カスタムCSSクラス',
            'tags': 'Obsidianタグ（ネストサポート）',
            'graph': 'グラフビューでの表示設定',
            'kanban-plugin': 'Kanbanボード設定',
            'excalidraw-plugin': 'Excalidraw図表設定'
        }

    def enhance_frontmatter(
        self,
        base_metadata: KnowledgeMetadata,
        obsidian_config: dict[str, Any]
    ) -> dict[str, Any]:
        """Obsidian固有のフロントマター強化"""

        enhanced = base_metadata.model_dump()

        # 1. Obsidianタグの階層化
        enhanced['tags'] = self._create_hierarchical_tags(base_metadata.tags)

        # 2. エイリアス自動生成
        enhanced['aliases'] = self._generate_aliases(base_metadata.title)

        # 3. 関連ファイルのWiki-linkリスト
        enhanced['related_files'] = self._generate_wikilinks(base_metadata)

        # 4. 可視化設定
        enhanced['graph'] = {
            'color': self._get_node_color(base_metadata.category),
            'shape': self._get_node_shape(base_metadata.complexity)
        }

        # 5. プラグイン固有設定
        if base_metadata.category == 'project_log':
            enhanced['kanban-plugin'] = self._create_kanban_config(base_metadata)

        return enhanced

    def _create_hierarchical_tags(self, flat_tags: list[str]) -> list[str]:
        """階層タグの作成"""
        hierarchical = []

        for tag in flat_tags:
            if '/' in tag:
                hierarchical.append(tag)
            else:
                # 自動階層化ルール
                if tag in ['python', 'javascript', 'bash']:
                    hierarchical.append(f'tech/{tag}')
                elif tag in ['opus', 'sonnet', 'haiku']:
                    hierarchical.append(f'claude/{tag}')
                elif tag in ['prompt', 'code', 'concept']:
                    hierarchical.append(f'type/{tag}')
                else:
                    hierarchical.append(tag)

        return hierarchical
```

### 4. 双方向リンクシステム

```python
class BiDirectionalLinkManager:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        self.link_graph = NetworkX.DiGraph()

    def create_intelligent_links(
        self,
        current_file: Path,
        metadata: KnowledgeMetadata
    ) -> list[str]:
        """インテリジェントな双方向リンク生成"""

        links = []

        # 1. プロジェクト関連リンク
        if metadata.project:
            project_files = self._find_project_files(metadata.project)
            links.extend([f"[[{f.stem}]]" for f in project_files])

        # 2. タグベースリンク
        similar_files = self._find_similar_by_tags(metadata.tags, current_file)
        links.extend([f"[[{f.stem}]]" for f in similar_files])

        # 3. セマンティック関連リンク
        semantic_matches = self._find_semantic_matches(current_file)
        links.extend([f"[[{f.stem}]]" for f in semantic_matches])

        # 4. 改善履歴リンク（プロンプト用）
        if metadata.category == 'prompt':
            version_history = self._find_version_history(current_file)
            links.extend([f"[[{f.stem}]]" for f in version_history])

        return list(set(links))  # 重複削除

    def maintain_link_integrity(self) -> None:
        """リンク整合性の維持"""

        # 1. 破損リンクの検出と修復
        broken_links = self._find_broken_links()
        for link in broken_links:
            self._repair_or_remove_link(link)

        # 2. 双方向性の保証
        self._ensure_bidirectional_links()

        # 3. リンクグラフの更新
        self._update_link_graph()
```

## 同期システム

### 1. HybridSyncManager

```python
class HybridSyncManager:
    def __init__(self, config: CKCConfig):
        self.config = config
        self.sync_targets = self._initialize_sync_targets()
        self.conflict_resolver = ConflictResolver()

    def sync_file(self, source_file: Path) -> SyncResult:
        """ファイルの複数ターゲット同期"""

        results = []
        metadata = self.metadata_manager.extract_metadata_from_file(source_file)

        for target in self.sync_targets:
            if target.enabled:
                try:
                    # 1. ターゲット固有の変換
                    transformed_content = self._transform_for_target(
                        source_file, metadata, target
                    )

                    # 2. 最適配置場所の決定
                    target_path = self._determine_target_path(
                        metadata, target
                    )

                    # 3. コンフリクト検出と解決
                    if self._detect_conflict(target_path, transformed_content):
                        resolution = self.conflict_resolver.resolve(
                            source_file, target_path, transformed_content
                        )
                        if resolution.action == 'skip':
                            continue

                    # 4. 同期実行
                    self._execute_sync(transformed_content, target_path, target)
                    results.append(SyncResult.success(target.name))

                except Exception as e:
                    results.append(SyncResult.error(target.name, str(e)))

        return SyncResult.aggregate(results)
```

### 2. Obsidian固有の同期機能

```python
class ObsidianSyncFeatures:
    def __init__(self, vault_manager: ObsidianVaultManager):
        self.vault_manager = vault_manager

    def create_moc_files(self) -> None:
        """Map of Content (MOC) ファイルの自動生成"""

        # 1. カテゴリ別MOC
        for category in ['Prompts', 'Code_Snippets', 'Concepts']:
            self._create_category_moc(category)

        # 2. プロジェクト別MOC
        projects = self._get_all_projects()
        for project in projects:
            self._create_project_moc(project)

        # 3. タグベースMOC
        popular_tags = self._get_popular_tags()
        for tag in popular_tags:
            self._create_tag_moc(tag)

    def _create_category_moc(self, category: str) -> None:
        """カテゴリMOCの作成"""

        files = self._get_files_by_category(category)

        moc_content = f"""# {category} Map of Content

## 概要
{category}関連の知識アイテム一覧

## 高品質アイテム
"""

        # 成功率順でソート
        high_quality = sorted(
            [f for f in files if f.metadata.success_rate and f.metadata.success_rate >= 90],
            key=lambda x: x.metadata.success_rate,
            reverse=True
        )

        for file in high_quality:
            moc_content += f"- [[{file.name}]] - {file.metadata.purpose or 'No description'}\n"

        moc_content += "\n## 最近追加\n"

        recent_files = sorted(files, key=lambda x: x.metadata.created, reverse=True)[:10]
        for file in recent_files:
            moc_content += f"- [[{file.name}]] - {file.metadata.created.strftime('%Y-%m-%d')}\n"

        # MOCファイル保存
        moc_path = self.vault_manager.vault_path / f"{category}_MOC.md"
        moc_path.write_text(moc_content, encoding='utf-8')
```

### 3. 動的テンプレートシステム

```python
class ObsidianTemplateManager:
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.template_engine = Jinja2Environment()

    def create_obsidian_template(
        self,
        template_type: str,
        metadata: KnowledgeMetadata
    ) -> str:
        """Obsidian固有テンプレートの作成"""

        template_mapping = {
            'prompt': self._create_prompt_template,
            'code_snippet': self._create_code_template,
            'concept': self._create_concept_template,
            'project_log': self._create_project_template,
            'moc': self._create_moc_template
        }

        creator = template_mapping.get(template_type, self._create_generic_template)
        return creator(metadata)

    def _create_prompt_template(self, metadata: KnowledgeMetadata) -> str:
        """プロンプト専用テンプレート"""

        return f"""---
{self._format_frontmatter(metadata)}
aliases:
  - {metadata.title}
tags:
  - type/prompt
  - {'/'.join(metadata.tags)}
graph:
  color: "#ff6b6b"
  shape: "diamond"
---

# {metadata.title}

## 🎯 目的
{metadata.purpose or 'TBD'}

## 📋 プロンプト内容

```
[プロンプト本文をここに記載]
```

## 🔍 実行例

### 入力
```
[入力例]
```

### 出力
```
[期待出力例]
```

## 📊 パフォーマンス
- **成功率**: {metadata.success_rate or 'TBD'}%
- **使用モデル**: {metadata.model or 'TBD'}
- **信頼度**: {metadata.confidence or 'TBD'}

## 🔗 関連リンク
{self._generate_related_links(metadata)}

## 📝 改善履歴
- **v{metadata.version}**: 初回作成

## 🏷️ タグ
{' '.join([f'#{tag}' for tag in metadata.tags])}
"""
```

## Analytics と最適化

### 1. 使用パターン分析

```python
class VaultAnalytics:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path

    def analyze_usage_patterns(self) -> dict[str, Any]:
        """ボルト使用パターンの分析"""

        return {
            'most_accessed_files': self._get_most_accessed(),
            'category_distribution': self._analyze_category_distribution(),
            'link_density': self._calculate_link_density(),
            'knowledge_evolution': self._track_knowledge_evolution(),
            'search_patterns': self._analyze_search_patterns(),
            'creation_patterns': self._analyze_creation_patterns()
        }

    def generate_insights(self) -> list[str]:
        """知見とアクション提案"""

        insights = []
        analysis = self.analyze_usage_patterns()

        # 使用頻度の低いカテゴリ検出
        underused_categories = [
            cat for cat, count in analysis['category_distribution'].items()
            if count < 5
        ]
        if underused_categories:
            insights.append(
                f"活用度が低いカテゴリ: {', '.join(underused_categories)}"
            )

        # 孤立したファイルの検出
        isolated_files = [
            f for f, links in analysis['link_density'].items()
            if links == 0
        ]
        if isolated_files:
            insights.append(f"リンクが不足しているファイル: {len(isolated_files)}個")

        return insights
```

### 2. 自動最適化

```python
class VaultOptimizer:
    def __init__(self, vault_manager: ObsidianVaultManager):
        self.vault_manager = vault_manager

    def optimize_vault_structure(self) -> OptimizationReport:
        """ボルト構造の最適化"""

        optimizations = []

        # 1. ファイル配置の最適化
        misplaced_files = self._find_misplaced_files()
        for file in misplaced_files:
            optimal_location = self._determine_optimal_location(file)
            optimizations.append(
                MoveOptimization(file.path, optimal_location)
            )

        # 2. 重複ファイルの統合提案
        duplicates = self._find_duplicate_content()
        for duplicate_group in duplicates:
            optimizations.append(
                MergeOptimization(duplicate_group)
            )

        # 3. タグの正規化
        tag_normalizations = self._suggest_tag_normalizations()
        optimizations.extend(tag_normalizations)

        return OptimizationReport(optimizations)
```

## エラーハンドリングと復旧

### 1. 同期エラーの処理

```python
class SyncErrorHandler:
    def __init__(self):
        self.error_handlers = {
            'file_conflict': self._handle_file_conflict,
            'permission_error': self._handle_permission_error,
            'format_error': self._handle_format_error,
            'network_error': self._handle_network_error
        }

    def handle_sync_error(self, error: SyncError) -> ErrorResolution:
        """同期エラーの自動処理"""

        handler = self.error_handlers.get(error.type, self._handle_generic_error)
        return handler(error)

    def _handle_file_conflict(self, error: SyncError) -> ErrorResolution:
        """ファイル競合の処理"""

        # 1. バックアップ作成
        backup_path = self._create_backup(error.target_file)

        # 2. 差分解析
        diff = self._analyze_differences(error.source_file, error.target_file)

        # 3. 自動マージ試行
        if diff.is_auto_mergeable:
            merged_content = self._auto_merge(diff)
            return ErrorResolution.merged(merged_content)
        else:
            return ErrorResolution.manual_intervention_required(diff)
```

### 2. データ整合性チェック

```python
class DataIntegrityChecker:
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path

    def check_integrity(self) -> IntegrityReport:
        """データ整合性の包括チェック"""

        issues = []

        # 1. フロントマター整合性
        frontmatter_issues = self._check_frontmatter_integrity()
        issues.extend(frontmatter_issues)

        # 2. リンク整合性
        link_issues = self._check_link_integrity()
        issues.extend(link_issues)

        # 3. ファイル構造整合性
        structure_issues = self._check_structure_integrity()
        issues.extend(structure_issues)

        # 4. メタデータ整合性
        metadata_issues = self._check_metadata_consistency()
        issues.extend(metadata_issues)

        return IntegrityReport(issues)
```

この包括的な分類・統合システムにより、CKC は知識の自然な進化を支援し、開発者の知見を持続可能な知識資産として蓄積します。
