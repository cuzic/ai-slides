#!/usr/bin/env python3
"""
Marp スライド修正スクリプト（汎用版）

使い方:
  python fix-slides.py add-css <file-or-dir>       # 共通CSSを追加
  python fix-slides.py auto-font <file-or-dir>     # オーバーフローに応じてフォントサイズ自動調整
  python fix-slides.py add-font-class <file> <slide-num> <class>  # 特定スライドにクラス追加

例:
  python fix-slides.py add-css src/01-intro.md
  python fix-slides.py add-css src/
  python fix-slides.py auto-font src/
  python fix-slides.py add-font-class src/01-intro.md 5 font-small
"""

import subprocess
import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ========================================
# CSS定義
# ========================================

# フォントサイズバリエーション
FONT_SIZE_CSS = """
  /* フォントサイズバリエーション */
  section[data-class~="font-large"] {
    font-size: 28px !important;
    line-height: 1.5 !important;
  }
  section[data-class~="font-large"] h2 {
    font-size: 42px !important;
  }

  section[data-class~="font-medium"] {
    font-size: 22px !important;
    line-height: 1.4 !important;
  }

  section[data-class~="font-small"] {
    font-size: 20px !important;
    line-height: 1.35 !important;
    padding: 35px 50px !important;
  }
  section[data-class~="font-small"] h2 {
    font-size: 32px !important;
  }
  section[data-class~="font-small"] li {
    margin-bottom: 0.15em !important;
  }

  section[data-class~="font-xsmall"] {
    font-size: 18px !important;
    line-height: 1.25 !important;
    padding: 30px 50px !important;
  }
  section[data-class~="font-xsmall"] h2 {
    font-size: 28px !important;
  }
  section[data-class~="font-xsmall"] li {
    margin-bottom: 0.1em !important;
  }

  section[data-class~="font-xxsmall"] {
    font-size: 16px !important;
    line-height: 1.2 !important;
    padding: 25px 45px !important;
  }
  section[data-class~="font-xxsmall"] h2 {
    font-size: 24px !important;
  }
  section[data-class~="font-xxsmall"] li {
    margin-bottom: 0.05em !important;
  }
"""

# レイアウトCSS
LAYOUT_CSS = """
  /* 2カラムレイアウト */
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;
    margin-top: 0.5em;
  }
  .columns ul {
    margin: 0;
  }

  /* 3カラムレイアウト */
  .columns-3 {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 1rem;
    margin-top: 0.5em;
  }
  .columns-3 ul {
    margin: 0;
    font-size: 0.85em;
  }

  /* コンパクトリスト */
  .compact-list li {
    margin-bottom: 0.2em;
    font-size: 0.95em;
  }

  /* ハイライトボックス */
  .highlight-box {
    background: #e8f0fe;
    border-left: 4px solid #1a73e8;
    padding: 1rem 1.5rem;
    margin: 1em 0;
    border-radius: 4px;
  }

  /* 警告ボックス */
  .warning-box {
    background: #fef7e0;
    border-left: 4px solid #f9ab00;
    padding: 1rem 1.5rem;
    margin: 1em 0;
    border-radius: 4px;
  }

  /* キーメッセージ */
  .key-message {
    font-size: 1.3em;
    font-weight: bold;
    color: #1a73e8;
    text-align: center;
    margin: 1.5em 0;
    padding: 1em;
    background: #f8f9fa;
    border-radius: 8px;
  }

  /* チェックリスト */
  .checklist ul {
    list-style: none;
    padding-left: 0;
  }
  .checklist li::before {
    content: "✓ ";
    color: #34a853;
    font-weight: bold;
  }
"""

ALL_CSS = FONT_SIZE_CSS + LAYOUT_CSS

# ========================================
# ヘルパー関数
# ========================================

def get_md_files(target: str) -> List[Path]:
    """対象のMarkdownファイルを取得"""
    target_path = Path(target)
    if target_path.is_file():
        return [target_path]
    elif target_path.is_dir():
        return sorted([
            f for f in target_path.glob('*.md')
            if not f.name.startswith('CLAUDE') and not f.name.startswith('README')
        ])
    return []


def find_style_block(content: str) -> Optional[Tuple[int, int]]:
    """<style>ブロックの位置を検出"""
    match = re.search(r'<style[^>]*>(.*?)</style>', content, re.DOTALL)
    if match:
        return match.start(), match.end()
    return None


def add_css_to_file(filepath: Path) -> bool:
    """ファイルにCSSを追加"""
    content = filepath.read_text(encoding='utf-8')

    # 既に追加済みかチェック
    if 'font-xxsmall' in content and '.highlight-box' in content:
        print(f"  ✓ {filepath.name}: 既に追加済み")
        return False

    style_pos = find_style_block(content)
    if style_pos:
        start, end = style_pos
        # </style>の前にCSSを挿入
        close_tag_pos = content.rfind('</style>', start, end)
        if close_tag_pos > 0:
            # 既存CSSがある場合は不足分のみ追加
            existing_style = content[start:end]
            css_to_add = ""
            if 'font-xxsmall' not in existing_style:
                css_to_add += FONT_SIZE_CSS
            if '.highlight-box' not in existing_style:
                css_to_add += LAYOUT_CSS

            if css_to_add:
                new_content = content[:close_tag_pos] + css_to_add + content[close_tag_pos:]
                filepath.write_text(new_content, encoding='utf-8')
                print(f"  ✓ {filepath.name}: CSSを追加しました")
                return True
    else:
        # <style>ブロックがない場合は作成
        # フロントマターの後に追加
        frontmatter_end = content.find('---', 4)
        if frontmatter_end > 0:
            insert_pos = frontmatter_end + 3
            style_block = f"\n\n<style>\n{ALL_CSS}\n</style>\n"
            new_content = content[:insert_pos] + style_block + content[insert_pos:]
            filepath.write_text(new_content, encoding='utf-8')
            print(f"  ✓ {filepath.name}: <style>ブロックを作成しました")
            return True

    print(f"  - {filepath.name}: 変更なし")
    return False


