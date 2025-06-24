# テスト戦略詳細

## 📋 テスト戦略概要

### 目的
適応型システム基盤統合における包括的品質保証を実現し、既存機能の完全保護と新機能の信頼性確保を両立する。

### テスト哲学
1. **既存機能の完全保護**: 一切の機能劣化を許容しない
2. **新機能の徹底検証**: 本番レベルでの信頼性確保
3. **統合品質の保証**: システム全体の整合性維持
4. **継続的品質向上**: テスト駆動による継続改善

## 🏗️ テスト アーキテクチャ

### テスト層構造
```
┌─────────────────────────────────────┐
│ E2E Tests (エンドツーエンドテスト)    │
├─────────────────────────────────────┤
│ Integration Tests (統合テスト)       │
├─────────────────────────────────────┤
│ Component Tests (コンポーネントテスト) │
├─────────────────────────────────────┤
│ Unit Tests (単体テスト)              │
└─────────────────────────────────────┘
```

### テストカテゴリ分類
```python
class TestCategory(Enum):
    """テストカテゴリ分類"""

    # 機能別テスト
    REGRESSION = "regression"           # 回帰テスト
    COMPATIBILITY = "compatibility"     # 互換性テスト
    INTEGRATION = "integration"         # 統合テスト
    PERFORMANCE = "performance"         # 性能テスト
    SECURITY = "security"              # セキュリティテスト

    # 段階別テスト
    PRE_MIGRATION = "pre_migration"     # 移行前テスト
    MIGRATION = "migration"             # 移行中テスト
    POST_MIGRATION = "post_migration"   # 移行後テスト

    # 環境別テスト
    LEGACY_ENV = "legacy_env"          # レガシー環境
    HYBRID_ENV = "hybrid_env"          # 適応型システム基盤環境
    MIXED_ENV = "mixed_env"            # 混在環境
```

## 🧪 層別テスト戦略

### 1. 単体テスト (Unit Tests)

#### クラス別テストスイート
```python
class AdaptiveSystemConfigTest(unittest.TestCase):
    """適応型システム基盤設定テスト"""

    def test_numbering_system_validation(self):
        """番号システム検証テスト"""
        # 有効な番号システム
        valid_configs = [
            {"numbering_system": "sequential"},
            {"numbering_system": "ten_step"}
        ]

        for config_data in valid_configs:
            config = AdaptiveSystemConfig(**config_data)
            self.assertIn(config.numbering_system, ["sequential", "ten_step"])

        # 無効な番号システム
        with self.assertRaises(ValidationError):
            AdaptiveSystemConfig(numbering_system="invalid")

    def test_custom_structure_validation(self):
        """カスタム構造検証テスト"""
        custom_structure = {
            "system_dirs": {"_test": "テスト用"},
            "core_dirs": {"00_Test": "テスト"},
            "auxiliary_dirs": {"Test": "テスト"}
        }

        config = AdaptiveSystemConfig(custom_structure=custom_structure)
        self.assertIsNotNone(config.custom_structure)
        self.assertEqual(len(config.custom_structure["system_dirs"]), 1)

class NumberingSystemTest(unittest.TestCase):
    """番号システムテスト"""

    def test_ten_step_number_allocation(self):
        """10刻み番号割り当てテスト"""
        numbering = NumberingSystem(system_type="ten_step")

        # 基本番号の確認
        self.assertEqual(numbering.base_numbers, [0, 10, 20, 30])

        # 中間番号の割り当て
        next_number = numbering.get_next_available_number(after=10)
        self.assertEqual(next_number, 15)  # 10と20の中間

        # 末尾番号の割り当て
        last_number = numbering.get_next_available_number(after=30)
        self.assertEqual(last_number, 40)

    def test_number_insertion_capability(self):
        """番号挿入可能性テスト"""
        numbering = NumberingSystem(system_type="ten_step")

        # 挿入可能
        self.assertTrue(numbering.can_insert_between(10, 20))

        # 挿入不可能（1刻み）
        numbering_seq = NumberingSystem(system_type="sequential")
        self.assertFalse(numbering_seq.can_insert_between(1, 2))

class KnowledgeClassifierTest(unittest.TestCase):
    """知識分類器テスト"""

    def setUp(self):
        self.classifier = KnowledgeClassifier()

    def test_prompt_classification(self):
        """プロンプト分類テスト"""
        # ベストプラクティス分類
        metadata = KnowledgeMetadata(
            title="高性能プロンプト",
            tags=["prompt"],
            success_rate=90
        )
        result = self.classifier._classify_prompt("", metadata)
        self.assertIn("Best_Practices", result)

        # 改善ログ分類
        content = "このプロンプトの改善点について"
        metadata = KnowledgeMetadata(title="改善記録", tags=["prompt"])
        result = self.classifier._classify_prompt(content, metadata)
        self.assertIn("Improvement_Log", result)

    def test_code_classification(self):
        """コード分類テスト"""
        # Python分類
        metadata = KnowledgeMetadata(title="Pythonスクリプト", tags=["code", "python"])
        result = self.classifier._classify_code("", metadata)
        self.assertIn("Python", result)

        # JavaScript分類
        metadata = KnowledgeMetadata(title="JSスクリプト", tags=["code", "javascript"])
        result = self.classifier._classify_code("", metadata)
        self.assertIn("JavaScript", result)
```

