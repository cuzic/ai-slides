# 21. Claude Codeカスタムコマンド：育て方とPlan Modeとの違い

**最終更新**: 2025-01-07
**カテゴリ**: 開発手法・ツール
**関連トピック**: [20. Claude Codeのモード切り替え](./20-claude-code-modes.md)、[19. Guardrails](./19-guardrails.md)

---

## 概要

Claude Codeのカスタムコマンドは、単なる「定型プロンプトのショートカット」ではない。**AIの思考プロセスを言語化し、実行前にレビューできる仕組み**であり、Plan Modeとは異なるアプローチで開発速度と品質を両立させる。

---

## カスタムコマンドとは

### 基本構造

`.claude/commands/` ディレクトリにMarkdownファイルを配置すると、自動的にスラッシュコマンドとして利用可能になる。

```
プロジェクトルート/
├── .claude/
│   └── commands/
│       ├── implement-feature.md    → /implement-feature
│       ├── review-pr.md            → /review-pr
│       └── fix-github-issue.md     → /fix-github-issue
└── CLAUDE.md
```

### 引数の受け渡し

`$ARGUMENTS` キーワードで、コマンド実行時の引数を受け取れる：

```markdown
<!-- .claude/commands/fix-github-issue.md -->
# GitHub Issue修正

以下の手順でIssue #$ARGUMENTS を修正してください：

1. `gh issue view $ARGUMENTS` でIssueの内容を確認
2. 参照されている設計書（CLAUDE.md記載）を読む
3. GIVEN WHEN THEN形式の受入条件をテストコードに変換
4. TDDサイクルで実装
5. Cyclomatic Complexity < 10 を確認
6. コミットメッセージ: "Fixes #$ARGUMENTS: [概要]"
```

**実行例**:
```bash
/fix-github-issue 123
# → Issue #123 を上記手順で修正
```

---

## カスタムコマンドを「育てる」3つの目的

### 1. 再利用可能な資産として蓄積

**従来の問題**:
- 毎回同じようなプロンプトを打つ（時間の無駄）
- 過去に使った良いプロンプトを忘れる
- チームで共有されない

**カスタムコマンドの解決策**:
- プロンプトをファイルに保存 → Git管理
- チームメンバーがリポジトリをクローン → 全員が同じコマンドを利用
- プロンプトの改善履歴が残る

**育て方**:
```
最初: シンプルなコマンド（10行程度）
　↓
使用中に不便を感じる → その都度改善
　↓
1ヶ月後: より詳細で実用的なコマンド（30-50行）
　↓
定期メンテナンス（月1回）: 使用頻度の低いコマンドを削除、新しいコマンドを追加
```

---

### 2. AIの思考プロセスを言語化させる

**重要な洞察**:

カスタムコマンドを作成する過程で、**AIに「何をどの順番で実行するか」を説明させる**ことで、実装前にレビューできる。

**Plan Modeとの違い**:

| 観点 | Plan Mode | カスタムコマンド作成 |
|------|-----------|----------------------|
| **タイミング** | 実装直前 | コマンド作成時（実装より前） |
| **再利用性** | 1回限り | 繰り返し利用可能 |
| **詳細度** | タスク固有 | 汎用的なワークフロー |
| **言語化** | その場で | 事前に明文化 |
| **レビュー** | 実行前1回 | コマンド作成時+毎回実行前 |

**具体例**:

