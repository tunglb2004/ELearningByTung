#!/usr/bin/env python3
"""
Tạo toàn bộ file MP3 thuyết minh (Edge TTS vi-VN).

    pip install -r requirements.txt
    python scripts/generate-audio.py
"""
from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from narration_lib import VOICE, regenerate_all  # noqa: E402


async def main() -> None:
    results = await regenerate_all()
    print(f"\nĐã tạo {len(results)} file. Giọng: {VOICE}")


if __name__ == "__main__":
    asyncio.run(main())
