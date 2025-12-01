# 01 入門編スライド作成スキル

このスキルは、AI駆動開発セミナー Day 1 の第1章「入門編：AIとの正しい付き合い方」のスライドを作成・改善するためのものです。

## 対象スライドファイル

`src/01-intro.md`

## 章の概要

- **時間**: 110分（講義60分 + ハンズオン20分 + 5-STEP解説30分）
- **対象者**: Java/Spring Boot経験者（AI駆動開発は初心者）
- **学習目標**: AI駆動開発の基本的なマインドセット、Claude Code活用法、プロジェクト初期化、AI特性理解、5-STEPワークフローの完全理解

## 必須トピック

### 1. AIの5つの特性
- **暴走（Scope Creep）**: Issue範囲外の機能を勝手に追加
- **手抜き（Test Hacking）**: テストを通すだけの仮実装
- **忘れっぽさ（Context Loss）**: 過去の指示を忘れる、コンテキスト汚染
- **凸凹知能（Uneven Intelligence）**: 得意分野と苦手分野の差が激しい
- **虚偽報告（Hallucination）**: 自信満々に誤った情報を提供

### 2. 3つの原則
- **Trust but Verify**: 信頼しつつ検証する（3段階レビュー）
- **Context is the New Code**: コンテキストが全て（設計書で3.4倍効率化）
- **小さく分けて進める**: 10分ルール

### 3. Claude Codeの基本
- コンテキストとトークン（200Kトークン、約13万文字）
- 4つのモード（Normal、Plan、Yolo、Bypass Permissions）
- カスタムコマンド（.claude/commands/）
- CLAUDE.mdとREADME.md
- AIに質問させる手法

### 4. プロジェクト初期化ハンズオン
- 開発環境準備
- Spring Bootプロジェクト作成
- CLAUDE.md作成（最重要）
- README.md作成
- カスタムコマンド準備

### 5. 5-STEPワークフロー概要
- STEP 1: 要件定義（ユーザーストーリー、MoSCoW分析）
- STEP 2: 設計（画面、DB、AC、API仕様）
- STEP 3: タスク分解（10分サイズ、GitHub Issues、BDD）
- STEP 4: 実装（TDD + 3段階レビュー）
- STEP 5: 品質改善（8つの質問と指示）

## 参照すべきknowledges

スライド作成・改善時に以下のknowledgesを参照してください：

### AI特性関連
- `knowledges/13-reward-hacking-ai.md` - Reward Hacking（Test Hacking）
- `knowledges/14-jagged-intelligence.md` - 凸凹知能
- `knowledges/15-ai-hallucination.md` - AI Hallucination
- `knowledges/16-ai-scope-creep.md` - Scope Creep
- `knowledges/17-context-limitations.md` - Context Limitations

### 原則・対策関連
- `knowledges/18-trust-but-verify.md` - Trust but Verify（3段階レビュー）
- `knowledges/19-guardrails.md` - ガードレール
- `knowledges/33-ai-context-documentation-importance.md` - コンテキストの重要性

### Claude Code関連
- `knowledges/20-claude-code-modes.md` - Claude Code 4つのモード
- `knowledges/21-claude-code-custom-commands.md` - カスタムコマンド
- `knowledges/29-plan-mode-and-custom-commands.md` - Planモードとカスタムコマンド
- `knowledges/27-ai-ask-questions.md` - AIに質問させる手法

### 5-STEP関連
- `knowledges/30-ai-context-guardrails-verify.md` - 5-STEPワークフロー全体像
- `knowledges/34-ai-driven-development-problems.md` - AI駆動開発の主要問題

### 生産性研究
- `knowledges/31-ai-coding-productivity-research.md` - AI Coding生産性研究
- `knowledges/32-claude-code-productivity-research.md` - Claude Code生産性研究

## スライド作成ルール

`src/CLAUDE.md`のルールに従ってください：

1. **Marp形式**: フロントマター必須、スライド間は`---`で区切る
2. **各スライド構成**: スライドタイトル + 最大3階層の箇条書き（5-13項目）
3. **箇条書きの原則**:
   - 第1階層: 主要なポイント
   - 第2階層: 補足説明、具体例
   - 第3階層: 詳細情報、数値データ
4. **項目数**: 最小5項目、最大13項目、推奨7-10項目
5. **階層**: 最大3階層まで（4階層以上は禁止）

## 使用方法

このスキルを使って以下のタスクを実行できます：

1. **新規スライド追加**: 「01-introに〇〇のスライドを追加して」
2. **既存スライド改善**: 「01-introの△△スライドを改善して」
3. **内容の確認**: 「01-introの内容がknowledgesと整合しているか確認して」
4. **クイズ追加**: 「01-introに理解度確認クイズを追加して」

## 出力例

```markdown
---

### スライドXX: [タイトル]

- **メイン項目1**
  - サブ項目1-1
    - 詳細1-1-1
  - サブ項目1-2
- **メイン項目2**
  - サブ項目2-1
  - サブ項目2-2
- **メイン項目3**
  - サブ項目3-1

---
```
