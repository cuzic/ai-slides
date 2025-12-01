# Serena MCP Server

## 概要

Serenaは、セマンティックな取得と編集機能を提供する強力なコーディングエージェントツールキット。Language Server Protocol (LSP)を活用してトークン効率を向上させ、IDE的なツールをLLMに提供する。

## 開発元

**Oraios AI**が開発・提供しているオープンソースプロジェクト

## 主な特徴

### トークン最適化
既存のコーディングエージェントと組み合わせることでトークン効率を向上：
- ファイル全体を読み込む必要がない
- grep的な検索を行う必要がない
- シンボルレベルでコードエンティティを抽出
- 関係構造を活用

### IDE的なツールの提供
LLMに以下のようなコード中心のツールを提供：
- `find_symbol`: シンボルを検索
- `find_referencing_symbols`: 参照しているシンボルを検索
- `insert_after_symbol`: シンボルの後に挿入
- その他のセマンティックな操作

### Language Server Protocolの活用
LSPに基づくセマンティックコード解析：
- 自動補完（auto-completion）
- 定義へジャンプ（go-to-definition）
- すべての参照を検索（find-all-references）
- 言語固有の機能

## トークン最適化のアプローチ

### 1. セマンティックコード解析
- LSPを使用した言語固有の機能
- コードの構造を理解
- 必要な部分だけを効率的に抽出

### 2. 効率的な操作
- ファイル全体を処理する代わりに必要な部分だけを取得
- コスト削減と品質向上
- 特に大規模プロジェクトで有効

### 3. シンボルレベルのアクセス
- シンボル単位でのコード操作
- 関係性を考慮した効率的な処理
- 不要な情報の除外

## インストール方法

### GitHub リポジトリ
```bash
git clone https://github.com/oraios/serena.git
```

### MCPサーバーとしての設定
```json
{
  "mcpServers": {
    "serena": {
      "command": "node",
      "args": ["path/to/serena/mcp-server.js"]
    }
  }
}
```

## 統合とサポート

### 対応クライアント
- Claude Code
- Claude Desktop
- VSCode
- Cursor
- その他のMCP互換ツール

### 追加統合
- Agno統合サポート
- 他のAIフレームワークとの連携

## アーキテクチャ

### Language Server Protocol統合
- 標準化されたコード解析
- 言語固有のサービスへのアクセス
- エディタとの一貫した連携

### MCPを通じた提供
- 標準化されたプロトコルで提供
- 他のツールとの組み合わせが容易
- 拡張性の高い設計

## 利点

1. **コスト削減**: トークン使用量の削減により開発コストを削減
2. **品質向上**: 効率的な操作により生成されるコードの品質が向上
3. **大規模プロジェクト対応**: 大規模なコードベースでも効率的に動作
4. **時間節約**: 必要な情報に素早くアクセス
5. **精度向上**: セマンティック解析により正確なコード理解

## ユースケース

- 大規模プロジェクトでのコード生成
- リファクタリング支援
- コードナビゲーション
- シンボル検索と参照
- インテリジェントなコード編集

## 技術的詳細

### セマンティック解析
- 構文木（AST）の活用
- 型情報の利用
- スコープ解析
- 参照関係の追跡

### 効率的なコード操作
従来のアプローチ：
```
ファイル全体を読み込む → 数万〜数十万トークン消費
```

Serenaのアプローチ：
```
必要なシンボルだけを取得 → 数百〜数千トークン消費
```

## 参考資料

- [GitHub: oraios/serena](https://github.com/oraios/serena)
- [Medium: Deconstructing Serena's MCP-Powered Architecture](https://medium.com/@souradip1000/deconstructing-serenas-mcp-powered-semantic-code-understanding-architecture-75802515d116)
- [Skywork AI: Serena MCP Server Deep Dive](https://skywork.ai/skypage/en/Serena%20MCP%20Server:%20A%20Deep%20Dive%20for%20AI%20Engineers/1970677982547734528)
- [Apidog: How to Use Serena MCP Server](https://apidog.com/blog/serena-mcp-server-2/)

## 対応言語

LSPが存在する言語なら利用可能：
- TypeScript / JavaScript
- Python
- Rust
- Go
- Java
- C/C++
- その他多数

## コミュニティ

- 活発なGitHubコミュニティ
- 継続的な機能追加と改善
- オープンソースでの開発
