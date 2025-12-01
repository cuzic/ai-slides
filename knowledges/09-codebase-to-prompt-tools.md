# Codebase to Prompt Tools（コードベースをプロンプトに変換するツール）

## 概要

コードベース全体を単一のテキストファイルに変換し、大規模言語モデル（LLM）に渡してコードレビュー、分析、ドキュメント生成などを行うためのツール群。

## 主要ツール

### 1. code2prompt

#### 概要
- CLIツールでコードベースを単一のLLMプロンプトに変換
- ソースツリー、プロンプトテンプレート、トークンカウント機能を提供

#### 主な機能
- **自動コード処理**: リポジトリ全体の自動処理
- **スマートフィルタリング**: Globパターンによるファイルフィルタ
- **柔軟なテンプレート**: Handlebarsテンプレート
- **トークン追跡**: トークン数のカウント
- **Git統合**: Gitリポジトリとの統合
- **自動クリップボードコピー**: 生成されたプロンプトを自動的にクリップボードにコピー

#### 実装言語
**Rust**製で高速かつ効率的

#### 特徴
- 大規模なコードベースを最小限のリソースで処理
- コンテキストエンジニアリングツール
- リポジトリを構造化されたAI対応プロンプトに変換

#### MCP サーバーとして
- Model Context Protocol (MCP)サーバーとして実行可能
- ローカルサービスとして実行
- LLMが自動的に適切に構造化されたコンテキストを収集

#### インストール
```bash
# Cargo経由
cargo install code2prompt

# または
npm install -g code2prompt
```

#### 使用例
```bash
code2prompt --path ./src --output codebase.md
```

