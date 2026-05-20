#!/usr/bin/env python3
"""Tạo audio chỉ cho PHASE 4."""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from narration_lib import (  # noqa: E402
    extract_slides_narrations,
    read_html,
    regenerate_audio_with_retry,
)


async def main() -> None:
    page = "phase4"
    narrations = extract_slides_narrations(read_html(page))
    print(f"PHASE 4: {len(narrations)} slide có thuyết minh\n")
    ok = err = 0
    for idx in sorted(narrations.keys()):
        print(f"  Slide {idx}...", end=" ", flush=True)
        result = await regenerate_audio_with_retry(page, str(idx), narrations[idx])
        if result["status"] == "ok":
            print("OK")
            ok += 1
        else:
            print("LỖI:", result.get("error"))
            err += 1
        await asyncio.sleep(0.35)
    print(f"\nXong: {ok} thành công, {err} lỗi")


if __name__ == "__main__":
    asyncio.run(main())
