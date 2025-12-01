# TDD Verify - すべてのテストが通ることを確認

Verify Phase: すべてのテストが通ることを確認し、品質を保証します。

## あなたの役割

1. **テストスイート全体を実行**
   - 単体テスト（Unit Tests）
   - 統合テスト（Integration Tests）
   - すべてのテストを実行

2. **テスト結果を分析**
   - すべてのテストがパスしているか
   - カバレッジは十分か
   - テストの実行時間は許容範囲か

3. **品質指標をチェック**
   - コードカバレッジ（推奨: 80%以上）
   - テスト数（新機能に対して十分なテストがあるか）
   - テストの品質（意味のあるテストか）

4. **結果を報告**
   - テスト結果のサマリー
   - カバレッジレポート
   - 次のアクション（コミット準備OK / さらにテストが必要）

## 実行コマンド

### Maven

```bash
# すべてのテストを実行
mvn clean test

# カバレッジレポート付き
mvn clean test jacoco:report

# 特定のテストクラスのみ
mvn test -Dtest=A001ServiceTest
```

### Gradle

```bash
# すべてのテストを実行
./gradlew clean test

# カバレッジレポート付き
./gradlew clean test jacocoTestReport

# 特定のテストクラスのみ
./gradlew test --tests A001ServiceTest
```

## チェックリスト

### テスト実行

- [ ] すべてのテストがパスした
- [ ] テストの実行時間が許容範囲内（目安: 1分以内）
- [ ] 警告やエラーメッセージがない

### コードカバレッジ

- [ ] 新規追加したコードのカバレッジが80%以上
- [ ] 既存のテストが壊れていない
- [ ] エッジケースがテストされている

### テストの品質

- [ ] テストは独立している（順序に依存しない）
- [ ] テストは再現可能（何度実行しても同じ結果）
- [ ] テストは高速（遅いテストはない）
- [ ] テストは明確（何をテストしているか分かる）

## 品質基準

### Good Test（良いテスト）の特徴

1. **Fast**: 高速に実行できる
2. **Independent**: 他のテストに依存しない
3. **Repeatable**: 再現可能（環境に依存しない）
4. **Self-Validating**: 自己検証（自動的に成功/失敗が分かる）
5. **Timely**: タイムリー（実装の前または直後に書かれる）

### カバレッジの目標

| レイヤー | 目標カバレッジ |
|---------|--------------|
| ドメインロジック | 90%以上 |
| サービス層 | 80%以上 |
| コントローラー層 | 70%以上 |
| ユーティリティ | 100% |

## テスト結果の読み方

### 成功例

```
Tests run: 15, Failures: 0, Errors: 0, Skipped: 0

[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
```

✅ すべてのテストがパス → コミット準備OK

### 失敗例

```
Tests run: 15, Failures: 1, Errors: 0, Skipped: 0

[ERROR] Failures:
[ERROR]   A001ServiceTest.shouldReturnErrorWhenCustomerCdIsEmpty:45
    Expected: "得意先CDは必須項目です"
    Actual:   "得意先CDが存在しません"
```

❌ テストが失敗 → 修正が必要

## 次のステップ

### ✅ すべてのテストがパスした場合

1. カバレッジレポートを確認
2. コミットメッセージを準備
3. `git add` でステージング
4. `git commit` でコミット
5. 次のタスクへ（または次の `/tdd-red`）

### ❌ テストが失敗した場合

1. 失敗したテストを確認
2. 原因を特定
3. `/tdd-green` に戻って修正
4. または `/tdd-refactor` でリファクタリング
5. 再度 `/tdd-verify` で確認

### ⚠️ カバレッジが不十分な場合

1. カバレッジされていないコードを特定
2. `/tdd-red` で追加のテストを書く
3. TDDサイクルを繰り返す

## レポート出力例

```markdown
### TDD Verify Results

#### Test Summary
- Total Tests: 15
- Passed: 15 ✅
- Failed: 0
- Skipped: 0
- Duration: 2.3s

#### Coverage Report
- Line Coverage: 87% (目標: 80%)
- Branch Coverage: 82% (目標: 75%)
- Method Coverage: 92%

#### Quality Check
✅ All tests passed
✅ Coverage meets target
✅ No warnings or errors
✅ Ready to commit

#### Next Steps
すべてのテストがパスし、品質基準を満たしています。
コミットして次のタスクに進んでください。

`git add .`
`git commit -m "Add customer validation feature"`
```

---

すべてのテストを実行して品質を確認してください。
