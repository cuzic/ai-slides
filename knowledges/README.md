# AI駆動開発セミナー - 技術資料集

このディレクトリには、AI駆動開発セミナー Day 1 - 02 基本編のスライドで扱うテクニカルタームに関する詳細な参考資料が含まれています。

**収録トピック数：25**（AI特性・問題点：5、対処法：2、開発手法・ツール：18）

## 📚 収録トピック一覧

### 開発手法・プラクティス

#### [01. GIVEN WHEN THEN - BDD形式の受入条件](./01-given-when-then-bdd.md)
- Behavior-Driven Development (BDD)の基本フォーマット
- 受入条件の明確化とテストケースへの変換
- Cucumber、SpecFlow、Behaveなどのツール

#### [02. Test Driven Development (TDD)](./02-test-driven-development-tdd.md)
- Red-Green-Refactor サイクル
- TDDのベストプラクティスと哲学
- RGRC (Red-Green-Refactor-Commit) ワークフロー

#### [22. 画面設計とVibe Coding](./22-screen-design-and-vibe-coding.md)
- 画面一覧・画面遷移図・画面部品一覧の作成
- Vibe Coding（バイブコーディング）によるモックアップ生成
- AI駆動開発における画面設計の重要性（Scope Creep/Reward Hacking対策）

#### [23. ユーザーストーリーの書き方](./23-user-story-writing.md)
- アジャイル開発における最小の作業単位
- INVEST原則（Independent, Negotiable, Valuable, Estimable, Small, Testable）
- AI駆動開発でのScope Creep/Reward Hacking対策

#### [24. 受入基準とチェックリスト](./24-acceptance-criteria.md)
- 受入基準（Acceptance Criteria）とDefinition of Doneの違い
- 2つのフォーマット：チェックリスト形式 vs シナリオ形式（Given-When-Then）
- AI開発での手抜き・暴走防止策

#### [25. タスク分解とトークン制限への対応](./25-task-decomposition.md)
- 階層的タスク分解（Epic → User Story → Task → Subtask）
- Context Window（トークン制限）の課題と対応戦略
- AI開発の3つの問題（暴走・手抜き・忘れっぽさ）への対策

### Model Context Protocol (MCP) エコシステム

#### [03. Model Context Protocol (MCP)](./03-model-context-protocol-mcp.md)
- AnthropicによるMCPの概要
- Claude Codeとの統合方法
- エコシステムと採用状況

#### [04. Context7 MCP Server](./04-context7-mcp-server.md)
- 最新のAPIドキュメントを提供するMCPサーバー
- リアルタイムドキュメントアクセス
- インストールと使用方法

#### [05. Serena MCP Server](./05-serena-mcp-server.md)
- Language Server Protocolを活用したトークン最適化
- セマンティックコード解析
- 大規模プロジェクトでの効率的なコード参照

#### [06. Playwright MCP Server](./06-playwright-mcp-server.md)
- AI駆動のE2Eテスト生成
- ビジュアルリグレッションテスト
- ブラウザ自動化とパフォーマンス分析

#### [12. Chrome DevTools MCP Server](./12-chrome-devtools-mcp-server.md)
- AIに"目"を与えるデバッグツール
- パフォーマンス分析とネットワーク監視
- コンソールエラーの自動検出

### コード品質とドキュメンテーション

#### [07. Cyclomatic Complexity（循環的複雑度）](./07-cyclomatic-complexity.md)
- コード複雑度の測定指標
- 複雑度を減らすリファクタリング戦略
- 推奨される閾値とベストプラクティス

#### [08. Architecture Decision Records (ADR)](./08-architecture-decision-records-adr.md)
- 技術的決定の記録方法
- ADRテンプレートとベストプラクティス
- ライフサイクル管理

#### [11. Living Documentation（リビングドキュメンテーション）](./11-living-documentation.md)
- 自動的に進化するドキュメント
- 実行可能な仕様とAPI自動生成
- アジャイル開発での活用

### 開発ツールとユーティリティ

#### [09. Codebase to Prompt Tools](./09-codebase-to-prompt-tools.md)
- code2prompt、Repomix、files-to-promptの比較
- コードベースをAI向けプロンプトに変換
- 複数AIでのコードレビュー手法

#### [10. Rust製開発ツール：Biome、Ruff、oxc](./10-rust-based-dev-tools.md)
- 高速なリンター・フォーマッターツール
- 従来ツールの10-100倍の速度
- JavaScript/TypeScript、Python向けツールチェイン

