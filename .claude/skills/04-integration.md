# 04 統合ハンズオンスライド作成スキル

このスキルは、AI駆動開発セミナー Day 1 の第4章「統合ハンズオン: STEP 1-5 完全実践」のスライドを作成・改善するためのものです。

## 対象スライドファイル

`src/04-integration.md`

## 章の概要

- **時間**: 30分
- **対象者**: Java/Spring Boot経験者（AI駆動開発は初心者）
- **学習目標**: STEP 1-5を通してTODO管理アプリを完成させ、AI駆動開発の全工程を実践する

## 必須トピック

### 1. 実装する機能
- **完了状態変更機能**: TODO管理の本質的機能
- **ユーザーストーリー**: As a ユーザー, I want TODOの完了状態を変更できる, So that 完了したタスクを記録し、やるべきことを管理できる

### 2. 時間配分
- **STEP 1: 要件定義（3分）**: ユーザーストーリー、MoSCoW分析
- **STEP 2: 設計（7分）**: 画面設計、受入基準、DBスキーマ、API設計、DoD
- **STEP 3: タスク分解（3分）**: GitHub Issue、BDDシナリオ、10分ルール適用
- **STEP 4: TDD実装（12分）**: 7段階TDD、3段階レビュー
- **STEP 5: リファクタリング（5分）**: 8つの質問と指示、完成度検証、`/clear`

### 3. STEP 1: 要件定義
- ユーザーストーリー作成
- MoSCoW分析
  - Must have: 完了状態変更機能
  - Should have: 完了したTODOの視覚的表示
  - Could have: 完了率の表示
  - Won't have: 自動完了機能

### 4. STEP 2: 設計
- **画面設計**: チェックボックス追加、取り消し線表示
- **受入基準（AC）**:
  - チェックボックスクリックで完了状態に
  - 完了TODOは取り消し線表示
  - 再クリックで未完了に戻せる
- **DBスキーマ**: completed カラム（BOOLEAN、デフォルト false）
- **API設計**: PATCH /api/todos/:id/status

### 5. STEP 3: タスク分解
- Subtask 1: DBスキーマ更新
- Subtask 2: Service層実装
- Subtask 3: Controller層実装
- Subtask 4: 画面実装

### 6. STEP 4: TDD実装
- Red → Green → Refactor → Verify
- 3段階レビュー（自動検証、AI自己検証、Scope Creep検出）

### 7. STEP 5: リファクタリング
- 8つの質問と指示
- 完成度検証（100点まで）
- `/clear`コマンド実行

### 8. 総合復習クイズ
- Day 1全体の理解度確認
- 5-STEPの順序、AI特性、7段階TDD、/clear、MoSCoW分析

## 参照すべきknowledges

スライド作成・改善時に以下のknowledgesを参照してください：

### 5-STEP全体
- `knowledges/30-ai-context-guardrails-verify.md` - 5-STEPワークフロー全体像
- `knowledges/34-ai-driven-development-problems.md` - AI特性5つ

### 要件定義
- `knowledges/23-user-story-writing.md` - ユーザーストーリー作成

### 設計
- `knowledges/24-acceptance-criteria.md` - 受入基準定義

### タスク分解
- `knowledges/25-task-decomposition.md` - タスク分解
- `knowledges/01-given-when-then-bdd.md` - BDDテストシナリオ

### TDD・レビュー
- `knowledges/02-test-driven-development-tdd.md` - TDD
- `knowledges/18-trust-but-verify.md` - 3段階レビュー
- `knowledges/19-guardrails.md` - ガードレール

### AIツール戦略
- `knowledges/36-ai-tools-separation-strategy.md` - AIツール分離戦略
- `knowledges/33-ai-context-documentation-importance.md` - コンテキストの重要性

### ドキュメント
- `knowledges/26-arc42-c4-adr.md` - ADR
- `knowledges/11-living-documentation.md` - リビングドキュメント
- `knowledges/40-optimal-documentation-for-ai-driven-development.md` - 最適なドキュメント

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

## 重要ポイント

### Day 1の成功要因（復習）
- 5-STEPワークフローの確実な実践
- AIの特性理解（暴走、手抜き、忘れっぽさ、凸凹知能、虚偽報告）
- ガードレール（事前防止）
- 3段階レビュー（事後検証）
- ツール分離戦略（Claude WEB、Claude Code）

### 完成した成果物
- 動作するコード（完了状態変更機能）
- テスト（カバレッジ80%以上）
- 設計書（受入基準、DBスキーマ）
- ドキュメント（JavaDoc、ADR）
- 1 commit

## 使用方法

このスキルを使って以下のタスクを実行できます：

1. **新規スライド追加**: 「04-integrationに〇〇のスライドを追加して」
2. **既存スライド改善**: 「04-integrationの△△スライドを改善して」
3. **内容の確認**: 「04-integrationの内容がknowledgesと整合しているか確認して」
4. **クイズ追加**: 「04-integrationに総合クイズを追加して」

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
