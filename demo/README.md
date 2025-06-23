# Claude Knowledge Catalyst v0.10.1 Demo Scripts

このディレクトリには、Claude Knowledge Catalyst (CKC) のYAKE統合および純粋タグ中心システムを実際に体験するためのデモスクリプトが含まれています。

> **🚀 v0.10.1 Production-Ready Release**: 高度なキーワード抽出システムが統合され、396の全テストが通過する本番品質の安定性を実現しました。多言語対応（7言語）とAI強化分類が利用可能です。

## 🎯 純粋タグ中心システム体験

### 1. メインデモ (`demo.sh`) ⭐ 推奨
**所要時間:** 4-5分  
**内容:** 純粋タグ中心知識管理システムの革新的アプローチを体験

```bash
./demo/demo.sh
```

**体験できる革新的機能:**
- ✅ 認知負荷ゼロの分類システム
- ✅ 多層スマートタグアーキテクチャ
- ✅ 🆕 YAKE統合: 多言語キーワード抽出システム (v0.10.0)
- ✅ 🆕 ハイブリッド分類: パターンマッチング + AI強化 (v0.10.0)
- ✅ 自動コンテンツ分析・提案システム
- ✅ 状態ベース組織化（ワークフロー駆動）
- ✅ 動的クロス次元知識発見
- ✅ Obsidianクエリ生成機能

**生成されるデモコンテンツ:**
- FastAPIプロンプト（複数技術スタック統合）
- Python デバッグ技術（実践的トラブルシューティング）
- React アーキテクチャ概念（高度パターン）
- 🆕 多言語コンテンツ（YAKE統合デモ用、English + Japanese）

### 🆕 2. Obsidian移行デモ (`tag_centered_demo.sh`) ⭐ Obsidian強化体験
**所要時間:** 8-10分  
**内容:** 既存ObsidianボルトをCKCの7次元タグシステムで革命的に強化

```bash
./demo/tag_centered_demo.sh
```

**Obsidian強化の体験:**
- 📊 基本Obsidianタグ → 7次元タグアーキテクチャへの変換
- 🏷️ 単純メタデータ → 多層インテリジェントシステムへの強化
- 🤖 自動メタデータ推論とスマート分類の追加
- 📋 状態ベースワークフロー（draft→tested→production）の統合
- 🔍 高度Obsidianクエリ生成による発見性向上
- 📈 スケーラブルな知識ベース成長の実現

**移行プロセスデモ:**
1. リアルなObsidianボルト作成（基本frontmatter付き）
2. CKC移行システムによる自動強化実行
3. 7次元タグメタデータの自動適用
4. 強化されたテンプレートとクエリの生成
5. 移行前後の詳細比較とメリット分析

### 3. マルチチーム協業デモ (`multi_project_demo.sh`) ⭐ チーム体験
**所要時間:** 7-8分  
**内容:** 複数チームでの純粋タグ中心知識共有システム

```bash
./demo/multi_project_demo.sh
```

**マルチチーム協業機能:**
- 👥 純粋タグベースチーム識別（ディレクトリサイロ廃止）
- 🔍 多次元タグによるクロスチーム知識発見
- 📋 状態ベースコンテンツライフサイクル（draft→tested→production）
- 🏷️ チーム固有メタデータと所有権追跡
- 🔗 技術・ドメインベースコンテンツ組織化
- 🏛️ インテリジェントコンテンツ配置による統一ボルト

**生成されるチームコンテンツ:**
- **Frontend Team**: React最適化パターン、デザインシステム生成プロンプト
- **Backend Team**: 非同期Python APIアーキテクチャ、ML本番パイプライン概念

## 📊 純粋タグ中心アーキテクチャ

### 革命的ボルト構造（状態ベース、コンテンツベースではない）
```
vault/
├── _system/          # テンプレートと設定
├── _attachments/     # メディアファイル
├── inbox/            # 未処理コンテンツ（status: draft）
├── active/           # 作業中コンテンツ（status: tested）
├── archive/          # 非推奨コンテンツ
└── knowledge/        # 成熟コンテンツ（90%のファイル、status: production）
```

