# Architecture Decision Records (ADR)

## 概要

Architecture Decision Records (ADR)は、ソフトウェアアーキテクチャに関する重要な技術的決定を記録するドキュメント形式。各ADRは、1つの重要な決定とそのコンテキスト、結果を捉える。

## 基本テンプレート（Michael Nygardによる）

Michael Nygard の "Documenting Architecture Decisions" で定義された基本構造：

### 必須要素
1. **Title（タイトル）**: 簡潔な決定の説明
2. **Status（状態）**: Proposed, Accepted, Deprecated, Superseded
3. **Context（コンテキスト）**: 決定の背景と理由
4. **Decision（決定）**: 実際に行われた決定
5. **Consequences（結果）**: 決定による影響（良い面と悪い面の両方）

## 主要なテンプレート形式

### 1. MADR (Markdown ADR)
完全版と最小版の両方を提供：
- アノテーション付き形式
- ベア（素）形式
- 検討したオプションとその長所・短所のトレードオフ分析を含む

### 2. Y-Statement テンプレート
簡潔な形式：
```
In the context of <use case/user story>,
facing <concern>
we decided for <option>
to achieve <quality>,
accepting <downside>
```

日本語例：
```
<ユースケース/ユーザーストーリー>のコンテキストにおいて、
<懸念事項>に直面して
<オプション>を選択することに決定し、
<品質>を達成するために、
<デメリット>を受け入れる
```

## ベストプラクティス

### 1. 1つのADRに1つの決定
- 複数のアーキテクチャ決定を1つのドキュメントにまとめない
- 各ADRは1つのコア技術方向またはその直接的な依存関係を扱う
- 明確性と追跡可能性を維持

### 2. 必須要素の定義
最低限、各ADRには以下が必要：
- 決定のコンテキスト
- 決定そのもの
- プロジェクトと成果物に対する決定の結果

### 3. ステータス管理
効果的なADRシステムには明確なステータス指標が必要：
- **Proposed（提案）**: 検討中
- **Accepted（承認）**: 採用決定
- **Deprecated（非推奨）**: 使用を推奨しない
- **Superseded（置換）**: 別のADRに置き換えられた

### 4. 簡潔なミーティング
- ADRミーティングは簡潔で時間を区切る
- 30〜45分を最大とする
- 焦点を絞った議論

### 5. 一元的な保管
- すべてのプロジェクトメンバーがアクセスできる場所に保管
- 透明性を促進
- アーキテクチャ決定をすべての関係者が容易に利用可能に

### 6. バージョン管理
- Gitなどのバージョン管理システムで管理
- 変更履歴を追跡
- コードと一緒に保管（例：`docs/adr/`）

## ADRの配置場所

### 推奨される配置
```
project-root/
├── docs/
│   └── adr/
│       ├── 0001-use-postgresql-for-database.md
│       ├── 0002-adopt-microservices-architecture.md
│       └── 0003-use-react-for-frontend.md
└── README.md
```

### 命名規則
```
NNNN-title-with-dashes.md
```
- NNNN: 4桁の連番（例：0001, 0002）
- title-with-dashes: ケバブケースのタイトル

## ADRの例

### 例1: データベース選択
```markdown
# 1. PostgreSQLをデータベースとして使用

## Status
Accepted

## Context
プロジェクトには以下が必要：
- ACID準拠のトランザクション
- 複雑なクエリのサポート
- JSON型のサポート
- 大規模なコミュニティとエコシステム

## Decision
PostgreSQLをメインデータベースとして採用する。

## Consequences
### 良い点
- 堅牢なACIDトランザクション
- 豊富な拡張機能とツール
- 優れたパフォーマンス
- 活発なコミュニティサポート

### 悪い点
- NoSQLに比べてスケールアウトが複雑
- セットアップと運用に専門知識が必要
- クラウドマネージドサービスのコストが高い
```

### 例2: フロントエンドフレームワーク
```markdown
# 2. Reactをフロントエンドフレームワークとして採用

## Status
Accepted

## Context
SPA（Single Page Application）を構築する必要があり、
以下の要件を満たす必要がある：
- コンポーネントベースの開発
- 大規模なエコシステム
- チームメンバーの既存スキル

## Decision
Reactを採用し、Next.jsをフレームワークとして使用する。

## Consequences
### 良い点
- チームメンバーが既に習熟している
- 豊富なライブラリとツール
- SSR/SSGのサポート（Next.js）
- 大企業による支援と維持

### 悪い点
- ボイラープレートコードが多い
- 状態管理に追加ライブラリが必要
- バンドルサイズが大きくなる傾向
```

## ADR管理ツール

### コマンドラインツール
- **ADR Tools**: Bashベースのツール
- **adr-log**: ADRログ生成ツール

### Webベースツール
- **Log4brains**: ADR管理のためのWebUI
- **ADR Manager**: ブラウザベースのADRマネージャー

### IDE統合
- VSCode拡張機能
- IntelliJ IDEAプラグイン

## ADRのライフサイクル

### 1. 提案（Proposed）
- 問題の特定
- 代替案の検討
- ADRのドラフト作成

### 2. レビュー
- チームでのレビュー
- フィードバックの収集
- 修正と改善

### 3. 承認（Accepted）
- 決定の確定
- ステータスを Accepted に更新
- 実装開始

### 4. 実装
- 決定に基づいた実装
- 結果の文書化

### 5. 見直し
- 定期的な見直し
- 必要に応じて Deprecated または Superseded に更新

## 利点

1. **透明性**: すべての決定が文書化され、理由が明確
2. **知識の共有**: 新しいメンバーがコンテキストを理解できる
3. **意思決定の品質**: 構造化されたアプローチで決定の質が向上
4. **変更の追跡**: 時間経過による決定の変遷を追跡
5. **説明責任**: 誰がいつ何を決定したかが明確
6. **将来の参照**: 過去の決定を簡単に参照可能

## AWS Prescriptive Guidanceによる推奨

### ADRプロセス
1. 決定が必要な問題を特定
2. 選択肢をリストアップ
3. 各選択肢の長所と短所を評価
4. 決定を下す
5. ADRを文書化
6. チームと共有
7. 定期的に見直し

## 参考資料

- [GitHub: architecture-decision-record](https://github.com/joelparkerhenderson/architecture-decision-record)
- [adr.github.io](https://adr.github.io/)
- [AWS Prescriptive Guidance: ADR process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html)
- [Microsoft: Architecture decision record](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)
- [TechTarget: Best practices for creating ADRs](https://www.techtarget.com/searchapparchitecture/tip/4-best-practices-for-creating-architecture-decision-records)

## まとめ

ADRは、アーキテクチャの決定を文書化し、チーム全体で共有するための強力なツール。適切に使用することで、プロジェクトの透明性、知識の共有、意思決定の質を大幅に向上させることができる。
