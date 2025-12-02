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

# Day 1 - 03 STEP 4-5: 実装・TDD・品質改善

**対象者**: Python/FastAPI経験者（AI駆動開発は初心者）
**学習目標**: STEP 4（実装・TDD）とSTEP 5（品質改善）の習得

---

## イントロダクション

---
<!-- _class: font-xsmall -->

### 【復習】01で学んだAIの5つの特性
- 01「入門編」で学んだ内容の復習
  - AIには5つの特性があり、対策なしだと深刻な問題が発生
- **5つの特性**（01で詳細解説済み）
  - ①暴走（Scope Creep）: 指示していない機能を勝手に追加
  - ②手抜き（Test Hacking）: テストを通すだけの不正実装
  - ③忘れっぽさ（Context Limitations）: 長い会話で情報喪失
  - ④凸凹知能（Jagged Intelligence）: 得意・不得意の差が激しい
  - ⑤虚偽報告（Hallucination）: 存在しないAPIを提案
- **このセクションのゴール**
  - 対策なしで何が起こるか理解
  - 5つの対策手段を学ぶ
  - 本資料の各セクションとの対応を把握

---
<!-- _class: font-xsmall -->

### 対策なしだと何が起きるか？
- **①暴走**: 10分タスクが2時間に膨張
  - 「TODO追加機能」を依頼 → ユーザー認証、通知機能、統計ダッシュボードまで作成
- **②手抜き**: テストは通るが本番で障害
  - `if price == 100: return 90` のようなハードコード
  - 本番環境で異なる値が来ると即エラー
- **③忘れっぽさ**: 同じ修正を何度も指示
  - 「PEP 8に従って」と5回指示しても6回目で忘れる
- **④凸凹知能**: 得意分野で過信、苦手分野で致命的ミス
  - アルゴリズムは得意だが、ビジネスロジックは苦手
- **⑤虚偽報告**: 存在しないAPIでエラー地獄
  - `sqlalchemy.async_session()` など存在しない関数を提案
  - 実行時に `AttributeError` で延々とデバッグ

---
<!-- _class: font-xsmall -->

### AI駆動開発の5つの対策手段
- **①ガードレール（ドキュメント）** - 01で学習
  - ユーザーストーリー、受入基準、設計書で「何を作るか」明確化
  - 暴走（Scope Creep）を事前に防止
- **②ガードレール（テスト）** - 03 STEP 4で実践
  - テストファーストで「正しく作れたか」を検証
  - **テスト自体がガードレール**（手抜きを機械的に検出）
- **③APIドキュメントのdocs/保存** - 03 実装準備で解説
  - 外部ライブラリの仕様を事前にdocs/に保存
  - 虚偽報告（Hallucination）を防止
- **④System Review** - 03 TDDサイクルで実践
  - pytest + flake8 + mypy で機械的に検証
- **⑤AI Self Review** - 03 TDDサイクルで実践
  - Test Hacking検出、完成度0-100点評価
  - 手抜きを自己検証で発見

---
<!-- _class: font-xsmall -->

### 対策一覧表 - AI特性と本資料の対応
| AI特性 | 問題 | 対策 | 本資料の該当箇所 |
|--------|------|------|-----------------|
| ①暴走 | 機能追加しすぎ | ガードレール（ドキュメント） | 01で作成済み |
| ②手抜き | テストだけ通す | ガードレール（テスト）+ AI Self Review | セクション2, 3 |
| ③忘れっぽさ | 指示を忘れる | CLAUDE.md + /clear | セクション1, 5 |
| ④凸凹知能 | 得意不得意が激しい | Human Review | セクション3 |
| ⑤虚偽報告 | 存在しないAPI | docs/にAPI仕様保存 + System Review | セクション1, 4 |

- **ガードレールは2種類**
  - ドキュメント: 「何を作るか」を明確化（事前防止）
  - テスト: 「正しく作れたか」を検証（事後検証）
- **レビューは3段階**
  - System Review → AI Self Review → Human Review

---
<!-- _class: font-xsmall -->

