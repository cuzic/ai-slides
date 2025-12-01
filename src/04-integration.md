---
marp: true
theme: default
paginate: true
---

<style>
  /* フォントサイズバリエーション */
  /* 大きめ（10行程度） */
  section[data-class~="font-small"] {
    font-size: 24px !important;
    line-height: 1.3 !important;
  }
  section[data-class~="font-small"] h2, section[data-class~="font-small"] h3 {
    font-size: 36px !important;
  }

  /* 中程度（12-14行） */
  section[data-class~="font-xsmall"] {
    font-size: 21px !important;
    line-height: 1.25 !important;
  }
  section[data-class~="font-xsmall"] h2, section[data-class~="font-xsmall"] h3 {
    font-size: 32px !important;
  }

  /* やや小さめ（15-17行） */
  section[data-class~="font-xxsmall"] {
    font-size: 18px !important;
    line-height: 1.2 !important;
  }
  section[data-class~="font-xxsmall"] h2, section[data-class~="font-xxsmall"] h3 {
    font-size: 28px !important;
  }

  /* コンパクト（18行以上） */
  section[data-class~="font-xxxsmall"] {
    font-size: 16px !important;
    line-height: 1.15 !important;
  }
  section[data-class~="font-xxxsmall"] h2, section[data-class~="font-xxxsmall"] h3 {
    font-size: 24px !important;
  }
</style>

# Day 1 - 04 統合ハンズオン: STEP 1-5 完全実践

**対象者**: Java/Spring Boot経験者（AI駆動開発は初心者）
**学習目標**: STEP 1-5を通してTODO管理アプリを完成させ、AI駆動開発の全工程を実践する

---

## 統合ハンズオン

---
<!-- _class: font-xsmall -->

### 統合ハンズオンの目的と進め方
- 目的
  - STEP 1-5を一貫して実践し、AI駆動開発の全工程を体験
  - TODO管理アプリの完了状態変更機能を実装（Must have機能の追加）
  - 5-STEPワークフローの実践的な習得
- 進め方
  - STEP 1: 要件定義
  - STEP 2: 設計
  - STEP 3: タスク分解
  - STEP 4: TDD実装
  - STEP 5: リファクタリング
- 実装する機能
  - 完了状態変更機能（TODO管理の本質的機能）
  - ユーザーが完了したタスクをチェックし、やるべきことを管理できるようにする

---
<!-- _class: font-xsmall -->

### STEP 1: 要件定義
- ユーザーストーリーの作成
  - As a ユーザー
  - I want TODOの完了状態を変更できる（完了/未完了を切り替える）
  - So that 完了したタスクを記録し、やるべきことを管理できる
- MoSCoW分析の実施
  - Must have: 完了状態変更機能（TODO管理の本質）
  - Should have: 完了したTODOの視覚的表示（取り消し線など）
  - Could have: 完了率の表示
  - Won't have: 自動完了機能
- AIへの指示内容
  - ユーザーストーリーの妥当性検証
  - 受入基準の確認

---
<!-- _class: font-xxsmall -->

### STEP 2: 設計
- 画面設計
  - チェックボックスまたは完了ボタンの追加
  - 完了したTODOの視覚的表示（取り消し線、グレーアウト）
- 受入基準（AC）の定義
  - チェックボックスをクリックしてTODOを完了状態にできる
  - 完了したTODOは取り消し線で表示される
  - 完了したTODOを再度クリックして未完了に戻せる
- DBスキーマ更新
  - todos テーブルに completed カラム追加（BOOLEAN型）
  - デフォルト値: false（未完了）
- API設計
  - PATCH /api/todos/:id/status
  - リクエストボディ: { "completed": true/false }
- DoD（Definition of Done）の確認
  - 全テストケースが緑（80%以上カバレッジ）
  - 画面表示が正常動作
  - ドキュメント更新完了

---
<!-- _class: font-xxsmall -->

### STEP 3: タスク分解
- GitHub Issue作成
  - タイトル: 「完了状態変更機能実装」
  - 説明: ユーザーストーリーと受入基準を記載
- BDDテストシナリオの作成
  - GIVEN: 未完了のTODOが存在する
  - WHEN: チェックボックスをクリックする
  - THEN: TODOが完了状態になり、取り消し線で表示される
- 10分ルール適用によるタスク分割
  - Subtask 1: DBスキーマ更新（completed カラム追加）
  - Subtask 2: Service層の実装（完了状態変更ロジック）
  - Subtask 3: Controller層の実装（PATCH /api/todos/:id/status）
  - Subtask 4: 画面実装（チェックボックス追加、取り消し線表示）
- タスク分割の効果
  - 各タスクが10分以内で完了可能
  - Scope Creep防止

---
<!-- _class: font-xsmall -->

