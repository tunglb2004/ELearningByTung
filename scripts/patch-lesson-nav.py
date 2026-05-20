# -*- coding: utf-8 -*-
"""Chuẩn hóa sidebar: lộ trình + slide nav + highlight slide."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LESSON_FILES = [
    "part1_oop_principles.html",
    "java_core_phase2_collections.html",
    "java_core_phase3_4_advanced.html",
    "video1_manual_vs_automation.html",
    "video2_4_types_testing.html",
    "phase2_selenium_webdriver.html",
    "phase3_testng_pom.html",
    "phase4_advanced_cicd.html",
]

HIGHLIGHT_LINE = (
    "            if (window.CourseNav && CourseNav.setActiveSlide) "
    "CourseNav.setActiveSlide(currentSlide);\n"
)


def patch_file(path: Path) -> None:
    t = path.read_text(encoding="utf-8")
    orig = t

    t = re.sub(
        r'<div class="sidebar">',
        '<div class="sidebar lesson-sidebar">',
        t,
        count=1,
    )
    t = t.replace(
        'class="sidebar-section slide-nav-section" style="max-height: 280px; overflow-y: auto;"',
        'class="sidebar-section slide-nav-section"',
    )
    t = re.sub(
        r"\s+<div data-course-nav></motion>",
        "\n                <motion data-course-nav></motion>",
        t,
    )
    t = t.replace("<motion data-course-nav></motion>", "<div data-course-nav></motion>")
    t = t.replace("<motion data-course-nav></motion>", "<div data-course-nav></div>")

    if "flex: 0 0 300px" in t:
        t = t.replace("flex: 0 0 300px", "flex: 0 0 380px")

    if "CourseNav.setActiveSlide" not in t:

        def add_highlight(m: re.Match) -> str:
            body = m.group(0)
            if "CourseNav.setActiveSlide" in body:
                return body
            return body.rstrip() + "\n" + HIGHLIGHT_LINE

        t = re.sub(
            r"function updateSlide\(\) \{.*?\n        \}",
            add_highlight,
            t,
            count=1,
            flags=re.DOTALL,
        )

    if t != orig:
        path.write_text(t, encoding="utf-8")
        print("patched", path.name)
    else:
        print("skip", path.name)


def main() -> None:
    for name in LESSON_FILES:
        patch_file(ROOT / name)


if __name__ == "__main__":
    main()