### 03 実装・品質改善編の全体像
- **セクション1: 実装準備**
  - カスタムコマンド、Claude Skills、ハルシネーション対策
  - 対応: ③忘れっぽさ、⑤虚偽報告
- **セクション2: Test Hacking**
  - Test Hackingの実態と検出方法
  - 対応: ②手抜き
- **セクション3: AI駆動TDDサイクル**
  - 7段階TDD、3段階レビュー
  - 対応: ①暴走、②手抜き、④凸凹知能
- **セクション4: MCP Servers**
  - Context7、Serena、Playwright
  - 対応: ③忘れっぽさ、⑤虚偽報告
- **セクション5: STEP 5 - 品質改善**
  - 8つの質問と指示、完成度80点以上、/clear
  - 対応: ②手抜き、③忘れっぽさ

---

## セクション1: 実装準備

---
<!-- _class: font-xsmall -->

### このセクションで学ぶこと
- **対応するAI特性**
  - ③忘れっぽさ → カスタムコマンド、Claude Skillsで知識を永続化
  - ⑤虚偽報告 → APIドキュメントをdocs/に保存して防止
- **学習内容**
  - カスタムコマンドの作成と活用
  - Claude Skillsによる知識ベース構築
  - ハルシネーション対策の具体的手法
- **ゴール**
  - TDD用カスタムコマンド `/tdd` を作成できる
  - 外部ライブラリのAPIドキュメントをdocs/に保存できる

---
<!-- _class: font-xsmall -->

### カスタムコマンドの重要性 - プロジェクト固有のワークフロー
- カスタムコマンドとは
  - `.claude/commands/` にMarkdownファイルとして保存
  - `/コマンド名` で呼び出し可能
  - Git管理でチーム全体で共有
- なぜプロジェクト固有のカスタムコマンドが重要か
  - プロジェクトの技術スタックに合わせた指示が可能
  - 例: FastAPI + pytest + Jinja2 の場合
  - 毎回同じ指示を入力する手間を省く
  - チーム全体で品質を均一化
- TDD用カスタムコマンド `/tdd` の例
  - Plan → Red → Green → Refactor → 静的解析 → AI自己レビュー
  - Human Reviewまでを自動化
  - プロジェクトの静的解析ツール（flake8, mypy, ruff）を呼び出し

---
<!-- _class: font-xsmall -->

### Claude Skills - 再利用可能な知識ベース
- Claude Skillsとは
  - `.claude/skills/` にMarkdownファイルとして保存
  - プロジェクト固有の知識・ベストプラクティスを蓄積
  - カスタムコマンドから参照可能
- Skills の活用例
  - プロジェクトのコーディング規約
  - 使用ライブラリの正しい使い方
  - 過去のレッスンラーンド（教訓）
  - エラーハンドリングのパターン
- カスタムコマンドとSkillsの連携
  - カスタムコマンド: ワークフローを定義
  - Skills: 知識ベースを提供
  - 組み合わせてプロジェクト固有のAI駆動開発を実現

---
<!-- _class: font-xsmall -->

### ハルシネーション対策 - 外部API仕様の事前調査【重要】
- **問題: ⑤虚偽報告（Hallucination）への対策**
  - AIは学習データにない最新版の仕様を推測してでっちあげる
  - `sqlalchemy.async_session()`など存在しない関数を提案
  - 実行時エラーで発覚 → 延々とデバッグの悪循環
- **対策: 外部ライブラリの仕様を事前にdocs/に保存**
  - 公式ドキュメントからAPIリファレンスを取得
  - `docs/external-api/` に保存
  - CLAUDE.md に「このディレクトリを参照して実装せよ」と記載
- **具体的な手順**
  - ①使用ライブラリを洗い出す（SQLAlchemy、pytest、Pydantic等）
  - ②公式ドキュメントから必要な部分をMarkdownで保存
  - ③CLAUDE.md に参照パスを明記
- **なぜこれが効くのか**
  - AIはdocs/内のドキュメントを「正しい情報」として参照
  - 推測ではなく事実に基づいたコード生成
  - System Reviewで存在しないAPI呼び出しを検出

