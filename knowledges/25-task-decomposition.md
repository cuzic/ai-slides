# 25. タスク分解とトークン制限への対応

**最終更新**: 2025-01-07
**カテゴリ**: 開発手法・プラクティス（タスク分解フェーズ）
**難易度**: ⭐⭐⭐ (中級)

## 📋 目次

1. [概要](#概要)
2. [タスク分解とは](#タスク分解とは)
3. [AI開発における3つの問題](#ai開発における3つの問題)
4. [Context Window（トークン制限）の課題](#context-windowトークン制限の課題)
5. [タスク分解の基本原則](#タスク分解の基本原則)
6. [タスク分解の方法論](#タスク分解の方法論)
7. [AI駆動開発でのタスク分解ワークフロー](#ai駆動開発でのタスク分解ワークフロー)
8. [トークン制限への対応戦略](#トークン制限への対応戦略)
9. [Java/Spring Boot開発での実例](#javaspring-boot開発での実例)
10. [ベストプラクティス](#ベストプラクティス)
11. [アンチパターン](#アンチパターン)
12. [まとめ](#まとめ)
13. [参考資料](#参考資料)

---

## 概要

### タスク分解とは

**タスク分解（Task Decomposition）**は、大きなユーザーストーリーやEpicを、実装可能な小さなタスクに分割するプロセスです。

**例**:
```
Epic: ECサイトの商品購入機能

↓ タスク分解

US-001: 商品一覧表示（1〜2日）
US-002: 商品検索（1〜2日）
US-003: カート追加（1〜2日）
US-004: カート確認（1〜2日）
US-005: 注文手続き（2〜3日）
```

### なぜ必要か

1. **見積もり精度の向上**
   - 「商品購入機能を作って」→ 見積もれない
   - 「カート追加機能（1〜2日）」→ 見積もれる

2. **並行開発が可能**
   - US-001とUS-002を別の開発者が同時に実装

3. **リスク分散**
   - US-003で問題が発生しても、US-001/US-002は完成している

4. **AI開発の3つの問題に対応**
   - **暴走（Scope Creep）**: 小さく分割することで実装範囲を明確化
   - **手抜き（Reward Hacking）**: 受入条件で完了判定を明確化
   - **忘れっぽさ（Context Limitations）**: トークン制限に対応

---

## タスク分解とは

### 定義

**タスク分解**は、以下の階層構造で機能を分割します：

```
Initiative（戦略目標）
  ↓
Epic（大きな機能群、数週間〜数ヶ月）
  ↓
User Story（小さな機能、1〜3日）
  ↓
Task（実装単位、数時間〜1日）
  ↓
Subtask（さらに細かい作業、30分〜数時間）
```

### 各階層の例

#### Initiative（戦略目標）
```
「2025年Q1にECサイトのコンバージョン率を15%向上させる」
```

#### Epic（大きな機能群）
```
Epic 1: 商品購入機能
Epic 2: 会員管理機能
Epic 3: レコメンデーション機能
```

#### User Story（小さな機能）
```
Epic 1: 商品購入機能
  ├── US-001: 商品一覧表示
  ├── US-002: 商品検索
  ├── US-003: カート追加
  ├── US-004: カート確認
  └── US-005: 注文手続き
```

#### Task（実装単位）
```
US-003: カート追加
  ├── Task 1: CartController実装
  ├── Task 2: CartService実装
  ├── Task 3: Cart/CartItemエンティティ実装
  ├── Task 4: カート追加ボタンのUI実装（Thymeleaf）
  └── Task 5: E2Eテスト作成（Playwright）
```

---

## AI開発における3つの問題

### 1. 暴走（Scope Creep）

**問題**: AIが指示していない機能を勝手に実装

**タスク分解による対策**:
```
❌ 悪い例: 「商品購入機能を作って」
→ AIが決済、クーポン、ポイント、レコメンデーション...すべて実装

✅ 良い例: 「US-003: カート追加機能のみ実装してください」
→ カート追加のみ実装、他は実装しない
```

**具体例**:
```
US-003: カート追加

実装範囲:
- カート追加ボタン
- カートバッジ数更新
- トースト通知

実装しないこと:
- 決済機能（US-010で別途実装）
- クーポン機能（US-011で別途実装）
- ポイント機能（US-012で別途実装）
```

### 2. 手抜き（Reward Hacking）

**問題**: AIが最低限の実装だけして「完了しました」と報告

**タスク分解による対策**:
```
❌ 悪い例: 「カート機能を作って」
→ AIがボタンだけ作って完了

✅ 良い例: 受入条件を詳細に記載
「US-003の受入条件（docs/user-stories/US-003-cart-add.md）を
すべて満たしてください」
```

**受入条件例**:
```
US-003: カート追加

受入条件:
✓ カート追加ボタンをクリックすると、バッジ数が+1される
✓ トースト通知「カートに追加しました」が3秒間表示される
✓ 同じ商品を再度追加すると、数量が+1される
✓ 在庫切れ商品は「カートに追加」ボタンが無効化される
✓ カート追加処理が0.5秒以内に完了する
```

→ すべての条件を満たさないと完了にならない。

### 3. 忘れっぽさ（Context Limitations）

**問題**: トークン制限でCompact後、情報が失われる

**タスク分解による対策**:
```
小さいタスクに分割 → トークン消費を削減
+ Git管理で外部化 → Compact後も参照可能
```

**例**:
```
docs/
├── user-stories/
│   ├── US-001-product-list.md
│   ├── US-002-product-search.md
│   └── US-003-cart-add.md
├── adr/
│   └── 0001-use-spring-boot.md
└── tasks/
    ├── TASK-001-cart-controller.md
    └── TASK-002-cart-service.md
```

→ Compact後も「docs/user-stories/US-003-cart-add.md を参照してください」で復元。

---

## Context Window（トークン制限）の課題

### トークンとは

**トークン**は、AIモデルが処理するテキストの最小単位です。

**トークン数の目安**:
```
英語: 1単語 ≒ 1.3トークン
日本語: 1文字 ≒ 2〜3トークン

例: "Hello, world!" ≒ 3トークン
例: "こんにちは、世界！" ≒ 20トークン
```

### Context Window（コンテキストウィンドウ）

**Context Window**は、AIが一度に処理できるトークン数の上限です。

**主要モデルのContext Window**（2025年1月時点）:
```
GPT-4 Turbo:     128,000トークン
Claude 3.5 Sonnet: 200,000トークン
Gemini 1.5 Pro:  1,000,000トークン
```

**Claude Codeの場合**:
```
入力（プロンプト + コードベース + 会話履歴） + 出力 ≤ 200,000トークン
```

### トークン制限の影響

**問題**:
```
長い会話 → トークン上限に達する
→ Compact（要約）が実行される
→ 古い情報が失われる
```

**具体例**:
```
会話1: 「商品一覧機能を実装してください」
会話2: 「商品検索機能を実装してください」
会話3: 「カート機能を実装してください」
...
会話50: トークン上限に達する
→ Compact実行
→ 会話1〜10の情報が失われる
→ AIが「商品一覧機能の仕様」を忘れる
```

### トークン消費の内訳

**Claude Codeの会話例**:
```
会話1: ユーザープロンプト（500トークン）+ AI応答（2,000トークン）= 2,500トークン
会話2: プロンプト（700トークン）+ 応答（3,000トークン）= 3,700トークン
会話3: プロンプト（1,000トークン）+ 応答（5,000トークン）= 6,000トークン
...
累積: 150,000トークン → 上限200,000トークンに近づく
```

---

## タスク分解の基本原則

### 1. INVEST原則（ユーザーストーリー）

ユーザーストーリーレベルでは**INVEST原則**を適用：

- **I**ndependent（独立している）
- **N**egotiable（交渉可能）
- **V**aluable（価値がある）
- **E**stimable（見積り可能）
- **S**mall（小さい、1〜3日）
- **T**estable（テスト可能）

### 2. タスクサイズの目安

| レベル | サイズ | 期間 | トークン消費 |
|-------|--------|------|------------|
| Epic | 数週間〜数ヶ月 | - | - |
| User Story | 1〜3日 | - | 中（10,000〜30,000トークン/ストーリー） |
| Task | 数時間〜1日 | - | 小（2,000〜10,000トークン/タスク） |
| Subtask | 30分〜数時間 | - | 極小（500〜2,000トークン/サブタスク） |

### 3. トークン消費を意識した分割

**大きすぎるタスク**:
```
❌「ECサイトの全機能を実装してください」
→ トークン消費: 100,000トークン以上
→ Compactのリスク大
```

**適切なサイズ**:
```
✅「US-003: カート追加機能を実装してください」
→ トークン消費: 10,000〜20,000トークン
→ Compactのリスク小
```

### 4. 段階的コンテキスト構築

**Progressive Context Building**:
```
Phase 1: 必須情報のみ読み込み（ユーザーストーリー、受入条件）
  ↓
Phase 2: 実装開始、詳細情報を追加（API仕様、DB設計）
  ↓
Phase 3: テスト、さらに詳細情報（E2Eシナリオ）
```

→ 最初から全情報を読み込まない。

---

## タスク分解の方法論

### 1. ユーザーストーリー分割パターン

#### パターン1: 機能による分割

**Epic**: 商品購入機能

```
US-001: 商品一覧表示
US-002: 商品検索
US-003: カート追加
US-004: カート確認
US-005: 注文手続き
```

#### パターン2: CRUD操作による分割

**Epic**: 会員管理機能

```
US-010: 会員登録（Create）
US-011: 会員情報表示（Read）
US-012: 会員情報更新（Update）
US-013: 会員退会（Delete）
```

#### パターン3: ユーザージャーニーによる分割

**Epic**: 注文処理

```
US-020: 配送先入力
US-021: 配送方法選択
US-022: 支払い方法選択
US-023: 注文確認
US-024: 注文確定
```

#### パターン4: データによる分割

**Epic**: レポート機能

```
US-030: 日次売上レポート
US-031: 週次売上レポート
US-032: 月次売上レポート
US-033: 年次売上レポート
```

### 2. タスク分割パターン

#### パターン1: レイヤーによる分割

**US-003**: カート追加

```
Task 1: Controller層（CartController#addItem）
Task 2: Service層（CartService#addItem）
Task 3: Repository層（CartRepository）
Task 4: Entity（Cart, CartItem）
Task 5: View層（Thymeleaf テンプレート）
Task 6: テスト（E2Eテスト）
```

#### パターン2: 機能コンポーネントによる分割

**US-003**: カート追加

```
Task 1: カート追加ボタンUI
Task 2: バッジ数更新ロジック
Task 3: トースト通知表示
Task 4: 在庫チェック
Task 5: 重複チェック（数量+1）
```

#### パターン3: テストシナリオによる分割

**US-003**: カート追加

```
Task 1: 正常系（初回追加）の実装
Task 2: 正常系（重複追加、数量+1）の実装
Task 3: 異常系（在庫切れ）の実装
Task 4: 異常系（未ログイン）の実装
Task 5: 境界値（数量上限99）の実装
```

### 3. ストーリー分割の原則

**nikkie-ftnext氏の記事**より:

> 「ユーザーストーリーをタスクに分解しないための考え方」

**ストーリー分割 ≠ タスク分割**:
```
❌ 悪い分割（タスクになっている）:
US-001: データベーステーブル作成
US-002: API実装
US-003: UI実装

✅ 良い分割（ストーリーとして価値がある）:
US-001: 商品一覧表示（エンドユーザーへの価値）
US-002: 商品検索（エンドユーザーへの価値）
US-003: カート追加（エンドユーザーへの価値）
```

---

## AI駆動開発でのタスク分解ワークフロー

### フェーズ1: 要件定義（ユーザーストーリー作成）

**アクティビティ**:
1. Epicを定義
2. ユーザーストーリーに分割（INVEST原則）
3. ストーリーマッピング

**成果物**:
```
docs/user-stories/
├── README.md（全ストーリー一覧）
├── Epic-01-product-purchase.md
├── US-001-product-list.md
├── US-002-product-search.md
└── US-003-cart-add.md
```

**トークン消費**: 中程度（ストーリー作成時）

### フェーズ2: 設計（受入基準作成）

**アクティビティ**:
1. 各ストーリーの受入基準を箇条書きで作成
2. 受入基準をGIVEN WHEN THEN形式に変換
3. チェックリスト作成

**成果物**:
```
docs/user-stories/US-003-cart-add.md:
  - ユーザーストーリー
  - 受入基準（チェックリスト形式）
  - 詳細シナリオ（Given-When-Then形式）
```

**トークン消費**: 中程度（詳細化のため）

### フェーズ3: タスク分解

**アクティビティ**:
1. ユーザーストーリーをタスクに分割
2. タスクサイズを確認（数時間〜1日）
3. 依存関係を整理

**成果物**:
```
docs/tasks/
├── US-003/
│   ├── TASK-001-cart-controller.md
│   ├── TASK-002-cart-service.md
│   ├── TASK-003-cart-entity.md
│   ├── TASK-004-cart-ui.md
│   └── TASK-005-cart-e2e-test.md
```

**トークン消費**: 小（タスクごとに実装）

### フェーズ4: 実装（TDD）

**アクティビティ**:
1. タスクごとに実装
2. E2Eテスト自動生成（受入基準から）
3. Red-Green-Refactorサイクル

**Claude Codeプロンプト例**:
```
「TASK-001: CartController実装

参照:
- docs/user-stories/US-003-cart-add.md（受入条件）
- docs/tasks/US-003/TASK-001-cart-controller.md（詳細仕様）

要件:
- CartController#addItem() メソッドを実装
- 受入条件のScenario 1〜3を満たすこと
- 単体テストを作成

実装しないこと:
- CartService（TASK-002で別途実装）
- UI（TASK-004で別途実装）
」
```

**トークン消費**: 小（タスクごと、2,000〜10,000トークン）

---

## トークン制限への対応戦略

### 戦略1: タスクを小さく分割

**効果**: トークン消費を削減

**実践例**:
```
❌ 大きいタスク（トークン消費: 50,000）:
「商品購入機能を実装してください」
→ Compactのリスク大

✅ 小さいタスク（トークン消費: 10,000×5回）:
「US-001: 商品一覧表示を実装してください」
「US-002: 商品検索を実装してください」
「US-003: カート追加を実装してください」
...
→ Compactのリスク小
```

### 戦略2: 階層的タスク分解

**Speaker Deck「失敗しないAIエージェント開発」より**:

```
Level 1: Epic（戦略目標）
  ↓ 分解
Level 2: User Story（機能単位）
  ↓ 分解
Level 3: Task（実装単位）
  ↓ 分解
Level 4: Subtask（コード単位）
```

→ 各レベルでトークン消費を管理。

### 戦略3: Git管理による外部化

**効果**: Compact後も情報を復元可能

**ディレクトリ構成**:
```bash
プロジェクトルート/
├── docs/
│   ├── user-stories/      # ユーザーストーリー
│   ├── acceptance-criteria/ # 受入基準
│   ├── tasks/             # タスク詳細
│   ├── adr/               # 技術的決定
│   └── screens/           # 画面設計
├── CLAUDE.md              # プロジェクト概要
└── .claude/
    └── commands/          # カスタムコマンド
```

**Compact後の復元**:
```
「docs/user-stories/US-003-cart-add.md を参照して、
カート追加機能を実装してください。」
```

### 戦略4: 段階的コンテキスト構築

**zenn記事「AIエージェントエンジニア必須」より**:

**トークン消費70%削減**の手法:

1. **必要な情報だけを読み込む**
   ```
   ❌ 全ファイルを読み込む（トークン消費: 100,000）
   ✅ 必要なファイルのみ（トークン消費: 30,000）
   ```

2. **RAG（Retrieval-Augmented Generation）活用**
   ```
   必要な情報をベクトル検索で取得
   → Context Windowに含める
   ```

3. **インテリジェントサマリゼーション**
   ```
   長いドキュメントを要約
   → 核心部分のみ保持
   → トークン消費削減
   ```

### 戦略5: フェーズごとにコンテキストをハンドオフ

**Factory.ai「Context Window Problem」より**:

```
Phase 1: 設計フェーズ
  - コンテキスト: ユーザーストーリー、受入条件
  - 成果物: 設計書（docs/design/）
  ↓ コンテキストハンドオフ
Phase 2: 実装フェーズ
  - コンテキスト: 設計書、タスク詳細
  - 成果物: コード
  ↓ コンテキストハンドオフ
Phase 3: テストフェーズ
  - コンテキスト: 受入条件、コード
  - 成果物: E2Eテスト
```

→ 各フェーズで明示的にコンテキストを引き継ぐ。

### 戦略6: AIツールによる自動分解

**goblin.tools「Magic ToDo」**:

```
入力: 「ECサイトの商品購入機能を実装」

↓ AIが自動分解

出力:
1. 商品一覧表示機能
   1.1 データベースから商品取得
   1.2 商品リストをHTMLで表示
   1.3 ページネーション実装
2. 商品検索機能
   2.1 検索バーUI作成
   2.2 キーワード検索ロジック
   2.3 検索結果表示
3. カート追加機能
   ...
```

---

## Java/Spring Boot開発での実例

### ケーススタディ: ECサイト開発

#### Epic: 商品購入機能

**トークン消費の見積もり**:
```
全体実装（一度に）: 100,000トークン
→ Compactのリスク大

タスク分解後: 10,000トークン × 10ストーリー
→ Compactのリスク小
```

#### タスク分解の実例

**US-003: カート追加機能**

```markdown
# US-003: カート追加

## タスク分解

### TASK-001: CartController実装（2時間）
**実装内容**:
- `@PostMapping("/cart/add")` を実装
- リクエストパラメータ: `productId`, `quantity`
- レスポンス: JSON `{"success": true, "cartCount": 3}`

**受入条件**:
- POST /cart/add を呼び出すと、カートに商品が追加される
- レスポンスにカート件数が含まれる

**トークン消費見積もり**: 2,000〜5,000トークン

### TASK-002: CartService実装（3時間）
**実装内容**:
- `CartService#addItem(Long userId, Long productId, Integer quantity)` を実装
- 在庫チェック（ProductService連携）
- 重複チェック（既存カートアイテムの数量+1）
- 数量上限チェック（99個まで）

**受入条件**:
- 在庫がない場合、`OutOfStockException` をスロー
- 同じ商品を追加した場合、数量が+1される
- 数量上限99個を超える場合、`QuantityLimitExceededException` をスロー

**トークン消費見積もり**: 3,000〜7,000トークン

### TASK-003: Cart/CartItemエンティティ実装（2時間）
**実装内容**:
- `Cart.java` エンティティ作成（@Entity, @OneToMany）
- `CartItem.java` エンティティ作成（@ManyToOne）
- `CartRepository` インターフェース作成

**受入条件**:
- CartとCartItemが1対多の関係
- userId、productId、quantityがカラムに含まれる

**トークン消費見積もり**: 2,000〜4,000トークン

### TASK-004: カート追加ボタンUI実装（3時間）
**実装内容**:
- products/detail.html にカート追加ボタン追加
- JavaScriptで非同期API呼び出し（fetch）
- バッジ数更新
- トースト通知表示（Bootstrap Toast）

**受入条件**:
- カート追加ボタンをクリックすると、バッジ数が+1される
- トースト通知「カートに追加しました」が3秒間表示される

**トークン消費見積もり**: 3,000〜6,000トークン

### TASK-005: E2Eテスト実装（2時間）
**実装内容**:
- Playwright E2Eテスト作成
- Scenario 1〜6（受入条件）をテストケース化

**受入条件**:
- 受入条件のすべてのシナリオがテストでパスする

**トークン消費見積もり**: 2,000〜5,000トークン
```

**合計トークン消費**: 12,000〜27,000トークン（タスクごとに分散）

#### Claude Codeへのプロンプト（タスクごと）

**TASK-001の実装**:
```
「TASK-001: CartController実装

参照:
- docs/user-stories/US-003-cart-add.md（受入条件）
- docs/tasks/US-003/TASK-001-cart-controller.md（詳細仕様）

要件:
- @PostMapping("/cart/add") を実装
- リクエストパラメータ: productId, quantity
- レスポンス: JSON {"success": true, "cartCount": 3}
- CartService#addItem() を呼び出す（モックで実装、TASK-002で本実装）

実装しないこと:
- CartService（TASK-002で別途実装）
- UI（TASK-004で別途実装）
- E2Eテスト（TASK-005で別途実装）

テスト:
- 単体テスト（MockMvcでPOSTリクエストテスト）を作成してください
」
```

→ トークン消費: 2,000〜5,000トークン

**TASK-002の実装**（次の会話）:
```
「TASK-002: CartService実装

参照:
- docs/user-stories/US-003-cart-add.md（受入条件）
- docs/tasks/US-003/TASK-002-cart-service.md（詳細仕様）

要件:
- CartService#addItem() を実装
- 在庫チェック（ProductServiceから在庫数取得、0の場合は例外）
- 重複チェック（既存カートアイテムがあれば数量+1）
- 数量上限チェック（99個まで）

例外:
- OutOfStockException（在庫切れ）
- QuantityLimitExceededException（数量上限超過）

テスト:
- 単体テスト（JUnit + Mockito）を作成してください
」
```

→ トークン消費: 3,000〜7,000トークン

→ **各タスクを別の会話で実装することで、トークン消費を分散**。

---

## ベストプラクティス

### 1. 1タスク = 数時間〜1日

**理由**: 小さく分割することでトークン消費を削減

**例**:
```
✅ TASK-001: CartController実装（2時間）
✅ TASK-002: CartService実装（3時間）

❌ TASK-001: カート機能全実装（3日）
```

### 2. タスク間の依存関係を最小化

**INVEST原則のI（Independent）**:

```
✅ 良い例: TASK-001とTASK-004は並行実装可能
TASK-001: CartController（モックでService呼び出し）
TASK-004: カート追加ボタンUI（APIはモック）

❌ 悪い例: TASK-001→TASK-002→TASK-003の順番でしか実装できない
```

### 3. 受入条件をタスクに紐付ける

**例**:
```
US-003: カート追加

受入条件:
✓ カート追加ボタンをクリックすると、バッジ数が+1される ← TASK-004で実装
✓ トースト通知が表示される ← TASK-004で実装
✓ 同じ商品を再度追加すると、数量が+1される ← TASK-002で実装
✓ 在庫切れ商品はボタンが無効化される ← TASK-002 + TASK-004で実装
```

### 4. Git管理で外部化

**ディレクトリ構成**:
```bash
docs/
├── user-stories/
│   └── US-003-cart-add.md（ユーザーストーリー + 受入条件）
└── tasks/
    └── US-003/
        ├── TASK-001-cart-controller.md
        ├── TASK-002-cart-service.md
        ├── TASK-003-cart-entity.md
        ├── TASK-004-cart-ui.md
        └── TASK-005-cart-e2e-test.md
```

### 5. 段階的コンテキスト構築

**Phase 1: 設計**
```
読み込み: US-003-cart-add.md のみ
トークン消費: 1,000〜2,000トークン
```

**Phase 2: 実装**
```
読み込み: TASK-001-cart-controller.md
トークン消費: 2,000〜5,000トークン
```

**Phase 3: テスト**
```
読み込み: US-003-cart-add.md（受入条件）
トークン消費: 2,000〜5,000トークン
```

→ 各フェーズで必要な情報のみ読み込む。

### 6. 定期的なCompactとリマインダー

**Compactのタイミング**:
```
トークン消費が150,000を超えたら:
1. 重要な決定事項をADRに記録
2. CLAUDE.mdを更新
3. Compactを実行
4. 次の会話で「docs/adr/0001-use-spring-boot.md を参照してください」
```

---

## アンチパターン

### アンチパターン1: 大きすぎるタスク

**Bad**:
```
TASK-001: カート機能全実装（3日）
```

→ トークン消費: 50,000トークン以上、Compactのリスク大

**Good**:
```
TASK-001: CartController実装（2時間）
TASK-002: CartService実装（3時間）
TASK-003: Cart/CartItemエンティティ実装（2時間）
TASK-004: カート追加ボタンUI実装（3時間）
TASK-005: E2Eテスト実装（2時間）
```

→ トークン消費: 2,000〜7,000トークン/タスク

### アンチパターン2: 技術的タスクに分解（価値がない）

**Bad**:
```
US-001: データベーステーブル作成
US-002: API実装
US-003: UI実装
```

→ ユーザーへの価値がない（技術的タスク）

**Good**:
```
US-001: 商品一覧表示（エンドユーザーへの価値）
US-002: 商品検索（エンドユーザーへの価値）
US-003: カート追加（エンドユーザーへの価値）
```

### アンチパターン3: 依存関係が強すぎる

**Bad**:
```
TASK-001: データベーステーブル作成
  ↓（TASK-001完了後のみ実行可能）
TASK-002: Repository実装
  ↓（TASK-002完了後のみ実行可能）
TASK-003: Service実装
```

→ 並行開発不可

**Good**:
```
TASK-001: CartController実装（Serviceはモック）
TASK-002: CartService実装（Repositoryはモック）
TASK-003: Cart/CartItemエンティティ実装
TASK-004: カート追加ボタンUI（APIはモック）
```

→ 並行開発可能

### アンチパターン4: トークン制限を無視

**Bad**:
```
「商品購入機能、会員管理機能、レコメンデーション機能をすべて実装してください」
```

→ トークン消費: 200,000トークン以上、確実にCompact

**Good**:
```
「US-003: カート追加機能のみ実装してください」
```

→ トークン消費: 10,000〜20,000トークン

---

## まとめ

### タスク分解の重要ポイント

1. **AI開発の3つの問題に対応**
   - 暴走（Scope Creep）: 小さく分割で実装範囲明確化
   - 手抜き（Reward Hacking）: 受入条件で完了判定明確化
   - 忘れっぽさ（Context Limitations）: トークン消費削減 + Git外部化

2. **トークン制限への対応**
   - 小さく分割（1タスク = 2,000〜10,000トークン）
   - 段階的コンテキスト構築
   - Git管理で外部化

3. **階層的分解**
   - Epic → User Story → Task → Subtask
   - 各レベルでトークン消費を管理

### 開発フェーズでの位置づけ

```
要件定義フェーズ:
1. ユーザーストーリー作成（23-user-story-writing.md）
   ↓
設計フェーズ:
2. 受入基準を箇条書きでまとめ（24-acceptance-criteria.md）
   ↓
タスク分解フェーズ:
3. タスク分解とトークン制限への対応（本記事）
   ↓ GIVEN WHEN THEN形式のBDDテストシナリオ定式化（01-given-when-then-bdd.md）
   ↓
実装フェーズ:
4. TDD（02-test-driven-development-tdd.md）
5. Trust but Verify（18-trust-but-verify.md）
```

---

## 参考資料

### 公式ドキュメント・ガイド

1. **Context Window Management**
   - [How to Solve AI Context Window Limitations - Complete Tutorial](https://zenvanriel.nl/ai-engineer-blog/solve-ai-context-window-limitations-tutorial/)
   - [The Context Window Problem: Scaling Agents Beyond Token Limits](https://factory.ai/news/context-window-problem) - Factory.ai
   - [Context Window Management: Maximizing AI Memory for Complex Tasks](https://blog.qolaba.ai/ai-tools-by-qolaba/context-window-management-maximizing-ai-memory-for-complex-tasks/) - Qolaba AI

2. **Tokens and Context Windows**
   - [What Are AI Tokens and Context Windows (And Why Should You Care)?](https://simple.ai/p/tokens-and-context-windows)
   - [Understanding Context Windows and Token Limits | Cursor & Claude Code](https://developertoolkit.ai/en/shared-workflows/context-management/context-windows/)
   - [Advanced ChatGPT: Context Window Limits and Prompt Engineering](https://www.o8.agency/blog/ai/advanced-chatgpt-context-windows-and-prompt-engineering) - O8

### 技術記事・ブログ

3. **タスク分解手法**
   - [失敗しないAIエージェント開発：階層的タスク分解の実践](https://speakerdeck.com/kworkdev/developing-ai-agents-without-failure) - Speaker Deck
   - [ChatGPTを使用したAIエージェントを活用するためのタスク分解術](https://zenn.dev/ktrszk/articles/a906854a6162fe) - Zenn
   - [生成AIと行うタスク分解の新時代](https://note.com/solobizjourney/n/n538d7161fba3) - note

4. **トークン最適化**
   - [【AIエージェントエンジニア必須】トークン消費70%削減！最新コンテキスト最適化技術の全手法](https://zenn.dev/taku_sid/articles/20250404_token_saving) - Zenn
   - [ChatGPTの文字数制限とは？回避テクニックとトークンについて解説](https://weel.co.jp/media/innovator/chatgpt-character-limit/) - WEEL

5. **AI駆動開発**
   - [AI駆動開発入門！具体的なタスクの進め方【全ツール対応】](https://eiji.page/blog/ai-coding-prompt-2025-05-31/) - eiji.page
   - [I tried using 'Magic ToDo', a task management tool that can be used for free and automatically subdivides tasks using AI](https://gigazine.net/gsc_news/en/20250326-magic-todo) - GIGAZINE

6. **ストーリー分割**
   - [ユーザストーリーをタスクに分解しないための考え方をさがして](https://nikkie-ftnext.hatenablog.com/entry/how-to-split-user-stories-not-split-into-tasks-202305) - nikkie-ftnext

### 関連トピック

- [01. GIVEN WHEN THEN - BDD形式の受入条件](./01-given-when-then-bdd.md)
- [02. Test Driven Development (TDD)](./02-test-driven-development-tdd.md)
- [13. Reward Hacking in AI](./13-reward-hacking-ai.md)
- [16. AI Scope Creep（暴走）](./16-ai-scope-creep.md)
- [17. Context Limitations（忘れっぽさ）](./17-context-limitations.md)
- [18. Trust but Verify（任せる＆確かめる）](./18-trust-but-verify.md)
- [23. ユーザーストーリーの書き方](./23-user-story-writing.md)
- [24. 受入基準とチェックリスト](./24-acceptance-criteria.md)

---

**次のトピック**: 実装・TDDフェーズ（[02. Test Driven Development](./02-test-driven-development-tdd.md)）
**前のトピック**: [24. 受入基準とチェックリスト](./24-acceptance-criteria.md)

---

**📝 更新履歴**:
- 2025-01-07: 初版作成（WEB検索による最新情報反映）
