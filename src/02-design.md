---
marp: true
theme: default
paginate: true
---

<style>

  /* フォントサイズバリエーション */
  section[data-class~="font-large"] {
    font-size: 28px !important;
    line-height: 1.5 !important;
  }
  section[data-class~="font-large"] h2 {
    font-size: 42px !important;
  }

  section[data-class~="font-medium"] {
    font-size: 22px !important;
    line-height: 1.4 !important;
  }

  section[data-class~="font-small"] {
    font-size: 18px !important;
    line-height: 1.25 !important;
    padding: 15px 25px !important;
  }
  section[data-class~="font-small"] h2, section[data-class~="font-small"] h3 {
    font-size: 26px !important;
    margin-bottom: 0.2em !important;
  }
  section[data-class~="font-small"] li {
    margin-bottom: 0.05em !important;
  }
  section[data-class~="font-small"] p {
    margin-bottom: 0.2em !important;
  }

  section[data-class~="font-xsmall"] {
    font-size: 16px !important;
    line-height: 1.15 !important;
    padding: 12px 22px !important;
  }
  section[data-class~="font-xsmall"] h2, section[data-class~="font-xsmall"] h3 {
    font-size: 22px !important;
    margin-bottom: 0.15em !important;
  }
  section[data-class~="font-xsmall"] li {
    margin-bottom: 0.02em !important;
  }
  section[data-class~="font-xsmall"] p {
    margin-bottom: 0.1em !important;
  }

  section[data-class~="font-xxsmall"] {
    font-size: 14px !important;
    line-height: 1.1 !important;
    padding: 10px 20px !important;
  }
  section[data-class~="font-xxsmall"] h2, section[data-class~="font-xxsmall"] h3 {
    font-size: 20px !important;
    margin-bottom: 0.1em !important;
  }
  section[data-class~="font-xxsmall"] li {
    margin-bottom: 0 !important;
  }
  section[data-class~="font-xxsmall"] p {
    margin-bottom: 0.05em !important;
  }
  section[data-class~="font-xxsmall"] pre {
    margin: 0.2em 0 !important;
    font-size: 0.85em !important;
  }

  /* 超コンパクト用 */
  section[data-class~="font-xxxsmall"] {
    font-size: 13px !important;
    line-height: 1.05 !important;
    padding: 8px 18px !important;
  }
  section[data-class~="font-xxxsmall"] h2, section[data-class~="font-xxxsmall"] h3 {
    font-size: 18px !important;
    margin-bottom: 0.08em !important;
  }
  section[data-class~="font-xxxsmall"] li {
    margin-bottom: 0 !important;
  }
  section[data-class~="font-xxxsmall"] p {
    margin-bottom: 0.02em !important;
  }
  section[data-class~="font-xxxsmall"] pre {
    margin: 0.1em 0 !important;
    font-size: 0.8em !important;
  }

  /* 2カラムレイアウト */
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-top: 0.5em;
  }
  .columns ul {
    margin: 0;
  }

  /* 3カラムレイアウト */
  .columns-3 {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
    margin-top: 0.5em;
  }
  .columns-3 ul {
    margin: 0;
    font-size: 0.85em;
  }

  /* コンパクトリスト */
  .compact-list li {
    margin-bottom: 0.2em;
    font-size: 0.95em;
  }

  /* ハイライトボックス */
  .highlight-box {
    background: #e8f0fe;
    border-left: 4px solid #1a73e8;
    padding: 1rem 1.5rem;
    margin: 1em 0;
    border-radius: 4px;
  }

  /* 警告ボックス */
  .warning-box {
    background: #fef7e0;
    border-left: 4px solid #f9ab00;
    padding: 1rem 1.5rem;
    margin: 1em 0;
    border-radius: 4px;
  }

  /* キーメッセージ */
  .key-message {
    font-size: 1.3em;
    font-weight: bold;
    color: #1a73e8;
    text-align: center;
    margin: 1.5em 0;
    padding: 1em;
    background: #f8f9fa;
    border-radius: 8px;
  }

  /* チェックリスト */
  .checklist ul {
    list-style: none;
    padding-left: 0;
  }
  .checklist li::before {
    content: "✓ ";
    color: #34a853;
    font-weight: bold;
  }

</style>


# Day 1 - 02 STEP 1-2-3: 要件定義・設計・タスク分解

**対象者**: Python開発者（AI駆動開発は初心者）
**前提知識**: 01-入門編受講済み（AI特性5つ、対処法2つ、5-STEPワークフロー全体像）
**学習目標**: STEP 1（要件定義）、STEP 2（設計）、STEP 3（タスク分解）を習得し、STEP 4（実装）の準備を整える

---

## イントロダクション: STEP 1-2-3の全体像

---
<!-- _class: font-small -->

### STEP 1-2-3とは - 実装前の準備3ステップ

- **4段階の詳細化プロセス**
  - 要件定義: 誰が何をなぜ（ユーザーストーリー）
  - 設計: 画面・DB・API（具体的な仕様）
  - タスク分解: 10分サイズ（実装可能な単位）
  - 実装: コード作成