```markdown
<!-- .claude/commands/implement-crud.md -->
# CRUD機能実装ワークフロー

$ARGUMENTS エンティティのCRUD機能を実装します。

## 実行手順

### Phase 1: 設計確認
1. `docs/schema.sql` でテーブル定義を確認
2. `docs/repository-spec.md` でRepositoryメソッド仕様を確認
3. `docs/requirements/$ARGUMENTS-crud.md` で受入条件（GIVEN WHEN THEN）を確認

### Phase 2: エンティティ・Repository作成
4. `src/main/java/com/example/entity/$ARGUMENTSEntity.java` を作成
   - @Entity、@Id、@GeneratedValue アノテーション
   - schema.sqlと整合性確認
5. `src/main/java/com/example/repository/$ARGUMENTSRepository.java` を作成
   - JpaRepository継承
   - カスタムメソッドはrepository-spec.mdに従う

### Phase 3: Service・TDD
6. `src/test/java/com/example/service/$ARGUMENTSServiceTest.java` を作成
   - 受入条件をJUnit 5テストに変換
   - @SpringBootTest、@Transactional使用
7. `src/main/java/com/example/service/$ARGUMENTSService.java` を実装
   - テストがグリーンになる最小実装
8. Refactor: Cyclomatic Complexity < 10

### Phase 4: Controller・統合テスト
9. `src/main/java/com/example/controller/$ARGUMENTSController.java` を作成
10. `src/test/java/com/example/controller/$ARGUMENTSControllerTest.java` を作成

### Phase 5: 検証
11. `mvn clean test` で全テスト実行
12. JaCoCo カバレッジ 80% 以上確認
13. Checkstyle 違反なし確認
14. git diff で Scope Creep（余計なファイル追加）チェック

## 制約
- PostgreSQL、MongoDB等は使用禁止（H2 Databaseのみ）
- テストなしの実装は禁止
- CLAUDE.md の「実装前チェックリスト」を必ず確認
```

**このコマンドを作ることで得られる効果**:

1. **AIの実行計画が明確化**: 「Phase 1-5」として言語化
2. **実行前レビュー**: コマンド作成時に手順を検討
3. **チーム標準化**: 全員が同じ手順でCRUD実装
4. **改善の蓄積**: 不具合があれば、コマンドを修正（次回から改善される）

---

### 3. 実行前レビューによる速いフィードバック

**Plan Mode の制約**:

Plan Modeは「その場で計画を立てる」ため、計画が複雑な場合、何度もEscapeキーで修正が必要。

**カスタムコマンドの優位性**:

事前に手順を定義しているため、**実行前に全体像が見える**。

**比較例**:

#### Plan Mode（その場で計画）
```
開発者: 「Todo CRUD機能を実装して」
　↓
Claude: 計画を提示（Phase 1-10）
　↓
開発者: Escape → 「Phase 2でRepositoryメソッド名を変更して」
　↓
Claude: 計画を再提示
　↓
開発者: Escape → 「Phase 5でCheckstyleも追加して」
　↓
Claude: 計画を再提示
　↓
開発者: 承認 → 実行
```

**所要時間**: 計画修正に5-10分

#### カスタムコマンド（事前定義）
```
開発者: 「/implement-crud Todo」
　↓
Claude: .claude/commands/implement-crud.md を読み込み
　↓
Claude: Phase 1-5 を自動実行（手順が明確なので迷わない）
```

**所要時間**: 0分（事前定義済み）

**さらに、カスタムコマンド自体を改善**:
```
# 実行後に気づいた問題
「Checkstyleチェックが抜けていた」

# コマンドファイルを修正
vim .claude/commands/implement-crud.md
# → Phase 5 に「Checkstyle 違反なし確認」を追加

# 次回から自動的に改善版が使われる
/implement-crud User
# → Phase 5 でCheckstyleも自動チェック
```

---

## Plan Mode とカスタムコマンドの使い分け

### カスタムコマンドを使うべき場合

- **繰り返し実行する定型ワークフロー**
  - CRUD機能実装
  - GitHub Issue修正
  - PRレビュー
  - リファクタリング（Complexity削減）

- **チーム全体で標準化したい作業**
  - コーディング規約チェック
  - テストカバレッジ確認
  - デプロイ前チェックリスト

- **複雑な手順を確実に実行したい**
  - 10ステップ以上のワークフロー
  - 設計書参照が必須のタスク

### Plan Mode を使うべき場合

- **1回限りの特殊なタスク**
  - 新しいアーキテクチャの導入
  - レガシーコードの大規模リファクタリング
  - 既存ライブラリの置き換え

- **探索的なタスク**
  - 新しいOSSプロジェクトの調査
  - パフォーマンス問題の原因調査
  - バグの根本原因分析

- **カスタムコマンド作成前の試行錯誤**
  - 新しいワークフローを試す
  - Plan Modeで成功したら、カスタムコマンド化

---

## 実践：カスタムコマンドの育て方

### ステップ1: 最小限のコマンドから始める

**初期バージョン（10行）**:

