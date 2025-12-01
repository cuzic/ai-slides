# Slide Fact Checker Skill

## Description
スライドの内容をknowledgesファイルとWeb検索を使ってファクトチェックし、実際の機能制限や最新情報と照らし合わせて検証するスキルです。

## Instructions

あなたはスライド内容のファクトチェッカーです。以下の手順で徹底的に検証を行ってください。

### Phase 1: スライドの読み込みと理解

1. 指定されたスライドファイルを読み込む
2. 主要な主張・機能説明・デモ内容を抽出
3. 検証が必要な項目をリスト化（特に機能の可否、制限事項、最新情報）

### Phase 2: Knowledges による検証

以下のknowledgesファイルを参照して、スライド内容と照合：

#### Google Gemini 関連
- `knowledges/12-google-gemini-fundamentals.md` - Gemini基本機能
- `knowledges/13-google-gem-custom-ai.md` - Gem（カスタムAI）

#### Workspace 連携
- `knowledges/04-workspace-integration.md` - Workspace統合の詳細
- `knowledges/14-google-workspace-integration.md` - @指定機能の制約
- `knowledges/16-gemini-in-workspace-apps.md` - アプリ内Gemini

#### NotebookLM
- `knowledges/NotebookLM-01-fundamentals.md` - 基本機能
- `knowledges/NotebookLM-02-complete-workflows.md` - ワークフロー
- `knowledges/15-notebooklm-latest-features.md` - 最新機能

#### AI画像生成・図解
- `knowledges/17-ai-image-generation.md` - 画像生成（Nano Banana Pro等）
- `knowledges/18-diagram-and-document-generation.md` - 図解生成（Mermaid, SVG等）

### Phase 3: 重要な制約事項の確認

特に以下の点を重点的にチェック：

#### Workspace連携（@指定）の制限
```
【重要】knowledges/14-google-workspace-integration.md より:

@Gmail/@Docs/@Sheets/@Drive/@Calendar は READ操作のみ

✅ 可能: 検索、読み取り、分析、要約
❌ 不可能: 自動作成、自動送信、自動更新、自動転記
```

#### Gemの制約
```
【重要】knowledges/13-google-gem-custom-ai.md より:

- Gemini Advanced内でのみ動作
- 外部サイト埋め込み不可
- URL共有による社内配布が基本
```

#### 地域制限
```
【重要】knowledges/17-ai-image-generation.md より:

- Imagen 3（ImageFX）: 米国・豪州・NZ・ケニアのみ
- Nano Banana Pro（Gemini 3 Pro Image）: 全世界で利用可能（日本含む）
```

### Phase 4: Web検索による最新情報確認

以下のトピックについてWeb検索で最新情報を確認：

1. **機能のリリース状況**
   - 検索例: "Gemini Canvas feature 2025"
   - 検索例: "NotebookLM Deep Research 2025"
   - 検索例: "Google Workspace Gemini integration 2025"

2. **機能制限の変更**
   - 検索例: "@Gmail Gemini write operations 2025"
   - 検索例: "Gemini Workspace limitations 2025"

3. **最新のアップデート**
   - 検索例: "Nano Banana Pro Gemini 3 release date"
   - 検索例: "NotebookLM Audio Overview languages"

### Phase 5: 検証結果のレポート作成

以下の形式でレポートを作成：

```markdown
## ファクトチェック結果: [スライド名]

### ✅ 正確な内容（問題なし）

1. **[機能名]**
   - スライド記載: [内容]
   - 検証結果: 正確
   - 根拠: [knowledgesファイル名] または [Web検索結果]

### ⚠️ 不正確または誤解を招く内容

1. **[機能名/記述]**
   - スライド記載: [現在の内容]
   - 問題点: [何が問題か]
   - 正しい内容: [正確な情報]
   - 根拠: [knowledgesファイル名] または [Web検索結果]
   - 修正提案: [具体的な修正案]

### ❌ 明らかに誤った内容

1. **[機能名/記述]**
   - スライド記載: [現在の内容]
   - 問題点: [何が間違っているか]
   - 正しい内容: [正確な情報]
   - 根拠: [knowledgesファイル名] または [Web検索結果]
   - 修正提案: [具体的な修正案]

### 📝 デモ内容の実現可能性チェック

各デモスライドについて：

1. **[デモ名]**
   - デモ内容: [記載されている内容]
   - 実現可能性: ✅ 可能 / ⚠️ 部分的に可能 / ❌ 不可能
   - 理由: [根拠]
   - 推奨する修正: [ある場合]

### 🔍 追加の注意事項

- 受講者が誤解しやすい表現
- 追加すべき警告や注意書き
- 最新情報の反映が必要な箇所
```

### Phase 6: 優先度付けと修正推奨

検証結果を以下の優先度で分類：

**🔴 緊急（即修正必要）**
- 明らかに誤った機能説明
- 実現不可能なデモ内容
- 重大な制限事項の見落とし

**🟡 重要（修正推奨）**
- 誤解を招きやすい表現
- 古い情報（2024年以前）
- 不完全な注意書き

**🟢 軽微（改善推奨）**
- より正確な表現への変更
- 最新情報の追加
- 補足説明の追加

## Usage Examples

### 例1: 単一スライドの検証
```
/slide-fact-checker slides/topic-03-workspace-integration.md
```

### 例2: 全スライドの検証
```
/slide-fact-checker slides/*.md
```

### 例3: 特定トピックのみ検証
```
/slide-fact-checker slides/topic-01-google-gemini.md slides/topic-02-google-gem.md
```

## Important Notes

1. **Knowledgesを最優先**
   - Web検索よりknowledgesファイルの情報を優先
   - Knowledgesは2025年11月時点の正確な情報

2. **機能制限に特に注意**
   - READ/WRITE操作の区別
   - 地域制限
   - プラン制限（無料/有料）

3. **デモ内容の実現可能性**
   - 実際に画面で操作できるか
   - 制限事項により不可能な操作が含まれていないか

4. **最新性の確認**
   - 2025年11月以降の情報はWeb検索で補完
   - リリース日、アップデート情報の正確性

5. **受講者視点**
   - 誤解を招く表現がないか
   - 実際に試したときに「できない」と混乱しないか

## Output Format

必ず以下の構造でレポートを出力：

1. サマリー（問題数のカウント）
2. 詳細な検証結果
3. 優先度別の修正リスト
4. 推奨する修正アクション

## Error Handling

- スライドファイルが見つからない場合: エラーメッセージを表示
- Knowledgesファイルが見つからない場合: Web検索のみで検証
- Web検索が失敗した場合: Knowledgesのみで検証継続
