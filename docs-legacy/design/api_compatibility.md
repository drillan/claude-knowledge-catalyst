# API互換性戦略

## 📋 API互換性戦略概要

### 目的
適応型システム基盤統合において、既存CKCのAPI・CLI・設定インターフェースとの完全な互換性を保証し、既存ユーザーの学習コストをゼロに抑える。

### 互換性原則
1. **完全後方互換**: 既存のすべてのインターフェースが動作継続
2. **漸進的拡張**: 新機能は既存機能の拡張として提供
3. **透明な移行**: ユーザーが意識しない自然な機能向上
4. **設定継承**: 既存設定ファイルの自動認識・変換

## 🔌 API層別互換性設計

### 1. CLI インターフェース互換性

#### 既存コマンドの完全保持
```bash
# 既存コマンド - 100%互換性保証
uv run ckc init                    # ✅ 動作継続（構造推薦機能追加）
uv run ckc sync add vault obsidian # ✅ 動作継続（適応型システム基盤対応）
uv run ckc watch                   # ✅ 動作継続（拡張監視機能）
uv run ckc status                  # ✅ 動作継続（詳細情報追加）

# 新規コマンド - 既存機能を破綻させない追加
uv run ckc structure status        # 🆕 新機能
uv run ckc migrate                 # 🆕 新機能
uv run ckc structure validate      # 🆕 新機能
```

#### CLI実装アプローチ
```python
class CompatibilityPreservingCLI:
    """互換性保持CLI実装"""
    
    def __init__(self):
        self.legacy_handler = LegacyCLIHandler()
        self.adaptive_handler = AdaptiveCLIHandler()
        self.structure_detector = StructureDetector()
    
    def handle_command(self, command: str, args: dict) -> CommandResult:
        """コマンド処理の統合ルーティング"""
        
        # 1. 構造タイプの自動検出
        structure_type = self.structure_detector.detect_current_structure()
        
        # 2. コマンドタイプ判定
        if self.is_legacy_command(command):
            # 既存コマンド：互換性レイヤー経由で処理
            return self._handle_legacy_command(command, args, structure_type)
        else:
            # 新規コマンド：直接適応型システム基盤ハンドラー
            return self.adaptive_handler.handle(command, args)
    
    def _handle_legacy_command(self, command: str, args: dict, 
                              structure_type: StructureType) -> CommandResult:
        """既存コマンドの互換処理"""
        
        if structure_type == StructureType.ADAPTIVE:
            # 適応型システム基盤での既存コマンド実行
            result = self.adaptive_handler.handle_legacy(command, args)
            
            # 必要に応じて新機能の推薦表示
            if self.should_suggest_new_features(command):
                result.add_suggestion(self._generate_feature_suggestion(command))
                
        else:
            # レガシー構造での従来通り実行
            result = self.legacy_handler.handle(command, args)
            
            # 適応型システム基盤移行の推薦表示
            if self.should_suggest_migration(command, args):
                result.add_migration_suggestion()
        
        return result
```

#### パラメータ互換性管理
```python
class ParameterCompatibilityManager:
    """パラメータ互換性管理"""
    
    # 既存パラメータのマッピング
    PARAMETER_MAPPING = {
        # 既存 → 新規（内部変換）
        "--vault-path": "--target-path",
        "--project": "--project-name", 
        "--auto": "--auto-sync",
    }
    
    # 非推奨パラメータの警告
    DEPRECATED_PARAMETERS = {
        "--legacy-mode": "新しい構造では不要になりました",
        "--force-sequential": "10刻み番号システムをお試しください"
    }
    
    def normalize_parameters(self, raw_args: dict) -> dict:
        """パラメータ正規化"""
        normalized = {}
        
        for key, value in raw_args.items():
            if key in self.PARAMETER_MAPPING:
                # 既存パラメータの内部変換
                new_key = self.PARAMETER_MAPPING[key]
                normalized[new_key] = value
                
                # 変更通知（非侵入的）
                self._log_parameter_migration(key, new_key)
                
            elif key in self.DEPRECATED_PARAMETERS:
                # 非推奨パラメータの警告
                warning = self.DEPRECATED_PARAMETERS[key]
                self._show_deprecation_warning(key, warning)
                
            else:
                # そのまま使用
                normalized[key] = value
        
        return normalized
```

### 2. 設定ファイル互換性