```markdown
<!-- .claude/commands/review-code.md -->
# コードレビュー

以下をレビューしてください：
1. セキュリティ問題（OWASP Top 10）
2. Cyclomatic Complexity > 10 の関数
3. テストカバレッジ < 80% のクラス
```

### ステップ2: 使用中に不便を感じたら即改善

**1週間後の改善版（30行）**:

```markdown
<!-- .claude/commands/review-code.md -->
# コードレビュー

## Phase 1: 静的解析
1. Checkstyle実行: `mvn checkstyle:check`
2. ESLint実行: `npx eslint src/main/resources/static/**/*.js`
3. Cyclomatic Complexity測定（SonarLint）

## Phase 2: セキュリティチェック
4. OWASP Top 10 確認
   - SQL Injection: native query使用箇所チェック
   - XSS: Thymeleaf th:text vs th:utext 確認
   - CSRF: Spring Security設定確認

## Phase 3: テストカバレッジ
5. `mvn test jacoco:report`
6. target/site/jacoco/index.html でカバレッジ確認
7. 80%未満のクラスをリスト化

## Phase 4: 設計整合性
8. CLAUDE.md のアーキテクチャ原則に従っているか
9. ADR（docs/adr/）の決定に反していないか

## 出力形式
- 問題点を優先度順（Critical / High / Medium / Low）にリスト化
- 各問題に対する修正案を提示
```

### ステップ3: 定期メンテナンス（月1回）

**チェックリスト**:
- [ ] 過去1ヶ月で1回も使われていないコマンド → 削除候補
- [ ] 頻繁に使うコマンド → さらに詳細化
- [ ] 新しいツール導入（例：Playwright MCP） → 既存コマンドに統合
- [ ] チームメンバーのフィードバック → 改善

---

## 高度な活用例

### 例1: GitHub Issues と連携

```markdown
<!-- .claude/commands/work-on.md -->
# GitHub Issue取り込み＆実装

## Phase 1: Issue取得
1. `gh issue view $ARGUMENTS --json title,body,labels` で詳細取得
2. Issue本文から参照設計書を抽出（例：`docs/requirements/todo-creation.md`）

## Phase 2: 設計書確認
3. Issue本文の参照設計書を全て読む
4. GIVEN WHEN THEN 形式の受入条件を確認

## Phase 3: タスク分解
5. Issue を 10分ルールでサブタスクに分解
6. 各サブタスクに対して、実装順序を決定

## Phase 4: TDDサイクル
7. サブタスク1から順に、Red-Green-Refactor-Verify
8. 各サブタスク完了後、進捗をIssueにコメント: `gh issue comment $ARGUMENTS --body "✅ サブタスク1完了"`

## Phase 5: 完了処理
9. 全テスト実行: `mvn clean test`
10. Checkstyle確認: `mvn checkstyle:check`
11. コミット: `git commit -m "Fixes #$ARGUMENTS: [概要]"`
12. Issue自動クローズ確認
```

**実行例**:
```bash
/work-on 42
# → Issue #42 を取得 → 設計書確認 → タスク分解 → TDD実装 → コミット → Issue自動クローズ
```

---

### 例2: サブエージェント連携

```markdown
<!-- .claude/commands/refactor-codebase.md -->
# コードベース全体リファクタリング

## Phase 1: 複雑度の高いファイル検出
1. サブエージェントで全Javaファイルを解析
2. Cyclomatic Complexity > 15 のメソッドをリスト化

## Phase 2: 優先順位付け
3. テストカバレッジとの相関を確認
4. カバレッジ < 50% かつ Complexity > 15 → 最優先
5. カバレッジ >= 80% かつ Complexity > 15 → 中優先

## Phase 3: 段階的リファクタリング
6. 最優先メソッドから1つずつリファクタリング
7. 各メソッドごとに：
   - 既存テストを実行（グリーン確認）
   - Extract Method適用
   - テスト再実行（グリーンを維持）
   - Complexity再測定（< 10確認）
   - コミット

## 制約
- 1回のコミットで1メソッドのみリファクタリング
- テストが壊れたら即ロールバック
```

---

## チーム展開のベストプラクティス

### 1. コマンドライブラリの共有

