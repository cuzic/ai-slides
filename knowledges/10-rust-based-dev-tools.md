# Rust製開発ツール：Biome、Ruff、oxc

## 概要

JavaScript/TypeScript、Python、その他の言語向けの高速で効率的な開発ツール群。Rustで書かれており、従来のツールに比べて10〜100倍高速。

## 共通哲学

### パフォーマンス至上主義
- JavaScriptツーリングはより高性能な言語で書き直すことができる
- Rustの速度と安全性を活用
- 既存ツールの10〜100倍の高速化を実現

### 統一ツールチェイン
- 複数のツールを1つに統合
- 一貫したエクスペリエンス
- 設定の簡素化

### インスピレーション
これらのプロジェクトは、BiomeとRuffなくしては存在しなかった。Rust製統一ツールチェインのパイオニアとして、他のプロジェクトに影響を与えている。

---

## 1. Biome

### 概要
Rustで構築された新しいオープンソースのリンター＆フォーマッター。ESLintやPrettierなどの従来ツールより高速。

### 前身
**Rome**の後継プロジェクト。Romeは、Babel、ESLint、webpack、Prettier、Jest等を最終的に置き換えることを目指していた。

### 対応言語/ファイル
- JavaScript
- TypeScript
- JSX
- JSON
- JSONC

### 主な機能

#### リンティング
- ESLintルールの互換性
- 高速な静的解析
- 自動修正機能

#### フォーマッティング
- Prettierとの互換性を目指す
- 一貫したコードスタイル
- 設定可能なルール

#### 統合ツールチェイン
将来的に以下を置き換える計画：
- Babel（トランスパイラ）
- ESLint（リンター）
- webpack（バンドラー）
- Prettier（フォーマッター）
- Jest（テストランナー）

### パフォーマンス
従来のツールに比べて**10-100倍高速**

### インストール
```bash
# npm
npm install --save-dev @biomejs/biome

# pnpm
pnpm add -D @biomejs/biome

# yarn
yarn add -D @biomejs/biome
```

### 使用例
```bash
# フォーマット
biome format --write .

# リント
biome lint .

# チェック（リント＋フォーマット）
biome check .
```

### 設定ファイル
```json
{
  "$schema": "https://biomejs.dev/schemas/1.5.0/schema.json",
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  }
}
```