#### メタデータ管理テスト
```python
class MetadataCompatibilityTest(unittest.TestCase):
    """メタデータ互換性テスト"""

    def test_legacy_metadata_preservation(self):
        """レガシーメタデータ保持テスト"""
        # v1.0 メタデータ形式
        legacy_metadata = {
            "title": "テストファイル",
            "created": "2024-01-01",
            "tags": ["test", "legacy"]
        }

        # v2.0 変換テスト
        enhanced = self._convert_to_v2(legacy_metadata)

        # 既存フィールド保持確認
        self.assertEqual(enhanced["title"], legacy_metadata["title"])
        self.assertEqual(enhanced["tags"], legacy_metadata["tags"])

        # 新フィールド追加確認
        self.assertIn("ckc_enhanced", enhanced)

    def test_metadata_round_trip(self):
        """メタデータ往復変換テスト"""
        original = KnowledgeMetadata(
            title="往復テスト",
            tags=["test"],
            success_rate=85
        )

        # ファイル保存・読み込み
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            self._save_with_metadata(f.name, original)
            loaded = self._load_metadata(f.name)

        # データ保持確認
        self.assertEqual(original.title, loaded.title)
        self.assertEqual(original.tags, loaded.tags)
        self.assertEqual(original.success_rate, loaded.success_rate)
```

### 2. 統合テスト (Integration Tests)