### 多層インテリジェントタグシステム
```yaml
# 純粋タグアーキテクチャ
type: [prompt, code, concept, resource]           # コンテンツ性質
tech: [python, react, fastapi, typescript, ...]   # 技術スタック
domain: [web-dev, backend, frontend, ml, ...]     # アプリケーション領域
team: [backend, frontend, fullstack, ml-research] # チーム所有権
status: [draft, tested, production, deprecated]   # ライフサイクル状態
complexity: [beginner, intermediate, advanced]    # スキルレベル
confidence: [low, medium, high]                   # コンテンツ信頼性
claude_model: [opus, sonnet, haiku, sonnet-4]     # Claude モデル
claude_feature: [code-generation, analysis, ...]  # Claude 機能
```

## 🚀 高度機能デモ内容

### 自動コンテンツ分類
- **パターンマッチング**でのコンテンツ自動分析
- **🆕 YAKE統合**による教師なしキーワード抽出 (v0.10.1)
- **🆕 ハイブリッド分析**: 従来手法 + AI強化 (v0.10.1)
- **多言語対応**: 7言語での技術用語検出 (English, Japanese, etc.)
- **証拠ベース推論**による分類決定
- **信頼度スコア**付き提案システム
- **自然言語検索**クエリ対応

### 動的知識発見例
```bash
# 技術横断検索
ckc search --tech python --status production

# チーム特化コンテンツ
ckc search --team frontend --complexity advanced

# クロスドメインパターン
ckc search --domain api-design --confidence high
```

### Obsidian動的クエリ生成
```obsidian
# 高品質API プロンプト
TABLE success_rate, tech, updated
FROM #prompt AND #api
WHERE success_rate > 80
SORT success_rate DESC

# Python自動化ツール
LIST FROM #code AND #python
WHERE contains(string(tags), "automation")
```

## 🧹 クリーンアップ

### デモ環境クリーンアップ
```bash
# すべてのデモアーティファクトを自動削除
./demo/cleanup.sh
```

**cleanup.shが削除する内容：**
- `my_project/`, `my_vault/` - メインデモアーティファクト
- `obsidian_vault/`, `enhanced_ckc_vault/`, `ckc_project/` - 移行デモアーティファクト  
- `frontend_team/`, `backend_team/`, `shared_vault/` - マルチチームデモアーティファクト
- 一時ファイル（*.log, *.tmp, .DS_Store）

**保持されるファイル：**
- デモスクリプト（demo.sh, tag_centered_demo.sh, multi_project_demo.sh）
- ドキュメント（README.md, CLAUDE.md）
- cleanup.sh

## 🔍 重要な違い：従来 vs 純粋タグ中心

### 📊 BEFORE（従来のカテゴリベース）
```
├── prompts/          # 認知負荷：「これはプロンプト？テンプレート？」
├── code/             # 硬直境界：「コードスニペット？ツール？」
├── concepts/         # 曖昧性：「概念？ベストプラクティス？」
└── misc/             # キャッチオール
```

**問題:**
- 決定疲労：どのカテゴリ？
- 硬直境界：コンテンツが適切に適合しない
- 発見性の欠如：単次元検索
- メンテナンス負荷：カテゴリ間でのファイル移動

### 📊 AFTER（純粋タグ中心状態ベース）
```
├── _system/          # システムファイルとテンプレート
├── inbox/            # 未処理アイテム（ワークフロー状態）
├── active/           # 現在作業中（活動状態）
├── archive/          # 非推奨・古い（ライフサイクル状態）
└── knowledge/        # 成熟コンテンツ（90%のファイル）
    └── 動的発見のための強化多層タグ
```

**利点:**
- 🧠 認知負荷削減：「どのカテゴリ？」決定なし
- 🔍 多次元発見：技術、ドメイン、チーム横断検索
- 📈 スケーラブル組織化：タグが知識と共に進化
- ⚡ 柔軟なワークフロー：コンテンツベースではなく状態ベース組織化
- 🔗 豊富な関係性：マルチプロジェクト、マルチドメイン接続

## 💡 認知革命の体験

**純粋タグ中心システムで体験できること:**
- カテゴリ決定なしの知識管理
- 境界のない発見可能な知識
- アルゴリズムによる自動スマートタグ付け
- 状態駆動ワークフロー組織化
- 動的クロス次元知識発見

---

**Welcome to the cognitive revolution!**  
もう「どのカテゴリ？」と悩む必要はありません - 純粋で発見可能な知識管理を体験してください。