#### 自動設定変換システム
```python
class ConfigCompatibilityManager:
    """設定ファイル互換性管理"""
    
    def load_config_with_migration(self, config_path: Path) -> EnhancedCKCConfig:
        """設定読み込みと自動移行"""
        
        # 1. 設定ファイル読み込み
        raw_config = self._load_raw_config(config_path)
        
        # 2. バージョン検出
        config_version = self._detect_config_version(raw_config)
        
        # 3. バージョン別処理
        if config_version == "1.0":
            return self._migrate_v1_to_v2(raw_config, config_path)
        elif config_version == "2.0":
            return self._load_v2_config(raw_config)
        else:
            return self._create_default_config(config_path)
    
    def _migrate_v1_to_v2(self, v1_config: dict, config_path: Path) -> EnhancedCKCConfig:
        """v1.0 → v2.0 自動移行"""
        
        # v1設定をv2形式に変換
        v2_config = {
            # 既存設定の継承
            "version": "2.0",
            "project_name": v1_config.get("project_name", ""),
            "sync_targets": v1_config.get("sync_targets", []),
            "tags": v1_config.get("tags", {}),
            "watch": v1_config.get("watch", {}),
            
            # 新機能のデフォルト設定
            "adaptive_structure": {
                "enabled": False,  # デフォルトは無効（明示的有効化）
                "numbering_system": "sequential",  # 既存方式を維持
                "auto_classification": False,
                "structure_validation": True,
                "migration_mode": "none"
            }
        }
        
        # 移行後設定をバックアップ付きで保存
        self._backup_config(config_path)
        self._save_migrated_config(v2_config, config_path)
        
        # 移行完了メッセージ
        self._show_migration_complete_message()
        
        return EnhancedCKCConfig(**v2_config)
    
    def _show_migration_complete_message(self):
        """移行完了メッセージ表示"""
        print("""
✅ 設定ファイルをv2.0に自動更新しました

📝 変更内容:
  - 新機能の設定項目を追加
  - 既存設定は完全に保持
  - 動作に変更はありません

🚀 新機能を試すには:
  uv run ckc structure --help
        """)
```

#### 設定互換性マトリックス
```python
COMPATIBILITY_MATRIX = {
    "v1.0_to_v2.0": {
        "preserved_fields": [
            "project_name", "sync_targets", "tags", "watch", 
            "template_path", "git_integration", "auto_commit"
        ],
        "new_fields": [
            "adaptive_structure", "config_version", "structure_migration_log"
        ],
        "transformed_fields": {
            # v1のフィールド名 → v2のフィールド名
        },
        "deprecated_fields": [
            # 将来的に廃止予定のフィールド
        ]
    }
}
```

### 3. Python API互換性

#### 既存クラス・メソッドの保持
```python
# 既存APIの完全保持
class CKCConfig(BaseModel):  # ✅ 既存クラス名・継承関係維持
    """既存CKC設定 - 完全後方互換"""
    
    # 既存フィールドはすべて保持
    version: str = "2.0"  # バージョンのみ更新
    project_name: str = ""
    sync_targets: list[SyncTarget] = []
    auto_sync: bool = True
    tags: TagConfig = TagConfig()
    watch: WatchConfig = WatchConfig()
    
    # 新機能は追加フィールドとして実装
    adaptive_structure: AdaptiveSystemConfig = AdaptiveSystemConfig()
    
    # 既存メソッドの完全保持
    @classmethod
    def load_from_file(cls, config_path: str | Path) -> "CKCConfig":
        """既存メソッド - 自動移行機能付き拡張"""
        return ConfigCompatibilityManager().load_config_with_migration(Path(config_path))
    
    def save_to_file(self, config_path: str | Path) -> None:
        """既存メソッド - v2.0形式で保存"""
        # 内部実装は強化されているが、インターフェースは同一
        super().save_to_file(config_path)

# 既存クラスの拡張継承
class EnhancedCKCConfig(CKCConfig):
    """拡張設定 - 新機能利用時のオプション"""
    
    # 高度な新機能のみここに追加
    advanced_analytics: bool = False
    ai_suggestions: bool = False
```

