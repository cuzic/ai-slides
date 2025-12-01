# 02 設計編スライド作成スキル

このスキルは、AI駆動開発セミナー Day 1 の第2章「STEP 1-2-3: 要件定義・設計・タスク分解」のスライドを作成・改善するためのものです。

## 対象スライドファイル

`src/02-design.md`

## 章の概要

- **時間**: 130分
- **対象者**: Java/Spring Boot経験者（AI駆動開発は初心者）
- **前提知識**: 01-入門編受講済み（AI特性5つ、対処法、5-STEPワークフロー全体像）
- **学習目標**: STEP 1（要件定義）、STEP 2（設計）、STEP 3（タスク分解）を習得し、STEP 4（実装）の準備を整える

## 必須トピック

### 1. AIツール選択戦略
- **Claude WEB版**: 探索・議論フェーズ（STEP 1-2）
  - ユーザーストーリー作成
  - 画面プロトタイプ作成（Vibe Coding）
  - 設計の試行錯誤
- **Claude Code**: 実装フェーズ（STEP 3-4-5）
  - タスク分解
  - TDD実装
  - リファクタリング
- **コンテキスト汚染を防ぐ**: フェーズ分離

### 2. STEP 1: 要件定義
- **ユーザーストーリー**: As a, I want, So that形式
- **INVEST原則**: Independent、Negotiable、Valuable、Estimable、Small、Testable
- **MoSCoW分析**: Must（20-30%）、Should、Could、Won't

### 3. STEP 2: 設計
- **画面設計**: 画面一覧、画面遷移図（Mermaid）、画面部品一覧
- **データベース設計**: ER図、正規化、schema.sql
- **データフロー図**: Controller → Service → Repository → DB
- **Vibe Coding**: Claudeアーティファクト機能でモックアップ作成
- **受入基準（AC）**: チェックリスト形式、GIVEN-WHEN-THEN
- **DoD（Definition of Done）**: テストカバレッジ80%以上、複雑度10以下

### 4. STEP 3: タスク分解
- **階層的分解**: Epic → User Story → Task → Subtask
- **10分ルール**: 1タスク = 10-30分
- **BDDテストシナリオ**: GIVEN-WHEN-THEN形式
- **GitHub Issues**: 1 Issue = 1 Subtask

### 5. ハンズオン
- 段階1: 要件定義（Claude WEB版、30分）
- 段階2: 設計（Claude WEB版、25分）
- 段階2-3間: 設計書をローカル保存（5分）
- 段階3: タスク分解（Claude Code、25分）

## 参照すべきknowledges

スライド作成・改善時に以下のknowledgesを参照してください：

### 要件定義関連
- `knowledges/23-user-story-writing.md` - ユーザーストーリー作成
- `knowledges/37-interview-transcription-ai-user-story-generation.md` - ユーザーストーリー生成

### 設計関連
- `knowledges/22-screen-design-and-vibe-coding.md` - 画面設計とVibe Coding
- `knowledges/24-acceptance-criteria.md` - 受入基準（AC）
- `knowledges/26-arc42-c4-adr.md` - arc42とC4 Model
- `knowledges/08-architecture-decision-records-adr.md` - ADR

### タスク分解関連
- `knowledges/25-task-decomposition.md` - タスク分解
- `knowledges/01-given-when-then-bdd.md` - BDD（GIVEN-WHEN-THEN）

### AIツール戦略関連
- `knowledges/36-ai-tools-separation-strategy.md` - AIツール分離戦略
- `knowledges/35-ai-context-contamination-quality-degradation.md` - コンテキスト汚染と品質劣化
- `knowledges/33-ai-context-documentation-importance.md` - コンテキストの重要性

### ガードレール関連
- `knowledges/19-guardrails.md` - ガードレール（4層構造）
- `knowledges/27-ai-ask-questions.md` - AIに質問させる手法

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

1. **新規スライド追加**: 「02-designに〇〇のスライドを追加して」
2. **既存スライド改善**: 「02-designの△△スライドを改善して」
3. **内容の確認**: 「02-designの内容がknowledgesと整合しているか確認して」
4. **クイズ追加**: 「02-designに理解度確認クイズを追加して」

## 重要な数値データ

スライドに含めるべき研究データ：

- **トークン効率**: 設計書なし150K+思考50K vs 設計書あり30K+思考170K（3.4倍）
- **エラー率**: 設計書なし42.1% vs 設計書あり22.8%（46%削減、CrowdStrike研究）
- **設計書ROI**: 作成1-2時間 vs 実装短縮5-10時間（3-10倍）
- **Must haveの割合**: 20-30%

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
