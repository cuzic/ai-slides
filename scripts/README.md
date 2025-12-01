# スクリプト一覧

Marpスライド作成・検証に使用するスクリプト集です。

## 必要なツール

- **bun**: JavaScript/TypeScriptランタイム
- **playwright**: ブラウザ自動化（オーバーフロー検出に使用）

```bash
# playwrightのインストール
bun add playwright
```

## スクリプト

### check-slides.js

スライドの検証を行う統合スクリプトです。

#### オーバーフロー検出

Playwrightを使って実際にレンダリングし、スライドのはみ出しを検出します。

```bash
# 単一ファイル
bun scripts/check-slides.js overflow src/01-intro.md

# ディレクトリ内の全.mdファイル
bun scripts/check-slides.js overflow src/
```

#### リンク切れ検出

ビルド後のHTMLファイル内のリンク切れを検出します。

```bash
bun scripts/check-slides.js links dist/
```

### fix-slides.py

スライドの自動修正を行う統合スクリプトです。

#### CSS追加

フォントサイズバリエーションとレイアウトCSSを追加します。

```bash
# 単一ファイル
python scripts/fix-slides.py add-css src/01-intro.md

# ディレクトリ内の全.mdファイル
python scripts/fix-slides.py add-css src/
```

追加されるCSS:
- `font-large`, `font-medium`, `font-small`, `font-xsmall`, `font-xxsmall`
- `.columns`, `.columns-3`, `.compact-list`
- `.highlight-box`, `.warning-box`, `.key-message`, `.checklist`

#### オーバーフロー自動修正

オーバーフロー量に応じて適切なフォントクラスを自動適用します。

```bash
python scripts/fix-slides.py auto-font src/
```

適用ルール:
- 50px未満 → `font-small`
- 50-150px → `font-xsmall`
- 150px以上 → `font-xxsmall`

#### 特定スライドにクラス追加

```bash
python scripts/fix-slides.py add-font-class src/01-intro.md 5 font-small
```

## 多数のスクリプトが必要だった理由

元のプロジェクト（keiz-2026）では、以下の理由で多数のスクリプトが存在しました：

1. **段階的な対応**: オーバーフロー量に応じてfont-small→xsmall→xxsmallと段階的に適用
2. **CSS追加のインクリメンタル化**: 既存CSSとの互換性を保ちながら追加
3. **ハードコードされたパス**: プロジェクト固有の`slides/topic-*.md`等が直接記述
4. **個別対応の必要性**: 特定スライドだけ修正するケースが多い

### 汎用化のポイント

1. **パスの引数化**: ファイルまたはディレクトリを引数で指定
2. **サブコマンド化**: 1つのスクリプトに複数機能を統合
3. **CSSの統合**: 複数のadd-font-*.pyを1つのadd-cssコマンドに
4. **自動判定**: オーバーフロー量から適切なクラスを自動選択

## ビルド

### build-html.sh（プロジェクトルート）

MarpスライドをHTMLにビルドします。

```bash
./build-html.sh
```
