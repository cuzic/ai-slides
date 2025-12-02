#!/usr/bin/env python3
"""
マークダウンファイルからスピーカーノートを抽出してmanifest.jsonを更新するスクリプト
"""

import re
import json
from pathlib import Path

# 処理するファイル
FILES = [
    {"src": "src/01-intro.md", "name": "01-intro", "title": "入門編"},
    {"src": "src/02-design.md", "name": "02-design", "title": "設計編"},
    {"src": "src/03-implementation-refactoring.md", "name": "03-implementation", "title": "実装編"},
]

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

        # セクションタイトル判定
        is_section = bool(re.match(r"^#{1,2}\s+", slide_clean)) and len(slide_clean.split("\n")) < 5

        # スピーカーノート用にコンテンツを整形
        # タイトル行を除去
        notes_content = re.sub(r"^#{1,3}\s+.+$", "", slide_clean, flags=re.MULTILINE)
        notes_content = notes_content.strip()

        # 箇条書きをテキストに変換
        notes_lines = []
        for line in notes_content.split("\n"):
            line = line.strip()
            if line.startswith("- "):
                # インデントレベルを判定
                original_line = [l for l in notes_content.split("\n") if line in l][0] if notes_content else ""
                indent = len(original_line) - len(original_line.lstrip())
                prefix = "  " * (indent // 2) if indent > 0 else ""
                notes_lines.append(prefix + "・" + line[2:])
            elif line.startswith("**") and line.endswith("**"):
                notes_lines.append("【" + line[2:-2] + "】")
            elif line:
                notes_lines.append(line)

        notes = "\n".join(notes_lines)

        parsed_slides.append({
            "index": len(parsed_slides) + 1,
            "title": title,
            "is_section": is_section,
            "notes": notes if notes else f"（{title}）"
        })

    return parsed_slides


def main():
    all_slides_data = []

    for file_info in FILES:
        src_path = file_info["src"]
        name = file_info["name"]
        title = file_info["title"]

        print(f"処理中: {src_path}")

        slides = parse_markdown_slides(src_path)
        print(f"  スライド数: {len(slides)}")

        file_slides = []
        for slide in slides:
            file_slides.append({
                "index": slide["index"],
                "title": slide["title"],
                "image": f"images/{name}/slide_{slide['index']:03d}.png",
                "is_section": slide["is_section"],
                "notes": slide["notes"]
            })

        all_slides_data.append({
            "name": name,
            "title": title,
            "slides": file_slides
        })

    # 削除対象のスライドを除外（manifest.jsonから読み込んで同期）
    # 今日の学習内容、3つのセッション、AI駆動開発で大切なこと(1/2)(2/2)、質問タイム
    removed_titles = [
        "今日の学習内容",
        "3つのセッション",
        "AI駆動開発で大切なこと（1/2）",
        "AI駆動開発で大切なこと（2/2）",
        "質問タイム"
    ]

    for section in all_slides_data:
        section["slides"] = [s for s in section["slides"] if s["title"] not in removed_titles]

    # マニフェストJSONを生成
    manifest_path = Path("docs/slide-viewer/manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(all_slides_data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ マニフェスト更新: {manifest_path}")

    # 統計
    total_slides = sum(len(f["slides"]) for f in all_slides_data)
    print(f"合計スライド数: {total_slides}")


if __name__ == "__main__":
    main()