# ========================================
# オーバーフロー検出・自動修正
# ========================================

def get_overflow_info(filepath: Path) -> Dict[int, int]:
    """check-slides.jsを使ってオーバーフロー情報を取得"""
    script_dir = Path(__file__).parent
    check_script = script_dir / 'check-slides.js'

    try:
        result = subprocess.run(
            ['node', str(check_script), 'overflow', str(filepath)],
            capture_output=True,
            text=True,
            timeout=120
        )
        output = result.stdout + result.stderr
    except Exception as e:
        print(f"  ⚠️ オーバーフロー検出エラー: {e}")
        return {}

    overflow_info = {}
    lines = output.split('\n')

    for i, line in enumerate(lines):
        # "❌ スライド 5: 150px オーバー" のようなパターンを検出
        match = re.search(r'スライド (\d+):\s*(\d+)px', line)
        if match:
            slide_num = int(match.group(1))
            overflow_px = int(match.group(2))
            overflow_info[slide_num] = overflow_px

    return overflow_info


def determine_font_class(overflow_px: int) -> Optional[str]:
    """オーバーフロー量に応じて適切なフォントクラスを決定"""
    if overflow_px <= 0:
        return None
    elif overflow_px < 50:
        return 'font-small'
    elif overflow_px < 150:
        return 'font-xsmall'
    else:
        return 'font-xxsmall'


def apply_font_class_to_slide(filepath: Path, slide_num: int, font_class: str) -> bool:
    """特定のスライドにフォントクラスを適用"""
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')

    current_slide = 0
    modified = False
    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if line.strip() == '---':
            current_slide += 1
            new_lines.append(line)
            i += 1

            # 対象スライドの直後に処理
            if current_slide == slide_num:
                # 既存の<!-- _class: -->を探す
                if i < len(lines) and '<!-- _class:' in lines[i]:
                    # 既存のクラスを更新
                    existing = lines[i]
                    if font_class not in existing:
                        # クラスを追加
                        new_class = existing.replace('-->', f' {font_class} -->')
                        new_lines.append(new_class)
                        modified = True
                    else:
                        new_lines.append(existing)
                    i += 1
                else:
                    # 新しいクラスディレクティブを挿入
                    new_lines.append(f'<!-- _class: {font_class} -->')
                    modified = True
            continue

        new_lines.append(line)
        i += 1

    if modified:
        filepath.write_text('\n'.join(new_lines), encoding='utf-8')
        return True
    return False


def auto_fix_overflows(filepath: Path) -> int:
    """オーバーフローを自動検出して修正"""
    overflow_info = get_overflow_info(filepath)

    if not overflow_info:
        print(f"  ✓ {filepath.name}: オーバーフローなし")
        return 0

    fixed = 0
    for slide_num, overflow_px in sorted(overflow_info.items()):
        font_class = determine_font_class(overflow_px)
        if font_class:
            if apply_font_class_to_slide(filepath, slide_num, font_class):
                print(f"    スライド {slide_num}: {overflow_px}px → {font_class}")
                fixed += 1

    return fixed


# ========================================
# メインコマンド
# ========================================

def cmd_add_css(target: str):
    """CSSを追加"""
    print(f"\n{'='*50}")
    print("CSS追加")
    print(f"{'='*50}\n")

    files = get_md_files(target)
    if not files:
        print("対象ファイルがありません")
        return

    updated = 0
    for f in files:
        if add_css_to_file(f):
            updated += 1

    print(f"\n✅ {updated}/{len(files)} ファイルを更新しました")


def cmd_auto_font(target: str):
    """オーバーフローに応じてフォントサイズを自動調整"""
    print(f"\n{'='*50}")
    print("オーバーフロー自動修正")
    print(f"{'='*50}\n")

    files = get_md_files(target)
    if not files:
        print("対象ファイルがありません")
        return

    total_fixed = 0
    for f in files:
        print(f"📄 {f.name}")
        fixed = auto_fix_overflows(f)
        total_fixed += fixed
        if fixed > 0:
            print(f"  → {fixed} スライドを修正")
        print()

    print(f"{'='*50}")
    print(f"✅ 合計 {total_fixed} スライドを修正しました")


def cmd_add_font_class(filepath: str, slide_num: int, font_class: str):
    """特定スライドにフォントクラスを追加"""
    path = Path(filepath)
    if not path.exists():
        print(f"❌ ファイルが見つかりません: {filepath}")
        return

    if apply_font_class_to_slide(path, slide_num, font_class):
        print(f"✅ {path.name} のスライド {slide_num} に {font_class} を追加しました")
    else:
        print(f"- 変更なし（既に適用済みの可能性があります）")


# ========================================
# エントリーポイント
# ========================================

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == 'add-css':
        cmd_add_css(sys.argv[2])
    elif command == 'auto-font':
        cmd_auto_font(sys.argv[2])
    elif command == 'add-font-class':
        if len(sys.argv) < 5:
            print("使い方: python fix-slides.py add-font-class <file> <slide-num> <class>")
            sys.exit(1)
        cmd_add_font_class(sys.argv[2], int(sys.argv[3]), sys.argv[4])
    else:
        print(f"❌ 不明なコマンド: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == '__main__':
    main()
