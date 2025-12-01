# TDD Refactor - コードをリファクタリング

Refactor Phase: テストをパスする状態を保ちながらコードを改善します。

## あなたの役割

1. **現在のコードを分析**
   - `/tdd-green` で書いたコードを確認
   - コードの臭い（Code Smells）を特定
   - 改善の余地を見つける

2. **リファクタリングを実施**
   - コードを綺麗にする（テストは変更しない）
   - 重複を排除（DRY原則）
   - 命名を改善
   - 構造を改善

3. **テストを実行**
   - リファクタリング後もすべてのテストがパスすることを確認
   - 振る舞いが変わっていないことを保証

4. **結果を報告**
   - 何をリファクタリングしたか
   - なぜそのリファクタリングが必要だったか
   - テストがすべてパスしていることを確認

## リファクタリングのパターン

### 1. 命名の改善

**Before:**
```java
public int calc(int x) {
    return x * 2;
}
```

**After:**
```java
public int calculateDoubleValue(int inputValue) {
    return inputValue * 2;
}
```

### 2. マジックナンバーの定数化

**Before:**
```java
if (age >= 18) {
    // ...
}
```

**After:**
```java
private static final int ADULT_AGE = 18;

if (age >= ADULT_AGE) {
    // ...
}
```

### 3. 複雑な条件式の抽出

**Before:**
```java
if (user.getAge() >= 18 && user.hasVerifiedEmail() && !user.isBanned()) {
    // ...
}
```

**After:**
```java
if (isEligibleUser(user)) {
    // ...
}

private boolean isEligibleUser(User user) {
    return user.getAge() >= 18
        && user.hasVerifiedEmail()
        && !user.isBanned();
}
```

### 4. 長いメソッドの分割

**Before:**
```java
public void processOrder(Order order) {
    // 検証
    if (order.getItems().isEmpty()) throw new Exception();

    // 計算
    int total = 0;
    for (Item item : order.getItems()) {
        total += item.getPrice() * item.getQuantity();
    }

    // 保存
    database.save(order);

    // 通知
    emailService.sendConfirmation(order.getCustomer());
}
```

**After:**
```java
public void processOrder(Order order) {
    validateOrder(order);
    int total = calculateTotal(order);
    saveOrder(order);
    sendConfirmation(order);
}

private void validateOrder(Order order) { /* ... */ }
private int calculateTotal(Order order) { /* ... */ }
private void saveOrder(Order order) { /* ... */ }
private void sendConfirmation(Order order) { /* ... */ }
```

### 5. 重複コードの排除（DRY）

**Before:**
```java
public void processA() {
    // 共通処理
    log("Start");
    validate();
    // A固有処理
    doA();
    // 共通処理
    log("End");
}

public void processB() {
    // 共通処理
    log("Start");
    validate();
    // B固有処理
    doB();
    // 共通処理
    log("End");
}
```

**After:**
```java
public void processA() {
    executeWithLogging(() -> doA());
}

public void processB() {
    executeWithLogging(() -> doB());
}

private void executeWithLogging(Runnable operation) {
    log("Start");
    validate();
    operation.run();
    log("End");
}
```

## Code Smells（コードの臭い）

リファクタリングが必要なサイン：

- **Long Method**: メソッドが長すぎる（20行以上）
- **Large Class**: クラスが大きすぎる（責任が多すぎる）
- **Duplicated Code**: 重複したコード
- **Magic Numbers**: ハードコードされた数値
- **Poor Naming**: 意味不明な変数名・メソッド名
- **Deep Nesting**: ネストが深い（if文の中のif文の中の...）
- **Comments**: コメントがないと理解できない（コードで説明すべき）

## リファクタリングの原則

### ✅ DO（すべきこと）

- **Keep tests green**: リファクタリング中もテストはパスし続ける
- **Small steps**: 小さなステップで進む
- **Run tests frequently**: 頻繁にテストを実行
- **Commit often**: 小さな改善ごとにコミット

### ❌ DON'T（してはいけないこと）

- **Change behavior**: 振る舞いを変更しない
- **Refactor without tests**: テストなしでリファクタリングしない
- **Add features**: 新機能を追加しない
- **Big refactoring**: 大きすぎるリファクタリングをしない

## 実行手順

1. リファクタリング前にテストがすべてパスすることを確認
2. 小さなリファクタリングを1つ実施
3. テストを実行（`mvn test` または `./gradlew test`）
4. テストがパスすることを確認
5. 次のリファクタリングへ（または次のフェーズへ）

## チェックリスト

- [ ] リファクタリング前にテストがパスしていた
- [ ] リファクタリング後もテストがパスしている
- [ ] コードが読みやすくなった
- [ ] 重複が減った
- [ ] 命名が改善された
- [ ] 構造が改善された
- [ ] 振る舞いは変わっていない

## 次のステップ

### パターンA: さらなるリファクタリングが必要
→ もう一度 `/tdd-refactor` を実行

### パターンB: リファクタリング完了
→ `/tdd-verify` を実行してすべてのテストが通ることを確認

### パターンC: 次のテストケースへ
→ `/tdd-red` を実行して次のテストケースを追加

---

現在のコードをリファクタリングして改善してください。
