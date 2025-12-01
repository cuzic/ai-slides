# Nano Banana Pro スライド画像生成スキル

このスキルは Gemini の Nano Banana Pro (gemini-3-pro-image-preview) を使用して、
Markdownスライドの内容を元にプロフェッショナルなスライド画像を生成します。

## 前提条件

- `uv add google-genai pillow` でライブラリがインストール済み
- 環境変数 `GOOGLE_API_KEY` が設定済み
- ドキュメント: `docs/external-api/gemini-image-generation.md` を参照

## 使用方法

### 単一スライドの画像生成

```python
from google import genai
from google.genai import types
from PIL import Image
import io
import os

client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

def generate_slide_image(title: str, content: str, output_path: str):
    """スライドの画像を生成する"""

    prompt = f"""プロフェッショナルなプレゼンテーションスライドを生成してください。

タイトル: {title}

内容:
{content}

デザイン要件:
- 16:9のアスペクト比
- 日本語テキストを正確に表示
- 青を基調としたモダンなビジネススタイル
- タイトルは上部に大きく配置
- 箇条書きは読みやすく整理
- シンプルで洗練されたデザイン
"""

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=['IMAGE'],
            image_config=types.ImageConfig(
                aspect_ratio="16:9",
                image_size="2K"
            )
        )
    )

    for part in response.parts:
        if part.inline_data is not None:
            image = Image.open(io.BytesIO(part.inline_data.data))
            image.save(output_path)
            return True
    return False
```

### バッチ生成（複数スライド）

```python
import re
from pathlib import Path

def parse_markdown_slides(filepath: str) -> list[dict]:
    """Markdownファイルからスライドを抽出"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # フロントマターとスタイルを除去
    content = re.sub(r"^---\nmarp:.*?---\n", "", content, flags=re.DOTALL)
    content = re.sub(r"<style>.*?</style>", "", content, flags=re.DOTALL)

    slides = content.split("\n---\n")
    parsed = []

    for i, slide in enumerate(slides):
        slide = re.sub(r"<!--.*?-->", "", slide, flags=re.DOTALL).strip()
        if not slide:
            continue

        title_match = re.search(r"^#{1,3}\s+(.+)$", slide, re.MULTILINE)
        title = title_match.group(1) if title_match else f"スライド {i+1}"

        parsed.append({"index": len(parsed) + 1, "title": title, "content": slide})

    return parsed

def generate_all_slides(md_file: str, output_dir: str):
    """Markdownファイルの全スライドを画像生成"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    slides = parse_markdown_slides(md_file)

    for slide in slides:
        output_path = f"{output_dir}/slide_{slide['index']:03d}.png"
        print(f"生成中: {slide['title']}")
        generate_slide_image(slide['title'], slide['content'], output_path)
```

## 実行例

```bash
# 環境変数を設定
export GOOGLE_API_KEY="your-api-key"

# スクリプトを実行
uv run python generate_slides.py
```

## プロンプトのカスタマイズ

スライドのスタイルを変更する場合は、プロンプト内のデザイン要件を調整:

- **配色**: 「青を基調」→「緑を基調」「モノクロ」など
- **スタイル**: 「ビジネス」→「カジュアル」「テック系」など
- **フォント**: 「シンプル」→「太字」「手書き風」など

## トラブルシューティング

### API キーエラー
```
環境変数 GOOGLE_API_KEY が設定されているか確認
echo $GOOGLE_API_KEY
```

### レート制限
```
生成間隔を空ける (time.sleep(2) など)
```

### 日本語テキストが正しく表示されない
```
プロンプトに「日本語テキストを正確に表示」を明示的に追加
```