#### システム間連携テスト
```python
class AdaptiveSystemIntegrationTest(unittest.TestCase):
    """適応型システム基盤統合テスト"""

    def setUp(self):
        self.test_vault = self._create_test_vault()
        self.config = self._create_test_config()
        self.manager = AdaptiveObsidianVaultManager(
            self.test_vault,
            MetadataManager(),
            self.config.adaptive_structure
        )

    def test_vault_initialization_integration(self):
        """バルト初期化統合テスト"""
        # 適応型システム基盤での初期化
        success = self.manager.initialize_vault()
        self.assertTrue(success)

        # 期待される構造の確認
        expected_dirs = [
            "_templates", "_attachments", "_scripts",
            "00_Catalyst_Lab", "10_Projects", "20_Knowledge_Base", "30_Wisdom_Archive",
            "Analytics", "Archive", "Evolution_Log"
        ]

        for dir_name in expected_dirs:
            dir_path = self.test_vault / dir_name
            self.assertTrue(dir_path.exists(), f"Missing directory: {dir_name}")

            # README存在確認
            readme_path = dir_path / "README.md"
            self.assertTrue(readme_path.exists(), f"Missing README: {dir_name}")

    def test_file_classification_integration(self):
        """ファイル分類統合テスト"""
        # テストファイル作成
        test_files = [
            ("prompt_template.md", {"tags": ["prompt"]}, "20_Knowledge_Base/Prompts/Templates"),
            ("python_script.md", {"tags": ["code", "python"]}, "20_Knowledge_Base/Code_Snippets/Python"),
            ("ai_concept.md", {"tags": ["concept"]}, "20_Knowledge_Base/Concepts"),
            ("project_log.md", {"tags": ["project_log"]}, "10_Projects")
        ]

        for filename, metadata, expected_path in test_files:
            # ファイル作成
            test_file = self._create_test_file(filename, metadata)

            # 同期実行
            success = self.manager.sync_file(test_file)
            self.assertTrue(success)

            # 配置確認
            expected_full_path = self.test_vault / expected_path
            synced_files = list(expected_full_path.glob("*.md"))
            self.assertGreater(len(synced_files), 0, f"No file synced to {expected_path}")

    def test_legacy_to_adaptive_migration_integration(self):
        """レガシー→適応型システム基盤移行統合テスト"""
        # レガシー構造作成
        legacy_structure = {
            "00_Inbox": ["test1.md", "test2.md"],
            "01_Projects": ["project1.md"],
            "02_Knowledge_Base": ["knowledge1.md"]
        }

        self._create_legacy_structure(legacy_structure)

        # 移行実行
        migration_manager = StructureMigrationManager(self.test_vault, self.config)
        plan = migration_manager.plan_migration(StructureType.ADAPTIVE)
        result = migration_manager.execute_migration(plan)

        # 移行結果確認
        self.assertTrue(result.success)
        self.assertEqual(result.files_migrated, 4)

        # 新構造確認
        self.assertTrue((self.test_vault / "00_Catalyst_Lab").exists())
        self.assertTrue((self.test_vault / "10_Projects").exists())
        self.assertTrue((self.test_vault / "20_Knowledge_Base").exists())
```

#### CLI統合テスト
```python
class CLIIntegrationTest(unittest.TestCase):
    """CLI統合テスト"""

    def test_cli_command_integration(self):
        """CLIコマンド統合テスト"""
        with tempfile.TemporaryDirectory() as test_dir:
            os.chdir(test_dir)

            # 初期化コマンドテスト
            result = subprocess.run(
                ["uv", "run", "ckc", "init", "--structure", "adaptive"],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0)

            # 設定ファイル存在確認
            config_path = Path(test_dir) / "ckc_config.yaml"
            self.assertTrue(config_path.exists())

            # 構造ステータスコマンドテスト
            result = subprocess.run(
                ["uv", "run", "ckc", "structure", "status"],
                capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("adaptive", result.stdout.lower())

    def test_backward_compatibility_commands(self):
        """後方互換性コマンドテスト"""
        # 既存コマンドが適応型システム基盤環境でも動作することを確認
        legacy_commands = [
            ["ckc", "status"],
            ["ckc", "sync", "--dry-run"]
        ]

        for command in legacy_commands:
            with self.subTest(command=command):
                result = subprocess.run(
                    ["uv", "run"] + command,
                    capture_output=True, text=True
                )
                self.assertEqual(result.returncode, 0,
                               f"Legacy command failed: {command}")
```

### 3. 性能テスト (Performance Tests)

