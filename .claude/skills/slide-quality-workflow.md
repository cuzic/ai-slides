# スライド品質管理ワークフロー

このスキルは、スライド作成から品質チェックまでの一連のワークフローを提供します。

## いつ使うか

- スライドの作成・編集が完了した時
- 「スライドの品質をチェックして」と依頼された時
- プレゼンテーション前の最終確認
- CI/CDパイプラインでの品質ゲート

## 品質チェックの流れ

```
┌─────────────────────────────────────────┐
│  1. CSS追加（初回のみ）                  │
│     python fix-slides.py add-css        │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  2. オーバーフローチェック               │
│     bun check-slides.js overflow        │
└─────────────────────────────────────────┘
                    ↓
        ┌─────────┴─────────┐
        │ オーバーフロー？   │
        └─────────┬─────────┘
           Yes    │    No
            ↓     │     ↓
┌───────────────┐ │ ┌───────────────┐
│ 自動修正      │ │ │ 完了！        │
│ auto-font     │ │ └───────────────┘
└───────────────┘ │
            ↓     │
┌───────────────┐ │
│ 再チェック    │ │
└───────────────┘ │
            ↓     │
        ┌─────────┴─────────┐
        │ まだ問題あり？     │
        └─────────┬─────────┘
           Yes    │    No
            ↓     │     ↓
┌───────────────┐ │ ┌───────────────┐
│ 手動対応      │ │ │ 完了！        │
│ - コンテンツ削減│ │ └───────────────┘
│ - スライド分割 │ │
└───────────────┘ │
```

## 実行コマンド一覧

### 基本ワークフロー

```bash
# Step 1: CSS追加（新規ファイルの場合）
python scripts/fix-slides.py add-css src/

# Step 2: オーバーフローチェック
bun scripts/check-slides.js overflow src/

# Step 3: 自動修正（問題があれば）
python scripts/fix-slides.py auto-font src/

# Step 4: 再チェック
bun scripts/check-slides.js overflow src/

# Step 5: リンクチェック（ビルド後）
./build-html.sh
bun scripts/check-slides.js links dist/
```

### 単一ファイルのワークフロー

```bash
FILE=src/02-design.md

# CSS追加
python scripts/fix-slides.py add-css $FILE

# チェック→修正→再チェック
bun scripts/check-slides.js overflow $FILE
python scripts/fix-slides.py auto-font $FILE
bun scripts/check-slides.js overflow $FILE
```

## 品質基準

### オーバーフロー

| 状態 | 基準 | 対応 |
|------|------|------|
| ✅ OK | オーバーフローなし | そのまま |
| ⚠️ 軽度 | 50px未満 | font-small適用 |
| ⚠️ 中度 | 50-150px | font-xsmall適用 |
| ❌ 重度 | 150px以上 | font-xxsmall + コンテンツ削減検討 |

### コンテンツ量の目安

| 要素 | 推奨 | 最大 |
|------|------|------|
| 箇条書き項目 | 5-7項目 | 10項目 |
| 階層の深さ | 2階層 | 3階層 |
| 1項目の文字数 | 30文字 | 50文字 |

## 手動対応が必要なケース

### 1. font-xxsmallでも解決しない

```markdown
# Before: 情報過多
### スライドタイトル
- 項目1の詳細な説明文がここに入ります
- 項目2の詳細な説明文がここに入ります
- 項目3の詳細な説明文がここに入ります
- 項目4の詳細な説明文がここに入ります
- 項目5の詳細な説明文がここに入ります
- 項目6の詳細な説明文がここに入ります
- 項目7の詳細な説明文がここに入ります

# After: 簡潔に
### スライドタイトル
- 項目1: 要点のみ
- 項目2: 要点のみ
- 項目3: 要点のみ
- 項目4: 要点のみ
- 項目5: 要点のみ
```

### 2. スライド分割

```markdown
# Before: 1スライドに詰め込み
### すべての機能

- 機能A: 説明...
- 機能B: 説明...
- 機能C: 説明...
- 機能D: 説明...
- 機能E: 説明...
- 機能F: 説明...

---

# After: 2スライドに分割
### 主要機能（1/2）

- 機能A: 説明...
- 機能B: 説明...
- 機能C: 説明...

---

### 追加機能（2/2）

- 機能D: 説明...
- 機能E: 説明...
- 機能F: 説明...
```

### 3. 2カラムレイアウトの活用

```markdown
---

### 比較表

<div class="columns">
<div>

**メリット**
- 高速
- 簡単
- 安価

</div>
<div>

**デメリット**
- 制限あり
- サポート限定

</div>
</div>
```

## エラー対応

### Playwrightエラー

```bash
# ブラウザがインストールされていない場合
bunx playwright install chromium
```

### CSSが適用されない

```bash
# CSSが追加されているか確認
grep -l "font-xxsmall" src/*.md

# 追加されていなければ
python scripts/fix-slides.py add-css src/
```

### スクリプトが見つからない

```bash
# scriptsディレクトリから実行していることを確認
ls scripts/check-slides.js scripts/fix-slides.py
```

## CI/CD統合例

```yaml
# GitHub Actions example
- name: Check slide quality
  run: |
    bun scripts/check-slides.js overflow src/

- name: Build slides
  run: ./build-html.sh

- name: Check links
  run: bun scripts/check-slides.js links dist/
```