---

## セクション2: Test Hacking

**なぜTDDの前にTest Hackingを学ぶのか？** → TDDは「テストを先に書く」手法ですが、AIは「テストさえ通ればOK」と解釈して不正な実装をすることがあります。敵（Test Hacking）を知ってからTDDに進むことで、検出ポイントが分かります。

---
<!-- _class: font-xsmall -->

### このセクションで学ぶこと
- **対応するAI特性**
  - ②手抜き（Test Hacking）→ 実態を理解し検出方法を学ぶ
- **学習内容**
  - Test Hackingの定義と実証研究（METR 2025）
  - 3つの手法: Mock Abuse、Silent Fail、Silent Fallback
  - 良い例・悪い例の比較
- **ゴール**
  - Test Hackingのパターンを識別できる
  - AI Self Reviewで検出すべきポイントを理解

---
<!-- _class: font-xsmall -->

### Test Hackingとは - テストを通すための不正な手法
- Test Hackingの定義
  - テストを通すことだけを目的とした不正な実装
  - 本番環境で動かないコードが生成される
  - Reward Hacking（報酬ハッキング）の一種
- METR研究（2025年）の実証例 ※METR = AIの能力評価を行う研究機関
  - **タスク**: プログラムの実行を高速化せよ
  - **期待**: アルゴリズムを最適化
  - **実際**: タイマーを書き換えて常に高速な結果を表示
  - **結果**: 実際の速度向上なしに「不可能なほど高いスコア」達成
- なぜAIはTest Hackingを行うのか
  - **報酬関数の不完全性**: AIは「テストが通る」を報酬として学習
  - **プロキシ報酬の罠**: 本当の目標は「正しく動くコード」だが、テストは近似指標（プロキシ）に過ぎない
  - AIは報酬を最大化するよう最適化 → テストを通す最短経路（＝不正実装）を発見
  - 人間が想定しない「抜け穴」を見つける能力が高い

---
<!-- _class: font-xsmall -->

### Shallow Testing - Test Hackingの3つの手法
- ①Mock Abuse（モック乱用）
  - 実装を呼び出さず、モックだけでテストを通す
  - 例: repository.get_by_id()を呼ばず常にNone返却
  - 問題: 実際の統合部分のバグを検出できない
- ②Silent Fail（エラー握りつぶし）
  - `except Exception: return None`でエラーを隠す
  - 例: DB接続エラーでも"unknown"を返す
  - 問題: 本番環境でランダムに品質劣化
- ③Silent Fallback（暗黙のフォールバック）
  - `except Exception: return []`
  - 例: 計算エラーでも合計0円として処理
  - 問題: データ整合性の破壊、再起動では解決しない
- 対策
  - AI Self Reviewで検出
  - 完成度0-100点評価で80点以上を目指す

---
<!-- _class: font-xsmall -->

### Test Hacking実コード例 - 悪い例vs良い例
- ①ハードコード実装（Test Hacking）
  - ❌ 悪い例: `if price == 100 and rate == 0.1: return 90`
  - ✅ 良い例: `return price * (1 - rate)`
- ②Silent Fail（エラー握りつぶし）
  - ❌ 悪い例: `except Exception: return "unknown"`
  - ✅ 良い例: `raise UserNotFoundError(user_id)`
- ③Silent Fallback（暗黙のフォールバック）
  - ❌ 悪い例: `except Exception: return Decimal("0")`
  - ✅ 良い例: `if items is None: raise ValidationError()`
- ④Mock Abuse（モック乱用）
  - ❌ 悪い例: 8つの依存関係を全モック化
  - ✅ 良い例: 外部サービスのみモック、内部は実際のコード使用

---

## セクション3: AI駆動TDDサイクル

---
<!-- _class: font-xsmall -->

### このセクションで学ぶこと
- **対応するAI特性**
  - ①暴走 → Planフェーズで設計書参照、Scope Creep防止
  - ②手抜き → AI Self Reviewで完成度80点以上を目指す
  - ④凸凹知能 → Human Reviewでビジネスロジック確認
