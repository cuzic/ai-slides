# Chrome DevTools MCP Server

## 概要

Chrome DevTools MCP Serverは、AIコーディングアシスタントがライブのChromeブラウザを制御・検査できるようにするツール。Chrome DevToolsの全機能をAIに提供し、信頼性の高い自動化、詳細なデバッグ、パフォーマンス分析を可能にする。

## 開発元

**Google Chrome DevTools チーム**が公式に開発・提供

## MCPとは

Model Context Protocol（MCP）は、Anthropicが2024年後半に導入したオープンスタンダードで、大規模言語モデル（LLM）を外部ツールやデータソースに接続するための仕組み。

## 主な機能

### 1. パフォーマンスインサイト
- Chrome DevToolsを使用してトレースを記録
- 実行可能なパフォーマンスインサイトを抽出
- ボトルネックを特定
- 最適化案を提示

### 2. 高度なブラウザデバッグ
- ネットワークリクエストの分析
- スクリーンショットの取得
- ブラウザコンソールのチェック
- DOM要素の検査

### 3. Puppeteerベースの自動化
- Chrome内でのアクション自動化
- アクション結果の自動待機
- 信頼性の高いE2Eテスト
- ページ操作の記録と再生

## AIコーディングアシスタントに"目"を与える

従来のAIコーディング：
- コードを見ることしかできない
- ブラウザでの実際の動作が見えない
- 「盲目のプログラミング」

Chrome DevTools MCP導入後：
- AIがブラウザを"見る"ことができる
- 実際のレンダリング結果を確認
- パフォーマンス問題を特定
- コンソールエラーを検出

## インストール方法

### NPMパッケージ
```bash
npm install chrome-devtools-mcp
```

### MCP Clientへの設定
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["chrome-devtools-mcp@latest"]
    }
  }
}
```

### Claude Codeでの設定例
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp"]
    }
  }
}
```

## 提供される機能

### 1. ネットワーク分析
- HTTPリクエスト/レスポンスの監視
- ステータスコード確認
- レスポンス時間の計測
- ペイロードの検査

### 2. コンソール監視
- JavaScriptエラーの自動検出
- 警告メッセージの収集
- ログ出力の確認
- スタックトレースの解析

### 3. パフォーマンス計測
- ページロード時間
- レンダリング時間
- JavaScript実行時間
- メモリ使用量

### 4. スクリーンショット
- ページ全体のキャプチャ
- 特定要素のキャプチャ
- ビジュアルリグレッション検出
- UI状態の記録

### 5. DOM検査
- 要素の検索
- スタイルの確認
- イベントリスナーの確認
- アクセシビリティ検査

## 使用例

### パフォーマンスデバッグ
```
このページのパフォーマンスを分析して、
ボトルネックを特定してください
```

AIの動作：
1. ページをロード
2. パフォーマンストレースを記録
3. ボトルネックを分析
4. 具体的な改善案を提示

### ネットワークエラーのデバッグ
```
APIリクエストが失敗しているか確認して、
問題があれば原因を特定してください
```

AIの動作：
1. ネットワークタブを監視
2. 失敗したリクエストを特定
3. ステータスコードとエラーメッセージを確認
4. 修正案を提示

### コンソールエラーの検出
```
このページでJavaScriptエラーが
出ていないか確認してください
```

AIの動作：
1. ブラウザコンソールを監視
2. エラーメッセージを収集
3. スタックトレースを解析
4. 修正方法を提案

## 対応AIアシスタント

- **Claude** (Claude Desktop, Claude Code)
- **Gemini CLI**
- **Cursor**
- **JetBrains AI Assistant**
- **GitHub Copilot**
- その他のMCP対応ツール

## 実践例

### ケーススタディ1: パフォーマンス最適化

#### 問題
ページロードが遅い

#### AIの対応
1. Chrome DevTools MCPでパフォーマンストレースを記録
2. 大きなJavaScriptバンドルを特定（3MB）
3. 未使用のコードを検出（1.5MB）
4. コード分割を提案
5. 遅延ロードを実装

#### 結果
- ページロード時間が3秒から1秒に短縮
- バンドルサイズを50%削減

### ケーススタディ2: ネットワークエラーのデバッグ

#### 問題
APIリクエストが時々失敗する

#### AIの対応
1. ネットワークリクエストを監視
2. 504 Gateway Timeoutを検出
3. リクエストタイムアウトの設定を確認
4. リトライロジックの実装を提案