- **各段階で詳細化し、次の段階のガードレールを構築**
  - 前の段階が後の段階の品質を決定
  - 設計書がAIの外部メモリとして機能
  - コンテキスト不足による暴走を防ぐ

---
<!-- _class: font-xxsmall -->

### 設計書がなぜ必要か - 人間もAIも同じ

- **人間でも設計書がなければ大変**
  - ソースコードのみから全体を理解するのは困難
  - 設計意図が分からず、修正時に既存機能を壊すリスク
- **AIでも同じ問題が起きる**
  - 設計書なし：全コード読解に150Kトークン消費
  - 設計書あり：30Kトークンで全体を把握
- **設計書の真の価値**
  - 人間同士・AIへのコミュニケーションツール

---
<!-- _class: font-xsmall -->

### トークン効率の観点 - 設計書で思考リソース3倍

- **設計書なしの場合**
  - 全コード読解: 150Kトークン
  - 思考: 50Kトークン
  - 合計: 200Kトークン
- **設計書ありの場合**
  - 設計書読解: 30Kトークン
  - 思考: 170Kトークン（3.4倍）
  - 合計: 200Kトークン（同じ）
- **AIは設計書を外部メモリとして活用**
  - 複雑なロジック対応が可能
  - エッジケース処理の品質向上
  - 実装速度の向上

---
<!-- _class: font-xsmall -->

## 実践準備: AIツール選択戦略

**STEP 1-2-3を実践する前に、どのAIツールを使うか決めておきましょう。** ツール選択を間違えると、せっかくの設計書作成がコンテキスト汚染で台無しになります。

---
<!-- _class: font-xxsmall -->

### Claude WebとClaude Codeの使い分け戦略

- **Claude WEB版: 探索・議論フェーズ（STEP 1-2）**
  - ユーザーストーリー作成、画面プロトタイプ
  - 設計の試行錯誤、複数案の比較
- **Claude Code: 実装フェーズ（STEP 3-4-5）**
  - タスク分解、TDD実装、リファクタリング
- **使い分けの目的**
  - コンテキスト汚染を防ぐ、トークン効率最大化

---
<!-- _class: font-xsmall -->

### Claude WEB/Code使い分けの実践 - コンテキスト汚染を防ぐ

- **悪い例: Claude Codeを最初から使う**
  - 試行錯誤の履歴が蓄積（80Kトークン）
  - 思考トークンが圧迫される
  - タスク分解の品質が低下
  - AIが過去の失敗パターンに引きずられる
