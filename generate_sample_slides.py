#!/usr/bin/env python3
"""
01-intro.md から4つのスライドをピックアップして画像生成
"""

import os
import io
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

# 生成するスライド
SLIDES = [
    {
        "filename": "slide_01_title.png",
        "prompt": """プロフェッショナルなプレゼンテーションのタイトルスライドを生成してください。

タイトル: AI駆動開発セミナー Day 1
サブタイトル: 入門編：AIとの正しい付き合い方

デザイン要件:
- 16:9のアスペクト比
- 深い青（#1a237e）を基調としたグラデーション背景
- タイトルは白文字で中央に大きく配置
- サブタイトルはやや小さく、タイトルの下に配置
- モダンでテック感のあるデザイン
- シンプルで洗練された印象
- 装飾は最小限（抽象的な幾何学模様やラインのみ）
"""
    },
    {
        "filename": "slide_02_ai_characteristics.png",
        "prompt": """プレゼンテーションスライドを生成してください。

タイトル: AIの特性への対策まとめ

内容（表形式で表示）:
| 特性 | 問題 | 本質的対策 |
| 暴走 | 機能追加しすぎ | 仕様書・受入基準で範囲を明確化 |
| 手抜き | テストだけ通す | 受入基準・テストケースを事前定義 |
| 忘れっぽさ | 指示を忘れる | CLAUDE.md・Claude Skills・/clear |
| 凸凹知能 | 得意不得意が激しい | 人間が期待値を適切に管理 |
| 虚偽報告 | 誤った情報 | pytest/ruff/pyright、公式ドキュメント |

重要メッセージ: これらの特性を理解して対策すれば、AIは強力なパートナーになる

デザイン要件:
- 16:9のアスペクト比
- 青系の配色（#1a73e8がメインカラー）
- 表は見やすく整理、行ごとに背景色を交互に
- タイトルは上部に大きく
- 重要メッセージは下部にハイライト表示
- 日本語テキストを正確に表示
"""
    },
    {
        "filename": "slide_03_context_is_code.png",
        "prompt": """プレゼンテーションスライドを生成してください。

タイトル: 原則2: Context is the New Code（コンテキストが全て）

内容:
■ AIは外部メモリが必要（Claude Codeのコンテキスト上限：200Kトークン）
  - 設計書なし：全コード読込150K → 思考50K → 単純なCRUDしか作れない
  - 設計書あり：設計書30K → 思考170K → 複雑なロジックも対応可能（3.4倍）

■ コンテキストの種類
  - CLAUDE.md：プロジェクトルール
  - README.md：プロジェクト概要
  - 設計書：画面、DB、API仕様
  - Issue：タスク定義
  - 受入基準（AC）

■ 研究データ
  - Microsoft Research：ユーザー意図との整合性90.4%達成
  - McKinsey 2024：ドキュメント作成45-50%削減

デザイン要件:
- 16:9のアスペクト比
- 青系の配色でプロフェッショナルな印象
- 「3.4倍」を強調表示
- 箇条書きは階層を明確に
- 日本語テキストを正確に表示
"""
    },
    {
        "filename": "slide_04_5step_workflow.png",
        "prompt": """プレゼンテーションスライドを生成してください。

タイトル: 5-STEPの全体像と効果

内容:
5つのステップを左から右に矢印でつなげて表示:

1. 要件定義（STEP 1）
   誰が、何を、なぜ
   ユーザーストーリー、MoSCoW分析

2. 設計（STEP 2）
   AIの外部メモリ構築
   画面、DB、AC、API仕様

3. タスク分解（STEP 3）
   10分サイズに分割
   GitHub Issues、BDD

4. 実装（STEP 4）
   TDD + 3段階レビュー
   Red-Green-Refactor + 検証

5. 品質改善（STEP 5）
   AIに任せる
   リファクタリング、ドキュメント

目的: AIの5つの特性を制御し、高品質なコードを効率的に生成

デザイン要件:
- 16:9のアスペクト比
- 青系のグラデーション背景
- 5つのステップは横並びで矢印で接続
- 各ステップは四角いカードまたは円形で表示
- 番号とアイコンを含む
- フローチャート風のデザイン
- 日本語テキストを正確に表示
"""
    }
]


def generate_image(prompt: str, output_path: Path) -> bool:
    """画像を生成して保存（Gemini 3 Pro Image / Nano Banana Pro）"""
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
                print(f"✓ 生成完了: {output_path}")
                return True

        print(f"✗ 画像なし: {output_path}")
        return False

    except Exception as e:
        print(f"✗ エラー: {output_path} - {e}")
        return False


def main():
    # 出力ディレクトリ
    output_dir = Path("docs/generated-images")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"モデル: {MODEL_NAME}")
    print(f"出力先: {output_dir}")
    print("=" * 50)

    generated_files = []
    for slide in SLIDES:
        output_path = output_dir / slide["filename"]
        print(f"\n生成中: {slide['filename']}")
        if generate_image(slide["prompt"], output_path):
            generated_files.append(slide["filename"])

    # HTMLギャラリーを生成
    html_content = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI駆動開発セミナー - 生成スライド</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: #f5f5f5;
        }
        h1 {
            text-align: center;
            color: #1a237e;
        }
        .gallery {
            display: grid;
            gap: 2rem;
        }
        .slide-container {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .slide-container img {
            width: 100%;
            height: auto;
            display: block;
        }
        .slide-title {
            padding: 1rem;
            font-weight: bold;
            color: #333;
            border-top: 1px solid #eee;
        }
        .note {
            text-align: center;
            color: #666;
            margin-top: 2rem;
            font-size: 0.9rem;
        }
    </style>
</head>
<body>
    <h1>AI駆動開発セミナー - Nano Banana Pro 生成スライド</h1>
    <div class="gallery">
"""

    slide_titles = [
        "タイトルスライド",
        "AIの特性への対策まとめ",
        "Context is the New Code",
        "5-STEPの全体像"
    ]

    for i, filename in enumerate(generated_files):
        title = slide_titles[i] if i < len(slide_titles) else f"スライド {i+1}"
        html_content += f"""        <div class="slide-container">
            <img src="generated-images/{filename}" alt="{title}">
            <div class="slide-title">{title}</div>
        </div>
"""

    html_content += """    </div>
    <p class="note">Generated with Gemini Nano Banana Pro (gemini-2.0-flash-preview-image-generation)</p>
</body>
</html>
"""

    html_path = Path("docs/generated-slides.html")
    html_path.write_text(html_content, encoding="utf-8")
    print(f"\n✓ HTMLギャラリー生成: {html_path}")
    print(f"\nURL: https://cuzic.github.io/ai-slides/generated-slides.html")


if __name__ == "__main__":
    main()