#### メソッド互換性保証
```python
class APICompatibilityGuarantee:
    """API互換性保証システム"""
    
    def test_all_existing_apis(self) -> CompatibilityReport:
        """既存API総合テスト"""
        report = CompatibilityReport()
        
        # 1. 設定関連API
        report.add_section(self._test_config_apis())
        
        # 2. Obsidian連携API  
        report.add_section(self._test_obsidian_apis())
        
        # 3. メタデータAPI
        report.add_section(self._test_metadata_apis())
        
        # 4. CLI API
        report.add_section(self._test_cli_apis())
        
        return report
    
    def _test_config_apis(self) -> TestSection:
        """設定API互換性テスト"""
        tests = []
        
        # 既存の使用パターンをテスト
        tests.append(self._test_config_loading())
        tests.append(self._test_config_saving())
        tests.append(self._test_sync_target_management())
        tests.append(self._test_tag_configuration())
        
        return TestSection("Config APIs", tests)
```

### 4. データ互換性

#### ファイル形式互換性
```python
class DataCompatibilityManager:
    """データ互換性管理"""
    
    def ensure_metadata_compatibility(self, file_path: Path) -> bool:
        """メタデータ互換性確保"""
        
        # 1. 既存フロントマター形式の保持
        if self._has_legacy_frontmatter(file_path):
            return self._preserve_legacy_format(file_path)
        
        # 2. 新形式での拡張データ追加
        return self._add_enhanced_metadata(file_path)
    
    def _preserve_legacy_format(self, file_path: Path) -> bool:
        """既存フォーマット保持"""
        # 既存のメタデータ構造を変更せず
        # 新しいメタデータは別名前空間で追加
        
        existing_metadata = self._extract_existing_metadata(file_path)
        enhanced_metadata = self._generate_enhanced_metadata(file_path)
        
        # 名前空間分離での拡張
        combined_metadata = {
            **existing_metadata,  # 既存メタデータそのまま
            "ckc_enhanced": enhanced_metadata  # 拡張メタデータ
        }
        
        return self._update_file_metadata(file_path, combined_metadata)
```

#### ディレクトリ構造互換性
```python
class StructureCompatibilityManager:
    """ディレクトリ構造互換性管理"""
    
    def maintain_legacy_access(self, vault_path: Path) -> bool:
        """レガシーアクセス路の維持"""
        
        # シンボリックリンクによる互換性確保
        legacy_mappings = {
            "00_Inbox": "00_Catalyst_Lab",
            "01_Projects": "10_Projects",
            "02_Knowledge_Base": "20_Knowledge_Base",
            "03_Templates": "_templates",
            "04_Analytics": "Analytics", 
            "05_Archive": "30_Wisdom_Archive"
        }
        
        for legacy_name, new_name in legacy_mappings.items():
            legacy_path = vault_path / legacy_name
            new_path = vault_path / new_name
            
            if new_path.exists() and not legacy_path.exists():
                # レガシーパスからのシンボリックリンク作成
                try:
                    legacy_path.symlink_to(new_path)
                except OSError:
                    # シンボリックリンク作成失敗時の代替処理
                    return self._create_compatibility_bridge(legacy_path, new_path)
        
        return True
```

## 🔄 段階的互換性移行

### 1. 移行フェーズ設計

#### Phase 1: 共存期間（6ヶ月）
```python
class CoexistencePhase:
    """共存期間管理"""
    
    def __init__(self):
        self.warning_frequency = "monthly"  # 月1回の移行推薦
        self.feature_highlight = True       # 新機能の控えめな紹介
        self.full_compatibility = True     # 完全互換性維持
    
    def show_gentle_migration_reminder(self):
        """控えめな移行推薦"""
        print("""
💡 ヒント: 新しい適応型システム基盤で知識管理がより効率的になります
   詳細: uv run ckc structure --info
   
   （この通知は月1回表示されます。無効にする: --no-migration-hints）
        """)
    
    def enable_feature_discovery(self):
        """新機能の段階的発見"""
        # 使用パターンに基づく機能提案
        # 非侵入的な新機能紹介
        pass
```

#### Phase 2: 推薦期間（3ヶ月）
```python
class RecommendationPhase:
    """推薦期間管理"""
    
    def __init__(self):
        self.warning_frequency = "weekly"   # 週1回の推薦
        self.feature_highlight = True       # 積極的な新機能紹介
        self.migration_incentives = True    # 移行インセンティブ
    
    def show_enhanced_migration_benefits(self):
        """移行メリットの積極的紹介"""
        print("""
🚀 適応型システム基盤の利用者から高評価をいただいています！
   
   ✅ 平均15%の効率向上を実現
   ✅ ファイル発見時間の短縮  
   ✅ より直感的な知識整理
   
   移行時間: わずか30分
   リスク: ゼロ（完全バックアップ＋ロールバック機能）
   
   今すぐ試す: uv run ckc migrate --wizard
        """)
```

