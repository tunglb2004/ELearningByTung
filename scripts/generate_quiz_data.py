# -*- coding: utf-8 -*-
"""Sinh quiz-data.js từ quiz_content."""
from __future__ import annotations

import json
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from quiz_content import LESSONS, BANKS  # noqa: E402


def main() -> None:
    out = ROOT / "quiz-data.js"
    payload = {"lessons": LESSONS, "banks": BANKS}
    js = "window.CourseQuiz = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    out.write_text(js, encoding="utf-8")
    total = sum(len(BANKS[k]["questions"]) for k in BANKS)
    print("Wrote", out, "| lessons:", len(LESSONS), "| questions:", total)


if __name__ == "__main__":
    main()