#### [20. Claude Codeのモード切り替え](./20-claude-code-modes.md)
- Plan Mode / YOLO Mode / Normal Mode / Bypass Permissions
- 各モードの使い分けと安全な使い方
- Trust but Verifyとの関係

#### [21. Claude Codeカスタムコマンド](./21-claude-code-custom-commands.md)
- カスタムコマンドを「育てる」3つの目的
- Plan Modeとの違いと使い分け
- チーム展開のベストプラクティス

### AI開発の課題と対策

#### AI特性・問題点

#### [13. Reward Hacking in AI](./13-reward-hacking-ai.md)
- AIの手抜き・ショートカット問題
- デフォルト値/フォールバックの悪用
- 対策：詳細な受入条件と複数の検証方法

#### [14. Jagged Intelligence（凸凹な知能）](./14-jagged-intelligence.md)
- AIの能力の不均一性
- フロンティア内（得意）とフロンティア外（苦手）のタスク
- ハーバード・ビジネス・スクールの研究データ
- Java開発での具体例と対策

#### [15. AI Hallucination（虚偽報告）](./15-ai-hallucination.md)
- 存在しないAPIやメソッドの提案
- 虚偽の「完了しました」報告
- 検出方法（SelfCheckGPT、Semantic Entropy）
- RAG、ファインチューニング、段階的検証による対策

#### [16. AI Scope Creep（暴走）](./16-ai-scope-creep.md)
- 指示していない機能の追加実装
- Java開発での具体例（UserService、Controller、設定ファイル）
- 対策：明確なスコープ指定、MVP原則、GitHub Issues

#### [17. Context Limitations（忘れっぽさ）](./17-context-limitations.md)
- トークン制限による記憶喪失
- Compact後の情報損失
- CLAUDE.md、カスタムコマンド、ADRによる外部化
- 定期的なリマインダーとチェックリスト

#### 対処法・ベストプラクティス

#### [18. Trust but Verify（任せる＆確かめる）](./18-trust-but-verify.md)
- 多層防御による検証戦略
- Layer 1（自動検証）：コンパイル、テスト、静的解析
- Layer 2（AI自己検証）：SelfCheckGPT方式
- Layer 3（人間レビュー）：ビジネスロジック、セキュリティ
- すべてのAI問題に対する包括的対策

#### [19. Guardrails（ガードレール）](./19-guardrails.md)
- 詳細な設計書・ルール文書による境界線設定
- CLAUDE.md、ADR、GitHub Issues、OpenAPI Spec
- AI問題の事前防止策
- プロジェクト、タスク、アーキテクチャ、APIレベルのガードレール

## 🎯 使用方法

### セミナー準備
各トピックの詳細資料として、スライド作成時の参考にしてください。

### 実務での活用
開発チームでの技術選定や実装ガイドラインとして活用できます。

### 継続学習
各ファイルには参考資料へのリンクが含まれており、さらなる学習に役立ちます。

## 📖 トピックの関連性

### STEP 3（タスク分解）関連
- [01. GIVEN WHEN THEN](./01-given-when-then-bdd.md) - 受入条件の明確化（Reward Hacking対策）
- [07. Cyclomatic Complexity](./07-cyclomatic-complexity.md) - タスクの適切なサイズ
- [19. Guardrails](./19-guardrails.md) - GitHub Issuesで実装範囲を明確化（Scope Creep対策）
- [22. 画面設計とVibe Coding](./22-screen-design-and-vibe-coding.md) - 画面一覧で実装範囲明確化、受入条件の可視化
- [23. ユーザーストーリーの書き方](./23-user-story-writing.md) - 要件定義フェーズでのストーリー明確化
- [24. 受入基準とチェックリスト](./24-acceptance-criteria.md) - 設計フェーズでの完了条件定義
- [25. タスク分解とトークン制限への対応](./25-task-decomposition.md) - トークン消費削減とContext Limitations対策