### 参考資料
- [Biome公式サイト](https://biomejs.dev/)
- [Space Jelly: Lint & Format JavaScript with Biome](https://spacejelly.dev/posts/lint-format-javascript-with-biome)

---

## 2. Ruff

### 概要
Rust製の超高速Python リンター＆コードフォーマッター。Flake8、isort等と互換性がある。

### 主な特徴

#### 驚異的な速度
- **10-100倍高速**: 既存ツールに比べて圧倒的に高速
- **サブ秒フィードバック**: 最大規模のコードベースでも1秒未満
- **リアルタイムフィードバック**: エディタ統合で即座にフィードバック

#### 包括的なルール
- **500以上のルール**: Flake8、isort、pyprojec などのルールをサポート
- **自動修正**: 多くのルールで自動修正が可能
- **カスタマイズ可能**: プロジェクトに応じた設定

#### ドロップイン互換性
- **Flake8互換**: 既存のFlake8設定をそのまま使用可能
- **isort互換**: importの並び替えをisortと同じように
- **Black互換**: Blackのフォーマットスタイルをサポート

### 対応するツール
Ruffは以下のツールを置き換え可能：
- Flake8（リンター）
- isort（import並び替え）
- Black（フォーマッター）
- pyupgrade（Python構文のアップグレード）
- autoflake（未使用インポート削除）
- pydocstyle（docstring検証）

### インストール
```bash
# pip
pip install ruff

# pipx
pipx install ruff

# uvx (推奨)
uvx ruff check .
```

### 使用例
```bash
# リント
ruff check .

# 自動修正
ruff check --fix .

# フォーマット
ruff format .

# ウォッチモード
ruff check --watch .
```

### 設定ファイル（pyproject.toml）
```toml
[tool.ruff]
line-length = 88
select = ["E", "F", "I"]
ignore = []

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
```

### エディタ統合
- VSCode
- PyCharm
- Vim/Neovim
- Sublime Text
- その他多数

### 参考資料
- [Astral: Ruff](https://astral.sh/ruff)
- [GitHub: astral-sh/ruff](https://github.com/astral-sh/ruff)

---

## 3. oxc (Oxidation Compiler)

### 概要
JavaScript Oxidation Compiler - Rust製のJavaScript言語向けの高性能ツール集。パーサー、リンター、フォーマッター、トランスパイラー、ミニファイアー、リゾルバーなどの必須コンパイラツールの構築に焦点。

### 主な特徴

#### 驚異的なパフォーマンス
- **50-100倍高速**: ESLintに比べて50-100倍高速（ルール数とCPUコア数による）
- **並列処理**: 複数CPUコアを活用
- **メモリ効率**: 最適化されたメモリ使用

#### 包括的なツールセット
- **Parser**: JavaScript/TypeScript パーサー
- **Linter**: 静的解析とリンティング
- **Formatter**: コードフォーマット（開発中）
- **Transpiler**: 最新のJS/TSを古いバージョンに変換
- **Minifier**: コード圧縮
- **Resolver**: モジュール解決

### 哲学
BiomeとRuffと同じ哲学を共有：
- JavaScriptツーリングをより高性能な言語で書き直す
- Rust製統一ツールチェインの構築
- 既存ツールとの互換性

### インストール（開発中）
```bash
# npm（リンターのみ現在利用可能）
npm install --save-dev oxlint

# cargo
cargo install oxlint
```

### 使用例
```bash
# リント
oxlint .

# 並列処理を指定
oxlint --threads 4 .
```

### 開発状況
- ✅ Parser: 完成
- ✅ Linter: 利用可能
- 🚧 Formatter: 開発中
- 🚧 Transpiler: 開発中
- 🚧 Minifier: 開発中
- 🚧 Resolver: 開発中

### 目標
以下のツールを統合して置き換える：
- Babel（トランスパイラー）
- ESLint（リンター）
- Prettier（フォーマッター）
- webpack/Rollup（バンドラー）
- Terser（ミニファイアー）

### パフォーマンス比較
```
ESLint:     ~10秒
oxc:        ~0.1秒（100倍高速）
```
※ルール数とコア数により変動

### 参考資料
- [oxc公式ドキュメント](https://oxc.rs/)
- [GitHub: oxc-project/oxc](https://github.com/oxc-project/oxc)

---

## ツール比較表

| 特徴 | Biome | Ruff | oxc |
|------|-------|------|-----|
| **対象言語** | JS/TS/JSON | Python | JS/TS |
| **リンター** | ✓ | ✓ | ✓ |
| **フォーマッター** | ✓ | ✓ | 🚧 |
| **トランスパイラー** | 🚧 | ✗ | 🚧 |
| **速度向上** | 10-100x | 10-100x | 50-100x |
| **並列処理** | ✓ | ✓ | ✓ |
| **自動修正** | ✓ | ✓ | ✓ |
| **エディタ統合** | ✓ | ✓ | 🚧 |
| **成熟度** | 安定 | 安定 | 開発中 |

✓: 利用可能、🚧: 開発中、✗: 非対応

## 採用のメリット

### 1. 劇的な速度向上
- CI/CDの時間短縮
- 開発者のフィードバックループの高速化
- リアルタイムのコード品質チェック

### 2. 統一されたツールチェイン
- 複数ツールの設定を1つに統合
- 一貫したエクスペリエンス
- 保守性の向上

### 3. 最新技術の活用
- Rustの安全性と速度
- モダンなアーキテクチャ
- 活発な開発コミュニティ

### 4. コスト削減
- CI/CDの実行時間削減
- 開発者の待ち時間削減
- クラウドコストの削減

## 移行ガイドライン

### Biomeへの移行（JavaScript/TypeScript）
```bash
# 既存の.eslintrc.jsonと.prettierrcを確認
# Biomeの設定に変換
npx @biomejs/biome migrate

# 既存ツールをアンインストール
npm uninstall eslint prettier

# Biomeをインストール
npm install --save-dev @biomejs/biome
```

### Ruffへの移行（Python）
```bash
# Ruffをインストール
pip install ruff

# 既存の設定を確認し、pyproject.tomlに統合
ruff check . --show-settings

# 既存ツールは段階的に削除
# flake8、isort、black等
```

### oxcへの移行
現在開発中のため、リンターのみ試験的に使用可能。ESLintと併用を推奨。

## CI/CDでの活用

### GitHub Actions例（Biome）
```yaml
name: Lint and Format
on: [push, pull_request]
jobs:
  biome:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx @biomejs/biome check .
```

### GitHub Actions例（Ruff）
```yaml
name: Lint
on: [push, pull_request]
jobs:
  ruff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: chartboost/ruff-action@v1
```

## 参考資料

### 公式サイト
- [Biome](https://biomejs.dev/)
- [Ruff](https://astral.sh/ruff)
- [oxc](https://oxc.rs/)

### GitHub
- [biomejs/biome](https://github.com/biomejs/biome)
- [astral-sh/ruff](https://github.com/astral-sh/ruff)
- [oxc-project/oxc](https://github.com/oxc-project/oxc)

### コミュニティ
- 活発なGitHubコミュニティ
- Discord/Slackチャンネル
- 定期的なアップデート

## まとめ

Rust製開発ツール（Biome、Ruff、oxc）は、従来のJavaScript/Python開発ツールを大幅に高速化し、統一されたツールチェインを提供する。CI/CDの高速化、開発者体験の向上、コスト削減など、多くのメリットがある。プロジェクトの規模が大きくなるほど、その効果は顕著になる。
