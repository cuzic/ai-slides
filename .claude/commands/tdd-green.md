# TDD Green - テストをパスする最小限の実装

Green Phase: テストをパスする最小限のコードを書きます。

## あなたの役割

1. **失敗したテストを確認**
   - `/tdd-red` で書いたテストが失敗していることを確認
   - 失敗の理由を理解する

2. **最小限の実装を書く**
   - テストをパスする **最小限** のコードを書く
   - 過剰な実装はしない（YAGNI - You Aren't Gonna Need It）
   - まずは動くコードを書く（最適化は後で）

3. **テストを実行**
   - テストを実行してパスすることを確認
   - 他のテストが壊れていないことを確認（リグレッション）

4. **結果を報告**
   - 何を実装したか
   - テストがパスしたことを確認
   - 次のステップ（`/tdd-refactor` または次の `/tdd-red`）

## 実装の原則

### ✅ DO（すべきこと）

- **Simplest thing that works**: 動く最もシンプルなコードを書く
- **Make the test pass**: テストをパスさせることに集中
- **Hardcode if necessary**: 必要なら定数をハードコードしても良い
- **Baby steps**: 小さなステップで進む

### ❌ DON'T（してはいけないこと）

- **Premature optimization**: 早すぎる最適化をしない
- **Over-engineering**: 過剰設計をしない
- **Add features not tested**: テストされていない機能を追加しない
- **Refactor yet**: まだリファクタリングしない（次のフェーズで）

## 実装例

### Phase 1: ハードコードから始める

```java
// 最初のテスト: 特定の入力に対する出力
public int calculate(int input) {
    return 42;  // ハードコード OK!
}
```

### Phase 2: 次のテストで一般化を強制

```java
// 2つ目のテストを追加した後
public int calculate(int input) {
    return input * 2;  // パターンが見えてきた
}
```

### Phase 3: さらにテストを追加して完全な実装へ

```java
// 複数のテストケースをカバー
public int calculate(int input) {
    if (input < 0) {
        throw new IllegalArgumentException("Input must be positive");
    }
    return input * 2;
}
```

## 実行手順

1. 実装コードを書く（最小限）
2. テストを実行（`mvn test` または `./gradlew test`）
3. テストがパスすることを確認
4. 他のテストも壊れていないことを確認
5. 結果を報告

## チェックリスト

- [ ] テストがパスした
- [ ] 既存のテストが壊れていない
- [ ] コードは理解しやすい
- [ ] 必要最小限の実装である
- [ ] ハードコードされた値は次のテストで改善される予定

## 次のステップ

### パターンA: コードが綺麗な場合
→ `/tdd-red` を実行して次のテストケースを追加

### パターンB: コードに改善の余地がある場合
→ `/tdd-refactor` を実行してコードをリファクタリング

---

現在失敗しているテストをパスする最小限のコードを書いてください。