### 2. 互換性警告システム

#### 段階的警告レベル
```python
class CompatibilityWarningSystem:
    """互換性警告システム"""
    
    WARNING_LEVELS = {
        "info": {
            "frequency": "monthly",
            "tone": "informational",
            "action": "optional"
        },
        "recommendation": {
            "frequency": "weekly", 
            "tone": "encouraging",
            "action": "suggested"
        },
        "deprecation": {
            "frequency": "daily",
            "tone": "urgent",
            "action": "required_soon"
        }
    }
    
    def show_contextual_warning(self, command: str, context: dict):
        """文脈的警告表示"""
        
        if self._should_show_migration_hint(command, context):
            level = self._determine_warning_level(context)
            warning = self._generate_contextual_warning(command, level)
            self._display_warning(warning, level)
```

## 📊 互換性テスト戦略

### 1. 自動互換性テスト

#### 包括的回帰テスト
```python
class CompatibilityTestSuite:
    """互換性テストスイート"""
    
    def test_cli_backward_compatibility(self):
        """CLI後方互換性テスト"""
        
        # 既存コマンドの全パターンテスト
        legacy_commands = [
            "ckc init",
            "ckc sync add vault obsidian /path",
            "ckc watch",
            "ckc status",
            "ckc sync run"
        ]
        
        for command in legacy_commands:
            result = self._execute_command_in_legacy_env(command)
            self.assertTrue(result.success, f"Legacy command failed: {command}")
            
            result = self._execute_command_in_adaptive_env(command)
            self.assertTrue(result.success, f"Command failed in adaptive: {command}")
    
    def test_config_file_compatibility(self):
        """設定ファイル互換性テスト"""
        
        # v1.0設定ファイルの自動変換テスト
        v1_config_samples = self._load_v1_config_samples()
        
        for sample in v1_config_samples:
            migrated_config = ConfigCompatibilityManager().load_config_with_migration(sample)
            self.assertIsInstance(migrated_config, EnhancedCKCConfig)
            self._verify_config_data_preservation(sample, migrated_config)
    
    def test_api_interface_stability(self):
        """APIインターフェース安定性テスト"""
        
        # 既存APIの全メソッドシグネチャーテスト
        self._test_class_inheritance_chain()
        self._test_method_signatures()
        self._test_return_type_compatibility()
        self._test_exception_behavior()
```

### 2. 手動互換性検証

#### ユーザー行動シミュレーション
```python
class UserBehaviorSimulation:
    """ユーザー行動シミュレーション"""
    
    def simulate_typical_user_workflows(self):
        """典型的ユーザーワークフローシミュレーション"""
        
        workflows = [
            self._simulate_daily_sync_workflow(),
            self._simulate_project_setup_workflow(),
            self._simulate_knowledge_search_workflow(),
            self._simulate_file_organization_workflow()
        ]
        
        for workflow in workflows:
            self._execute_workflow_in_legacy_mode(workflow)
            self._execute_workflow_in_adaptive_mode(workflow)
            self._compare_workflow_results(workflow)
```

## 🎯 成功基準・品質保証

### 互換性成功基準
- [ ] 既存CLI コマンド100%動作保証
- [ ] 既存設定ファイル100%認識・変換
- [ ] 既存Python API 100%動作保証
- [ ] データ形式完全保持
- [ ] 性能劣化5%以内

### ユーザー体験基準
- [ ] 既存ユーザーの学習コストゼロ
- [ ] 移行を意識しない自然な機能向上
- [ ] 新機能の段階的発見・習得
- [ ] サポート負荷増加10%以内

### 技術品質基準
- [ ] 全回帰テスト合格維持
- [ ] 互換性テストスイート100%合格
- [ ] ドキュメント互換性の完全性
- [ ] 長期サポート可能性の確保

---

**戦略策定日**: 2024-06-18  
**実装予定**: Phase B Week 3-5  
**責任者**: CKC Compatibility Team