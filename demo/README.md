# Claude Knowledge Catalyst Demo Scripts

このディレクトリには、Claude Knowledge Catalyst (CKC) の機能を実際に試すためのデモスクリプトが含まれています。

## 🎯 簡単なデモ実行

### 統合デモマネージャー (`run_demo.sh`) ⭐ 最も簡単
**すべてのデモを一つのコマンドで管理**

```bash
# ユーザー体験デモ（推奨）
./demo/run_demo.sh user

# 他のオプション
./demo/run_demo.sh quick     # 開発者向けクイックデモ
./demo/run_demo.sh full      # マルチプロジェクトデモ
./demo/run_demo.sh status    # 現在の状態確認
./demo/run_demo.sh cleanup   # クリーンアップ
./demo/run_demo.sh help      # ヘルプ表示
```

## 🚀 個別デモスクリプト

### 1. メインデモ (`demo.sh`) ⭐ 推奨
**所要時間:** 3-4分  
**内容:** 実際のユーザーワークフローを体験

```bash
./demo/demo.sh
```

**特徴:**
- ✅ 実際のユーザーコマンドを表示・実行
- ✅ ステップバイステップの説明
- ✅ 現実的な使用シナリオ

## 🔧 開発者向けデモ

### 2. クイックデモ (`quick_demo.sh`)
**所要時間:** 2-3分  
**内容:** 内部実装を使用した基本機能デモ

```bash
./demo/quick_demo.sh
```

**何をテストするか:**
- 適応型システム基盤の初期化
- Obsidianボルト同期の設定
- 様々なコンテンツタイプの分類（prompt、code、concept）
- 自動メタデータ処理

**生成される出力:**
- `demo_project/` - CKCプロジェクト設定
- `demo_vault/` - 生成されたObsidianボルト

### 2. フルデモ (`full_demo.sh`)
**所要時間:** 5-7分  
**内容:** マルチプロジェクト環境での本格的な機能テスト

```bash
./demo/full_demo.sh
```

**何をテストするか:**
- 複数プロジェクトでのボルト共有
- プロジェクト固有コンテンツの分離
- 汎用知識の共有メカニズム
- 高度な分類・整理機能

**生成される出力:**
- `project_A/` - プロジェクトA設定とコンテンツ
- `project_B/` - プロジェクトB設定とコンテンツ  
- `vault/` - 共有Obsidianボルト

## 📁 期待される結果

### ボルト構造例
```
vault/
├── 00_Catalyst_Lab/           # 実験的コンテンツ
├── 10_Projects/               # プロジェクト固有コンテンツ
│   ├── project_A/
│   └── project_B/
├── 20_Knowledge_Base/         # 共有知識ベース
│   ├── Prompts/              # プロンプトテンプレート
│   ├── Code_Snippets/        # コードスニペット
│   │   └── Python/
│   └── Concepts/             # 概念・理論
├── 30_Wisdom_Archive/         # 高品質知識アーカイブ
└── _templates/               # システムテンプレート
```

## 🧹 クリーンアップ

### 自動クリーンアップ（推奨）
```bash
# 確認付きクリーンアップ
./demo/run_demo.sh cleanup

# または
./demo/cleanup.sh

# 確認なしでクリーンアップ
./demo/run_demo.sh cleanup --force
```

### 手動クリーンアップ
```bash
rm -rf demo/demo_project demo/demo_vault demo/project_A demo/project_B demo/vault demo/my_project demo/my_obsidian_vault demo/user_project demo/user_vault
```

### 現在の状態確認
```bash
./demo/run_demo.sh status
```

## 🔧 トラブルシューティング

### 一般的な問題

1. **"command not found" エラー**
   ```bash
   # 実行権限を確認
   chmod +x demo/*.sh
   ```

2. **"uv not found" エラー**
   ```bash
   # 仮想環境の確認
   ls .venv/bin/python
   ```

3. **パスエラー**
   ```bash
   # プロジェクトルートから実行
   cd /path/to/claude-knowledge-catalyst
   ./demo/quick_demo.sh
   ```

## 📋 デモ内容詳細

### サンプルコンテンツ

#### プロンプト例
- コードレビューアシスタント
- ドキュメント作成支援
- 技術説明プロンプト

#### コードスニペット例  
- Python ユーティリティ関数
- ファイル処理関数
- データ検証関数

#### 概念ノート例
- 適応型システム基盤の説明
- AI/ML研究知見
- 知識管理理論

### 期待される学習効果

1. **CKCの基本概念理解**
   - 適応型システム基盤のメリット
   - 自動分類の仕組み
   - メタデータの活用方法

2. **実践的な使用方法**
   - プロジェクト初期化の手順
   - コンテンツ作成のベストプラクティス
   - ボルト管理の効率的な方法

3. **高度な機能の体験**
   - マルチプロジェクト管理
   - 知識の再利用と共有
   - 自動化された整理システム

---

**注意:** デモスクリプトは開発環境での使用を想定しています。本番環境での実行前には内容を十分に確認してください。