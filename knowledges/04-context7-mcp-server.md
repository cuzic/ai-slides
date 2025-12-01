# Context7 MCP Server

## 概要

Context7は、大規模言語モデル（LLM）とAIコードエディタのための最新ドキュメントを提供するMCPサーバー。公式ドキュメントから最新のドキュメントとコード例を直接取得し、モデルのコンテキストに注入する。

## 開発元

**Upstash**が開発・提供しているオープンソースプロジェクト

## 主な機能

### リアルタイムドキュメントアクセス
- 最新のドキュメントとコード例を公式ソースから取得
- バージョン固有のコード例を提供
- 非推奨のAPIを使用するリスクを回避

### 生産性向上
- ドキュメントを手動で検索する時間を削減
- コンテキストに直接最新情報を注入
- より正確なコード生成を支援

### 互換性
主要なMCP互換クライアントで動作：
- Claude Desktop
- Claude Code
- Cursor
- Windsurf
- その他のMCP対応ツール

## インストール方法

### npmパッケージ
```bash
npm install @upstash/context7-mcp
```

### Claude Codeでの設定
```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["@upstash/context7-mcp@latest"]
    }
  }
}
```

## 提供されるツール

Context7 MCPは2つの主要ツールを提供：

### 1. resolve-library-id
- 一般的なライブラリ名をContext7互換のライブラリIDに解決
- ライブラリの正確な識別を支援

### 2. get-library-docs
- Context7互換のライブラリIDを使用してドキュメントを取得
- 最新のAPIリファレンス、使用例、ベストプラクティスを含む

## 使用方法

### Cursorでの使用例
質問に`use context7`を追加するだけ：

```
use context7 ReactのuseEffectフックの最新の使い方を教えて
```

### 対応ライブラリ（例）
- React
- Next.js
- TypeScript
- Python標準ライブラリ
- その他多数のフレームワークとライブラリ

## アーキテクチャ

### 公開コンポーネント
- **MCPサーバー実装**: GitHubで公開

### プライベートコンポーネント
以下は非公開：
- APIバックエンド
- パース（解析）エンジン
- クローリング（情報収集）エンジン

## 技術的詳細

### ホストされたMCPエンドポイント
```
https://mcp.context7.com/mcp
```

### GitHub リポジトリ
```
https://github.com/upstash/context7
```

## 利点

1. **常に最新**: ドキュメントの古い情報に基づくコード生成を防ぐ
2. **時間節約**: 手動でのドキュメント検索が不要
3. **精度向上**: 正確なAPIの使い方でコード品質が向上
4. **非推奨API回避**: 古いAPIを使ってしまうリスクを削減
5. **バージョン対応**: 使用しているライブラリのバージョンに合わせたドキュメント

## ユースケース

- 新しいライブラリの学習
- APIの最新の使い方の確認
- マイグレーションガイドの参照
- ベストプラクティスの適用
- バージョン固有の実装方法の確認

## 参考資料

- [GitHub: upstash/context7](https://github.com/upstash/context7)
- [Upstash Blog: Context7 MCP](https://upstash.com/blog/context7-mcp)
- [Apidog: How to Install and Use Context7 MCP Server](https://apidog.com/blog/context7-mcp-server/)
- [MCP Servers: Context7](https://mcpservers.org/servers/upstash/context7-mcp)

## コミュニティとサポート

- MCP Serversディレクトリに登録
- LobeHub MCP Serversカタログに掲載
- Smithery AI サーバーレジストリに登録
- 活発なコミュニティサポート