#### 参考資料
- [GitHub: mufeedvh/code2prompt](https://github.com/mufeedvh/code2prompt)
- [code2prompt.dev](https://code2prompt.dev/)

### 2. Repomix

#### 概要
- リポジトリ全体を単一のAI対応ファイルにパック
- Claude、ChatGPT、DeepSeek、Perplexity、Gemini、Llama、Grokなどに最適

#### 主な機能
- **単一ファイル出力**: クリアなセパレータでコードの異なる部分を分離
- **AI指向の説明**: ファイルの冒頭にAI理解を向上させる説明を追加
- **Model Context Protocol対応**: AIアシスタントがコードベースと直接対話可能
- **ローカル/リモートリポジトリ対応**: ローカルだけでなくリモートリポジトリも処理可能

#### 出力形式
- XML
- Markdown
- Plain Text

#### トークン数表示
生成されたファイルのトークン数を表示し、効率を確認可能

#### インストール
```bash
npm install -g repomix
```

#### 使用例
```bash
# デフォルト出力
repomix

# XML形式で出力
repomix --output codebase.xml --format xml

# トークン数を表示
repomix --show-tokens
```

#### 参考資料
- [GitHub: yamadashy/repomix](https://github.com/yamadashy/repomix)

### 3. files-to-prompt (Simon Willison作)

#### 概要
- シンプルで軽量なツール
- 指定した複数ファイルを1つのプロンプトに変換

#### 主な特徴
- **シンプルさ**: 最小限の機能で使いやすい
- **Markdown形式**: ファイルパスとコンテンツを明示
- **軽量**: すぐに使える

#### 使用例
```bash
# 特定のディレクトリ配下のファイルを変換
files-to-prompt src/**/*.ts > codebase.txt

# 複数のファイルタイプを対象
files-to-prompt src/**/*.{js,ts,jsx,tsx} > codebase.txt
```

#### 参考資料
- Simon Willison's blog

### 4. Your Source to Prompt

#### 概要
ブラウザベースのツールで、完全にブラウザ内で動作

#### 主な特徴
- **単一HTMLファイル**: 単一の.htmlファイルで完結
- **外部依存なし**: 外部サービスやライブラリ不要
- **プライバシー**: すべての処理がローカルで完結
- **ブラウザベース**: インストール不要

#### 使用方法
1. HTMLファイルをブラウザで開く
2. コードファイルをドラッグ＆ドロップ
3. プロンプトが生成される

#### 参考資料
- [GitHub: your-source-to-prompt.html](https://github.com/Dicklesworthstone/your-source-to-prompt.html)

## ツールの比較

| 特徴 | code2prompt | Repomix | files-to-prompt | Your Source to Prompt |
|------|-------------|---------|-----------------|----------------------|
| **実装言語** | Rust | TypeScript/JavaScript | Python | HTML/JavaScript |
| **速度** | 非常に高速 | 高速 | 高速 | ブラウザ依存 |
| **機能** | 豊富 | 豊富 | 基本的 | 基本的 |
| **MCP対応** | ✓ | ✓ | ✗ | ✗ |
| **テンプレート** | Handlebars | ✓ | ✗ | ✗ |
| **トークンカウント** | ✓ | ✓ | ✗ | ✗ |
| **出力形式** | 複数 | XML/Markdown/Text | Text | Text |
| **インストール** | 必要 | 必要 | 必要 | 不要（ブラウザ） |
| **プライバシー** | ローカル | ローカル | ローカル | ローカル |

## 使い分けの指針

### code2prompt を選ぶべき場合
- 大規模プロジェクトで高速処理が必要
- カスタムテンプレートが必要
- MCPサーバーとして使用したい
- トークン数を正確に把握したい

### Repomix を選ぶべき場合
- AIツール向けに最適化された出力が必要
- XML形式で出力したい
- リモートリポジトリを処理したい
- AI理解を向上させる説明が必要

### files-to-prompt を選ぶべき場合
- シンプルで軽量なツールが欲しい
- 特定のファイルのみを対象としたい
- すぐに使い始めたい

### Your Source to Prompt を選ぶべき場合
- インストールしたくない
- ブラウザで完結させたい
- プライバシーを最優先したい
- 小規模なコードベース

## 活用シーン

### 1. コードレビュー
複数のAI（Claude、ChatGPT、Gemini）でコードをレビュー：
```bash
# コードベースをプロンプト化
code2prompt --path ./src --output codebase.md

# 各AIにプロンプトを投入
# "このコードをセキュリティの観点でレビューしてください"
```

### 2. ドキュメント生成
```bash
repomix --output codebase.xml

# AIに投入
# "このコードベースの包括的なドキュメントを生成してください"
```

### 3. リファクタリング提案
```bash
code2prompt --path ./src --output codebase.md

# AIに投入
# "このコードベースをClean Architectureの観点でレビューし、リファクタリング案を提案してください"
```

### 4. バグ発見
```bash
files-to-prompt src/**/*.ts > codebase.txt

# AIに投入
# "潜在的なバグやセキュリティ脆弱性を探してください"
```

## レビュー観点の例

### セキュリティレビュー
- SQLインジェクション
- XSS（クロスサイトスクリプティング）
- CSRF（クロスサイトリクエストフォージェリ）
- 認証・認可の問題
- 機密情報のハードコード

### パフォーマンスレビュー
- N+1問題
- 不要なループ
- メモリリーク
- 非効率なアルゴリズム

### 設計レビュー
- SOLID原則の遵守
- デザインパターンの適用
- DRY原則
- コードの重複

### 保守性レビュー
- 命名規則
- コメント
- 関数の長さ
- 循環的複雑度

## ベストプラクティス

### 1. 除外設定
不要なファイルを除外：
- `node_modules/`
- `.git/`
- `dist/`, `build/`
- テストカバレッジレポート
- 自動生成ファイル

### 2. トークン制限の考慮
- LLMのトークン制限を考慮
- 必要なファイルのみを含める
- 大規模プロジェクトは分割して処理

### 3. バージョン管理
- 生成されたプロンプトファイルは`.gitignore`に追加
- 必要に応じて生成

### 4. プライバシー
- 機密情報を含むファイルは除外
- `.env`ファイルなどを除外
- APIキーやパスワードを含まない

## 参考資料

- [16x Prompt: CLI Tools Collection](https://prompt.16x.engineer/cli-tools)
- [GitHub: mufeedvh/code2prompt](https://github.com/mufeedvh/code2prompt)
- [GitHub: yamadashy/repomix](https://github.com/yamadashy/repomix)
- [THEJO AI: Code2prompt](https://www.thejoai.com/ai-tools/code2prompt-convert-codebase-to-prompt/)

## まとめ

コードベースをプロンプトに変換するツールは、AIを活用したコードレビュー、ドキュメント生成、リファクタリング提案などに不可欠。プロジェクトの規模や要件に応じて適切なツールを選択し、効率的な開発を実現できる。