#### 性能ベンチマーク
```python
class PerformanceTest(unittest.TestCase):
    """性能テスト"""

    def test_large_vault_performance(self):
        """大規模バルト性能テスト"""
        # 1000ファイルのテストバルト作成
        large_vault = self._create_large_test_vault(file_count=1000)

        # 初期化時間測定
        start_time = time.time()
        manager = AdaptiveObsidianVaultManager(large_vault, MetadataManager(), AdaptiveSystemConfig())
        init_success = manager.initialize_vault()
        init_time = time.time() - start_time

        self.assertTrue(init_success)
        self.assertLess(init_time, 10.0, "初期化が10秒を超過")

        # 同期時間測定
        test_files = self._create_test_files(count=100)
        start_time = time.time()

        for test_file in test_files:
            manager.sync_file(test_file)

        sync_time = time.time() - start_time
        avg_sync_time = sync_time / len(test_files)

        self.assertLess(avg_sync_time, 0.1, "平均同期時間が0.1秒を超過")

    def test_memory_usage(self):
        """メモリ使用量テスト"""
        import psutil
        import gc

        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # 大量操作実行
        manager = AdaptiveObsidianVaultManager(
            self._create_test_vault(),
            MetadataManager(),
            AdaptiveSystemConfig()
        )

        for i in range(1000):
            test_file = self._create_test_file(f"test_{i}.md")
            manager.sync_file(test_file)

        gc.collect()
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        self.assertLess(memory_increase, 100, "メモリ使用量が100MB以上増加")

    def test_concurrent_operations(self):
        """並行操作テスト"""
        import threading
        import queue

        vault = self._create_test_vault()
        manager = AdaptiveObsidianVaultManager(vault, MetadataManager(), AdaptiveSystemConfig())
        manager.initialize_vault()

        # 並行同期テスト
        results = queue.Queue()
        threads = []

        def sync_worker(file_list):
            for file_path in file_list:
                success = manager.sync_file(file_path)
                results.put(success)

        # 10スレッドで100ファイルを並行同期
        file_batches = self._create_file_batches(total_files=100, batch_count=10)

        start_time = time.time()

        for batch in file_batches:
            thread = threading.Thread(target=sync_worker, args=(batch,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        concurrent_time = time.time() - start_time

        # 結果検証
        successes = 0
        while not results.empty():
            if results.get():
                successes += 1

        self.assertEqual(successes, 100, "並行同期で失敗が発生")
        self.assertLess(concurrent_time, 30, "並行同期が30秒を超過")
```

### 4. 回帰テスト (Regression Tests)

#### 既存機能保護テスト
```python
class RegressionTestSuite(unittest.TestCase):
    """回帰テストスイート"""

    def test_legacy_config_loading(self):
        """レガシー設定読み込み回帰テスト"""
        # v1.0設定ファイルのサンプル
        legacy_configs = self._load_legacy_config_samples()

        for config_file in legacy_configs:
            with self.subTest(config=config_file.name):
                # 設定読み込みテスト
                config = CKCConfig.load_from_file(config_file)

                # 基本フィールド確認
                self.assertIsInstance(config.project_name, str)
                self.assertIsInstance(config.sync_targets, list)
                self.assertIsInstance(config.tags, TagConfig)

                # v2.0フィールド確認
                self.assertIsInstance(config.hybrid_structure, HybridStructureConfig)
                self.assertEqual(config.version, "2.0")

    def test_obsidian_sync_behavior(self):
        """Obsidian同期動作回帰テスト"""
        # 既存のテストケースをすべて実行
        legacy_test_cases = self._load_legacy_sync_test_cases()

        for test_case in legacy_test_cases:
            with self.subTest(case=test_case.name):
                # レガシー環境でのテスト
                legacy_result = self._execute_in_legacy_env(test_case)

                # 適応型システム基盤環境でのテスト
                adaptive_result = self._execute_in_adaptive_env(test_case)

                # 結果比較
                self.assertEqual(
                    legacy_result.success,
                    adaptive_result.success,
                    f"動作が変化: {test_case.name}"
                )

                # ファイル内容比較
                self._compare_sync_results(legacy_result, adaptive_result)

    def test_metadata_extraction_consistency(self):
        """メタデータ抽出一貫性回帰テスト"""
        # 既存のテストファイルセット
        test_files = self._load_metadata_test_files()

        for test_file in test_files:
            with self.subTest(file=test_file.name):
                # v1.0での抽出結果
                v1_metadata = self._extract_with_v1_system(test_file)

                # v2.0での抽出結果
                v2_metadata = self._extract_with_v2_system(test_file)

                # 基本メタデータの一致確認
                self._assert_core_metadata_match(v1_metadata, v2_metadata)
```

## 🔄 継続的テスト戦略

### 1. CI/CD パイプライン統合

