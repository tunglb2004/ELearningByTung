#!/usr/bin/env python3
"""Thêm course-nav vào sidebar các bài học."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LESSON_FILES = [
    "part1_oop_principles.html",
    "video1_manual_vs_automation.html",
    "video2_4_types_testing.html",
    "phase2_selenium_webdriver.html",
    "phase3_testng_pom.html",
    "phase4_advanced_cicd.html",
]

HEAD_LINK = '    <link rel="stylesheet" href="course-nav.css">\n'
SCRIPT_TAG = '    <script src="course-nav.js"></script>\n'

# Các tiêu đề navigation cũ → slide nav heading
NAV_HEADINGS = [
    "📑 Điều hướng",
    "📑 Navigation",
    "📑 Điều Hướng",
]

SLIDE_NAV_OPEN = """                <motion data-course-nav></motion>
                <div class="sidebar-section slide-nav-section" style="max-height: 300px; overflow-y: auto;">
                    <h3 class="slide-nav-heading">📑 Slide trong bài</h3>
""".replace("<motion ", "<motion ").replace("<motion data", "<div data").replace(
    "<motion class", "<div class"
)


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "course-nav.css" not in text:
        text = text.replace(
            '<link rel="stylesheet" href="course-code-blocks.css">',
            '<link rel="stylesheet" href="course-code-blocks.css">\n' + HEAD_LINK,
        )
        if "course-nav.css" not in text:
            text = text.replace(
                '<link rel="stylesheet" href="narration-editor.css">',
                '<link rel="stylesheet" href="narration-editor.css">\n' + HEAD_LINK,
            )
    if "course-nav.js" not in text:
        text = text.replace(
            '<script src="narration-editor.js"></script>',
            '<script src="narration-editor.js"></script>\n' + SCRIPT_TAG,
        )

    if "data-course-nav" in text:
        path.write_text(text, encoding="utf-8")
        print(f"  skip (already): {path.name}")
        return

    for heading in NAV_HEADINGS:
        marker = f'<h3 style="font-size: 0.95em; margin-bottom: 15px; color:'
        idx = text.find(heading)
        if idx == -1:
            marker2 = f'<h3 style="font-size: 1em; margin-bottom: 15px; color:'
            for m in [marker, marker2]:
                pos = text.find(m)
                if pos != -1 and heading in text[pos : pos + 120]:
                    # find start of wrapping div
                    div_start = text.rfind('<motion style="background: #f0f0f0', 0, pos)
                    if div_start == -1:
                        div_start = text.rfind('<div style="background: #f0f0f0', 0, pos)
                    if div_start != -1:
                        text = (
                            text[:motion_start if (motion_start := div_start) else div_start]
                            + SLIDE_NAV_OPEN.replace("<motion ", "<div ")
                            + text[pos:]
                        )
                        # fix h3 line
                        for h in NAV_HEADINGS:
                            text = text.replace(
                                f'color: #667eea;">{h}</h3>',
                                'class="slide-nav-heading">📑 Slide trong bài</h3>',
                                1,
                            )
                            text = text.replace(
                                f'color: #2a5298;">{h}</h3>',
                                'class="slide-nav-heading">📑 Slide trong bài</h3>',
                                1,
                            )
                            text = text.replace(
                                f'color: #ff6b6b;">{h}</h3>',
                                'class="slide-nav-heading">📑 Slide trong bài</h3>',
                                1,
                            )
                        text = text.replace(
                            f'<h3 style="font-size: 1em; margin-bottom: 15px; color: #667eea;">{h}</h3>',
                            '<h3 class="slide-nav-heading">📑 Slide trong bài</h3>',
                            1,
                        )
                        break
            continue

    # Insert data-course-nav before first nav-links block in sidebar
    needle = '<ul class="nav-links">'
    if "data-course-nav" not in text and needle in text:
        pos = text.find(needle)
        wrap_start = text.rfind('<div style="background: #f0f0f0', 0, pos)
        if wrap_start == -1:
            wrap_start = text.rfind('<div style="margin-top: 30px; background: #f0f0f0', 0, pos)
        insert = '                <div data-course-nav></motion>\n                <div class="sidebar-section slide-nav-section" style="max-height: 300px; overflow-y: auto;">\n'
        insert = insert.replace("</motion>", "").replace("<motion ", "<div ")
        if wrap_start != -1:
            # replace opening div only, add course nav before inner h3
            h3_pos = text.find("<h3", wrap_start, pos)
            if h3_pos != -1:
                text = text[:h3_pos] + insert + text[h3_pos:]
                for h in NAV_HEADINGS:
                    import re

                    text = re.sub(
                        r"<h3[^>]*>" + re.escape(h) + r"</h3>",
                        '<h3 class="slide-nav-heading">📑 Slide trong bài</h3>',
                        text,
                        count=1,
                    )
        else:
            text = text.replace(
                needle,
                insert.replace('</motion>', '') + '                    <h3 class="slide-nav-heading">📑 Slide trong bài</h3>\n                    '
                + needle,
                1,
            )

    # video1 uses inline list without nav-links class
    if "data-course-nav" not in text and 'onclick="goToSlide(0)"' in text and "nav-links" not in text:
        pos = text.find('onclick="goToSlide(0)"')
        wrap_start = text.rfind('<motion style="margin-top: 30px; background: #f0f0f0', 0, pos)
        wrap_start = wrap_start if wrap_start != -1 else text.rfind('<div style="margin-top: 30px; background: #f0f0f0', 0, pos)
        insert = '                <div data-course-nav></div>\n                <div class="sidebar-section slide-nav-section" style="max-height: 280px; overflow-y: auto;">\n                    <h3 class="slide-nav-heading">📑 Slide trong bài</h3>\n                    <ul class="nav-links" style="list-style: none; font-size: 0.9em;">\n'
        if wrap_start != -1:
            h3_end = text.find("</h3>", wrap_start) + 5
            ul_start = text.find("<ul", wrap_start, pos)
            text = text[:wrap_start] + insert + text[ul_start:]
            text = text.replace('<ul style="list-style: none; font-size: 0.9em;">', "", 1)

    path.write_text(text, encoding="utf-8")
    print(f"  patched: {path.name}")


def main() -> None:
    for name in LESSON_FILES:
        patch_file(ROOT / name)


if __name__ == "__main__":
    main()