#### 結果
- エラー率が5%から0.1%に削減
- ユーザー体験が大幅に向上

## デバッグ効率の向上

### 従来のデバッグフロー
1. コードを書く
2. ブラウザで手動テスト
3. DevToolsを手動で開く
4. エラーを探す
5. コードに戻って修正
6. 繰り返し

### Chrome DevTools MCP を使った フロー
1. コードを書く
2. AIに「デバッグして」と指示
3. AIが自動的にDevToolsを確認
4. AIが問題を特定して修正案を提示
5. 修正を実装
6. 完了

**時間削減**: 約70%の時間短縮（体感値）

## パフォーマンス分析の詳細

### 計測される指標
- **FCP (First Contentful Paint)**: 最初のコンテンツ表示時間
- **LCP (Largest Contentful Paint)**: 最大コンテンツ表示時間
- **FID (First Input Delay)**: 最初の入力遅延
- **CLS (Cumulative Layout Shift)**: レイアウトシフトの累積
- **TTFB (Time to First Byte)**: 最初のバイト受信時間

### AIによる分析
```
このページのCore Web Vitalsを
分析して改善案を提案してください
```

AIの出力例：
```
分析結果：
- LCP: 4.2秒（改善が必要）
  原因：大きな画像が遅延ロードされていない
  推奨：<img loading="lazy">を使用

- CLS: 0.25（改善が必要）
  原因：画像に width/height 属性がない
  推奨：サイズ属性を追加

- FID: 50ms（良好）
  問題なし
```

## セキュリティとプライバシー

### 安全な使用
- ローカル環境でのみ実行
- 本番環境では使用しない
- 機密情報を含むページでは注意

### ベストプラクティス
- 開発環境でのみ使用
- アクセス権限を適切に設定
- ログに機密情報が含まれないよう注意

## 制限事項

### 技術的制限
- Chromeブラウザのみ対応
- ヘッドレスモードでは一部機能が制限
- リモートデバッグには追加設定が必要

### パフォーマンス
- 大規模なページでは処理に時間がかかる場合がある
- 複雑なSPAでは分析に時間が必要

## トラブルシューティング

### よくある問題

#### Chromeが起動しない
```bash
# Chrome実行ファイルのパスを確認
which google-chrome
which chromium

# 環境変数で指定
export CHROME_PATH=/path/to/chrome
```

#### ポート競合
```bash
# 別のポートを使用
chrome-devtools-mcp --port 9223
```

## GitHub リポジトリ

- [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- [benjaminr/chrome-devtools-mcp](https://github.com/benjaminr/chrome-devtools-mcp)

## 参考資料

### 公式ドキュメント
- [Chrome for Developers Blog: Chrome DevTools MCP](https://developer.chrome.com/blog/chrome-devtools-mcp)
- [Addy Osmani: Give your AI eyes](https://addyosmani.com/blog/devtools-mcp/)

### チュートリアル
- [LogRocket: Debugging with Chrome DevTools MCP](https://blog.logrocket.com/debugging-with-chrome-devtools-mcp/)
- [DebugBear: Performance Debugging](https://www.debugbear.com/blog/chrome-devtools-mcp-performance-debugging)
- [MCPCN: Chrome DevTools MCP Guide](https://mcpcn.com/en/blog/chrome-devtools-mcp-ai-debugging/)

### コミュニティ
- [LobeHub MCP Servers](https://lobehub.com/mcp/benjaminr-chrome-devtools-mcp)
- [Awesome MCP Servers](https://mcpservers.org/servers/github-com-chromedevtools-chrome-devtools-mcp)

## 将来の展望

### 計画中の機能
- Firefox対応
- Safari対応
- より高度なパフォーマンス分析
- AI駆動の自動修正

### コミュニティ貢献
- オープンソースプロジェクト
- コントリビューション歓迎
- フィードバックを反映

## まとめ

Chrome DevTools MCP Serverは、AIコーディングアシスタントに"目"を与え、ブラウザでの実際の動作を確認できるようにする革新的なツール。パフォーマンスデバッグ、ネットワーク分析、コンソールエラー検出など、多くの場面でデバッグ効率を大幅に向上させる。

**主な利点**:
- デバッグ時間の大幅短縮
- より正確な問題特定
- 自動化されたパフォーマンス分析
- AIによる改善提案

AIとDevToolsの組み合わせにより、Web開発の新しい時代が始まっている。
