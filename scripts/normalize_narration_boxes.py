#!/usr/bin/env python3
"""Đổi script-box / Script Giảng → narration-box (sửa được + TTS)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from narration_lib import PAGE_FILES, clean_narration, format_narration_html  # noqa: E402

SCRIPT_BOX = re.compile(
    r'<motion class="script-box">\s*<strong>\s*🎤\s*Script Giảng:\s*</strong>\s*["\u201c](.*?)["\u201d]\s*</motion>',
    re.DOTALL | re.IGNORECASE,
)
SCRIPT_BOX = re.compile(
    r'<div class="script-box">\s*<strong>\s*🎤\s*Script Giảng:\s*</strong>\s*["\u201c](.*?)["\u201d]\s*</div>',
    re.DOTALL | re.IGNORECASE,
)


def normalize_html(content: str) -> tuple[str, int]:
    count = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return f'<div class="narration-box">{format_narration_html(clean_narration(m.group(1)))}</div>'

    return SCRIPT_BOX.sub(repl, content), count


def main() -> None:
    total = 0
    for _page, filename in PAGE_FILES.items():
        path = ROOT / filename
        if not path.exists():
            continue
        raw = path.read_text(encoding="utf-8")
        raw = raw.replace('"</motion>', '"</div>')
        updated, n = normalize_html(raw)
        if raw != updated or n:
            path.write_text(updated, encoding="utf-8")
            if n:
                print(f"{filename}: {n}")
                total += n
    print(f"Done. Converted {total} block(s).")


if __name__ == "__main__":
    main()
