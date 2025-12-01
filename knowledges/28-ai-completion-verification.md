# AIの「完成しました！」を検証する - Trust but Verifyの本質

**対象**: AI駆動開発でVerifyフェーズを実施する開発者
**目的**: AIの「完成しました！」を鵜呑みにせず、客観的に検証する手法を習得する
**AI問題との関連**: 手抜き（Reward Hacking）、虚偽報告（Hallucination）に対する最終防衛線

---

## AIの特性：「元気よく完成しました！」とうそをつく

AIは「完成しました！」と元気よく報告するが、実際には：
- テストはパスしているが、ハードコード実装
- コンパイルは通るが、ビジネスロジックが間違っている
- ファイルは生成されたが、受入条件を満たしていない

**重要な発見**: AIに「完成度を0-100点で答えて」と質問すると、正直に答える。
- 「完成しました！」→ 元気よく報告
- 「完成度は？」→ 「60点です。受入条件の3つ目を満たしていません」と正直に回答

これがTrust but Verifyの本質。「任せる（Trust）」けど「必ず確かめる（Verify）」。

---

## 完成度を点数で答えさせる手法

### Claude Codeへの指示例

```
TodoService.create()の実装が完了しました。
以下の受入条件に対して、現在の完成度を0-100点で評価してください。
満たしていない条件があれば、具体的に指摘してください。

【受入条件】
1. GIVEN H2 Databaseが空の状態 WHEN タイトル「買い物」でTODO作成 THEN todosテーブルに1レコード追加
2. GIVEN タイトルが空文字 WHEN TODO作成 THEN IllegalArgumentExceptionがスローされる
3. GIVEN タイトルが201文字 WHEN TODO作成 THEN IllegalArgumentExceptionがスローされる
```

### AIの回答例

```markdown
## 完成度評価: 60点

### 満たしている条件
✅ 1. GIVEN H2 Databaseが空の状態 WHEN タイトル「買い物」でTODO作成 THEN todosテーブルに1レコード追加
   - 実装済み。`todoRepository.save(todo)`でH2に保存されることを確認済み。

✅ 2. GIVEN タイトルが空文字 WHEN TODO作成 THEN IllegalArgumentExceptionがスローされる
   - 実装済み。`validateTitle()`メソッドで空文字チェック実施。

### 満たしていない条件
❌ 3. GIVEN タイトルが201文字 WHEN TODO作成 THEN IllegalArgumentExceptionがスローされる
   - **未実装**。現在は`validateTitle()`で空文字チェックのみ。長さチェックが未実装。

### 修正が必要な箇所
`TodoService.java`の`validateTitle()`メソッドに以下を追加する必要があります：

```java
private void validateTitle(String title) {
    if (title == null || title.isEmpty()) {
        throw new IllegalArgumentException("タイトルは必須です");
    }
    // ↓ この行を追加
    if (title.length() > 200) {
        throw new IllegalArgumentException("タイトルは200文字以内です");
    }
}
```

修正後、完成度は100点になります。
```

**重要**: AIは「完成しました！」と報告していたが、実際には60点。点数で聞くことで正直に答える。

---

## Trust but Verify 3層検証

AIの「完成しました！」を信用せず、3層で検証する。

### Layer 1: 自動検証（AI不要）

コンパイル、テスト、静的解析ツールで機械的に検証。

**実行コマンド**:
```bash
# コンパイル
mvn compile

# テスト実行
mvn test

# 静的解析（CheckStyle、SpotBugs、PMD、JaCoCo）
mvn clean verify
```

**Pass基準**:
- コンパイルエラーなし
- 全テストパス
- CheckStyle、SpotBugs、PMDエラーなし
- カバレッジ80%以上

### Layer 2: AI自己検証

AIに自分の実装をレビューさせる。

#### 方法1: SelfCheckGPT方式

```
あなたが実装したTodoService.create()について、以下の観点でレビューしてください：
1. 受入条件を100%満たしているか？（0-100点で評価）
2. Cyclomatic Complexity 10以下か？
3. DRY原則に違反していないか？
4. エラーハンドリングは適切か？
5. JavaDocは記載されているか？

満たしていない点があれば、具体的に指摘し、修正案を提示してください。
```

#### 方法2: Repomix複数AI相互レビュー

Repomixでコードベースをパッケージング → Claude、ChatGPT、Geminiの3つのAIでレビュー → 相互に矛盾を指摘し合う。

詳細: knowledges/09-repomix-ai-code-review.md

### Layer 3: 人間レビュー

人間が以下をレビュー：
1. **ビジネスロジック**: AIが仕様を誤解していないか
2. **アーキテクチャ**: 設計原則に沿っているか
3. **Scope Creep検出**: `git diff`で、指示していない機能が追加されていないか

**`git diff`の活用**:
```bash
git diff --stat
git diff src/main/java/com/example/todo/service/TodoService.java
```

変更行数が想定より多い場合、Scope Creepの可能性。

---

## Refactor/Document工程での残作業ドキュメント化

