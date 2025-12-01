# スライドオーバーフロー検出スキル

このスキルは、Marpスライドのオーバーフロー（はみ出し）を検出し、修正を支援します。

## いつ使うか

- スライドを新規作成・編集した後
- ビルド前の品質チェック
- 「スライドがはみ出ていないか確認して」と依頼された時
- スライドの内容が多く、表示に問題がありそうな時

## 使用するスクリプト

```bash
# 単一ファイルのチェック
bun scripts/check-slides.js overflow src/01-intro.md

# ディレクトリ全体のチェック
bun scripts/check-slides.js overflow src/
```

## 出力の読み方

### 正常な場合
```
📄 01-intro.md
   ✅ すべてOK (45スライド)
```

### オーバーフローがある場合
```
📄 01-intro.md
   ❌ スライド 5: 150px オーバー
      クラス: font-small
   ❌ スライド 12: 80px オーバー
```

## オーバーフロー検出後の対応

### 1. 自動修正を試す

```bash
python scripts/fix-slides.py auto-font src/01-intro.md
```

これにより、オーバーフロー量に応じて適切なフォントクラスが自動適用されます：
- 50px未満 → `font-small`
- 50-150px → `font-xsmall`
- 150px以上 → `font-xxsmall`

### 2. 手動でクラスを追加

スライドの先頭に以下を追加：

```markdown
---

<!-- _class: font-small -->

### スライドタイトル
```

### 3. コンテンツを削減

- 箇条書きの項目数を減らす
- 詳細な説明を別スライドに分割
- 不要な装飾や説明を削除

### 4. スライドを分割

1つのスライドに情報が多すぎる場合は、2つ以上に分割を検討。

## フォントクラスの効果

| クラス | フォントサイズ | 用途 |
|--------|--------------|------|
| font-large | 28px | タイトルスライド、キーメッセージ |
| font-medium | 22px | 通常より少し小さく |
| font-small | 20px | 軽度のオーバーフロー対応 |
| font-xsmall | 18px | 中程度のオーバーフロー対応 |
| font-xxsmall | 16px | 重度のオーバーフロー対応 |

## ワークフロー例

```bash
# 1. 編集後にチェック
bun scripts/check-slides.js overflow src/02-design.md

# 2. オーバーフローがあれば自動修正
python scripts/fix-slides.py auto-font src/02-design.md

# 3. 再チェックして確認
bun scripts/check-slides.js overflow src/02-design.md

# 4. まだオーバーフローがあれば手動対応
#    - コンテンツ削減
#    - スライド分割
```

## 注意点

- CSSが追加されていない場合、先に `add-css` を実行してください
- オーバーフロー検出にはPlaywrightが必要です（`bun add playwright`）
- 実際のブラウザでレンダリングして検出するため、CSS適用後の正確な結果が得られます