#### GitHub Actions ワークフロー
```yaml
# .github/workflows/adaptive_integration_tests.yml
name: Adaptive Integration Tests

on:
  push:
    branches: [ main, feature/adaptive-integration ]
  pull_request:
    branches: [ main ]

jobs:
  compatibility-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11, 3.12]
        test-env: [legacy, adaptive, mixed]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        pip install uv
        uv sync --dev

    - name: Run compatibility tests
      run: |
        uv run pytest tests/compatibility/ -v --env=${{ matrix.test-env }}

    - name: Run regression tests
      run: |
        uv run pytest tests/regression/ -v

    - name: Performance benchmarks
      run: |
        uv run pytest tests/performance/ -v --benchmark-json=benchmark.json

    - name: Upload benchmark results
      uses: actions/upload-artifact@v3
      with:
        name: benchmark-results-${{ matrix.python-version }}-${{ matrix.test-env }}
        path: benchmark.json

  migration-tests:
    runs-on: ubuntu-latest
    needs: compatibility-tests

    steps:
    - uses: actions/checkout@v3

    - name: Test migration scenarios
      run: |
        uv run pytest tests/migration/ -v --capture=no

    - name: Validate migration integrity
      run: |
        uv run python scripts/validate_migration.py
```

### 2. 自動テスト生成

#### プロパティベーステスト
```python
from hypothesis import given, strategies as st

class PropertyBasedTests(unittest.TestCase):
    """プロパティベーステスト"""

    @given(st.text(min_size=1, max_size=100))
    def test_filename_sanitization_property(self, filename):
        """ファイル名サニタイゼーションプロパティテスト"""
        # どんな文字列でもサニタイズ後は安全なファイル名になる
        sanitized = self._sanitize_filename(filename)

        # プロパティ1: 空でない
        self.assertGreater(len(sanitized), 0)

        # プロパティ2: 危険文字を含まない
        dangerous_chars = '<>:"/\\|?*'
        for char in dangerous_chars:
            self.assertNotIn(char, sanitized)

        # プロパティ3: 有効なファイル名
        self.assertTrue(self._is_valid_filename(sanitized))

    @given(
        st.lists(st.text(min_size=1), min_size=0, max_size=20),
        st.one_of(st.just("sequential"), st.just("ten_step"))
    )
    def test_numbering_system_consistency(self, directories, numbering_type):
        """番号システム一貫性プロパティテスト"""
        numbering = NumberingSystem(system_type=numbering_type)

        allocated_numbers = []
        for directory in directories:
            number = numbering.allocate_number(directory)
            allocated_numbers.append(number)

        # プロパティ1: 重複なし
        self.assertEqual(len(allocated_numbers), len(set(allocated_numbers)))

        # プロパティ2: 順序性
        if numbering_type == "sequential":
            self.assertEqual(allocated_numbers, sorted(allocated_numbers))

        # プロパティ3: 番号範囲の妥当性
        for number in allocated_numbers:
            self.assertGreaterEqual(number, 0)
            self.assertLess(number, 1000)  # 合理的上限
```

### 3. テストデータ管理

#### テストファクトリー
```python
class TestDataFactory:
    """テストデータファクトリー"""

    @staticmethod
    def create_test_config(structure_type: str = "adaptive") -> EnhancedCKCConfig:
        """テスト用設定作成"""
        return EnhancedCKCConfig(
            project_name="test-project",
            adaptive_structure=AdaptiveSystemConfig(
                enabled=(structure_type == "adaptive"),
                numbering_system="ten_step" if structure_type == "adaptive" else "sequential"
            )
        )

    @staticmethod
    def create_test_metadata(category: str = "test") -> KnowledgeMetadata:
        """テスト用メタデータ作成"""
        return KnowledgeMetadata(
            title=f"Test {category}",
            category=category,
            tags=[category, "test"],
            status="draft"
        )

    @staticmethod
    def create_test_vault(structure_type: str = "adaptive") -> Path:
        """テスト用バルト作成"""
        temp_dir = tempfile.mkdtemp()
        vault_path = Path(temp_dir)

        if structure_type == "adaptive":
            TestDataFactory._create_adaptive_structure(vault_path)
        else:
            TestDataFactory._create_legacy_structure(vault_path)

        return vault_path

    @staticmethod
    def create_migration_test_scenario() -> MigrationTestScenario:
        """移行テストシナリオ作成"""
        scenario = MigrationTestScenario()

        # レガシー構造
        scenario.add_legacy_directory("00_Inbox", ["note1.md", "note2.md"])
        scenario.add_legacy_directory("01_Projects", ["project1.md"])
        scenario.add_legacy_directory("02_Knowledge_Base", ["knowledge1.md"])

        # 期待される移行結果
        scenario.set_expected_mapping({
            "00_Inbox": "00_Catalyst_Lab",
            "01_Projects": "10_Projects",
            "02_Knowledge_Base": "20_Knowledge_Base"
        })

        return scenario
```

