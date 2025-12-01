---
name: link-checker
description: Check for broken links in GitHub Pages deployment - validates all links in index.html against built files in dist/
tags: [marp, github-pages, validation, links]
---

# Link Checker Skill

このスキルは、GitHub Pages デプロイメントのリンク切れをチェックします。

## 主な機能

1. **index.html のリンク抽出**: すべての `.html` リンクを検出
2. **dist/ ディレクトリ検証**: ビルドされたファイルの存在確認
3. **404 URL 検出**: リンク切れが発生する URL を網羅的にリスト
4. **未リンクファイル検出**: dist/ にあるが index.html からリンクされていないファイル

## 使用方法

### 基本的な使い方

```bash
bun run check-links.js
```

### 出力例

```
📊 GitHub Pages リンクチェック開始

🔍 index.html から 9 個のリンクを検出

📁 dist/ 内の HTML ファイル: 10 個

  ✅ 00-overview-introduction.html
  ✅ topic-01-google-gemini.html
  ❌ topic-09-missing.html - ファイルが存在しません
  ...

============================================================
📊 チェック結果サマリー
============================================================
✅ OK: 8 個
❌ NG: 1 個
⚠️  未リンク: 1 個

🔧 修正が必要なファイル:
  - topic-09-missing.html (元ファイル: slides/topic-09-missing.md)

🌐 GitHub Pages URL:
  トップページ: https://cuzic.github.io/keiz-2026/

❌ 404 エラーが発生する URL:
  https://cuzic.github.io/keiz-2026/topic-09-missing.html
```

## スキルの実行フロー

ユーザーがこのスキルを呼び出したとき、以下の手順を実行します:

### ステップ 1: リンクチェック実行

```bash
bun run check-links.js
```

### ステップ 2: 結果の分析

- **NG が 0 個**: ✅ すべてのリンクが正常 → 成功メッセージを表示
- **NG が 1 個以上**: ⚠️ リンク切れを検出 → 詳細分析へ

### ステップ 3: 問題の特定（NG がある場合）

以下を確認:

1. **index.html のリンクが誤っている場合**
   - index.html を修正
   - 該当する `<a href="...">` タグを確認

2. **ビルドが実行されていない場合**
   - `.github/workflows/marp.yml` を確認
   - ビルド対象のパターンを確認（例: `slides/*.md` vs `slides/topic-*.md`）
   - 欠落しているファイルを手動ビルド

3. **元の Markdown ファイルが存在しない場合**
   - `slides/` ディレクトリ内のファイル一覧を確認
   - 必要に応じてファイルを作成または index.html からリンクを削除

### ステップ 4: 修正の実行

#### パターン A: ワークフローの修正が必要

```yaml
# .github/workflows/marp.yml
- name: Convert slides to HTML
  run: |
    for file in slides/*.md; do  # topic-*.md から *.md に変更
      if [ -f "$file" ]; then
        filename=$(basename "$file" .md)
        marp "$file" --html --allow-local-files -o "dist/${filename}.html"
      fi
    done
```

修正後:
```bash
git add .github/workflows/marp.yml
git commit -m "Fix: include all slides in GitHub Pages build"
git push
```

#### パターン B: 手動ビルドが必要

```bash
# 欠落しているファイルをビルド
bun x @marp-team/marp-cli@latest slides/00-overview-introduction.md \
  --html --allow-local-files -o dist/00-overview-introduction.html

# index.html をコピー
cp index.html dist/

# 再度チェック
bun run check-links.js
```

#### パターン C: index.html の修正が必要

```html
<!-- 削除または修正 -->
<a href="topic-09-missing.html" class="topic-card">
  ...
</a>
```

### ステップ 5: GitHub Pages への反映確認

```bash
# 最新の GitHub Actions 実行状況を確認
gh run list --limit 1

# ビルドログを確認（エラーがある場合）
gh run view --log

# デプロイ完了後、実際の URL にアクセスして確認
```

## よくある問題と解決方法

### 問題 1: 00-overview-introduction.html が 404

**原因**: ワークフローが `slides/topic-*.md` のみをビルド

**解決**:
```yaml
# slides/topic-*.md → slides/*.md に変更
for file in slides/*.md; do
```

### 問題 2: index.html 内のリンクが古い

**原因**: ファイル名変更やファイル削除後に index.html を更新していない

**解決**:
```bash
# 現在の slides/ 内のファイル一覧を確認
ls slides/*.md

# index.html を実際のファイルに合わせて更新
```

### 問題 3: dist/ にファイルがあるが index.html からリンクされていない

**原因**: 新しいスライドを追加したが index.html を更新していない

**解決**:
```html
<!-- index.html に追加 -->
<a href="topic-09-new-feature.html" class="topic-card">
  <div class="topic-number">Topic 9</div>
  <div class="topic-title">新機能</div>
  <div class="topic-description">
    新機能の説明<br>
    ⏱️ 60分 | 📊 15スライド
  </div>
</a>
```

## チェックリスト

リンク切れを修正する際、以下を確認:

- [ ] `bun run check-links.js` が NG: 0 を表示
- [ ] GitHub Actions のビルドが成功
- [ ] 実際の GitHub Pages URL にアクセスして全リンクが動作
- [ ] `slides/` 内のすべての `.md` ファイルがビルド対象に含まれている
- [ ] `index.html` のリンクが最新のファイル構成と一致

## 自動化の提案

### GitHub Actions への統合（オプション）

```yaml
# .github/workflows/marp.yml に追加
- name: Check for broken links
  run: |
    npm install -g bun
    bun run check-links.js
```

これにより、デプロイ前に自動的にリンクチェックが実行されます。

## トラブルシューティング

### bun がインストールされていない

```bash
# mise を使用してインストール
mise install bun

# または直接インストール
curl -fsSL https://bun.sh/install | bash
```

### check-links.js が実行できない

```bash
# 実行権限を付与
chmod +x check-links.js

# 直接 bun で実行
bun check-links.js
```

## 関連ツール

- **check-overflow.js**: スライドのオーバーフローチェック
- **check-all-overflow.sh**: 全スライドの一括オーバーフローチェック
- **.github/workflows/marp.yml**: GitHub Pages デプロイワークフロー

## まとめ

このスキルを使用することで:

1. ✅ リンク切れを自動検出
2. ✅ 404 エラーが発生する URL を事前に把握
3. ✅ デプロイ前に問題を修正
4. ✅ GitHub Pages の信頼性を向上

定期的に実行して、常にすべてのリンクが正常に動作することを確認してください。