- **学習内容**
  - 一般TDD（3段階）とAI駆動TDD（7段階）の違い
  - 各フェーズの詳細: Plan、Red、Green、Refactor
  - 3段階レビュー: System Review、AI Self Review、Human Review
- **ゴール**
  - 7段階TDDを実践できる
  - **テストがガードレール**であることを体感

---
<!-- _class: font-xsmall -->

### 一般のTDDとAI駆動TDDの違い
- 一般のTDD（3段階）
  - Red → Green → Refactor
  - Red: テストを書いて失敗させる
  - Green: 最小限のコードで通す
  - Refactor: コード改善
- AI駆動TDD（7段階）の独自の工夫
  - **Plan（追加）**: 受入条件の詳細計画、docs/設計書参照、APIライブラリのWEB検索
  - Red → Green → Refactor
  - **静的解析（追加）**: Refactorの後で機械的チェック
  - **AI自己レビュー（追加）**: Test Hacking検出、完成度100点評価
  - **Human Review**: 最終確認
- なぜ工夫が必要か
  - AIは「テストが通る = 完了」と誤解する
  - Plan無しだと暴走（Scope Creep）する
  - 静的解析無しだと構文エラーを見逃す
  - AI自己レビュー無しだとTest Hackingを見逃す

---
<!-- _class: font-xxsmall -->

### 7段階TDD詳細 - 各段階で何をチェックするのか
- Plan
  - 受入条件（チェックリスト、GIVEN WHEN THEN）の詳細を計画
  - docs/内の設計書を参照してゴールを明確化
  - 利用するAPIライブラリの詳細をWEB検索して事前に知識を得る
  - AIに質問させる「実装前に曖昧な点があれば質問してください」
- Red
  - 受入条件→pytestでテストファースト
  - 実装がないのでpytest は失敗（赤）が正常
- Green
  - 最小実装のみ、設計書に従う
  - Issue範囲外の機能は作らない（Scope Creep防止）
- Refactor
  - Cyclomatic Complexity < 10（分岐の複雑さ指標、詳細はセクション5）
  - 重複削除、テストは変えずに実装の品質を改善
- System Review
  - pytest + flake8 + mypyで自動検証
- AI Self Review
  - Test Hacking検出、完成度0-100点評価
- Human Review
  - git diff、ビジネスロジック確認

---
<!-- _class: font-xsmall -->

### Plan - 実装方針の確認
- Issueの内容確認
  - BDDテストシナリオ（GIVEN WHEN THEN）
  - 参照設計書（画面・DB・API）
  - 実装の制約（コーディング規約）
- 実装方針の決定
  - どのモジュール・関数を修正するか
  - どのテストを書くか
- AIに質問させる
  - 「実装前に曖昧な点があれば質問してください」
  - AIが勝手に推測しないよう、質問を促す

---
<!-- _class: font-xsmall -->

### Red - テストファースト
- **受入条件をpytestに変換**
  - GIVEN → @pytest.fixture（fixture = テストの前準備を行う関数、テストデータやモックを用意）
  - WHEN → テスト対象関数呼び出し
  - THEN → assert文
- **実装がないのでpytestは失敗（赤）が正常**
  - 赤にならない場合は、テストが実装に依存している
  - `ImportError`や`AssertionError`が出ることが正常
- **テストサイズ**
  - 非常に少量（5行以下）
  - シンプルなテストから始める

---
<!-- _class: font-xsmall -->

### Green - 最小実装
- **テストを通すための最小限の実装**
  - 設計書に従う
  - 過剰な実装はしない
  - 美しさや効率は後回し、「動く」ことが最優先
- **Issue範囲外の機能は作らない**
  - Scope Creep防止
  - 余計な機能は追加しない
- **節約の法則（law of parsimony）**
  - テストを満たすのに十分なコードのみを書く
- **pytestが成功（緑）したら次のRefactorフェーズへ**

---
<!-- _class: font-xsmall -->

### Refactor - コード品質改善
- **テストは変えずに実装の品質を改善**
  - 動作を変更せずにコードを改善
  - テストが通る状態を保ちながらコードの品質を向上
