# Configuration Reference

CKCの設定システムの完全なリファレンスです。

## 設定ファイル構造

CKCは `ckc_config.yaml` ファイルで設定を管理します。

### 基本構造

```yaml
version: "2.0"
project_name: "My Project"
project_root: "."

# 同期設定
auto_sync: true
git_integration: true
auto_commit: false

# 同期先設定
sync_targets:
  - name: "main-vault"
    type: "obsidian"
    path: "/path/to/vault"
    enabled: true

# タグ設定
tags:
  category_tags: ["prompt", "code", "concept"]
  tech_tags: ["python", "javascript"]

# ファイル監視設定
watch:
  watch_paths: [".claude"]
  file_patterns: ["*.md", "*.txt"]
  include_claude_md: false  # CLAUDE.md同期設定

# テンプレート設定
template_path: "templates"

# ハイブリッド構造設定
hybrid_structure:
  enabled: true
```

## 設定セクション詳細

### プロジェクト基本設定

| フィールド | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `version` | string | `"2.0"` | 設定ファイルのバージョン |
| `project_name` | string | `""` | プロジェクト名 |
| `project_root` | Path | `"."` | プロジェクトルートディレクトリ |

### 同期設定

| フィールド | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `auto_sync` | boolean | `true` | 自動同期の有効/無効 |
| `git_integration` | boolean | `true` | Git統合の有効/無効 |
| `auto_commit` | boolean | `false` | 自動コミットの有効/無効 |

### 同期先設定 (sync_targets)

```yaml
sync_targets:
  - name: "vault-name"          # 同期先名（必須）
    type: "obsidian"            # 同期先タイプ（必須）
    path: "/path/to/vault"      # 同期先パス（必須）
    enabled: true               # 有効/無効（任意、デフォルト: true）
    metadata:                   # 追加メタデータ（任意）
      description: "説明文"
```

#### 対応同期先タイプ
- `obsidian` - Obsidian vault
- `notion` - Notion データベース（実装予定）
- `file` - ファイルシステム

### タグ設定

```yaml
tags:
  category_tags:    # カテゴリタグ
    - "prompt"
    - "code"
    - "concept"
    - "resource"
    - "project_log"
    
  tech_tags:        # 技術タグ
    - "python"
    - "javascript"
    - "typescript"
    - "react"
    
  claude_tags:      # Claudeモデルタグ
    - "opus"
    - "sonnet"
    - "haiku"
    
  status_tags:      # ステータスタグ
    - "draft"
    - "tested"
    - "production"
    - "deprecated"
    
  quality_tags:     # 品質タグ
    - "high"
    - "medium"
    - "low"
    - "experimental"
```

### ファイル監視設定 (watch)

```yaml
watch:
  # 監視パス
  watch_paths:
    - ".claude"
    - "docs/claude"
    
  # ファイルパターン
  file_patterns:
    - "*.md"
    - "*.txt"
    - "*.json"
    
  # 除外パターン
  ignore_patterns:
    - ".git"
    - "__pycache__"
    - "*.pyc"
    - ".DS_Store"
    - "node_modules"
    
  # デバウンス設定
  debounce_seconds: 1.0
  
  # CLAUDE.md同期設定
  include_claude_md: false              # CLAUDE.md同期の有効/無効
  claude_md_patterns:                   # 対象ファイルパターン
    - "CLAUDE.md"
    - ".claude/CLAUDE.md"
  claude_md_sections_exclude:           # 除外セクション
    - "# secrets"
    - "# private"
    - "# confidential"
```

#### CLAUDE.md同期設定詳細

| フィールド | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `include_claude_md` | boolean | `false` | CLAUDE.mdファイルの同期有効/無効 |
| `claude_md_patterns` | list[string] | `["CLAUDE.md", ".claude/CLAUDE.md"]` | 同期対象ファイルパターン |
| `claude_md_sections_exclude` | list[string] | `[]` | 除外するセクションヘッダーのリスト |

**セキュリティ重要事項**: 
- `include_claude_md` はデフォルトで `false` です
- 機密情報を含む場合は必ず `claude_md_sections_exclude` を設定してください
- セクション除外は大文字小文字を区別しません

### テンプレート設定

| フィールド | 型 | デフォルト | 説明 |
|-----------|-----|-----------|------|
| `template_path` | Path | `"templates"` | テンプレートファイルディレクトリ |

