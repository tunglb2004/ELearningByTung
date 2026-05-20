# -*- coding: utf-8 -*-
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
FILES = [
    "part1_oop_principles.html",
    "video1_manual_vs_automation.html",
    "video2_4_types_testing.html",
    "phase2_selenium_webdriver.html",
    "phase3_testng_pom.html",
    "phase4_advanced_cicd.html",
]

SLIDE_HEADING = re.compile(
    r"<h3[^>]*>📑 (?:Điều hướng|Navigation|Điều Hướng)</h3>",
    re.I,
)

OPEN_REPLACEMENTS = [
    (
        '<motion style="background: #f0f0f0; padding: 15px; border-radius: 8px; max-height: 420px; overflow-y: auto;">',
        "part1",
    ),
    (
        '<div style="background: #f0f0f0; padding: 15px; border-radius: 8px; max-height: 420px; overflow-y: auto;">',
        "part1-div",
    ),
    (
        '<div style="background: #f0f0f0; padding: 15px; border-radius: 8px; max-height: 500px; overflow-y: auto;">',
        "phase2/4",
    ),
    (
        '<div style="margin-top: 30px; background: #f0f0f0; padding: 15px; border-radius: 8px; overflow-y: auto; max-height: 350px;">',
        "video2",
    ),
    (
        '<div style="margin-top: 30px; background: #f0f0f0; padding: 15px; border-radius: 8px;">',
        "video1",
    ),
]

INSERT = (
    "                <motion data-course-nav></motion>\n"
    "                <div class=\"sidebar-section slide-nav-section\" "
    "style=\"max-height: 280px; overflow-y: auto;\">"
).replace("<motion data-course-nav></motion>", "<div data-course-nav></div>")


def add_assets(t: str) -> str:
    if "course-nav.css" not in t:
        for anchor in (
            '<link rel="stylesheet" href="course-code-blocks.css">',
            '<link rel="stylesheet" href="narration-editor.css">',
        ):
            if anchor in t:
                t = t.replace(
                    anchor,
                    anchor + '\n    <link rel="stylesheet" href="course-nav.css">',
                )
                break
    if "course-nav.js" not in t:
        t = t.replace(
            '<script src="narration-editor.js"></script>',
            '<script src="narration-editor.js"></script>\n'
            '    <script src="course-nav.js"></script>',
        )
    return t


def patch_sidebar(t: str) -> str:
    if "data-course-nav" in t:
        return t
    t = SLIDE_HEADING.sub(
        '<h3 class="slide-nav-heading">📑 Slide trong bài</h3>',
        t,
        count=1,
    )
    for old, _ in OPEN_REPLACEMENTS:
        old = old.replace("<motion", "<div")
        if old in t:
            t = t.replace(old, INSERT, 1)
            break
    return t


def main() -> None:
    for name in FILES:
        p = ROOT / name
        t = p.read_text(encoding="utf-8")
        t = add_assets(t)
        t = patch_sidebar(t)
        if name == "video1_manual_vs_automation.html":
            t = t.replace(
                '<ul style="list-style: none; font-size: 0.9em;">',
                '<ul class="nav-links" style="list-style: none; font-size: 0.9em;">',
                1,
            )
        p.write_text(t, encoding="utf-8")
        print(name, "OK" if "data-course-nav" in t else "FAIL")


if __name__ == "__main__":
    main()
