#!/usr/bin/env python3
"""Thêm disable speakBtn khi slide không có narration-box."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SNIPPET = """
            const speakBtn = document.getElementById('speakBtn');
            if (speakBtn) {
                const nb = slides[currentSlide].querySelector('.narration-box');
                speakBtn.disabled = !nb;
            }
"""

FILES = [
    "api_testing_buoi1_fundamentals.html",
    "api_testing_advanced_auth.html",
    "api_testing_restassured.html",
    "part1_oop_principles.html",
    "java_core_phase2_collections.html",
    "java_core_phase3_4_advanced.html",
    "video1_manual_vs_automation.html",
    "video2_4_types_testing.html",
    "phase2_selenium_webdriver.html",
    "phase3_testng_pom.html",
    "phase4_advanced_cicd.html",
]

MARKER = "const speakBtn = document.getElementById('speakBtn');"


def patch(path: Path) -> bool:
    t = path.read_text(encoding="utf-8")
    if MARKER in t:
        return False
    # Chèn sau nextBtn disabled, trước slidesContainer scrollTop (hoặc tương đương)
    m = re.search(
        r"(document\.getElementById\('nextBtn'\)\.disabled\s*=\s*[^;]+;)\s*\n\s*(document\.getElementById\('slidesContainer'\)\.scrollTop)",
        t,
    )
    if not m:
        print("SKIP pattern", path.name)
        return False
    insert = m.group(1) + SNIPPET + "\n            " + m.group(2)
    t = t[: m.start(1)] + insert + t[m.end(2) :]
    path.write_text(t, encoding="utf-8")
    return True


def main() -> None:
    for name in FILES:
        p = ROOT / name
        if not p.exists():
            print("MISSING", name)
            continue
        if patch(p):
            print("OK", name)


if __name__ == "__main__":
    main()
