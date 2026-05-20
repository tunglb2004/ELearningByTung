# -*- coding: utf-8 -*-
"""Sửa HTML API: sidebar phải nằm trong .content (layout 2 cột)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FILES = [
    "api_testing_buoi1_fundamentals.html",
    "api_testing_advanced_auth.html",
    "api_testing_restassured.html",
]

BROKEN = re.compile(
    r"\n        </div>\s*\n\s*<!-- SIDEBAR[^>]*-->\s*\n\s*</div>\s*\n(\s*<div class=\"sidebar\">)",
    re.IGNORECASE,
)


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    text = BROKEN.sub(r"\n            </div>\n\1", text)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    for name in FILES:
        p = ROOT / name
        if fix_file(p):
            print("fixed", name)
        else:
            print("no change", name)


if __name__ == "__main__":
    main()
