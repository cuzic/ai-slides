# スライド自動修正スキル

このスキルは、Marpスライドの問題を自動修正します。

## いつ使うか

- 新規スライドファイルを作成した後（CSS追加）
- オーバーフローが検出された後（自動フォント調整）
- 「スライドを修正して」「オーバーフローを直して」と依頼された時
- 複数スライドを一括で修正したい時

## 使用するスクリプト

### 1. CSS追加（add-css）

フォントサイズバリエーションとレイアウトCSSを追加します。

```bash
# 単一ファイル
python scripts/fix-slides.py add-css src/01-intro.md

# ディレクトリ全体
python scripts/fix-slides.py add-css src/
```

**追加されるCSS:**
- フォントサイズ: `font-large`, `font-medium`, `font-small`, `font-xsmall`, `font-xxsmall`
- レイアウト: `.columns`, `.columns-3`, `.compact-list`
- ボックス: `.highlight-box`, `.warning-box`, `.key-message`, `.checklist`

### 2. オーバーフロー自動修正（auto-font）

オーバーフロー量に応じて適切なフォントクラスを自動適用します。

```bash
# 単一ファイル
python scripts/fix-slides.py auto-font src/01-intro.md

# ディレクトリ全体
python scripts/fix-slides.py auto-font src/
```

**適用ルール:**
| オーバーフロー量 | 適用クラス |
|----------------|----------|
| 50px未満 | `font-small` |
| 50-150px | `font-xsmall` |
| 150px以上 | `font-xxsmall` |

### 3. 特定スライドにクラス追加（add-font-class）

```bash
python scripts/fix-slides.py add-font-class src/01-intro.md 5 font-small
```

## 典型的なワークフロー

### 新規スライド作成時

```bash
# 1. スライドを作成/編集

# 2. CSSを追加（初回のみ）
python scripts/fix-slides.py add-css src/01-intro.md

# 3. オーバーフローチェック
bun scripts/check-slides.js overflow src/01-intro.md

# 4. 問題があれば自動修正
python scripts/fix-slides.py auto-font src/01-intro.md

# 5. 再チェック
bun scripts/check-slides.js overflow src/01-intro.md
```

### 全ファイル一括修正

```bash
# 1. 全ファイルにCSS追加
python scripts/fix-slides.py add-css src/

# 2. 全ファイルのオーバーフローチェック
bun scripts/check-slides.js overflow src/

# 3. 全ファイルの自動修正
python scripts/fix-slides.py auto-font src/

# 4. 再チェック
bun scripts/check-slides.js overflow src/
```

## スライドでのクラス使用例

### フォントサイズ

```markdown
---

<!-- _class: font-small -->

### 情報量の多いスライド

- 項目1
- 項目2
- 項目3
...
```

### 複数クラスの組み合わせ

```markdown
---

<!-- _class: font-small compact-list -->

### コンパクトなリスト

- 項目が多い場合
- このように組み合わせる
```

### レイアウトクラス

```markdown
---

### 2カラムレイアウト

<div class="columns">
<div>

**左カラム**
- 項目1
- 項目2

</div>
<div>

**右カラム**
- 項目A
- 項目B

</div>
</div>
```

### ボックススタイル

```markdown
---

### ハイライトボックス

<div class="highlight-box">

**重要ポイント**: ここに強調したい内容を記載

</div>

<div class="warning-box">

**注意**: 警告メッセージ

</div>
```

## 出力例

### add-css

```
==================================================
CSS追加
==================================================

  ✓ 01-intro.md: CSSを追加しました
  ✓ 02-design.md: 既に追加済み
  ✓ 03-implementation.md: CSSを追加しました

✅ 2/3 ファイルを更新しました
```

### auto-font

```
==================================================
オーバーフロー自動修正
==================================================

📄 01-intro.md
  ✓ 01-intro.md: オーバーフローなし

📄 02-design.md
    スライド 15: 120px → font-xsmall
    スライド 23: 45px → font-small
  → 2 スライドを修正

==================================================
✅ 合計 2 スライドを修正しました
```

## 注意点

- `auto-font` を実行する前に `add-css` でCSSを追加しておく必要があります
- 自動修正後も再度オーバーフローチェックを行い、問題が解決したか確認してください
- フォントを小さくしても解決しない場合は、コンテンツの削減やスライド分割を検討してください