### STEP 4: TDD実装
- TDDサイクルの実践
  - Red: テストを書いて失敗させる
  - Green: 最小限のコードで通す
  - Refactor: コード改善
  - Verify: 3段階レビューで検証
- 3段階レビューの適用
  - Layer 1: 自動検証（テスト実行、カバレッジ確認）
  - Layer 2: AI自己検証（コード品質チェック、完成度評価）
  - Layer 3: Scope Creep検出（git diff確認）
- 実装の進め方
  - Subtask単位で実装
  - 各Subtask完了後に3段階レビュー実施
- 実装例
  - completed カラム追加 → テスト → 完了状態変更メソッド → テスト → API → テスト → UI

---
<!-- _class: font-xxsmall -->

### STEP 5: リファクタリング
- 8つの質問と指示でAIに任せる
  - ①技術的負債はないか？
  - ②冗長・重複・dead codeがないか？
  - ③循環的複雑度は適切か？
  - ④ライブラリを活用できないか？
  - ⑤デザインパターンを活用できないか？
  - ⑥JavaDocは適切か？
  - ⑦ADRは更新したか？
  - ⑧今回の知見を保存したか？
- 完成度検証の実施
  - AIに「今回のリファクタリングの完成度を0-100点で評価して」と指示
  - 100点になるまで改善を繰り返す
  - 改善点が明確な場合は追加指示
- タスク完了後の処理
  - `/clear` コマンドでコンテキストクリア
  - 次のタスクへ移行

---
<!-- _class: font-xsmall -->

## 【総合復習クイズ】Day 1の理解度確認

### 問題：次の文章が正しければ〇、間違っていれば×をつけてください

1. **「5-STEPワークフローは、要件定義→タスク分解→設計→実装→品質改善の順である」**
2. **「AIの5特性は、暴走、手抜き、忘れっぽさ、凸凹知能、虚偽報告である」**
3. **「7段階TDDは、Plan→Red→Green→Refactor→System→AI→Humanの順である」**
4. **「/clearコマンドは、タスク完了後にコンテキスト汚染を防ぐために実行する」**
5. **「MoSCoW分析では、Must haveに全機能の50-60%を含めるべきである」**

### 答え
1. **×** - 正しくは「要件定義→**設計**→**タスク分解**→実装→品質改善」
2. **〇** - AIの5特性を理解して対策すれば、AIは強力なパートナーになる
3. **〇** - 従来の3段階TDD（Red-Green-Refactor）にPlanと3段階レビューを追加
4. **〇** - /clearでコンテキストをリセットし、次のタスクを新鮮な状態で開始
5. **×** - Must haveは20-30%。スコープを絞ることで品質を確保

---
<!-- _class: font-xxsmall -->

### まとめと振り返り
- 完成した成果物
  - 動作するコード（完了状態変更機能）
  - テスト（カバレッジ80%以上）
  - 設計書（受入基準、DBスキーマ）
  - ドキュメント（JavaDoc、ADR）
  - 1 commit（全変更をまとめてコミット）
- Must have機能を実装できた
  - TODO管理の本質的機能（完了/未完了の切り替え）
  - ユーザーストーリーの価値を実現
  - MoSCoW分析で優先順位を正しく判断
- AI駆動開発の成功要因（復習）
  - 5-STEPワークフローの確実な実践
  - AIの特性理解（暴走、手抜き、忘れっぽさ、凸凹知能、虚偽報告）
  - ガードレール（事前防止）
  - 3段階レビュー（事後検証）
  - ツール分離戦略（Claude WEB、Claude Code）
- 今後の学習
  - Day 2: 保守開発（リバースエンジニアリング + テスト + 保守開発）

---

## 参考資料

### 5-STEPワークフロー全体
- knowledges/30-ai-context-guardrails-verify.md - 5-STEPワークフロー全体像

### AI特性と対処法
- knowledges/34-ai-driven-development-problems.md - AI特性5つ
- knowledges/19-guardrails.md - ガードレール
- knowledges/18-trust-but-verify.md - 3段階レビュー

### 各ステップの詳細
- knowledges/23-user-story-writing.md - ユーザーストーリー作成
- knowledges/24-acceptance-criteria.md - 受入基準定義
- knowledges/25-task-decomposition.md - タスク分解
- knowledges/01-given-when-then-bdd.md - BDDテストシナリオ
- knowledges/02-test-driven-development-tdd.md - TDD

### ツールと戦略
- knowledges/36-ai-tools-separation-strategy.md - AIツール分離戦略
- knowledges/33-ai-context-documentation-importance.md - コンテキストの重要性

### ドキュメント
- knowledges/26-arc42-c4-adr.md - ADR（アーキテクチャ決定記録）
- knowledges/11-living-documentation.md - リビングドキュメント
- knowledges/40-optimal-documentation-for-ai-driven-development.md - 最適なドキュメント