```
.claude/commands/
├── _README.md                    # コマンド一覧とカテゴリ分け
├── implement-feature.md          # 汎用：新機能実装
├── fix-github-issue.md           # 汎用：Issue修正
├── review-pr.md                  # 汎用：PRレビュー
├── java/
│   ├── implement-crud.md         # Java固有：CRUD実装
│   ├── add-repository-method.md  # Java固有：Repositoryメソッド追加
│   └── refactor-service.md       # Java固有：Service層リファクタリング
└── frontend/
    ├── implement-ui.md           # フロントエンド：UI実装
    └── add-validation.md         # フロントエンド：バリデーション追加
```

### 2. コマンドレビュー会（月1回）

**アジェンダ**:
1. 新しいコマンドの紹介（5分）
2. 既存コマンドの改善提案（10分）
3. 不要なコマンドの削除（5分）
4. ベストプラクティス共有（10分）

### 3. コマンドのバージョニング

```markdown
<!-- .claude/commands/implement-crud.md -->
# CRUD機能実装ワークフロー

**Version**: 2.1.0
**Last Updated**: 2025-01-07
**Author**: @yourname
**Changelog**:
- v2.1.0: Checkstyleチェックを追加
- v2.0.0: Phase 5 にJaCoCoカバレッジ確認を追加
- v1.0.0: 初版作成

...（コマンド内容）
```

---

## よくある質問

**Q1: カスタムコマンドとPlan Modeを併用すべきか？**

A: **Yes**。以下のワークフローが最強：

```
1. カスタムコマンドで基本的なワークフロー実行
   /implement-crud Todo
   ↓
2. 複雑な部分でPlan Modeに切り替え
   Shift+Tab×2 → 「Phase 3のServiceメソッドの実装を詳細計画して」
   ↓
3. Plan承認後、カスタムコマンドの続きを実行
```

**Q2: カスタムコマンドが多すぎて管理できない**

A: カテゴリ分けとプレフィックスを使う：

```
/java:implement-crud
/java:refactor-service
/frontend:implement-ui
/devops:deploy-staging
```

**Q3: カスタムコマンドとGitHub Issuesテンプレートの違いは？**

A:
- **GitHub Issuesテンプレート**: タスクの**内容**を定義（何をやるか）
- **カスタムコマンド**: タスクの**手順**を定義（どうやるか）

両者を組み合わせることで、Issue → カスタムコマンド実行 → 自動完了の流れが作れる。

---

## 参考資料

### 公式・準公式
- [Claude Code Best Practices - Anthropic](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Customize Claude Code with plugins](https://www.anthropic.com/news/claude-code-plugins)
- [Common workflows - Claude Docs](https://docs.claude.com/en/docs/claude-code/common-workflows)

### コミュニティ記事（英語）
- [Shipyard - Claude Code CLI Cheatsheet](https://shipyard.build/blog/claude-code-cheat-sheet/)
- [Cooking with Claude Code: The Complete Guide](https://www.siddharthbharath.com/claude-code-the-complete-guide/)
- [GitHub - awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)

### コミュニティ記事（日本語）
- [Claude Codeカスタムコマンド完全ガイド - Zenn](https://zenn.dev/tmasuyama1114/articles/claude_code_commands)
- [【基礎編】Claude Code カスタムコマンド - Qiita](https://qiita.com/tomada/items/25577a683a4432ee8698)
- [【Claude Codeの活用事例】よく使うカスタムスラッシュコマンド5選 - Findy](https://tech.findy.co.jp/entry/2025/07/23/070000)
- [Claude Code 疲れを軽減する 30+ 個のカスタムコマンド](https://wasabeef.jp/blog/claude-code-cookbook)
- [Claude Code でカスタムスラッシュコマンドを作成する](https://azukiazusa.dev/blog/claude-code-custom-slash-command/)

---

## セミナーでの活用

**01 入門編**:
- カスタムコマンドの基本（スライド15）に、以下を追加：
  - 「育てる」目的：再利用、思考プロセス言語化、実行前レビュー
  - Plan Modeとの違い

**02 基本編**:
- `/fix-github-issue` コマンドをライブデモ
- Issue #4 を取得 → TDD実装 → コミット の流れ

**03 実践編**:
- `/review-code` コマンドで自動レビューデモ
- チームでのコマンドライブラリ管理方法を紹介
