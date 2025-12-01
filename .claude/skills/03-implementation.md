# 03 実装・品質改善編スライド作成スキル

このスキルは、AI駆動開発セミナー Day 1 の第3章「STEP 4-5: 実装・TDD・3段階レビュー・MCP Servers・品質改善」のスライドを作成・改善するためのものです。

## 対象スライドファイル

`src/03-implementation-refactoring.md`

## 章の概要

- **時間**: 60分
- **対象者**: Java/Spring Boot経験者（AI駆動開発は初心者）
- **学習目標**: STEP 4（実装・TDD）とSTEP 5（品質改善）の習得、3段階レビュー・MCP Servers・8つの質問と指示で高品質なコードを実現

## 必須トピック

### 1. Test Hackingと対策
- **Test Hackingとは**: テストを通すだけの不正な実装
- **Shallow Testingの3つの手法**:
  - Mock Abuse（モック乱用）
  - Silent Fail（エラー握りつぶし）
  - Silent Fallback（暗黙のフォールバック）
- **検出方法**: AI Self Review、完成度0-100点評価

### 2. 7段階TDDサイクル
- **Plan（30秒）**: Issue内容・実装方針・設計書参照
- **Red（2分）**: 受入条件→JUnit 5でテストファースト
- **Green（5分）**: 最小実装、Issue範囲外の機能は作らない
- **Refactor（2分）**: Cyclomatic Complexity < 10、重複削除
- **System Review（30秒）**: mvn verifyで自動検証
- **AI Self Review（30秒）**: Test Hacking検出、完成度0-100点
- **Human Review（30秒）**: git diff、ビジネスロジック確認

### 3. 3段階レビュー詳細
- **System Review**: CheckStyle、SpotBugs、PMD、JaCoCo
- **AI Self Review**: SelfCheckGPT方式、Repomix複数AIレビュー
- **Human Review**: ビジネスロジック、Scope Creep検出

### 4. MCP Servers
- **Context7**: 最新APIドキュメント（Hallucination防止）
- **Serena**: トークン最適化（LSP活用、最大90%削減）
- **Playwright**: E2Eテスト自動生成
- **Chrome DevTools**: UIデバッグ（AIに「目」を与える）

### 5. STEP 5: 8つの質問と指示
1. 技術的負債を見付けて
2. 冗長・重複・dead codeを削除して
3. 循環的複雑度を減らして
4. 効果的にライブラリを活用できる箇所は
5. 効果的にデザインパターンを活用できる箇所は
6. JavaDocを書いて
7. arc42とC4 ModelでADRを書いて
8. 知見を保存して（→ `/clear`でコンテキストクリア）

## 参照すべきknowledges

スライド作成・改善時に以下のknowledgesを参照してください：

### TDD関連
- `knowledges/02-test-driven-development-tdd.md` - TDD詳細
- `knowledges/01-given-when-then-bdd.md` - BDD（GIVEN-WHEN-THEN）
- `knowledges/テストアンチパターン4選.md` - Test Hacking/Mock Abuse/Shallow Testing

### Test Hacking・AI問題関連
- `knowledges/13-reward-hacking-ai.md` - Reward Hacking（Test Hacking）
- `knowledges/AI駆動開発におけるSilent Fail問題と対策.md` - Silent Fail詳細
- `knowledges/28-ai-completion-verification.md` - AI完成度検証

### 3段階レビュー関連
- `knowledges/18-trust-but-verify.md` - Trust but Verify（3段階レビュー）
- `knowledges/09-repomix-ai-code-review.md` - Repomix AI Code Review

### MCP Servers関連
- `knowledges/03-model-context-protocol-mcp.md` - MCP概要
- `knowledges/04-context7-mcp-server.md` - Context7 MCP Server
- `knowledges/05-serena-mcp-server.md` - Serena MCP Server
- `knowledges/06-playwright-mcp-server.md` - Playwright MCP Server
- `knowledges/12-chrome-devtools-mcp-server.md` - Chrome DevTools MCP Server

### 品質改善関連
- `knowledges/07-cyclomatic-complexity.md` - 循環的複雑度
- `knowledges/08-architecture-decision-records-adr.md` - ADR
- `knowledges/26-arc42-c4-adr.md` - arc42とC4 Model
- `knowledges/11-living-documentation.md` - Living Documentation
- `knowledges/10-rust-based-dev-tools.md` - Rust製開発ツール

### AI問題全般
- `knowledges/34-ai-driven-development-problems.md` - AI駆動開発の主要問題
- `knowledges/35-ai-context-contamination-quality-degradation.md` - コンテキスト汚染と品質劣化
- `knowledges/42_AI駆動開発における典型的な落とし穴と対策.md` - 典型的な落とし穴

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

## 重要な数値データ

スライドに含めるべき研究データ：

- **TDD効果**: 210分 → 35分（175分削減、83%削減）
- **Cyclomatic Complexity閾値**: 1-10（目標）、11-20（中程度）、21-50（要リファクタリング）、50+（即座にリファクタリング）
- **7段階TDD時間配分**: Plan 30秒 + Red 2分 + Green 5分 + Refactor 2分 + 3段階レビュー 2分30秒 = 約12分
- **Serenaトークン削減**: 最大90%削減

## 使用方法

このスキルを使って以下のタスクを実行できます：

1. **新規スライド追加**: 「03-implementationに〇〇のスライドを追加して」
2. **既存スライド改善**: 「03-implementationの△△スライドを改善して」
3. **内容の確認**: 「03-implementationの内容がknowledgesと整合しているか確認して」
4. **クイズ追加**: 「03-implementationに理解度確認クイズを追加して」

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