### ハイブリッド構造設定 (hybrid_structure)

```yaml
hybrid_structure:
  enabled: true                        # ハイブリッド構造の有効/無効
  
  # 従来のPARA method設定
  para_method:
    enabled: true
    areas_path: "02-Areas"
    projects_path: "01-Projects"
    resources_path: "03-Resources"
    archive_path: "04-Archive"
    
  # モダンなPKM設定  
  modern_pkm:
    enabled: true
    concepts_path: "concepts"
    projects_path: "projects"
    daily_notes_path: "daily"
    templates_path: "templates"
```

## 設定の読み込みと検証

### Python API

```python
from claude_knowledge_catalyst.core.config import CKCConfig

# 設定ファイルからの読み込み
config = CKCConfig.load_from_file("ckc_config.yaml")

# デフォルト設定の使用
config = CKCConfig()

# 設定の保存
config.save_to_file("ckc_config.yaml")

# 有効な同期先の取得
enabled_targets = config.get_enabled_sync_targets()

# 同期先の追加
from claude_knowledge_catalyst.core.config import SyncTarget
new_target = SyncTarget(
    name="backup-vault",
    type="obsidian", 
    path="/path/to/backup"
)
config.add_sync_target(new_target)
```

### CLI コマンド

```bash
# 設定表示
ckc config show

# 設定検証
ckc config validate

# 設定初期化
ckc config init

# CLAUDE.md同期設定の確認
ckc config show --section watch
```

## 設定例

### 基本的な個人利用

```yaml
version: "2.0"
project_name: "Personal Development"
auto_sync: true

sync_targets:
  - name: "personal-vault"
    type: "obsidian"
    path: "~/Documents/Obsidian/Personal"
    enabled: true

watch:
  include_claude_md: true
  claude_md_sections_exclude:
    - "# private"
    - "# personal"
```

### チーム開発環境

```yaml
version: "2.0"
project_name: "Team Project"
auto_sync: true
git_integration: true

sync_targets:
  - name: "team-vault"
    type: "obsidian"
    path: "/shared/obsidian/team-vault"
    enabled: true

watch:
  include_claude_md: true
  claude_md_patterns:
    - "CLAUDE.md"
    - "docs/CLAUDE.md"
  claude_md_sections_exclude:
    - "# secrets"
    - "# api-keys"
    - "# confidential"
    - "# personal"

tags:
  tech_tags:
    - "python"
    - "fastapi"
    - "postgresql"
    - "docker"
```

### 高セキュリティ環境

```yaml
version: "2.0"
project_name: "Secure Project"
auto_sync: false  # 手動同期のみ

sync_targets:
  - name: "secure-vault"
    type: "obsidian"
    path: "/secure/vault"
    enabled: true

watch:
  include_claude_md: false  # CLAUDE.md同期を無効化
  
# または、厳格な除外設定
watch:
  include_claude_md: true
  claude_md_sections_exclude:
    - "# secrets"
    - "# api-keys"
    - "# passwords"
    - "# confidential"
    - "# internal"
    - "# classified"
    - "# private"
    - "# credentials"
```

## バリデーション

設定ファイルはPydanticモデルによって自動的にバリデーションされます：

- **必須フィールド**: `name`, `type`, `path` (sync_targets)
- **パス検証**: 存在しないパスは警告表示
- **タイプ検証**: サポートされていない同期先タイプはエラー
- **循環参照**: 設定の循環参照をチェック

## 環境変数

一部の設定は環境変数で上書き可能です：

```bash
export CKC_PROJECT_ROOT="/custom/project/path"
export CKC_AUTO_SYNC="false" 
export CKC_CLAUDE_MD_ENABLED="true"
```

対応する環境変数：
- `CKC_PROJECT_ROOT` → `project_root`
- `CKC_AUTO_SYNC` → `auto_sync`
- `CKC_CLAUDE_MD_ENABLED` → `watch.include_claude_md`

## マイグレーション

古い設定ファイルは自動的に新しい形式に移行されます：

```bash
# 設定マイグレーション
ckc config migrate

# マイグレーション確認
ckc config migrate --dry-run
```

設定の互換性については[Migration Guide](../developer-guide/migration.md)を参照してください。