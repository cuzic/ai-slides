# Gemini Image Generation API (Nano Banana / Nano Banana Pro)

## モデル名

| モデル | API名 | 特徴 |
|--------|-------|------|
| Nano Banana | `gemini-2.5-flash-image` | 高速、一般的な画像生成向け |
| Nano Banana Pro | `gemini-3-pro-image-preview` | 高品質、プロフェッショナル用途向け |

## インストール

```bash
uv add google-genai pillow
```

## 環境変数

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

## 基本的な使い方

### セットアップ

```python
from google import genai
from google.genai import types
from PIL import Image
import io
import os

client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
```

### テキストから画像生成

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",  # または "gemini-3-pro-image-preview"
    contents=["プロンプトテキスト"],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE']
    )
)

for part in response.parts:
    if part.inline_data is not None:
        image = Image.open(io.BytesIO(part.inline_data.data))
        image.save("output.png")
```

### 高解像度・アスペクト比指定（Nano Banana Pro）

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=["プロンプトテキスト"],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE'],
        image_config=types.ImageConfig(
            aspect_ratio="16:9",  # 1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
            image_size="2K"       # 1K, 2K, 4K
        )
    )
)
```

### 画像編集（既存画像 + テキスト）

```python
from PIL import Image

# 既存画像を読み込み
input_image = Image.open("input.png")

response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents=["編集指示テキスト", input_image],
    config=types.GenerateContentConfig(
        response_modalities=['IMAGE']
    )
)
```

### マルチターン会話（反復的な改善）

```python
chat = client.chats.create(
    model="gemini-3-pro-image-preview",
    config=types.GenerateContentConfig(
        response_modalities=['TEXT', 'IMAGE']
    )
)

# 初回生成
response = chat.send_message("最初のプロンプト")

# 改善指示
response = chat.send_message("背景をもっと青くして")
```

## 設定オプション

### 解像度 (image_size)
- `1K` - デフォルト
- `2K` - 高解像度
- `4K` - 最高解像度（Nano Banana Pro のみ）

### アスペクト比 (aspect_ratio)
- `1:1` - 正方形
- `16:9` - ワイドスクリーン（プレゼンテーション向け）
- `9:16` - 縦長（モバイル向け）
- `4:3`, `3:4`, `2:3`, `3:2`, `4:5`, `5:4`, `21:9`

## プロンプトのベストプラクティス

### 良い例（説明的な文章）
```
青を基調としたモダンなビジネススライド。
タイトル「AI駆動開発の5-STEPワークフロー」が上部に大きく表示され、
下には5つのステップが左から右に矢印でつながっている。
各ステップには番号とアイコンが含まれる。
背景はグラデーションで、プロフェッショナルな印象。
```

### 避けるべき例（キーワードの羅列）
```
スライド, 青, ビジネス, 5ステップ, 矢印
```

## 参考リンク

- [Gemini API 画像生成ドキュメント](https://ai.google.dev/gemini-api/docs/image-generation)
- [Google AI Studio](https://aistudio.google.com/)