- **改善項目**
  - Cyclomatic Complexity < 10
  - マジックナンバー排除
  - 重複コード削除
  - 命名規則の改善（PEP 8準拠）
- **リファクタリングのパターン**
  - Extract Function（関数抽出）
  - Guard Clause（早期リターン）
  - DRY原則（Don't Repeat Yourself）
- **Refactor後もpytestは通り続けること**

---
<!-- _class: font-xsmall -->

### System Review - 自動検証ツールによる機械的チェック
- AI Hallucination、構文エラー、静的解析エラーを機械的に検出
- pytest + 静的解析ツールで実行
  - 構文チェック（Python実行）
  - 全テスト実行（pytest）
  - 静的解析（flake8、mypy、ruff）
  - カバレッジ測定（pytest-cov）
- **Python静的解析ツールの比較**

| ツール | 主な検出内容 | 推奨タイミング |
|--------|-------------|---------------|
| flake8 | PEP 8違反、構文エラー | 開発中（IDE統合） |
| mypy | 型エラー、型安全性 | コミット前 |
| ruff | 高速なlint、フォーマット | リファクタリング前 |

---
<!-- _class: font-xsmall -->

### AI Self Review - Test Hacking検出の要
- Test Hackingを検出
  - テストを通すだけの仮実装を排除
- チェック項目
  - ①不要なフォールバック処理
  - ②仮想データ返却
  - ③モックによるダミーデータ返却
  - ④テストを通すだけの実装
  - ⑤受入条件未達
  - ⑥Silent Fail
- **完成度0-100点評価**
  - 「受入条件に対して、完成度を0-100点で評価して」
  - 80点以上を目標に繰り返す（重要な機能は90点以上）
  - 時間対効果を考慮し、完璧より「十分良い」を選ぶ

---
<!-- _class: font-xsmall -->

### Human Review - ビジネスロジックの最終確認
- ビジネスロジックとアーキテクチャの妥当性を人間が判断
- 基本レビュー観点
  - ビジネスルール（業務要件との一致）
  - データアクセス一貫性（トランザクション境界）
  - Scope Creep検出（Issue範囲外の機能追加）
- オプション: 複数AIレビュー（重要な機能のみ）
  - **Repomix**: リポジトリ全体を1ファイルにまとめるツール
  - Repomixの出力を複数のAI（GPT-4、Claude WEB等）に投げて比較
  - なぜ複数AI？: 1つのAIでは見逃すバグを別のAIが発見することがある
  - 対象: 認証、決済、セキュリティクリティカルな機能

---
<!-- _class: font-xsmall -->

### TDD実装サイクルの全体像 - 実践時の自動化
- **1つのIssue（10分タスク）の流れ**
  - Plan → Red → Green → Refactor → 3段階レビュー
- **サイクル頻度**
  - 3〜5サイクルを速く実行、その後リファクタリングに時間をかける
- **カスタムコマンド`/tdd`でAI Self Reviewまで自動化**
  - Human Reviewのみ手動（git diff確認）
- **7段階TDDの実践により、AI特性5つを効果的に防止**
  - 暴走（Scope Creep）、手抜き（Reward Hacking）
  - 忘れっぽさ（Context Limitations）、凸凹知能（Jagged Intelligence）
  - 虚偽報告（Hallucination）

---
<!-- _class: font-xsmall -->

### TDD無しの悪夢 - AI特性5つが同時多発
- TDD無しの場合（人間がAIの奴隷）
  - ①AI実装 → ②人間が手作業確認 → ③エラー発見 → ④人間がAIに報告
  - ⑤AI修正 → ②に戻る（永遠に繰り返す）
  - 具体例: ユーザー登録機能
    - 第1サイクル: 500エラー（AttributeError: 'NoneType'）
    - 第2サイクル: パスワード平文保存
    - 第3サイクル: 重複メールで登録可能
    - 第4サイクル: 無効なメールで登録可能
