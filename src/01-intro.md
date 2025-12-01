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
    font-size: 20px !important;
    line-height: 1.35 !important;
    padding: 35px 50px !important;
  }
  section[data-class~="font-small"] h2 {
    font-size: 32px !important;
  }
  section[data-class~="font-small"] li {
    margin-bottom: 0.15em !important;
  }

  section[data-class~="font-xsmall"] {
    font-size: 18px !important;
    line-height: 1.25 !important;
    padding: 30px 50px !important;
  }
  section[data-class~="font-xsmall"] h2 {
    font-size: 28px !important;
  }
  section[data-class~="font-xsmall"] li {
    margin-bottom: 0.1em !important;
  }

  section[data-class~="font-xxsmall"] {
    font-size: 16px !important;
    line-height: 1.2 !important;
    padding: 25px 45px !important;
  }
  section[data-class~="font-xxsmall"] h2 {
    font-size: 24px !important;
  }
  section[data-class~="font-xxsmall"] li {
    margin-bottom: 0.05em !important;
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


# AI駆動開発セミナー Day 1
## 入門編：AIとの正しい付き合い方

**対象者**: Python開発者（AI駆動開発は初心者）
**学習目標**: AI駆動開発の基本的なマインドセット、Claude Code活用法、プロジェクト初期化、AI特性理解、5-STEPワークフローの完全理解

---
<!-- _class: font-xsmall -->

## なぜAI駆動開発なのか

---
<!-- _class: font-small -->

### 成功例① Harvard/BCG研究（2023年）

**研究概要**
- BCGコンサルタント758人を対象にGPT-4の効果を測定
- 対象者：学士以上、実務経験4年以内のジュニアコンサルタント
- 3グループに分割：①AI未使用、②GPT-4使用、③GPT-4＋プロンプト指導

**結果（AIの得意領域のタスク）**
- タスク完了数：12.2%増加
- 作業速度：25.1%高速化
- 成果物の品質：40%以上向上

**重要な発見：「凸凹フロンティア」**
- AIが苦手な領域のタスクでは、正解率が19ポイント低下
- AIの得意・不得意を見極めることが成功の鍵

---
<!-- _class: font-small -->

### 成功例② 楽天のClaude Code活用事例（2025年）

**タスク内容**
- vLLM（オープンソースLLM推論ライブラリ、1,250万行）に対して
- 特定のActivation Vector抽出手法を実装

**驚異的な結果**
- Claude Codeが**7時間連続で自律作業**（人間は方向修正のみ）
- 実装精度：リファレンス手法と比較して**99.9%の数値精度**
- 「7時間、私はコードを1行も書かなかった」（機械学習エンジニア談）

**ビジネスインパクト**
- 機能リリース期間：24営業日 → 5日（**79%短縮**）
- 並列作業：5タスクを同時進行（4つをClaude Codeに委任）

---
<!-- _class: font-small -->

### 失敗例① Uplevel社調査（2024年）- バグ41%増加

**研究概要**
- 約800人の開発者を対象にGitHub Copilotの効果を測定
- 期間：導入前（2023年1-4月）と導入後（2024年1-4月）を比較
- 測定指標：サイクルタイム、PRスループット、バグ率、残業時間

**衝撃的な結果**
- **バグ率：41%増加**（Copilot使用グループ）
- PRスループット：有意な変化なし（速くなっていない）
- バーンアウトリスク軽減：Copilotなし28%減 vs Copilotあり17%減

**原因の考察**
- 「AIはWeb上の様々な品質のコードで訓練されている」（Uplevel PM談）
- Copilotへのアクセス権があるだけで、適切な使い方の指導がなかった

---
<!-- _class: font-small -->

### 失敗例② GitClear社調査（2025年）- コード品質の劣化

**研究概要**
- **2億1,100万行**のコード変更を分析（2020年1月〜2024年12月）
- 史上最大規模のコード品質調査

**深刻な発見**
- **コード重複：8倍増加**（5行以上の重複ブロック）
- リファクタリング比率：25%（2021年）→ **10%未満**（2024年）
- コードチャーン（2週間以内の修正）：3.1%（2020年）→ **5.7%**（2024年）

**長期的な影響**
- 「Copy/Paste」が「Move（リファクタリング）」を初めて上回った
- 「35年のキャリアで、これほど短期間に技術的負債が蓄積されるのを見たことがない」（API専門家談）
- 2025年予測：リファクタリングは全変更の**3%以下**に

---
<!-- _class: font-small -->

### 失敗例③ Google DORA 2025 - AIは組織を増幅する

**調査概要**
- 約5,000人の技術者を対象に調査
- AI採用率：90%（前年比14%増）、1日平均2時間AI使用

**光と影**
- **ポジティブ**：80%以上が「生産性向上」を実感、スループット向上
- **ネガティブ**：ソフトウェア配信の安定性は**低下**

**重要な発見：AIは「増幅器」**
- AIは組織の強みも弱みも増幅する
- 自動テスト、バージョン管理、フィードバックループが弱いと → 不安定化
- **30%がAI生成コードを「信頼していない」**

**Stack Overflow 2025調査**
- 66%：「AIの回答は"ほぼ正しい"が完全ではない」が最大の課題
- 45%：「AI生成コードのデバッグは時間がかかる」

---
<!-- _class: font-small -->

### 失敗例④ エンジニアのバーンアウト（2024年調査）

**調査概要**
- 604人のソフトウェア開発者・エンジニアを対象
- AI導入組織（61%）とそうでない組織を比較

**深刻な結果**
- **65%がバーンアウトを経験**（AI導入の有無に関わらず）
- 43%：「経営層は現場の課題を理解していない」
- 37%：「効率性・予測可能性・生産性が過去1年で低下」

**AIがバーンアウトを悪化させる理由（Harness調査）**
- 95-98%：「AIでバーンアウトが減る」と**期待**
- **67%**：「AI生成コードのデバッグに**より多くの時間**がかかる」（現実）
- **68%**：「AI関連のセキュリティ問題の修正に**より多くの時間**」（現実）

**結論**：AIは銀の弾丸ではない。正しい使い方を学ばないと逆効果

---
<!-- _class: font-xsmall -->

### CrowdStrike事件 - 検証不足が招いた大規模障害

**2024年7月19日の事件**
- 全世界で約850万台のWindowsデバイスがブルースクリーン
- 航空会社、銀行、病院など社会インフラに深刻な影響
- 原因：ソフトウェアアップデートの検証不足

**AI時代の教訓**
- 自動化されたプロセスでも人間の検証が必要
- "Trust but Verify"（信頼しつつ検証する）の重要性
- テスト環境と本番環境の差異に注意

**被害規模**
- 推定損害額：数十億ドル規模
- 復旧に数日〜数週間を要したケースも

---
<!-- _class: font-small -->

## AIの5つの特性を理解する

**なぜ特性を理解するのか？** → 前スライドの失敗例（エラー率2倍、コード重複8倍）は、AIの特性を知らずに使った結果です。特性を理解すれば、対策を打てます。

---
<!-- _class: font-xsmall -->

### AIが持つ5つの特性（1/2）

**1. 暴走（Scope Creep）**
- Issue範囲外の機能を勝手に追加
- 本質的対策：仕様書で機能範囲を明確化、受入基準で「完了」を定義

**2. 手抜き（Test Hacking）**
- テストを通すだけの仮実装
- 本質的対策：受入基準を具体的かつ厳密に記述、テストケースを事前に明記

**3. 忘れっぽさ（Context Loss）**
- 過去の指示を忘れる、コンテキスト汚染
- 本質的対策：CLAUDE.mdに永続ルール記載、**Claude Skills**で再利用可能な知識を定義

---

### AIが持つ5つの特性（2/2）

**4. 凸凹知能（Jagged Intelligence）**
- 得意分野と苦手分野の差が激しい
- 本質的対策：人間がAIの能力限界を理解し、適切な期待値を持つ

**5. 虚偽報告（Hallucination）**
- 自信満々に誤った情報を提供
- 本質的対策：自動テスト（pytest, ruff, pyright）、公式ドキュメント確認

---

### AIの特性への対策まとめ

| 特性 | 問題 | 本質的対策 |
|------|------|------|
| 暴走 | 機能追加しすぎ | 仕様書・受入基準で範囲を明確化 |
| 手抜き | テストだけ通す | 受入基準・テストケースを事前定義 |
| 忘れっぽさ | 指示を忘れる | CLAUDE.md・Claude Skills・/clear |
| 凸凹知能 | 得意不得意が激しい | 人間が期待値を適切に管理 |
| 虚偽報告 | 誤った情報 | pytest/ruff/pyright、公式ドキュメント |

**重要**: これらの特性を理解して対策すれば、AIは強力なパートナーになる

---

## AIとの付き合い方：3つの原則

**5つの特性への対策を、覚えやすい3つの原則に整理します。** これを守れば、前述の5特性すべてに対処できます。

---
<!-- _class: font-xsmall -->

### 原則1: Trust but Verify（信頼しつつ検証する）

**AIは優秀だが完璧ではない**
- テストは通るが本番で動かない
- 「完成しました！」と報告するが実際は不完全
- 自信満々に誤った情報を提供する

**対策：3段階レビュー**
1. 自動検証（pytest && ruff check && pyright）
2. AI自己検証（「100点満点で評価して」）
3. 人間レビュー（git diff確認）

---
<!-- _class: font-xsmall -->

### Trust but Verify の起源

**レーガン大統領と核軍縮交渉**
- 1987年、米ソ間の中距離核戦力全廃条約（INF条約）
- レーガン大統領がロシアのことわざを引用
- 「Doveryay, no proveryay」（信頼せよ、されど検証せよ）

**AI開発への適用**
- AIは優秀なパートナーだが、盲目的な信頼は危険
- 出力は必ず検証する
- 検証プロセスを仕組み化する（自動テスト、レビュー）

**「信頼」と「検証」のバランス**
- 過度な不信：AIの恩恵を受けられない
- 過度な信頼：品質低下、障害のリスク
- 適切なバランス：効率と品質の両立

---
<!-- _class: font-xsmall -->

### 原則2: Context is the New Code（コンテキストが全て）

**AIは外部メモリが必要**
- Claude Codeのコンテキスト上限：200Kトークン（約13万文字）
- **設計書なしの場合**
  - 全ソースコード（数万行）を読む → 150Kトークン消費
  - 残り50Kトークンで思考 → 単純なCRUDしか作れない
- **設計書ありの場合**
  - 設計書（数十ページ）を読む → 30Kトークン
  - 残り170Kトークンで思考 → 複雑なロジックも対応可能（**3.4倍**）

**コンテキストの種類**
- CLAUDE.md：プロジェクトルール（Claudeが最初に読む）
- README.md：プロジェクト概要
- 設計書：画面、DB、API仕様
- Issue：タスク定義
- 受入基準（AC）：「何ができればOKか」

**研究データ**
- Microsoft研究：明示的仕様で改良が68%削減（初回で正しいコード生成）
- Stanford研究：標準化で満足度89% vs 非標準化34%（2.6倍）
- 設計に2時間投資 → 実装10時間→3時間に短縮（ROI 3.5倍）

---
<!-- _class: font-xxsmall -->

### Context is the New Code - 研究データ

**Microsoft Research 2023**
- 明示的な仕様で改良（修正要求）が68%削減

**Stanford HAI 2024**
- 標準化されたコンテキストで満足度89%（非標準34%）

**実務での効果**
- 設計2時間投資 → 実装10時間→3時間（ROI 3.5倍）

---

### 原則3: 段階的に進める

**なぜ段階的に進めるのか**
- AIの集中力には限界がある
- 長いタスクは暴走・手抜き・忘れるリスク増大
- 小さなステップで品質を維持

**具体例：ユーザー認証機能**

❌ 悪い例（大きすぎる）:
「ユーザー認証機能を実装して」

✅ 良い例（段階的）:
1. Userモデルを作成（10分）
2. パスワードハッシュ化を実装（10分）
3. ログインエンドポイントを作成（10分）
4. JWTトークン発行を実装（10分）※JWT = JSON Web Token、認証情報を安全に伝達する標準形式

**効果**: 各ステップで品質確認、問題の早期発見、進捗が明確

---
<!-- _class: font-xsmall -->

## Claude Codeとは：AI駆動開発のツール

**3つの原則を実践するためのツールがClaude Codeです。** CLAUDE.mdでコンテキストを与え、段階的にタスクを実行し、検証を自動化できます。

---
<!-- _class: font-xsmall -->

### Claude Codeの基本

**Claude Codeとは**
- AnthropicのCLIツール（コマンドライン上で動作）
- Claude AIとの対話でコード開発を行う
- ファイル読み書き、コマンド実行が可能

**3つの重要ファイル**
- CLAUDE.md：プロジェクトのルール（Claudeが最初に読む）
- README.md：プロジェクト概要
- .claude/commands/：カスタムコマンド格納場所

**特徴**
- 200Kトークンのコンテキスト容量
- ファイル検索・編集・テスト実行を自動化
- チャット履歴を保持してコンテキストを維持

---
<!-- _class: font-small -->

### Claude Skills とは

**Skills の概念**
- AIの能力を拡張するための設定ファイル
- `.claude/skills/` ディレクトリに配置
- 特定のタスクに特化した指示を定義

**Skills の種類**
- コード生成スキル: 言語やフレームワーク固有のルール
- 品質管理スキル: テスト、レビューの自動化
- ドキュメントスキル: 仕様書、README生成

**忘れっぽさへの対策**
- CLAUDE.mdだけでは伝えきれない詳細なルールを保存
- タスク種別ごとに最適な指示を再利用可能
- プロジェクト固有の知識を永続化

---
<!-- _class: font-xxsmall -->

### コンテキストとトークンの理解

**トークンとは**
- テキストの単位（日本語：約1.5文字/トークン、英語：約4文字/トークン）
- Claude Codeの容量：200,000トークン（約13万文字の日本語）

**コンテキストの使われ方**
```
200K トークン
├── 読み込んだコード: 150K
└── 思考・生成: 50K  ← これでは単純なCRUDしか作れない

200K トークン
├── 設計書: 30K
└── 思考・生成: 170K  ← 複雑なロジックも対応可能（3.4倍！）
```

**だから設計書が重要**
- 設計書があればAIの思考容量が3.4倍に
- コード全体を読む必要がなくなる

---
<!-- _class: font-xsmall -->

### Claude Codeの4つのモード

**Normal（通常モード）**
- 慎重に動作、ユーザーに確認を取る
- ファイル変更前に許可を求める
- 初心者向け、安全重視

**Plan（プランモード）**
- 実装前に計画を立てる
- タスクを分解して提示
- 承認後に実装開始

**Yolo（高速モード）**
- 確認なしで高速実行
- 危険な操作も即実行
- 上級者向け、スピード重視

**Bypass Permissions（権限バイパス）**
- ファイル操作の許可を自動承認
- 繰り返し作業の効率化

---
<!-- _class: font-xsmall -->

### カスタムコマンド: TDDサイクル

**カスタムコマンドとは**
- よく使う指示を登録して再利用
- `.claude/commands/` に保存
- `/コマンド名` で実行

**TDDサイクル用コマンド**
- `/tdd-plan`：実装計画を立てる
- `/tdd-red`：失敗するテストを書く
- `/tdd-green`：テストを通す最小実装
- `/tdd-refactor`：コードを改善
- `/tdd-verify`：完成度を検証

**使用例**
```bash
/tdd-plan ユーザー認証機能
/tdd-red ログイン機能のテストを書いて
/tdd-green テストを通して
/tdd-refactor コードを改善して
```

---
<!-- _class: font-small -->

### CLAUDE.mdとREADME.md

**CLAUDE.md（最重要）**
- Claudeが最初に読むプロジェクトルール
- コーディング規約、アーキテクチャ方針を記載
- 例：「テストカバレッジ80%以上必須」「実装前に不明点があれば質問すること」

**README.md**
- プロジェクト概要、セットアップ方法
- 人間とAI両方が読む
- プロジェクトの全体像を把握

**効果**
- CLAUDE.mdがあれば、毎回同じ指示を繰り返さなくていい
- プロジェクト全体で一貫した品質を保てる
- 新しいタスクでもルールを自動適用

---
<!-- _class: font-xxsmall -->

### CLAUDE.md のディレクトリ別配置

**モノレポでの活用**（モノレポ = 1つのリポジトリで複数プロジェクトを管理する手法）
```
project/
├── CLAUDE.md       ← 全体ルール
├── frontend/CLAUDE.md  ← フロントエンド固有
├── backend/CLAUDE.md   ← バックエンド固有
└── tests/CLAUDE.md     ← テスト固有
```

**ディレクトリ別ルールの例**
- frontend/: React、biome
- backend/: Python、ruff/pyright
- tests/: pytest、80%カバレッジ

---

### AIにあいまいな点を明確化させる

**問題：AIは推測で進める**
- 技術スタック未定義 → 勝手にライブラリを選択
- テスト方法不明 → ハードコードで済ませる
- 設計方針なし → 独自の判断で実装

**CLAUDE.mdに記載する指示**
```markdown
実装前に、以下について不明・あいまいな点があれば必ず質問してください：
- 使用する技術スタック・ライブラリ
- テスト方法とカバレッジ目標
- エラーハンドリングの方針
```

**AIからの質問例**
- 「Webフレームワークは？（FastAPI / Django / Flask）」
- 「DBは？（PostgreSQL / SQLite / MySQL）」
- 「テストカバレッジ目標は何%ですか？」

**効果**: 技術選定のミスマッチ防止、一貫性、手戻り削減

---
<!-- _class: font-xsmall -->

## プロジェクトの初期化（ハンズオン）

---
<!-- _class: font-xsmall -->

### 開発環境の準備

**必要なツール**
- Python 3.12以上
- Git
- mise（複数言語のバージョン管理ツール、pyenv/nodenvの統合版）
- IDE（VS Code + Python拡張）

**Claude Code CLIインストール**
```bash
npm install -g @anthropic-ai/claude-code
```

**APIキー設定**
- Claude.aiでAPIキーを取得
- 環境変数に設定またはCLIで設定
- 初回起動時に認証

---
<!-- _class: font-xxsmall -->

### モダンなPython開発ツール

**mise**: pyenv + nodenv + rbenvを1つに統合したツール。プロジェクトごとに言語バージョンを自動切り替え

**ruff**: Pythonの高速リンター・フォーマッター（Rust製、10-100倍高速）

**pyright**: 静的型解析でバグを早期発見

---

### Pythonプロジェクトの作成

**ステップ1: プロジェクト作成**
```bash
mkdir todo-app && cd todo-app
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn sqlalchemy pytest ruff pyright
```

**ステップ2: git初期化**
```bash
git init
echo -e ".venv/\n__pycache__/\n.pytest_cache/" >> .gitignore
git add .
git commit -m "chore: initial commit"
```

**重要**: `.gitignore`に仮想環境、キャッシュを追加

---

### CLAUDE.md作成（最重要）

**ステップ3: CLAUDE.md作成**

プロジェクトルートに`CLAUDE.md`を作成：

```markdown
# TODO管理アプリ

## プロジェクト概要
FastAPIによるTODO管理Web API

## 技術スタック
- Python 3.12
- FastAPI
- SQLAlchemy
- SQLite（開発用）
- pytest

## ディレクトリ構造
- app/
  - main.py - エントリーポイント
  - models.py - SQLAlchemyモデル
  - schemas.py - Pydanticスキーマ
  - crud.py - データアクセス
  - routers/ - APIルーター

## コーディング規約
- ruff でフォーマット・リント
- pyright で型チェック
- テストカバレッジ80%以上必須
- 実装前に不明点があれば必ず質問すること
```

**効果**: Claudeが毎回このルールに従う

---

### README.md作成

**ステップ4: README.md作成**

```markdown
# TODO管理アプリ

## セットアップ
\`\`\`bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
\`\`\`

## テスト実行
\`\`\`bash
pytest
\`\`\`
```

**AIがREADMEを読む**: プロジェクト全体を理解

---
<!-- _class: font-small -->

### カスタムコマンドの準備

**ステップ5: カスタムコマンド作成（オプション）**

`.claude/commands/plan.md`を作成：

```markdown
実装前に計画を立ててください：

1. 実装する機能リスト
2. 変更するファイルリスト
3. 新規作成するファイルリスト
4. テスト戦略
5. 所要時間見積もり

計画を承認してから実装を開始してください。
```

**使用方法**: `/plan ユーザー作成機能`

---
<!-- _class: font-xxsmall -->

### 成果物の確認

**ステップ6: 成果物確認**

```bash
git status
```

**確認項目**: ✅ CLAUDE.md、✅ README.md、✅ .gitignore、✅ pytest実行可能

**これで準備完了**: 02以降で使い続ける

---

### Claude Codeの使い方のコツ

**モード切り替え（Shift+Tab）**
- **Normalモード**：標準、確認しながら進める
- **Planモード**：実装前に計画を立てる
- **Yolomode**：高速・自律的（上級者向け）
- **Bypass permission**：権限チェックをスキップ

**`/clear`コマンドの重要性**
- タスク完了ごとに`/clear`でコンテキストをクリア
- コンテキスト汚染を防ぐ（前のタスクの誤りが次に伝播するのを防止）
- 間違いに気づいたら訂正ではなく`/clear`して再開

**AIに質問させる**
- 「実装前に不明点があれば必ず質問してください」を習慣化
- CLAUDE.mdに記載しておくと毎回有効

---
<!-- _class: font-xxsmall -->

## AI駆動開発の5-STEPワークフロー

---

### 5-STEPの全体像と効果

**5つのステップ**
1. **要件定義**（STEP 1）：誰が、何を、なぜ（ユーザーストーリー、MoSCoW分析）
2. **設計**（STEP 2）：AIの外部メモリ構築（画面、DB、AC、API仕様）
3. **タスク分解**（STEP 3）：10分サイズに分割（GitHub Issues、BDD = 振る舞い駆動開発、ユーザー視点でテストを書く手法）
4. **実装**（STEP 4）：TDD + 3段階レビュー（Red-Green-Refactor + 検証）
5. **品質改善**（STEP 5）：AIに任せる（リファクタリング、ドキュメント、8つの質問）

**目的**
- AIの5つの特性（暴走、手抜き、忘れっぽさ、凸凹知能、虚偽報告）を制御
- 高品質なコードを効率的に生成
- 人間とAIの役割分担を明確化

---

### 5-STEPと人間・AIの役割分担

| STEP | 人間の役割 | AIの役割 | 防ぐAI特性 |
|------|-----------|----------|-----------|
| 1. 要件定義 | ユーザーストーリー作成 | 妥当性検証 | 暴走 |
| 2. 設計 | 画面・DB・AC定義 | 設計レビュー | 忘れっぽさ、凸凹知能 |
| 3. タスク分解 | 10分タスクに分割 | BDDシナリオ作成 | 暴走、忘れっぽさ |
| 4. 実装 | 人間レビュー | TDD実装 | 手抜き、虚偽報告 |
| 5. 品質改善 | 最終確認 | リファクタリング | - |

**効果**
- エラー伝播41%削減、改良68%削減、満足度2.6倍向上
- 設計への投資で実装時間70%削減（10時間→3時間）
- 5-STEPで、AIの特性を制御し、高品質なコードを効率的に生成

---
<!-- _class: font-xxsmall -->

## 今日の学習内容

---
<!-- _class: font-xxsmall -->

### 3つのセッション

**02: STEP 1-2-3**
- 要件定義・設計・タスク分解
- ユーザーストーリー、画面設計、受入基準
- Planモード、AIに質問させる手法

**03: STEP 4-5**
- TDD実装・3段階レビュー
- Test Hacking対策、/clearでコンテキスト管理
- MCP Servers活用、品質改善

**04: 統合ハンズオン**
- STEP 1-5の完全実践
- TODO管理アプリ実装

---
<!-- _class: font-xsmall -->

### AI駆動開発で大切なこと（1/2）

**マインドセット**
1. AIを信頼しつつ検証する（3段階レビュー）
2. コンテキスト（設計書）に投資する（3.4倍の効果）
3. 段階的に進める（10分ルール）

**覚えておくこと**
- AIは優秀だが完璧ではない（エラー率2倍のリスク）
- 設計書があればAIは3倍賢くなる
- Planモードで早期軌道修正（手戻り54%削減）

---
<!-- _class: font-xsmall -->

### AI駆動開発で大切なこと（2/2）

**覚えておくこと（続き）**
- `/clear`でコンテキスト汚染を防ぐ
- AIに質問させる（暴走・手抜き・忘れっぽさを防ぐ）

**成功の条件**
- 正しく使えば最大10倍の生産性向上
- 間違えるとコード重複8倍、レビュー負担91%増加
- 5-STEPワークフローで品質と速度の両立

**これから**
- 02で実際に設計書を作成します
- 03でTDD実装を体験します
- 04で全体を通して実践します

---

## 質問タイム

準備ができたら、02に進みましょう！