- **良い例: フェーズを分離する**
  - Claude WEBで探索・議論（STEP 1-2）
  - 設計書をローカル保存（docs/*）
  - Claude Code新セッション開始（STEP 3-5）
  - 設計書のみ参照（30Kトークン）
  - 思考に170Kトークン使える
- **推奨ワークフロー**
  - Claude WEB: 要件定義
  - 設計書保存
  - CLAUDE.md更新
  - Claude Code新セッション: タスク分解・実装

---
<!-- _class: font-small -->

## セクション1: 要件定義フェーズ - ユーザーストーリー

---
<!-- _class: font-xxsmall -->

### AIを活用したユーザーストーリー生成

- **基本的なアプローチ**
  - やりたいことをAIに伝え、ユーザーストーリーを生成
  - 例：「ToDo管理アプリを作りたい」
- **AIの特性を活かす**
  - ブレインストーミングが得意、たくさん生成して選ぶ
- **AIの傾向への対処**
  - AIは要件を作りすぎるので、MoSCoW分析で優先順位付け

---
<!-- _class: font-xsmall -->

### 要件定義フェーズの目的

- **顧客要望をユーザーストーリーに変換**
  - As a（誰が）
  - I want（何を）
  - So that（なぜ）
- **MoSCoW分析でMust（必須）を絞る**
  - Must: 必須（20-30%）
  - Should: 重要（30-40%）
  - Could: あれば良い（30-40%）
  - Won't: 今回はやらない（10-20%）
- **AIの暴走を防ぐ**
  - スコープを明確化
  - 優先順位を決定
  - 過剰実装を防止

---
<!-- _class: font-small -->

### ユーザーストーリーとは

- **基本フォーマット**
  - "As a [ペルソナ], I want [目的], So that [利益]"
  - 例: "As a 一般ユーザー, I want タスクを作成, So that やるべきことを管理"
- **顧客視点で価値を明確化**
  - 技術仕様ではなく、ビジネス価値を記述
  - 開発者とステークホルダーの共通言語
- **ユーザーストーリーの3C**
  - Card: インデックスカードに書ける短さ
  - Conversation: 詳細は会話で補う
  - Confirmation: 受入基準で完了を確認
- **アンチパターン**
  - 技術タスクを書く（例: DBテーブル作成）
  - 詳細すぎる仕様書になる
  - 「システムは〜する」という主語

---
<!-- _class: font-xxsmall -->

### なぜユーザーストーリー形式を使うか

- **開発者にとって**
  - 何を実装すべきかが明確
  - スコープ縮小時の判断基準として適切な粒度
- **顧客にとって**
  - 技術用語なしで理解できる
  - ビジネス価値が明確
- **AIにとって**
  - 構造化されていて理解しやすい
  - 受入基準への変換が容易
- **チームにとって**
  - 合意形成の単位として適切
  - 認識のズレを防ぐ

---
<!-- _class: font-xxsmall -->

### INVEST原則

- **Independent（独立している）**
  - 他のストーリーに依存しない
  - 単独でリリース可能、順序変更が容易
- **Negotiable（交渉可能）**
  - 詳細は議論の余地がある
  - 契約ではなく会話のきっかけ
- **Valuable（価値がある）**
  - 顧客に価値を提供する
  - 技術タスクではなくビジネス価値で表現
- **Estimable（見積もり可能）**
  - 工数を見積もれる程度に具体的
  - 大きすぎて見積もれないなら分割
- **Small（小さい）**
  - 1-3日で完了できるサイズ
  - スプリント内で複数完了できる粒度
- **Testable（テスト可能）**
  - 受入基準が明確
  - 完了条件を客観的に判定できる

---
<!-- _class: font-xxsmall -->

### MoSCoW分析 - AIに優先順位を付けてもらう

- **なぜMoSCoW分析か**
  - AIは大量のユーザーストーリーを生成する
  - 優先順位がないと人間の判断が難しい
  - 「MoSCoW分析して」の一言で効率的に分類
- **AIへのプロンプトの工夫**
  - 「理由も含めて」→ 判断根拠を説明
  - 「推奨案を提示して」→ 意思決定を支援
  - 「メリット・デメリットを」→ トレードオフを明確化
- **良いプロダクトを作るコツ**
  - MoSCoW分析に時間をかける
  - AIに複数の観点から分析させる
  - 最終判断は人間が行う

---
<!-- _class: font-xsmall -->

### ペルソナを活用した多角的MoSCoW分析

- **複数ペルソナによる分析**
  - 事前に利用者のペルソナを複数設定
  - ペルソナごとにMoSCoW分析を実施
  - 異なる価値観からの優先順位付け
- **ペルソナ例**
  - ビジネスユーザー：効率重視、時間短縮
  - 技術者：拡張性重視、API充実
  - 初心者：使いやすさ重視、学習コスト低
- **効果**
  - 異なる価値判断基準での優先順位
  - 見落としがちな要件の発見
  - ターゲットユーザーの明確化

---
<!-- _class: font-xsmall -->

### 要件定義フェーズの成果物

- **ユーザーストーリー（3-10個）**
  - As a, I want, So that形式
  - INVEST原則を満たす
- **MoSCoW分析結果**
  - Must: 20-30%に絞る
  - Should/Could/Won't: 残り70-80%
- **ペルソナ設定**
  - ターゲットユーザーの具体像
- **次のステップ**
  - STEP 2（設計）で具体的な設計に落とし込む

---
<!-- _class: font-xsmall -->

### モックアップで早期フィードバックを得る

- **企画段階でプロトタイプを作る**
  - Claude WEB版のアーティファクト機能
  - Gemini Canvas機能
  - 簡単に画面モックアップを作成
- **早期フィードバックのメリット**
  - ユーザーの反応を早く得られる
  - ユーザーストーリーの選択が速くなる
  - 手戻りコストの削減
- **フィードバックループ**
  - モックアップ作成（10分）→ ユーザーに見せる
  - フィードバックを反映 → ユーザーストーリーを確定

---
<!-- _class: font-small -->

### Claudeアーティファクト機能でモックアップ作成

- **Vibe Coding（雰囲気で伝える）** - 厳密な仕様ではなく「こんな感じで」と伝えてAIに作らせる手法
  - 「TODO管理アプリのTODO一覧画面を作って」
  - 「左にサイドバー、右にTODOリスト、上に検索バー」
  - 「青系の配色で、モダンなデザインにして」
- **顧客と認識を合わせる**
  - 言葉だけでなく、ビジュアルで確認
  - 早期フィードバック
  - 手戻りを防ぐ

---
<!-- _class: font-small -->

### モックアップ生成の実例とチェックポイント

- **指示例**
  - 「TODO管理アプリのTODO一覧画面を作って」
  - 「検索機能、フィルタ機能、ソート機能を含めて」
  - 「レスポンシブデザインで、モバイルでも使いやすくして」
- **チェックポイント**
  - ユーザビリティ: 直感的に操作できるか
  - レスポンシブデザイン: モバイル/タブレット/デスクトップ対応
  - アクセシビリティ: キーボード操作、スクリーンリーダー対応
- **反復改善**
  - 「検索バーを右上に移動して」
  - 「フォントサイズを大きくして」
  - 「ダークモード対応して」

---
<!-- _class: font-small -->

## セクション2: STEP 2 - 設計（画面・DB・API・受入基準・DoD）

---
<!-- _class: font-small -->

### STEP 2の目的と成果物 - AIの外部メモリを構築

- **ユーザーストーリーを具体的な設計に落とし込む**
  - 画面設計（どう見えるか）
  - DBスキーマ（どう保存するか）
  - 受入基準（何ができればOKか）
- **AIが何度でも参照できる外部メモリを構築**
  - 設計書をdocs/配下に保存
  - CLAUDE.mdに参照パスを記載
  - AIが必要な情報をいつでも取得可能

---
<!-- _class: font-small -->

### 設計書のROI - 研究が証明する劇的な効果

- **設計書作成時間 vs 実装時間短縮**
  - 設計書作成: 1-2時間
  - 実装時間短縮: 5-10時間
  - ROI: 3-10倍
- **エラー率の低下**
  - 設計書なし: 脆弱性45%発生（Veracode 2025研究）
  - 設計書あり: 明示的仕様で修正要求68%削減（Microsoft研究）
  - コンテキストが品質を決定する
- **品質向上の理由**
  - AIがコンテキストを正確に理解
  - エッジケース対応が漏れにくい
  - 複雑なロジックの実装精度向上

---
<!-- _class: font-xsmall -->

### 要件から実装までの一連の流れ - 4段階の詳細化プロセス

- **ユーザーストーリー → 画面設計**
  - 誰が何をなぜ → どう見えるか
  - 画面一覧、画面遷移図、画面部品一覧
- **画面設計 → 受入基準**
  - どう見えるか → 何ができればOKか
  - チェックリスト形式（正常系1 + 異常系2-3）
  - GIVEN-WHEN-THEN形式
- **受入基準 → BDDテストシナリオ**
  - ユーザー視点 → 開発者視点
  - GIVEN（前提）、WHEN（操作）、THEN（期待結果）
  - pytestに直接変換可能

---
<!-- _class: font-xsmall -->

### 画面設計の3要素

- **画面一覧**
  - 全画面をリスト化（画面ID、画面名、URL、役割）
  - 例: 01-ログイン、02-ダッシュボード、03-TODO一覧
- **画面遷移図（Mermaid記法）**
  - 画面間の遷移を可視化
  - ログイン → ダッシュボード → TODO一覧の流れ
- **画面部品一覧（UI Component Inventory）**
  - 各画面の部品をリスト化
  - ボタン、入力フォーム、テーブルなど
  - バリデーションルール、イベントハンドラ

---
<!-- _class: font-small -->

### 画面一覧の作成方法

- **全画面をリスト化**
  - 画面ID（例: 01, 02, 03）
  - 画面名（例: ログイン、ダッシュボード）
  - URL（例: /login, /dashboard）
  - 役割（例: 認証、タスク一覧表示）
- **Claude WEB版に指示**
  - 「ユーザーストーリーから画面一覧を作って」
  - 「各画面のURL、役割、アクセス権限を含めて」
- **レビューポイント**
  - 画面の漏れがないか
  - URL命名規則が統一されているか
  - アクセス権限が適切か

---
<!-- _class: font-small -->

### 画面遷移図（Mermaid記法）

- **画面間の遷移をMermaid記法で可視化**
  ```mermaid
  graph TD
    A[ログイン] --> B[ダッシュボード]
    B --> C[TODO一覧]
    C --> D[TODO作成]
    D --> C
  ```
- **遷移条件を明記**
  - ログイン成功 → ダッシュボード
  - TODO作成完了 → TODO一覧に戻る
- **エラー遷移も含める**
  - ログイン失敗 → ログイン画面（エラーメッセージ表示）
  - バリデーションエラー → 同じ画面（エラーメッセージ表示）

---
<!-- _class: font-small -->

### 画面部品一覧（UI Component Inventory）

- **各画面の部品をリスト化**
  - 部品ID（例: btn-submit）
  - タイプ（例: Button, Input, Table）
  - ラベル（例: "送信", "タイトル入力"）
- **バリデーションルールを記載**
  - 必須入力、文字数制限
  - フォーマット（メールアドレス、URL）
  - 重複チェック
- **イベントハンドラを記載**
  - onClickイベント（例: 送信ボタン → API呼び出し）
  - onChangeイベント（例: 入力フォーム → バリデーション）

---
<!-- _class: font-small -->

### データベース設計の基本 - ER図とschema.sql

- **エンティティ抽出**
  - ユーザーストーリーから名詞を抽出
  - 例: User, Todo, Tag
- **正規化（第3正規形）** - データの重複を排除する設計手法
  - 第1正規形：繰り返しグループを排除（1セルに1値）
  - 第2正規形：部分関数従属を排除
  - 第3正規形：推移的関数従属を排除（「A→B→C」の関係を分離）
  - 効果：更新異常を防ぎ、データ整合性を保証
- **物理設計（schema.sql）**
  - CREATE TABLE文
  - PRIMARY KEY、FOREIGN KEY、INDEX
  - NOT NULL、UNIQUE、DEFAULT制約
- **ER図（Mermaid記法）でエンティティ、属性、リレーションシップを可視化**
  - エンティティ（User, Todo）
  - 属性（id, title, description）
  - リレーションシップ（1対多、多対多）

---
<!-- _class: font-small -->

### データベース設計の重要性

- **なぜ早期に時間をかけるべきか**
  - あとからの手戻りの影響が大きい
  - スキーマ変更はデータ移行を伴う
  - 関連する全機能に影響
- **設計時のポイント**
  - 関係者を含めた合意形成
  - ER図で視覚化して共有
  - 正規化（第3正規形）の検討
- **AIへの指示**
  - 「ER図をMermaid記法で作成して」
  - 「インデックス設計も含めて」

---
<!-- _class: font-small -->

### Mermaid記法の活用

- **Mermaid記法とは**
  - テキストでダイアグラムを記述
  - UML（統一モデリング言語、ソフトウェア設計を図で表現する標準規格）でよく使われる図を簡単に作成
  - Markdownと組み合わせて使用
- **対応する図の種類**
  - シーケンス図、クラス図
  - ER図、画面遷移図（stateDiagram）
- **メリット**
  - 人間：俯瞰して見やすい
  - AI：少ないトークンで全体を把握
  - Git管理が容易（差分が見やすい）

---
<!-- _class: font-small -->

### データフロー図の基本

- **Router → Service → Repository → DBの流れを可視化**
  - Router: リクエスト受信、レスポンス返却
  - Service: ビジネスロジック
  - Repository: DB操作（CRUD）
  - DB: データ永続化
- **レイヤードアーキテクチャ**
  - 各層の責務を明確化
  - 依存関係を一方向に保つ
  - テスタビリティの向上
- **トランザクション境界を明確化**
  - SQLAlchemy Sessionの位置

---
<!-- _class: font-xsmall -->

### AIに複数案を提案させる

- **指示例**
  - 「3つの案を提案して、それぞれのPros/Consを説明して」
  - 「シンプルな案と高機能な案の両方を提案して」
- **AIに選択肢を与え、人間が最終決定**
  - 案A: シンプル（開発コスト低、機能少ない）
  - 案B: 中間（バランス型）
  - 案C: 高機能（開発コスト高、UX良い）
- **比較ポイント**
  - 開発コスト
  - ユーザビリティ
  - 保守性

---
<!-- _class: font-xxsmall -->

### ガードレールの4層構造（復習）

- **Layer 1: プロジェクトルール（CLAUDE.md）**
  - コーディング規約
  - アーキテクチャ方針
  - 開発ワークフロー
- **Layer 2: タスク固有（Issue）**
  - 実装すべき機能
  - BDDテストシナリオ
  - 参照設計書
- **Layer 3: 受入基準（AC）**
  - 何ができればOKか
  - 正常系1 + 異常系2-3
  - GIVEN-WHEN-THEN形式
- **Layer 4: コード規約（ruff、pyright）**
  - 静的解析ツール
  - テストカバレッジ閾値
  - 複雑度制限

---
<!-- _class: font-xsmall -->

### 受入基準（AC）を作成 - チェックリスト形式で検収基準を明確化

- **モックアップを見ながら「これができればOK」をチェックリスト化**
  - ユーザー視点で記述
  - 正常系1 + 異常系2-3
  - GIVEN-WHEN-THEN形式
- **正常系の例**
  - ✅ タイトル入力して作成ボタンを押したらTODOが一覧に表示される
  - ✅ TODO完了ボタンを押したら完了状態になる
- **異常系の例**
  - ✅ タイトル空でエラーメッセージが表示される
  - ✅ タイトル256文字以上でエラーメッセージが表示される
  - ✅ ネットワークエラー時にエラーメッセージが表示される

---
<!-- _class: font-xxsmall -->

### 受入基準（AC）の例 - ユーザー視点のチェックリスト

- **正常系**
  - GIVEN: TODO一覧画面が表示されている
  - WHEN: タイトルに「牛乳を買う」と入力して作成ボタンを押す
  - THEN: TODO一覧に「牛乳を買う」が表示される
- **異常系1: タイトル空**
  - GIVEN: TODO一覧画面が表示されている
  - WHEN: タイトルを入力せずに作成ボタンを押す
  - THEN: 「タイトルは必須です」というエラーメッセージが表示される
- **異常系2: タイトル長すぎ**
  - GIVEN: TODO一覧画面が表示されている
  - WHEN: タイトルに256文字以上入力して作成ボタンを押す
  - THEN: 「タイトルは255文字以内で入力してください」というエラーメッセージが表示される

---
<!-- _class: font-xsmall -->

### 受入条件の段階的詳細化

- **3段階の詳細化**
  - ユーザーストーリー：「As a ユーザー, I want ...」
  - チェックリスト形式：✅ タイトルを入力して作成できる
  - GIVEN-WHEN-THEN形式：具体的なシナリオ
- **詳細化していく中で精度を上げる**
  - 後続の実装フェーズで確実に実装される
  - AIの手抜きを防ぐ
  - 最終的な製品のクオリティ向上
- **階層的なタスク分解とも関連**
  - ユーザーストーリー → タスク → サブタスク
  - 各階層で詳細化

---
<!-- _class: font-small -->

### 受入基準（AC）が手抜きを防ぐ仕組み

- **AIはACを100%満たすまで実装を続ける**
  - AI Self Reviewで検証
  - 「受入基準を満たしているか確認して」と指示
- **ACがないとAIは「適当に実装して終了」**
  - Test Hacking: テストが通れば良いという手抜き
  - エッジケース対応が漏れる
- **ACがあると品質が劇的に向上**
  - 正常系だけでなく、異常系も実装
  - ユーザビリティが向上

---
<!-- _class: font-small -->

### 人間が明示的に指定すべき技術選定

- **AIから提案されにくいモダンなツール**
  - パッケージマネージャ：pip → uv
  - フォーマッター：black/flake8 → ruff
  - 型チェック：mypy → pyright
- **AIから提案されにくい設計パターン**
  - エラーハンドリング：dry-python/returnsのResult型
  - テスト戦略（TDD、Property-based testing）
- **人間の役割**
  - 最新のベストプラクティスを知っておく
  - CLAUDE.mdに記載して共有

---
<!-- _class: font-xsmall -->

### AIに技術的決定事項を質問させる

- **CLAUDE.mdに記載する指示**
  - 「実装前に不明・あいまいな点があれば質問して」
  - 使用ライブラリ・フレームワーク
  - エラーハンドリングの方針
- **質問を欠かさずすることが重要**
  - 「モダンなベストプラクティスは？」と聞けば出てくることも多い
  - uv、ruffなどのツール系は提案されやすい
- **ただし設計パターン系は自分でキャッチアップ**
  - dry-python/returnsなどは設計段階では出てきにくい
  - 技術ブログ、カンファレンス、書籍で情報収集

---
<!-- _class: font-xsmall -->

### dry-python/returnsによるResult型

- **従来の例外処理の問題**
  - `try-except`を書き忘れても、コンパイル時にエラーにならない
  - どの関数が例外を投げるか、コードを読まないと分からない
  - 「例外を握りつぶす」バグが発生しやすい
- **Result型とは** - 成功/失敗を返り値で明示する設計パターン
  - `Success(value)`: 成功時の値を包む
  - `Failure(error)`: 失敗時のエラーを包む
  - 呼び出し側は必ず両方を処理しないとpyrightエラー
- **dry-python/returnsの利点**
  - 型チェックで「エラー処理漏れ」をコンパイル時に検出
  - コードを読まなくても「この関数は失敗する可能性がある」と分かる
- **AIへの指示例**
  - 「dry-python/returnsを使ってResult型でエラー処理して」

---
<!-- _class: font-xxsmall -->

### Definition of Done (DoD)とは

**ACとDoDの違い**: ACは「この機能が何をできればOKか」（機能単位）、DoDは「コードを完了と呼ぶための品質基準」（全機能共通）です。ACを満たし、かつDoDも満たして初めて「完了」です。

- **DoDの目的**
  - チーム全体で「完了」の定義を統一
  - 品質のばらつきを防ぐ
  - AIにも明確な完了基準を与える
- **テストカバレッジ80%以上**
  - pytest-covで自動計測
  - 重要なロジックは必ずテスト
- **Cyclomatic Complexity 10以下**
  - 循環的複雑度：if/for/whileなど分岐の数を測る指標
  - 10以下 = テストしやすい、バグが少ない
  - ruffで自動チェック（C901ルール = 複雑度超過を検出）
  - 超過したら関数を分割してリファクタリング
- **静的解析エラーなし**
  - ruff、pyrightをCI/CDで自動化
  - PRマージ前に必ずパス
- **docstring完備**
  - 公開関数にdocstringを記載
  - 引数・戻り値・例外を明記
- **ADR作成**
  - 重要な設計判断を記録
  - 将来の開発者への引き継ぎ

---
<!-- _class: font-xsmall -->

### 設計フェーズの成果物まとめ - タスク分解の土台

- **設計成果物**
  - 画面設計（画面一覧、画面遷移図、画面部品一覧）
  - DBスキーマ（ER図、schema.sql）
  - 受入基準（AC、GIVEN-WHEN-THEN）
  - DoD（完了条件）
- **すべてdocs/配下に保存**
  - docs/design/er-diagram.md
  - docs/design/data-flow.md
  - docs/requirements/acceptance-criteria.md
  - migrations/や schema.sql
- **Git管理、CLAUDE.mdに参照パスを記載**
  - AIが必要な情報をいつでも取得可能
  - チーム全体で共有
- **次のSTEP 3（タスク分解）の土台**
  - 設計書を基にタスクを分解
  - GIVEN-WHEN-THENをBDDテストシナリオに変換

---
<!-- _class: font-small -->

## セクション3: STEP 3 - タスク分解（GitHub Issues・BDDテストシナリオ・10分ルール）

---
<!-- _class: font-xsmall -->

### STEP 3の目的と成果物 - 10分サイズに分割

- **ユーザーストーリーを10分サイズのSubtaskに分解**
  - AIが迷わないサイズ（10-30分）
  - 1つの機能を実装できる単位
  - 集中力を維持できるサイズ
- **GitHub Issuesに登録**
  - 1 Issue = 1 Subtask = 10分タスク
  - タイトル、概要、参照設計書、BDDテストシナリオ、DoDを記載
- **GIVEN WHEN THEN形式のBDDテストシナリオを記載**
  - 開発者視点に変換
  - pytestに直接変換可能
  - テストファーストで実装

---
<!-- _class: font-xsmall -->

### 階層的タスク分解（Epic → User Story → Task → Subtask）

- **Epic（数週間-数ヶ月）**
  - 例: TODO管理アプリ開発
  - 大きな機能群
- **User Story（1-3日、AC）**
  - 例: TODOを作成できる
  - INVEST原則を満たす
  - 受入基準（AC）を含む
- **Task（2-4時間）**
  - 例: TODO作成機能の実装
  - DBスキーマ、Repository、Service、Router
- **Subtask（10-30分、GIVEN WHEN THEN）**
  - 例: todo_repository.save()の実装
  - BDDテストシナリオを含む
  - 1 Issue = 1 Subtask

---
<!-- _class: font-small -->

### GIVEN WHEN THEN形式のBDDテストシナリオ - 開発者視点への変換

- **GIVEN（前提条件）**
  - データベースの初期状態
  - モックの設定
  - テストデータの準備
- **WHEN（操作）**
  - テスト対象関数の呼び出し
  - 例: todo_repository.save(todo)
- **THEN（期待結果）**
  - 戻り値の検証
  - データベースの状態検証
  - 例外の検証
- **pytestに直接変換可能**
  - fixture: GIVEN
  - テスト対象関数: WHEN
  - assert: THEN

---
<!-- _class: font-xsmall -->

### 受入基準（AC）→ BDDテストシナリオ → pytestの変換

- **受入基準（AC、ユーザー視点）**
  - 「タイトル入力して作成したら一覧に表示」
  - 「タイトル空でエラーメッセージ表示」
- **BDDテストシナリオ（開発者視点）**
  - GIVEN: 画面表示
  - WHEN: create()呼び出し
  - THEN: find_all()に含まれる
- **pytestコード**
  ```python
  def test_create_success():
      # GIVEN
      todo = Todo(title="牛乳を買う")
      # WHEN
      saved = todo_repository.save(todo)
      # THEN
      assert saved in todo_repository.find_all()
  ```

---
<!-- _class: font-xsmall -->

### タスク分解の実例 - TODO作成機能

- **Issue #1: DBスキーマ作成（10分）**
  - schema.sqlまたはAlembicマイグレーション作成（Alembic = PythonのDBマイグレーションツール、スキーマ変更をバージョン管理）
  - CREATE TABLE todos文
  - PRIMARY KEY、NOT NULL制約
- **Issue #2: Repository実装（10分）**
  - todo_repository.save()実装
  - pytestテスト作成
- **Issue #3: Service実装（10分）**
  - todo_service.create()実装
  - バリデーション（タイトル必須、長さ制限）
  - pytestテスト作成
- **Issue #4: Router実装（10分）**
  - @router.post("/todos")実装
  - pytestテスト作成（TestClient）
- **各Issue 10分以内で完了できるサイズ**

---
<!-- _class: font-xxsmall -->

### GitHub Issuesでタスク管理

- **1 Issue = 1 Subtask = 10分タスク**
  - タイトル: [TODO作成] todo_repository.save()の実装
  - 概要: TODOを保存するRepository関数を実装する
- **IssueにBDDテストシナリオを記載**
  - GIVEN: Todoオブジェクトが準備されている
  - WHEN: todo_repository.save(todo)を呼び出す
  - THEN: 保存されたTodoが返される
- **参照設計書を記載**
  - schema.sql: テーブル定義
  - acceptance-criteria.md: 受入基準
- **DoDを記載**
  - テストカバレッジ80%以上
  - 静的解析エラーなし

---
<!-- _class: font-xxsmall -->

### Issueテンプレートの構造

- **タイトル**
  - [カテゴリ] 具体的なタスク名
  - 例: [TODO作成] todo_repository.save()の実装
- **概要**
  - 何を実装するか
  - なぜ必要か
- **参照設計書**
  - schema.sql、er-diagram.md、acceptance-criteria.md
- **BDDテストシナリオ**
  - GIVEN: 前提条件
  - WHEN: 操作
  - THEN: 期待結果
- **DoD（Definition of Done）**
  - テストカバレッジ80%以上
  - 静的解析エラーなし
  - docstring完備
- **テンプレートをClaude Codeに作成させる**

---
<!-- _class: font-xsmall -->

### 10分ルール

- **1つのタスクは10分で完了できるサイズに分割**
  - AIの集中力の限界
  - 10分以内なら高品質を維持
  - 30分以上なら暴走・手抜き・忘れっぽさが発生
- **大きすぎるタスクの問題**
  - 暴走: スコープを勝手に拡大
  - 手抜き: Test Hacking、エッジケース対応漏れ
  - 忘れっぽさ: 最初に指示したことを忘れる
- **10分ルールの効果**
  - 品質向上
  - 進捗管理しやすい
  - デバッグしやすい

---
<!-- _class: font-small -->

## セクション4: まとめとQ&A

---
<!-- _class: font-small -->

### STEP 1-2-3の復習 - 4段階の詳細化プロセス

- **要件定義 → 設計 → タスク分解 → 実装**
  - 各段階で詳細化
  - 前の段階が後の段階の品質を決定
- **設計書があればトークン効率3.4倍**
  - 設計書なし: 読解150K + 思考50K
  - 設計書あり: 読解30K + 思考170K
- **複雑なロジック・エッジケース対応が可能**
  - AIが外部メモリとして設計書を活用
  - 明示的仕様で修正要求68%削減（Microsoft研究）

---
<!-- _class: font-small -->

### STEP 1-2-3でClaude Codeが自動化できること

- **タスク分解は自動化可能**
  - TODOリスト作成
  - BDDテストシナリオ作成
  - GitHub Issues作成
- **要件定義・設計は人間とAIの協働**
  - Claude WEB版で探索・議論
  - 複数案を比較
  - 人間が最終決定
- **自動化の限界**
  - ビジネス価値の判断
  - デザインの良し悪し
  - ユーザー視点の評価

---
<!-- _class: font-xxsmall -->

### 次のステップ - STEP 4（実装）へ

- **次回03ではSTEP 4（TDD実装）とSTEP 5（品質改善）を学ぶ**
  - 7段階TDDサイクル
  - 3段階レビュー（AI Self Review、ADR、MCP Servers）
  - リファクタリング
- **GitHub Issues #1-10を7段階TDDサイクルで実装**
  - Red: テスト失敗
  - Green: 最小実装
  - Refactor: リファクタリング
- **成果物**
  - 動作するコード
  - テストカバレッジ80%以上
  - 静的解析エラーなし

---
<!-- _class: font-xsmall -->

### コンテキストエンジニアリング - STEP 2がSTEP 4の品質を決める

- **設計書が充実していれば、STEP 4の品質・速度が飛躍的に向上**
  - エラー率46%削減
  - 実装時間5-10時間短縮
  - ROI 3-10倍
- **「設計に1時間、実装に10時間」ではなく、「設計に2時間、実装に3時間」**
  - 設計に時間をかけるほど、実装が速くなる
  - トークン効率3.4倍
- **設計書はAIの外部メモリ**
  - 複雑なロジック対応
  - エッジケース処理
  - 高品質なコード生成

---
<!-- _class: font-xsmall -->

### Q&A

- **Q1: Claude WEB版とClaude Codeの使い分けは必須か?**
  - A: 必須ではないが、強く推奨。コンテキスト汚染を防ぎ、トークン効率を最大化できる。
- **Q2: 設計書作成に時間がかかりすぎないか?**
  - A: 1-2時間で作成でき、実装時間を5-10時間短縮できる（ROI 3-10倍）。
- **Q3: 10分ルールは厳密に守る必要があるか?**
  - A: 目安として有効。10-30分なら許容範囲。30分以上は分割を検討。

---
<!-- _class: font-xsmall -->

## 付録

---
<!-- _class: font-xxsmall -->

### 参考資料

- **要件定義**
  - knowledges/23-user-story-writing.md - ユーザーストーリー
  - knowledges/19-guardrails.md - ガードレール
- **設計**
  - knowledges/22-screen-design-and-vibe-coding.md - 画面設計
  - knowledges/24-acceptance-criteria.md - 受入基準
  - knowledges/27-ai-ask-questions.md - AI質問戦略
- **タスク分解**
  - knowledges/25-task-decomposition.md - タスク分解
  - knowledges/01-given-when-then-bdd.md - BDD
- **AIツール戦略**
  - knowledges/36-ai-tools-separation-strategy.md - AIツール分離戦略
  - knowledges/33-ai-context-documentation-importance.md - コンテキストの重要性
  - knowledges/35-ai-context-contamination-quality-degradation.md - コンテキスト汚染

---
<!-- _class: font-xsmall -->

### 次回までの課題

- **課題1: 自分のプロジェクトでユーザーストーリーを3つ作成**
  - As a, I want, So that形式
  - INVEST原則を満たす
  - MoSCoW分析（Must 20-30%）
- **課題2: そのうち1つを画面設計に落とし込む**
  - 画面一覧（画面ID、画面名、URL、役割）
  - 画面遷移図（Mermaid記法）
  - 画面部品一覧（UI Component Inventory）
- **課題3: 受入基準（AC）をチェックリスト形式で作成**
  - GIVEN-WHEN-THEN形式
  - 正常系1 + 異常系2-3
  - ユーザー視点で記述
- **提出物: Google Docsリンク（次回セッション開始時に共有）**