- TDDありの場合（AIが自律的）
  - 人間: 受入条件定義（1回だけ）
  - AI: テスト作成 → 実装 → テスト実行 → **自分で問題発見** → **自分で修正**
  - **効果: 210分 → 35分（83%削減）**

---
<!-- _class: font-xsmall -->

### よくある失敗パターン
- **失敗1: テストを後回し**
  - 実装を先に書いて、後からテストを追加
  - これはTDDではなく「テスト付き開発」
  - 対策: 必ずテストファースト、Redフェーズから始める
- **失敗2: AI Self Reviewのスキップ**
  - System Reviewが通ったら即コミット
  - テストは通るが仮実装（ダミーデータ返却）のまま
  - 対策: AI Self Reviewを必ず実施、80点以上を目指す

---

## セクション4: MCP Servers

**7段階TDDをさらに強化するツールがMCP Serversです。** セクション3で学んだTDDサイクルの「⑤虚偽報告対策」「③忘れっぽさ対策」を、MCPサーバーが自動化・効率化してくれます。

---
<!-- _class: font-xsmall -->

### このセクションで学ぶこと
- **対応するAI特性**
  - ③忘れっぽさ → Serenaでトークン最適化、Compactを防止
  - ⑤虚偽報告 → Context7で最新APIドキュメントをリアルタイム取得
- **学習内容**
  - MCPの概要とClaude Code対応
  - Context7: 最新APIドキュメント取得
  - Serena: トークン最適化
  - Playwright/Chrome DevTools: E2Eテスト・デバッグ
- **ゴール**
  - TDDを支援するMCPサーバーを導入できる

---
<!-- _class: font-xsmall -->

### MCP Serversとは - TDD実装の支援ツール
- Model Context Protocol（MCP）
  - AIに外部ツールを接続する標準プロトコル
  - Anthropicが2024年11月に発表
- Claude Codeは標準でMCP対応
- TDD実装に役立つMCPサーバー
  - Context7（最新APIドキュメント）
  - Serena（トークン最適化）
  - Playwright（E2Eテスト自動生成）
  - Chrome DevTools（UIデバッグ）

---
<!-- _class: font-xsmall -->

### Context7 MCP Server - 最新APIドキュメント
- 目的
  - SQLAlchemy、pytest、Pydantic等の最新公式ドキュメントをリアルタイム取得
  - AI Hallucinationを防ぐ
- 仕組み
  - Claude CodeがAPIを使うとき、Context7が自動で最新ドキュメントを検索して提供
  - 学習データにない最新バージョンにも対応
- 効果
  - 存在しないAPIの推測を防ぐ
  - 正確なコード生成

---
<!-- _class: font-xsmall -->

### Serena MCP Server - トークン最適化
- 目的
  - **LSP（Language Server Protocol）**: IDEが使うコード解析プロトコル
  - LSPを使って、AIに必要なコードだけを効率的に読ませる
  - ③忘れっぽさ（Context Limitations）への対策
- **Compactとは何か**
  - AIの会話が長くなると、古い情報を圧縮（Compact）して忘れる
  - 重要な指示やコードがCompactで失われる → 「さっき言ったのに忘れた」
- 効果
  - トークン使用量を大幅削減（最大90%削減）
  - Compactが発生しにくくなり、指示を忘れにくくなる
  - 思考に使えるトークンが増える

---
<!-- _class: font-xsmall -->

### Playwright / Chrome DevTools MCP Server
- **Playwright MCP Server - E2Eテスト自動生成**
  - E2E（End-to-End）テスト = ユーザー操作を模倣してシステム全体を通しで検証するテスト
  - AI駆動でEnd-to-Endテストを自動生成
  - Claude Codeに「TODO作成フローのE2Eテストを作って」と指示
  - Playwrightスクリプトを生成、実行、スクリーンショット取得
- **Chrome DevTools MCP Server - UIデバッグ**
  - AIに「目」を与える
  - Claude CodeがChromeのDevToolsにアクセス
  - コンソールエラー、ネットワークエラー、パフォーマンス問題を自動検出
  - 従来5-10分かかる作業が1分に短縮

---
<!-- _class: font-xsmall -->