### STEP 4（実装・TDD）関連
- [02. Test Driven Development](./02-test-driven-development-tdd.md) - TDDサイクル
- [03-06. MCP Servers](./03-model-context-protocol-mcp.md) - 開発効率化
- [10. Rust製開発ツール](./10-rust-based-dev-tools.md) - リンター・フォーマッター
- [13. Reward Hacking](./13-reward-hacking-ai.md) - 手抜き問題の検出と対策
- [14. Jagged Intelligence](./14-jagged-intelligence.md) - 苦手分野の理解と役割分担
- [15. AI Hallucination](./15-ai-hallucination.md) - 虚偽報告の検出方法
- [16. AI Scope Creep](./16-ai-scope-creep.md) - 暴走の防止策
- [18. Trust but Verify](./18-trust-but-verify.md) - 多層検証による品質確保
- [20. Claude Codeのモード切り替え](./20-claude-code-modes.md) - Plan/YOLO/Normalモードの使い分け
- [21. カスタムコマンド](./21-claude-code-custom-commands.md) - 育て方と実行前レビュー
- [22. 画面設計とVibe Coding](./22-screen-design-and-vibe-coding.md) - Vibe Codingでモックアップ生成、E2Eテスト自動生成

### STEP 5（リファクタリング・ドキュメント化）関連
- [07. Cyclomatic Complexity](./07-cyclomatic-complexity.md) - リファクタリング指標
- [08. ADR](./08-architecture-decision-records-adr.md) - 技術的決定の記録（Context Limitations対策）
- [09. Codebase to Prompt Tools](./09-codebase-to-prompt-tools.md) - コードレビュー
- [11. Living Documentation](./11-living-documentation.md) - ドキュメント自動化
- [17. Context Limitations](./17-context-limitations.md) - 知見の外部化と維持管理
- [19. Guardrails](./19-guardrails.md) - CLAUDE.md、カスタムコマンドの整備

## 🔄 更新履歴

### 2025-01-07（第5版）
- タスク分解フロー関連の記事を追加
- 新規記事追加：
  - 23-user-story-writing.md（ユーザーストーリーの書き方、INVEST原則）
  - 24-acceptance-criteria.md（受入基準とチェックリスト、Definition of Doneとの違い）
  - 25-task-decomposition.md（タスク分解とトークン制限への対応、Context Window対策）
- 日本語・英語の両方でWEB検索を実施し、2025年最新情報を反映
- AI開発の3つの問題（暴走・手抜き・忘れっぽさ）への対策を体系化
- 要件定義→設計→タスク分解の一連のフローを詳述

### 2025-01-07（第4版）
- 画面設計とVibe Coding関連の記事を追加
- 新規記事追加：
  - 22-screen-design-and-vibe-coding.md（画面一覧・画面遷移図・画面部品一覧、Vibe Codingによるモックアップ生成）
- 日本語・英語の両方でWEB検索を実施し、2025年最新情報を反映
- AI駆動開発における画面設計の重要性（Scope Creep/Reward Hacking対策）を詳述
- Vibe Codingツール比較（Cursor, v0, Lovable, Claude Artifacts等）
- Java/Spring Boot開発での実践例を追加

### 2025-01-07（第3版）
- Claude Code開発ツール関連の記事を追加
- 新規記事追加：
  - 20-claude-code-modes.md（モード切り替え：Plan/YOLO/Normal/Bypass Permissions）
  - 21-claude-code-custom-commands.md（カスタムコマンドの育て方とPlan Modeとの違い）
- 日本語・英語の両方でWEB検索を実施し、2025年最新情報を反映
- 実践的な使い分けフローとベストプラクティスを詳述

### 2025-01-06（第2版）
- AI特性・問題点と対処法を明確に分類
- 新規記事追加：
  - 14-jagged-intelligence.md（凸凹な知能）
  - 15-ai-hallucination.md（虚偽報告）
  - 16-ai-scope-creep.md（暴走）
  - 17-context-limitations.md（忘れっぽさ）
  - 18-trust-but-verify.md（任せる＆確かめる）
  - 19-guardrails.md（ガードレール）
- すべての例をJava/Spring Boot中心に更新
- 各AI問題に対する具体的な対処法を詳述

### 2025-01-06（初版）
- 初版作成
- 13トピックの詳細資料を収録
- WEB検索に基づく最新情報を反映（2024-2025年）

## 📝 ライセンスと出典

各ファイルには、参考にした以下のソースへのリンクが含まれています：
- 公式ドキュメント
- GitHub リポジトリ
- 技術ブログ記事
- 学術論文

## 🤝 貢献

このドキュメント集は、セミナーの品質向上のために継続的に更新されます。
新しいトピックや更新情報があれば追加してください。

## 📞 問い合わせ

セミナーに関する質問や、ドキュメントの改善提案がある場合は、プロジェクトの管理者にお問い合わせください。