サイクル終了後に、AIに「今後の改善すべき点」と「残作業」をドキュメント化させる。

### Claude Codeへの指示例

```
TodoService.create()の実装が完了しました。
以下の2つのドキュメントを作成してください：

1. docs/improvements/todo-service-improvements.md
   - 今後改善すべき点（パフォーマンス、保守性、テスタビリティ等）
   - 優先度付き（P0/P1/P2）

2. docs/remaining-tasks/todo-service-remaining.md
   - 実装が完了していない機能
   - 次のスプリントで対応すべきタスク
```

### AIの生成例

**docs/improvements/todo-service-improvements.md**:
```markdown
# TodoService 改善提案

## P0（即座に対応）
なし。現時点で重大な問題はなし。

## P1（今週中に対応）
1. **バリデーションロジックの共通化**
   - 現状：`validateTitle()`がTodoServiceにのみ存在
   - 問題：他のサービスで同じバリデーションを再実装する可能性
   - 提案：`ValidationUtils`クラスを作成し、共通バリデーションを集約

2. **エラーメッセージの国際化**
   - 現状：エラーメッセージが日本語ハードコード
   - 問題：英語圏ユーザーに対応できない
   - 提案：`messages.properties`でメッセージを外部化

## P2（来週以降に対応）
3. **パフォーマンス最適化**
   - 現状：`findAll()`で全件取得
   - 問題：データ量が増えると遅延
   - 提案：ページネーション実装

4. **監査ログ**
   - 現状：誰がいつTODOを作成したかの記録なし
   - 提案：`created_by`、`updated_by`カラム追加
```

**docs/remaining-tasks/todo-service-remaining.md**:
```markdown
# TodoService 残作業

## Phase 1（MVP）: 完了
✅ TODO作成機能（`create()`）
✅ 受入条件3つを満たす実装
✅ 単体テスト（カバレッジ80%以上）

## Phase 2（次のスプリント）: 未実装
- [ ] TODO一覧取得（`findAll()`）
- [ ] TODO更新（`update()`）
- [ ] TODO削除（`delete()`）
- [ ] ステータス変更（`updateStatus()`）
- [ ] 優先度変更（`updatePriority()`）

## Phase 3（将来）: 未定
- [ ] TODO検索（タイトル部分一致、ステータスフィルター、優先度フィルター）
- [ ] TODO一括削除
- [ ] TODO並び替え（作成日順、期限順、優先度順）
```

---

## 完成度検証のチェックリスト

各サイクル終了時に、以下をチェック：

### 1. AIに完成度を点数で答えさせる
- [ ] 「受入条件に対して、完成度を0-100点で評価して」と質問
- [ ] 80点未満の場合、未実装部分を修正
- [ ] 100点になるまで繰り返す

### 2. Layer 1（自動検証）
- [ ] `mvn compile` → エラーなし
- [ ] `mvn test` → 全テストパス
- [ ] `mvn verify` → CheckStyle、SpotBugs、PMDエラーなし
- [ ] カバレッジ80%以上

### 3. Layer 2（AI自己検証）
- [ ] AIに自己レビューさせる（SelfCheckGPT方式）
- [ ] または、Repomixで複数AI相互レビュー

### 4. Layer 3（人間レビュー）
- [ ] ビジネスロジックが正しいか確認
- [ ] `git diff`でScope Creep検出

### 5. 残作業ドキュメント化
- [ ] 改善提案ドキュメント作成（docs/improvements/）
- [ ] 残作業ドキュメント作成（docs/remaining-tasks/）

---

## AIの「完成しました！」に騙されないための心構え

### ❌ NGパターン：Trust but NOT Verify

```
開発者: TODO作成機能を実装して
AI: 完成しました！テストも全部通っています！
開発者: ありがとう！じゃあ次の機能に進もう
→ 後で発見：ハードコード実装だった
```

### ✅ OKパターン：Trust but Verify

```
開発者: TODO作成機能を実装して
AI: 完成しました！テストも全部通っています！
開発者: 受入条件に対して、完成度を0-100点で評価して
AI: 60点です。受入条件3つ目（タイトル長さチェック）が未実装です
開発者: じゃあ修正して
AI: 修正しました！
開発者: もう一度完成度を評価して
AI: 100点です。全ての受入条件を満たしています
開発者: `mvn test` 実行 → 全テストパス確認
開発者: `git diff` 確認 → Scope Creepなし確認
開発者: OK、次の機能に進もう
```

---

## まとめ

AIは「元気よく完成しました！」とうそをつくが、「完成度は？」と聞くと正直に答える。
この特性を理解し、Trust but Verify 3層検証を徹底することで、確実に完成させる。

さらに、Refactor/Document工程で残作業をドキュメント化することで：
- 次のスプリントで何をすべきか明確
- 技術的負債の可視化
- チームメンバー間での情報共有

「完成しました！」を信じず、「完成度は？」と聞く習慣が、AI駆動開発の成功の鍵。
