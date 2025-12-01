#!/usr/bin/env python3
"""
Nano Banana Pro (Gemini 3 Pro Image) を使ってスライド画像を生成するスクリプト

使用前に:
1. uv add google-genai pillow
2. 環境変数 GOOGLE_API_KEY を設定

実行:
    uv run python generate_slides.py
"""

import os
import re
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image
import io

# API キーの設定
API_KEY = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")

client = genai.Client(api_key=API_KEY)

# Nano Banana Pro (Gemini 3 Pro Image) モデル
MODEL_NAME = "gemini-3-pro-image-preview"


def parse_markdown_slides(filepath: str) -> list[dict]:
    """Markdownファイルからスライドを抽出する"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # フロントマターを除去
    content = re.sub(r"^---\nmarp:.*?---\n", "", content, flags=re.DOTALL)

    # スタイルブロックを除去
    content = re.sub(r"<style>.*?</style>", "", content, flags=re.DOTALL)

    # スライドを分割
    slides = content.split("\n---\n")

    parsed_slides = []
    for i, slide in enumerate(slides):
        # コメントを除去
        slide = re.sub(r"<!--.*?-->", "", slide, flags=re.DOTALL)
        slide = slide.strip()

        if not slide:
            continue

        # タイトルを抽出
        title_match = re.search(r"^#{1,3}\s+(.+)$", slide, re.MULTILINE)
        title = title_match.group(1) if title_match else f"スライド {i+1}"

        parsed_slides.append({
            "index": len(parsed_slides) + 1,
            "title": title,
            "content": slide
        })

    return parsed_slides


def generate_slide_image(slide: dict, output_dir: Path) -> str:
    """スライドの内容を元に画像を生成する"""

    prompt = f"""あなたはプレゼンテーションスライドのデザイナーです。
以下の内容を元に、プロフェッショナルなスライド画像を生成してください。

タイトル: {slide['title']}

内容:
{slide['content']}

要件:
- 16:9のアスペクト比
- 日本語のテキストを含める
- シンプルで読みやすいデザイン
- 青系の配色でモダンなビジネススライド風
- 箇条書きは読みやすく整理
- タイトルは大きく目立つように
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(
                    aspect_ratio="16:9",
                    image_size="2K"
                )
            )
        )

        # 画像を保存
        for part in response.parts:
            if part.inline_data is not None:
                image = Image.open(io.BytesIO(part.inline_data.data))
                output_path = output_dir / f"slide_{slide['index']:03d}.png"
                image.save(output_path)
                print(f"✓ 生成完了: {output_path}")
                return str(output_path)

        print(f"✗ 画像なし: {slide['title']}")
        return ""

    except Exception as e:
        print(f"✗ エラー: {slide['title']} - {e}")
        return ""


def main():
    # 出力ディレクトリ
    output_dir = Path("generated_slides")
    output_dir.mkdir(exist_ok=True)

    # Markdownファイル一覧
    src_dir = Path("src")
    md_files = [
        "01-intro.md",
        "02-design.md",
        "03-implementation-refactoring.md",
        "04-integration.md"
    ]

    for md_file in md_files:
        filepath = src_dir / md_file
        if not filepath.exists():
            print(f"ファイルが見つかりません: {filepath}")
            continue

        print(f"\n{'='*50}")
        print(f"処理中: {md_file}")
        print(f"{'='*50}")

        # サブディレクトリ作成
        file_output_dir = output_dir / md_file.replace(".md", "")
        file_output_dir.mkdir(exist_ok=True)

        # スライドを解析
        slides = parse_markdown_slides(str(filepath))
        print(f"スライド数: {len(slides)}")

        # 各スライドの画像を生成
        for slide in slides:
            print(f"\n[{slide['index']}/{len(slides)}] {slide['title']}")
            generate_slide_image(slide, file_output_dir)


if __name__ == "__main__":
    main()
