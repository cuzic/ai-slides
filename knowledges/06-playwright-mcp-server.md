# Playwright MCP Server

## 概要

Playwright MCP ServerはAIエージェントとライブブラウザセッションを橋渡しし、AIがPlaywrightを介してWebアプリケーションと対話できるようにするツール。

## 開発元

**Microsoft**が開発・提供している公式プロジェクト

## 主な機能

### 生成的自動化テスト
- Vibe Codingの体験でE2Eテストを生成
- AIがサイトを探索してテストを書く
- 手動テストからAI生成自動化への移行

### ブラウザ自動化
- Puppeteer ベースの自動化
- Chrome内でのアクション自動化
- アクション結果の自動待機

### パフォーマンス分析
- Chrome DevToolsを使用してトレースを記録
- 実行可能なパフォーマンスインサイトを抽出
- ボトルネックの特定

### 高度なデバッグ
- ネットワークリクエストの分析
- スクリーンショットの取得
- ブラウザコンソールのチェック

## Visual Regression Testing（ビジュアルリグレッションテスト）

### 基本的なアプローチ
- スクリーンショット比較による視覚的変更の検出
- ベースライン画像との比較
- UIバグを本番環境に到達する前にキャッチ

### GPT-5 + Playwright MCP PixelDiff Engine
AI駆動のビジュアルリグレッションテスト：
- 自動化されたビジュアルリグレッションテストのセットアップ
- 本番環境到達前のUIバグ検出

#### 実績データ
あるチームの統合結果：
- 最初の1週間で手動テストでは見逃していた12のUIリグレッションを発見
- 顧客から報告される視覚的バグが40%削減
- テストサイクルが3倍高速化

### 制限事項
純粋な視覚的検証には以下が必要：
- 従来の方法での補完
- Playwrightの組み込みスクリーンショットアサーションの使用
- 事前定義されたベースライン画像

## 複雑なテストシナリオの作成

### 複数MCPサーバーの組み合わせ
Playwrightを複数のMCPサーバーに接続：
- ビジュアルツール
- アクセシビリティチェッカー
- APIファザー
- その他の専門ツール

### 利点
- コードを大きくすることなく複雑なシナリオを作成
- 各ツールの専門性を活用
- モジュラーなテスト設計

## インストールと設定

### 基本的なセットアップ
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

### Claude Code での使用
```
このページのログインフローをテストするPlaywrightテストを作成してください
```

## 主な機能と操作

### AIによるインタラクティブな操作
- ページナビゲーション
- 要素のクリック
- フォーム入力
- スクロール
- スクリーンショット取得

### テスト生成
- ユーザーフローの自動テストコード生成
- 例：「ログイン→ダッシュボード表示→ログアウト」
- テスト失敗時の原因特定と修正

## 利点

1. **AI支援テスト生成**: 手動でのテストコード作成が不要
2. **時間削減**: テストサイクルの大幅な短縮
3. **品質向上**: より多くのバグを早期に発見
4. **保守性**: 生成されたテストコードは理解しやすい
5. **包括的カバレッジ**: AIが複雑なシナリオも考慮

## ユースケース

### E2Eテスト生成
- ユーザーフローのテスト
- フォーム送信のテスト
- ナビゲーションのテスト

### ビジュアルリグレッションテスト
- UIの視覚的変更の検出
- レイアウトの崩れの発見
- CSSの意図しない変更の検出

### パフォーマンステスト
- ページロード時間の計測
- レンダリング時間の分析
- ボトルネックの特定

## 実践例

### Azure DevOps + Playwright MCP
Microsoftの事例：
- 手動テストからAI生成自動化への成功事例
- 開発チームの生産性向上
- テスト品質の向上

## 参考資料

- [Medium: Generative Automation Testing with Playwright MCP](https://adequatica.medium.com/generative-automation-testing-with-playwright-mcp-server-45e9b8f6f92a)
- [Azure DevOps Blog: MCP + Playwright Success Story](https://devblogs.microsoft.com/devops/from-manual-testing-to-ai-generated-automation-our-azure-devops-mcp-playwright-success-story/)
- [Markaicode: Visual Regression with GPT-5](https://markaicode.com/visual-regression-gpt5-playwright/)
- [Codoid: Playwright MCP Expert Strategies](https://codoid.com/automation-testing/playwright-mcp-expert-strategies-for-success/)
- [Testomat.io: Playwright MCP Modern Guide](https://testomat.io/blog/playwright-mcp-modern-test-automation-from-zero-to-hero/)

## 技術スタック

- **Playwright**: ブラウザ自動化フレームワーク
- **MCP**: Model Context Protocol for AI integration
- **Chrome DevTools**: パフォーマンス分析
- **AI/LLM**: テスト生成とシナリオ作成

## 対応ブラウザ

- Chromium
- Firefox
- WebKit
- すべての主要ブラウザをカバー

## コミュニティとサポート

- Microsoft公式サポート
- 活発なコミュニティ
- 豊富なドキュメント
- 継続的なアップデート
