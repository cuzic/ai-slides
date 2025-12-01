# Model Context Protocol (MCP)

## 概要

Model Context Protocol (MCP)は、2024年11月にAnthropicが発表したオープンソースプロトコルで、AIアシスタントとデータが存在するシステム（コンテンツリポジトリ、ビジネスツール、開発環境など）を接続するための標準。

## 主な特徴

### オープン標準
- AIツール統合のためのオープンソース標準
- データソースとAI駆動ツール間の安全な双方向接続を可能にする
- 開発者はMCPサーバー経由でデータを公開、またはMCPクライアント（AI アプリケーション）を構築可能

### アーキテクチャ
- 意図的にLanguage Server Protocol (LSP)のメッセージフロー思想を再利用
- JSON-RPC 2.0で転送
- シンプルで理解しやすい構造

## Claude Codeとの統合

### 接続機能
- Claude Codeは、MCPを通じて数百の外部ツールとデータソースに接続可能
- MCPサーバーはClaude Codeにツール、データベース、APIへのアクセスを提供
- Claude CodeにMCPサーバーを追加、またはClaude CodeをMCPサーバーとして使用可能

### 使用方法
MCPサーバーの設定は、Claude Codeの設定ファイルに以下のような形式で追加：

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["package-name@latest"]
    }
  }
}
```

## エコシステムと採用状況

### 急速な成長
2024年11月のローンチ以来、採用は急速に進んでいる：
- コミュニティが数千のMCPサーバーを構築
- すべての主要なプログラミング言語でSDKが利用可能
- エージェントをツールやデータに接続するためのデファクトスタンダードとして業界で採用

### 事前構築済みMCPサーバー
Anthropicは、人気のあるエンタープライズシステム向けの事前構築済みMCPサーバーを提供：
- Google Drive
- Slack
- GitHub
- Git
- Postgres
- Puppeteer

## 技術的詳細

### Language Server Protocolとの関係
- LSPはエディタとプログラミング言語サービス間の標準化されたプロトコル
- MCPはこの成功したパターンをAIツール統合に適用
- 同様のメッセージフロー設計を採用

### JSON-RPC 2.0
- 軽量なリモートプロシージャコール（RPC）プロトコル
- シンプルで実装しやすい
- 広くサポートされている

## 利点

1. **標準化**: ツールごとにカスタム統合を構築する必要がない
2. **相互運用性**: 異なるAIツールとデータソース間の統合が容易
3. **拡張性**: 新しいツールやデータソースの追加が簡単
4. **セキュリティ**: 安全な接続メカニズム
5. **オープンソース**: コミュニティ駆動の開発と改善

## コード実行とMCP

Anthropicは、MCPを使用したコード実行について詳しく説明している：
- より効率的なAIエージェントの構築
- サンドボックス化された実行環境
- 安全なコード実行

## 参考資料

- [Anthropic: Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol)
- [Claude Docs: Model Context Protocol (MCP)](https://docs.claude.com/en/docs/mcp)
- [Connect Claude Code to tools via MCP](https://docs.claude.com/en/docs/claude-code/mcp)
- [Wikipedia: Model Context Protocol](https://en.wikipedia.org/wiki/Model_Context_Protocol)
- [Anthropic: Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)

## 対応AIツール

- Claude Desktop
- Claude Code
- Cursor
- Windsurf
- その他のMCP互換クライアント
