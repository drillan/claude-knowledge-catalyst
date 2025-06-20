---
category: concept
complexity: advanced
created: '2025-06-19'
project: claude-knowledge-catalyst
purpose: Auto-generated metadata for metadata_system
quality: high
status: draft
subcategory: Development_Patterns
tags:
- architecture
- design
- system
- structure
title: Metadata System
updated: '2025-06-19'
version: '1.0'
---

# メタデータシステム詳細仕様

## 概要

CKC のメタデータシステムは、知識アイテムの文脈化、検索性向上、および自動分類を実現するコア機能です。Pydantic モデルベースの堅牢な型安全性と、インテリジェントな自動抽出機能を提供します。

## KnowledgeMetadata モデル

### 基本構造

```python
class KnowledgeMetadata(BaseModel):
    # 基本情報
    title: str                    # タイトル（必須）
    created: datetime            # 作成日時
    updated: datetime            # 更新日時
    version: str                 # バージョン（例: "1.0", "2.1"）
    
    # コンテンツ分類
    category: str | None         # 主カテゴリ
    tags: list[str]             # タグリスト
    
    # Claude特有のメタデータ
    model: str | None           # 使用モデル（opus, sonnet, haiku）
    confidence: str | None      # 信頼度レベル
    success_rate: int | None    # 成功率（0-100）
    
    # プロジェクト文脈
    project: str | None         # 主プロジェクト名
    purpose: str | None         # 目的・用途
    related_projects: list[str] # 関連プロジェクト
    
    # ステータス・品質管理
    status: str                 # ステータス（draft, tested, production, deprecated）
    quality: str | None         # 品質評価（high, medium, low, experimental）
    complexity: str | None      # 複雑度レベル
    
    # 管理情報
    author: str | None          # 作成者
    source: str | None          # ソースファイルパス
    checksum: str | None        # コンテンツチェックサム
```

### フィールド詳細

#### 1. 基本情報フィールド

**title**: コンテンツのタイトル
- 自動抽出順序: frontmatter > H1見出し > 最初の非空行（50文字まで）
- バックアップ: "Untitled"

**created/updated**: タイムスタンプ管理
- ISO 8601 形式で保存
- 自動更新メカニズム
- タイムゾーン対応

**version**: セマンティックバージョニング
- デフォルト: "1.0"
- 手動更新またはAI判定による自動インクリメント

#### 2. 分類システム

**category**: 主要分類
- prompt: プロンプト関連
- code: コードスニペット
- concept: 概念・理論
- resource: リソース・参考資料
- project_log: プロジェクトログ

**tags**: 多次元タグシステム
```yaml
tag_dimensions:
  category: [prompt, code, concept, resource, project_log]
  tech: [python, javascript, react, nodejs, docker, git]
  claude: [opus, sonnet, haiku]
  status: [draft, tested, production, deprecated]
  quality: [high, medium, low, experimental]
```

#### 3. Claude 固有メタデータ

**model**: 使用したClaudeモデル
- 会話履歴から自動検出
- APIレスポンスヘッダーからの抽出

**confidence**: AI応答の信頼度
- high: 高度に確実な回答
- medium: 一般的な確実性
- low: 不確実性を含む
- experimental: 実験的・推測的

**success_rate**: プロンプトの成功率
- 数値: 0-100（パーセンテージ）
- 複数実行結果の統計
- 時系列での成功率推移追跡

#### 4. プロジェクト文脈

**project**: 主プロジェクト識別
- 自動検出ロジック:
  1. `.claude/project.yaml` の `project_name`
  2. Git リポジトリ名
  3. プロジェクトルートディレクトリ名

**purpose**: 知識アイテムの目的
- 自由記述フィールド
- AI による自動推論機能

**related_projects**: 関連プロジェクトリスト
- クロスプロジェクト知識リンク
- 知識再利用性の向上

## MetadataManager クラス

### 初期化と設定

```python
class MetadataManager:
    def __init__(self, tag_config: dict[str, list[str]] | None = None):
        self.tag_config = tag_config or default_tag_config
```

### 主要メソッド

#### 1. メタデータ抽出
```python
def extract_metadata_from_file(self, file_path: Path) -> KnowledgeMetadata:
```
- frontmatter パースing（python-frontmatter）
- コンテンツ解析
- 自動タグ推論
- プロジェクト文脈検出

#### 2. ファイル更新
```python
def update_file_metadata(self, file_path: Path, metadata: KnowledgeMetadata) -> None:
```
- frontmatter の安全な更新
- 既存コンテンツの保持
- バックアップ機能（オプション）

#### 3. 自動推論機能
```python
def _infer_tags_from_content(self, content: str) -> set[str]:
```

**技術スタック検出**:
```python
tech_keywords = {
    "python": ["python", "pip", "conda", "pytest", "django", "flask", "asyncio"],
    "javascript": ["javascript", "node.js", "npm install", "react", "vue.js"],
    "react": ["react", "jsx", "component", "useState", "useEffect"],
    "docker": ["docker", "dockerfile", "container", "image"],
    "git": ["git", "commit", "branch", "merge", "pull request"],
}
```

