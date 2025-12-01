#!/usr/bin/env python3
"""
01, 02, 03 の全スライドを Nano Banana Pro で生成するスクリプト
"""

import os
import io
import re
import json
import time
from pathlib import Path
from google import genai
from google.genai import types
from PIL import Image

# API キー
API_KEY = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY または GEMINI_API_KEY を設定してください")

client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-3-pro-image-preview"

# 処理するファイル
FILES = [
    {"src": "src/01-intro.md", "name": "01-intro", "title": "入門編"},
    {"src": "src/02-design.md", "name": "02-design", "title": "設計編"},
    {"src": "src/03-implementation-refactoring.md", "name": "03-implementation", "title": "実装編"},
]

OUTPUT_DIR = Path("docs/slide-viewer/images")


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
        slide_clean = re.sub(r"<!--.*?-->", "", slide, flags=re.DOTALL)
        slide_clean = slide_clean.strip()

        if not slide_clean:
            continue

        # タイトルを抽出
        title_match = re.search(r"^#{1,3}\s+(.+)$", slide_clean, re.MULTILINE)
        title = title_match.group(1) if title_match else f"スライド {len(parsed_slides)+1}"

        # セクションタイトル判定（# または ## で始まる短いスライド）
        is_section = bool(re.match(r"^#{1,2}\s+", slide_clean)) and len(slide_clean.split("\n")) < 5

        parsed_slides.append({
            "index": len(parsed_slides) + 1,
            "title": title,
            "content": slide_clean,
            "is_section": is_section
        })

    return parsed_slides


def generate_slide_image(slide: dict, output_path: Path, file_title: str) -> bool:
    """スライドの画像を生成"""

    if slide["is_section"]:
        # セクションタイトル用のプロンプト
        prompt = f"""プロフェッショナルなセクションタイトルスライドを生成してください。

タイトル: {slide['title']}

デザイン要件:
- 16:9のアスペクト比
- 深い青（#1a237e）から紺（#0d47a1）へのグラデーション背景
- タイトルは白文字で中央に大きく配置
- モダンでテック感のあるデザイン
- シンプルで洗練された印象
- 装飾は最小限（抽象的な幾何学模様やラインのみ）
"""
    else:
        # 通常のコンテンツスライド用のプロンプト
        prompt = f"""プロフェッショナルなプレゼンテーションスライドを生成してください。

セクション: {file_title}
タイトル: {slide['title']}

内容:
{slide['content'][:1500]}

デザイン要件:
- 16:9のアスペクト比
- 青系の配色（#1a73e8がメインカラー）
- タイトルは上部に大きく配置
- 箇条書きは読みやすく整理
- 日本語テキストを正確に表示
- シンプルで洗練されたビジネススライド
- 表がある場合は見やすく整理
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
            )
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                pil_image = Image.open(io.BytesIO(part.inline_data.data))
                pil_image.save(output_path)
                return True

        return False

    except Exception as e:
        print(f"    エラー: {e}")
        return False


def main():
    all_slides_data = []

    for file_info in FILES:
        src_path = file_info["src"]
        name = file_info["name"]
        title = file_info["title"]

        print(f"\n{'='*60}")
        print(f"処理中: {src_path} ({title})")
        print(f"{'='*60}")

        # 出力ディレクトリ
        output_dir = OUTPUT_DIR / name
        output_dir.mkdir(parents=True, exist_ok=True)

        # スライドを解析
        slides = parse_markdown_slides(src_path)
        print(f"スライド数: {len(slides)}")

        file_slides = []

        for slide in slides:
            output_path = output_dir / f"slide_{slide['index']:03d}.png"

            # 既存ファイルがあればスキップ
            if output_path.exists():
                print(f"  [{slide['index']:3d}/{len(slides)}] スキップ（既存）: {slide['title'][:30]}")
                file_slides.append({
                    "index": slide["index"],
                    "title": slide["title"],
                    "image": f"images/{name}/slide_{slide['index']:03d}.png",
                    "is_section": slide["is_section"]
                })
                continue

            print(f"  [{slide['index']:3d}/{len(slides)}] 生成中: {slide['title'][:30]}...")

            if generate_slide_image(slide, output_path, title):
                print(f"    ✓ 完了")
                file_slides.append({
                    "index": slide["index"],
                    "title": slide["title"],
                    "image": f"images/{name}/slide_{slide['index']:03d}.png",
                    "is_section": slide["is_section"]
                })
            else:
                print(f"    ✗ 失敗")

            # レート制限対策
            time.sleep(1)

        all_slides_data.append({
            "name": name,
            "title": title,
            "slides": file_slides
        })

    # マニフェストJSONを生成
    manifest_path = Path("docs/slide-viewer/manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(all_slides_data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ マニフェスト生成: {manifest_path}")

    # 統計
    total_slides = sum(len(f["slides"]) for f in all_slides_data)
    print(f"\n合計スライド数: {total_slides}")


if __name__ == "__main__":
    main()
