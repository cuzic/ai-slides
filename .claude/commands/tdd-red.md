# TDD Red - 失敗するテストを書く

Red Phase: まず失敗するテストを書きます。

## あなたの役割

1. **テストファイルの確認/作成**
   - テスト対象のクラス/メソッドに対応するテストファイルを確認
   - 存在しない場合は適切な場所に作成

2. **失敗するテストを書く**
   - `/tdd-plan` で計画した次のテストケースを実装
   - テストメソッド名は明確で説明的にする
   - Arrange-Act-Assert パターンに従う
   - まだ実装していない機能をテストする（だから失敗する）

3. **テストを実行**
   - テストを実行して失敗することを確認
   - エラーメッセージが明確で理解しやすいことを確認

4. **結果を報告**
   - どのテストを追加したか
   - なぜ失敗するのか（期待する動作と現在の状態）
   - 次のステップ（`/tdd-green`）

## テストの書き方

### Javaの場合（JUnit 5）

```java
@Test
@DisplayName("説明的なテスト名")
void testMethodName() {
    // Arrange - テストデータの準備
    var input = ...;
    var expected = ...;

    // Act - テスト対象のメソッドを実行
    var actual = targetMethod(input);

    // Assert - 期待値と実際の値を検証
    assertEquals(expected, actual, "エラーメッセージ");
}
```

### テスト命名規則

- `should[ExpectedBehavior]When[StateUnderTest]`
- 例: `shouldReturnErrorWhenCustomerCdIsEmpty()`
- 例: `shouldInsertSlipWhenAllRequiredFieldsAreProvided()`

## 実行手順

1. テストファイルを作成/更新
2. テストを実行（`mvn test` または `./gradlew test`）
3. テストが失敗することを確認
4. 失敗の理由を確認（まだ実装していないため）
5. 結果を報告

## 重要な原則

- **Write the test first**: 実装コードを書く前にテストを書く
- **Test should fail**: テストは失敗しなければならない（実装がないため）
- **Clear failure message**: 失敗メッセージは明確で理解しやすくする
- **One concept per test**: 1つのテストで1つの概念のみをテストする

## 次のステップ

テストが失敗したら `/tdd-green` を実行してテストをパスする最小限の実装を書いてください。

---

現在のタスクに対して失敗するテストを書いてください。