**Claudeモデル検出**:
- "opus", "sonnet", "haiku" の言及
- タグ形式: `claude/opus`, `claude/sonnet`

**コンテンツタイプ判定**:
- コードブロック（```）の存在 → `code` タグ
- AI/LLM関連キーワード → `prompt` タグ
- 概念説明パターン → `concept` タグ

### プロジェクト自動検出

#### 検出優先順位
1. **.claude/project.yaml**: 明示的プロジェクト設定
2. **Git情報**: リポジトリ名の取得
3. **プロジェクトファイル検索**: package.json, pyproject.toml等
4. **ディレクトリ構造**: パス解析によるプロジェクト推定

#### 実装詳細
```python
def _auto_detect_project(self, file_path: Path) -> str | None:
    # 1. .claude/project.yaml チェック
    claude_dir = self._find_claude_directory(file_path)
    if claude_dir and (claude_dir / "project.yaml").exists():
        return self._load_project_config(claude_dir / "project.yaml")
    
    # 2. Git リポジトリ名
    git_project = self._detect_project_from_git(file_path)
    if git_project:
        return git_project
    
    # 3. ファイルパス解析
    return self._detect_project_from_path(file_path)
```

## タグシステム

### 階層型タグ構造

```yaml
tags:
  category_tags:
    - prompt
    - code
    - concept
    - resource
    - project_log
  
  tech_tags:
    - python
    - javascript
    - react
    - nodejs
    - docker
    - git
  
  claude_tags:
    - opus
    - sonnet
    - haiku
  
  status_tags:
    - draft
    - tested
    - production
    - deprecated
  
  quality_tags:
    - high
    - medium
    - low
    - experimental
```

### 自動タグ推論

#### コンテンツ解析ベース
- **キーワードマッチング**: 技術固有の用語検出
- **パターン認識**: コードブロック、リスト構造等
- **文体解析**: 説明文、手順書、ログ等の判別

#### 使用例
```python
# プロンプト関連コンテンツ
content = "Claude, please analyze this code and suggest improvements..."
inferred_tags = metadata_manager._infer_tags_from_content(content)
# → {'prompt', 'claude', 'code'}

# Python コードスニペット
content = "```python\ndef calculate_metrics():\n    return statistics\n```"
inferred_tags = metadata_manager._infer_tags_from_content(content)
# → {'code', 'python'}
```

### タグ検証と正規化

```python
def validate_tags(self, tags: list[str]) -> list[str]:
    valid_tags = []
    for tag in tags:
        tag = tag.lower().strip()
        if tag and tag.replace("_", "").replace("-", "").isalnum():
            valid_tags.append(tag)
    return valid_tags
```

## フロントマター管理

### 標準フォーマット

```yaml
---
title: "プロンプト最適化テクニック"
created: 2024-06-18T10:30:00+09:00
updated: 2024-06-18T15:45:00+09:00
version: "1.2"
category: prompt
tags:
  - prompt
  - claude/sonnet
  - optimization
  - best_practices
model: sonnet
confidence: high
success_rate: 95
project: claude-knowledge-catalyst
purpose: プロンプトエンジニアリングの効率化
related_projects:
  - ai-automation-tools
  - prompt-library
status: production
quality: high
complexity: medium
author: system
---
```

### 更新メカニズム

1. **既存メタデータ保持**: 手動編集された値の尊重
2. **自動補完**: 未設定フィールドの推論値追加
3. **タイムスタンプ管理**: updated の自動更新
4. **バージョン管理**: 内容変更時の自動インクリメント

## パフォーマンス最適化

### キャッシュ戦略
- **メタデータキャッシュ**: 頻繁にアクセスされるファイルのメタデータ
- **チェックサム比較**: 内容変更の効率的検出
- **増分更新**: 変更されたファイルのみ処理

### メモリ効率
- **ストリーミング処理**: 大容量ファイルの分割読み込み
- **遅延評価**: 必要時のみメタデータ抽出実行
- **ガベージコレクション**: 不要なオブジェクトの適切な解放

## エラーハンドリング

### 例外処理パターン
```python
try:
    metadata = metadata_manager.extract_metadata_from_file(file_path)
except FileNotFoundError:
    # ファイルが存在しない場合のフォールバック
    metadata = metadata_manager.create_default_metadata(file_path.name)
except (UnicodeDecodeError, yaml.YAMLError):
    # ファイル形式エラーの場合の復旧処理
    metadata = metadata_manager.extract_partial_metadata(file_path)
```

### 堅牢性の確保
- **グレースフルデグラデーション**: 部分的なメタデータでも処理継続
- **自動修復**: 破損したfrontmatterの復元試行
- **警告システム**: 品質問題の早期発見と通知