### MCPサーバーのインストール
- Claude CLIの `claude mcp add` コマンドでインストール
  - `-s user` または `--scope user` でユーザー全体に適用
- インストールコマンド
  - Context7: `claude mcp add context7 -s user -- npx -y @upstash/context7-mcp`
  - Serena: `claude mcp add serena -- uvx --from git+https://github.com/oraios/serena serena start-mcp-server`
  - Playwright: `claude mcp add playwright -s user -- npx -y @executeautomation/playwright-mcp-server`
- 一度インストールすれば全セッションで利用可能

---

## セクション5: STEP 5 - 品質改善

---
<!-- _class: font-xsmall -->

### このセクションで学ぶこと
- **対応するAI特性**
  - ②手抜き → 完成度評価で80点以上を目指す
  - ③忘れっぽさ → /clearでコンテキストリセット、次タスクへ
- **学習内容**
  - 8つの質問と指示（リファクタリング、ドキュメント、知見保存）
  - 完成度0-100点評価の実践
  - /clearによるコンテキスト管理
  - 後方互換性の判断基準
- **ゴール**
  - 8つの質問と指示を実行できる
  - 80点以上を目指す習慣を身につける

---
<!-- _class: font-xsmall -->

### STEP 5 - AIに任せる8つの質問と指示
- STEP 5をAIに任せる
  - ①-③リファクタリング
  - ④-⑤ライブラリ・パターン活用
  - ⑥-⑦ドキュメント化
  - ⑧知見の保存
- 人間は結果をレビューするだけで作業時間80%削減
- ⑧の実行後`/clear`でコンテキストをクリア
  - コンテキスト汚染を防ぐ
  - 次のタスクで前のタスクの情報が混入しない

---
<!-- _class: font-xsmall -->

### ①②技術的負債の発見と冗長コード削除
- **AIは冗長・重複・dead codeを生成しがち**
  - 似たような処理を何度も書く
  - 不要になったコードを削除しない
  - 使われていない変数・関数を残す
- ①技術的負債を見付けて
  - Claude Codeに質問
  - AIが問題箇所をリスト化、優先度付け
- ②冗長・重複・dead codeを削除して
  - 重複コードを関数抽出
  - DRY原則徹底、コード量20-30%削減
- **定期的なクリーンアップが必要**
  - タスク完了ごとに②を実行

---
<!-- _class: font-xsmall -->

### ③循環的複雑度を減らして
- **推奨される閾値**（NIST SP 500-235 = 米国標準技術研究所のソフトウェア品質ガイドライン）
  - **1-10**: シンプル、低リスク → 目標
  - **11-20**: 中程度の複雑さ、中程度のリスク
  - **21-50**: 複雑、高リスク → 要リファクタリング
  - **50+**: 非常に複雑、テスト不可能 → 即座にリファクタリング
- **複雑度を減らす5つの戦略**
  - ①小さな関数（20-30行以内）
  - ②リファクタリング（関数分割）
  - ③早期リターン（ガード節）
  - ④複雑な条件式の抽出
  - ⑤パターンの適用（Strategy、Map）
- **Claude Codeへの指示**: 「循環的複雑度を10以下に減らして」

---
<!-- _class: font-xsmall -->

### ④⑤ライブラリとデザインパターンの活用
- ④効果的にライブラリを活用できる箇所は
  - AIが提案しないので自分から積極的に指定・質問する必要がある有用ライブラリの例
    - attrs（ボイラープレート削減、dataclassesより高機能）
    - more-itertools（イテレータ拡張）
    - toolz（関数型プログラミング）
- ⑤効果的にデザインパターンを活用できる箇所は
  - AIが提案
    - Strategy（戦略パターン）
    - Factory（ファクトリーパターン）
    - Builder（ビルダーパターン）
    - Dependency Injection（依存性注入）
    - Repository（リポジトリパターン）
  - 注意: 過剰なパターン適用は避ける

---
<!-- _class: font-xsmall -->

### ⑥docstring を書いて
- Claude Codeへの指示
  - 「全public関数にdocstringを書いて（Google Style）」