## 📊 テスト品質指標

### 1. カバレッジ要件

#### コードカバレッジ目標
```python
COVERAGE_REQUIREMENTS = {
    "overall": 95,        # 全体カバレッジ
    "core_modules": 98,   # コアモジュール
    "new_features": 100,  # 新機能
    "compatibility": 100, # 互換性レイヤー
    "migration": 95,      # 移行機能
}

class CoverageValidator:
    """カバレッジ検証"""

    def validate_coverage_requirements(self, coverage_report: dict) -> bool:
        """カバレッジ要件検証"""
        for module, required_coverage in COVERAGE_REQUIREMENTS.items():
            actual_coverage = coverage_report.get(module, 0)
            if actual_coverage < required_coverage:
                raise CoverageError(
                    f"{module} coverage {actual_coverage}% < required {required_coverage}%"
                )
        return True
```

#### 機能カバレッジ目標
```python
FEATURE_COVERAGE_MATRIX = {
    "adaptive_structure": {
        "initialization": ["create_dirs", "validate_structure", "setup_config"],
        "classification": ["auto_classify", "manual_classify", "reclassify"],
        "migration": ["plan", "execute", "rollback", "validate"]
    },
    "compatibility": {
        "cli_commands": ["all_legacy_commands"],
        "config_files": ["v1_to_v2_migration", "preservation"],
        "api_interfaces": ["all_public_methods"]
    }
}
```

### 2. 品質ゲート

#### 自動品質チェック
```python
class QualityGate:
    """品質ゲート"""

    def __init__(self):
        self.criteria = [
            CoverageCriterion(min_coverage=95),
            RegressionCriterion(max_failures=0),
            PerformanceCriterion(max_degradation=5),
            CompatibilityCriterion(compatibility_rate=100),
            SecurityCriterion(vulnerabilities=0)
        ]

    def evaluate(self, test_results: TestResults) -> QualityGateResult:
        """品質ゲート評価"""
        result = QualityGateResult()

        for criterion in self.criteria:
            evaluation = criterion.evaluate(test_results)
            result.add_evaluation(evaluation)

            if not evaluation.passed:
                result.overall_passed = False
                result.add_blocker(evaluation.failure_reason)

        return result

    def generate_quality_report(self, result: QualityGateResult) -> str:
        """品質レポート生成"""
        if result.overall_passed:
            return "✅ すべての品質基準を満たしています"
        else:
            blockers = "\n".join(f"❌ {blocker}" for blocker in result.blockers)
            return f"🚫 品質ゲート不合格:\n{blockers}"
```

## 🎯 成功基準・評価指標

### テスト成功基準
- [ ] 全テストスイート合格率100%
- [ ] コードカバレッジ95%以上
- [ ] 機能カバレッジ100%
- [ ] 性能劣化5%以内
- [ ] 回帰テスト0件失敗

### 品質保証基準
- [ ] 既存機能の完全動作保証
- [ ] 新機能の信頼性確保
- [ ] 移行プロセスの安全性確保
- [ ] ユーザー体験の品質維持
- [ ] 長期保守性の確保

### 継続改善基準
- [ ] テスト実行時間最適化
- [ ] テストケース自動生成
- [ ] 品質指標の可視化
- [ ] CI/CDパイプライン効率化
- [ ] テスト技術負債の最小化

---

**戦略策定日**: 2024-06-18
**実装予定**: Phase B 全期間
**責任者**: CKC Quality Assurance Team
