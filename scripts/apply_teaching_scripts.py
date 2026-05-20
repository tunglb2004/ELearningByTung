#!/usr/bin/env python3
"""Áp script giảng dạy từ file .txt vào narration-box trong HTML."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

from narration_lib import NARRATION_BOX, format_narration_html, read_html, write_html

SCRIPT_ENTRY = re.compile(
    r"^((?:\d+\.\d+)|RECAP_PHASE_\d+)\s+[^\n]*\n\n\"((?:[^\"\\]|\\.)*)\"\s*$",
    re.MULTILINE,
)

PAGE_MAP = {
    "video1": "video1",
    "video2": "video2",
    "phase2": "phase2",
    "phase3": "phase3",
    "phase4": "phase4",
}

PHASE1_FILE = Path(r"c:\Users\ADMIN\Downloads\SCRIPT_GIANG_DAY_PHASE_1_CHUAN_FORMAT.txt")
PHASE2_FILE = Path(r"c:\Users\ADMIN\Downloads\SCRIPT_GIANG_DAY_PHASE_2_CHUAN_FORMAT.txt")
PHASE34_FILE = Path(r"c:\Users\ADMIN\Downloads\SCRIPT_GIANG_DAY_PHASE_3_4_CHUAN_FORMAT.txt")

# (page, keys theo thứ tự narration-box, nguồn scripts)
JOBS: list[tuple[str, list[str], Path]] = [
    (
        "video1",
        [
            "1.1",
            "1.1",
            "1.1",
            "1.2",
            "1.4",
            "1.5",
            "1.4",
            "1.5",
            "1.6",
            "1.3",
            "1.7",
            "1.7",
        ],
        PHASE1_FILE,
    ),
    (
        "video2",
        [
            "2.1",
            "2.2",
            "2.3",
            "2.4",
            "2.5",
            "2.6",
            "2.7",
            "2.8",
            "2.9",
            "2.10",
            "2.11",
            "2.13",
            "2.15",
        ],
        PHASE1_FILE,
    ),
    (
        "phase2",
        [f"2.{i}" for i in range(1, 20)],
        PHASE2_FILE,
    ),
    ("phase3", [f"3.{i}" for i in range(1, 11)], PHASE34_FILE),
    (
        "phase4",
        [
            "PHASE4_INTRO",
            "4.1",
            "4.2",
            "4.3",
            "4.4",
            "4.5",
            "4.6",
            "4.11",
        ],
        PHASE34_FILE,
    ),
]


def parse_script_file(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    scripts: dict[str, str] = {}
    for m in SCRIPT_ENTRY.finditer(text):
        scripts[m.group(1)] = m.group(2).replace('\\"', '"').strip()
    return scripts


def phase4_intro(scripts: dict[str, str]) -> str:
    recap = scripts.get("4.11", "")
    marker = "PHASE 4:"
    if marker in recap:
        start = recap.index(marker)
        end = recap.find("Sekarang", start)
        snippet = recap[start:end].strip() if end > start else recap[start:].strip()
        return (
            "Chào mừng đến PHASE 4 — Kiểm thử nâng cao cho môi trường sản xuất. "
            + snippet.replace("PHASE 4:", "Trong phase này chúng ta học:")
        )
    t = scripts.get("3.10", "")
    if "Next PHASE 4" in t:
        return t[t.index("Next PHASE 4") :].replace("Next PHASE 4 - ", "PHASE 4 — ", 1)
    return (
        "PHASE 4 — Kiểm thử nâng cao: screenshots, listeners, retry logic, "
        "cross-browser, CI/CD, reporting và logging."
    )


def resolve_key(key: str, scripts: dict[str, str]) -> str:
    if key == "PHASE4_INTRO":
        return phase4_intro(scripts)
    if key not in scripts:
        raise KeyError(f"Thiếu script '{key}'")
    return scripts[key]


def apply_page(page: str, keys: list[str], scripts: dict[str, str]) -> int:
    html_content = read_html(PAGE_MAP[page])
    count = 0
    idx = 0

    def repl(m: re.Match) -> str:
        nonlocal idx, count
        if idx >= len(keys):
            return m.group(0)
        text = resolve_key(keys[idx], scripts)
        idx += 1
        count += 1
        return m.group(1) + format_narration_html(text) + m.group(3)

    updated = NARRATION_BOX.sub(repl, html_content)
    if count != len(keys):
        print(f"  WARN {page}: {count} boxes, expected {len(keys)}")
    write_html(PAGE_MAP[page], updated)
    return count


def main() -> None:
    total = 0
    for page, keys, script_path in JOBS:
        if not script_path.is_file():
            raise FileNotFoundError(script_path)
        scripts = parse_script_file(script_path)
        n = apply_page(page, keys, scripts)
        print(f"{page} ({script_path.name}): {n} boxes")
        total += n
    print(f"\nTotal: {total} narration-box updated.")


if __name__ == "__main__":
    main()