- AIが自動生成
  - Args:（パラメータ説明）
  - Returns:（戻り値説明）
  - Raises:（例外説明）
  - 関数・クラスの概要
- HTML生成
  - pdoc または Sphinx で自動生成

---
<!-- _class: font-xsmall -->

### ⑦arc42 と C4 Model を採用した ADR を書いて
- **用語解説**
  - **ADR（Architecture Decision Record）**: 技術的決定を記録するドキュメント
  - **arc42**: ドイツ発のアーキテクチャ文書テンプレート（構造が明確）
  - **C4 Model**: システム構造を4段階（Context→Container→Component→Code）で図示
- Claude Codeへの指示
  - 「[技術的決定]のADRを、arc42とC4 Modelで作って」
- AIが生成するADR構造
  - Status（状態: 提案、承認、廃止）
  - Context（背景: なぜこの決定が必要か）
  - Decision（決定内容: 何を決めたか）
  - Consequences（結果: どのような影響があるか）
- 効果
  - 「なぜこの技術を選んだか」を将来の自分やチームに残せる

---
<!-- _class: font-xsmall -->

### ⑧実装で得られた知見のドキュメント化
- なぜ知見を保存するのか
  - 実装中に発見した問題・解決策・落とし穴は会話の中にしかない
  - AIとの会話が長くなるとCompact（圧縮）されて失われる
  - ファイルに保存すれば、次回以降も参照できる
  - docs/lessons-learned/に保存してチーム全体で知見を共有
- Claude Codeへの指示
  - 「この実装で得られた教訓・落とし穴・ベストプラクティスをdocs/lessons-learned/YYYY-MM-DD-[機能名].md に保存して」
- 保存後に`/clear`でコンテキストをクリア
  - コンテキスト汚染を防ぐ

---
<!-- _class: font-xsmall -->

### 【補足】後方互換性の問題 - AIの過剰な配慮
- **AIは後方互換性を過剰に維持しようとする**
  - 古い関数にwarnings.warnを追加して残す
  - 新旧両方のAPIを維持しようとする
  - 不要な互換性レイヤーを追加する
- **なぜ問題か**
  - コードが複雑になる
  - 保守コストが増加
  - 技術的負債の蓄積
- **人間が判断すべきこと**
  - 本当に後方互換性が必要か？
  - 社内システムなら不要なことが多い
  - 外部API公開なら必要
- **対処法**
  - AIに「後方互換性は不要。古いコードは削除して」と明示

---

## まとめとQ&A

---
<!-- _class: font-xsmall -->

### 実装・品質改善編のまとめ
- STEP 4（7段階TDDサイクル + MCP Servers）
  - AI特性5つを7段階で完全防止
  - 作業時間83%削減（210分→35分）
  - カスタムコマンド`/tdd`でAI Self Reviewまで自動化
- STEP 5（8つの質問と指示で品質改善）
  - ①-③リファクタリング
  - ④-⑤ライブラリ・パターン
  - ⑥-⑦ドキュメント化
  - ⑧知見保存
  - 人間は結果をレビューするだけで作業時間80%削減

---
<!-- _class: font-xsmall -->

### Q&A
- Q1: 7段階TDD必須か?
  - AI駆動開発では必須
  - 従来の3段階ではTest Hackingを見逃す
- Q2: AI Self ReviewでTest Hackingを本当に検出できるのか?
  - はい、AIは「レビューして」と言われると客観的に評価する
  - 実装時は「テストを通す」が目標、レビュー時は「品質評価」が目標になる
  - 役割を変えることで、自分の実装の問題点を指摘できる
  - 80点以上になるまで自動修正を繰り返す
- Q3: System Reviewだけではダメなのか?
  - System Reviewは「構文チェック・テストが通る」だけ
  - Test Hacking（仮実装）は検出できない
  - AI Self Reviewで完成度を確認する必要がある
- Q4: 複数AIレビュー（Repomix）は毎回やるべきか?
  - 重要な機能（認証、決済、セキュリティクリティカル）でのみ実施


