#!/usr/bin/env python3
"""Chèn thanh audio player vào các trang bài học."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PLAYER_BLOCK = """
                    <motion id="ttsPlayerSlot" class="tts-player-slot" hidden>
                        <audio id="courseAudio" controls preload="metadata"></audio>
                        <motion class="tts-rate-row">
                            <label for="ttsRateSelect">Tốc độ</label>
                            <select id="ttsRateSelect" aria-label="Tốc độ đọc">
                                <option value="0.75">0.75×</option>
                                <option value="1" selected>1× Bình thường</option>
                                <option value="1.25">1.25×</option>
                                <option value="1.5">1.5×</option>
                                <option value="1.75">1.75×</option>
                                <option value="2">2×</option>
                            </select>
                        </motion>
                    </motion>
""".replace("<motion", "<div").replace("</motion>", "</div>")

OLD = """                    <button class="btn-secondary" id="speakBtn">🔊 Đọc thuyết minh</button>
                    <button class="btn-stop" id="stopSpeakBtn" type="button" hidden>⏹ Dừng đọc</button>
                    <button class="btn-secondary" id="resetBtn">🔄 Reset</button>"""

NEW = """                    <button class="btn-secondary" id="speakBtn">🔊 Đọc thuyết minh</button>""" + PLAYER_BLOCK + """
                    <button class="btn-secondary" id="resetBtn">🔄 Reset</button>"""

CSS_LINK = '    <link rel="stylesheet" href="course-audio-player.css">\n'

for name in [
    "video2_4_types_testing.html",
    "phase2_selenium_webdriver.html",
    "phase3_testng_pom.html",
]:
    path = ROOT / name
    text = path.read_text(encoding="utf-8")
    if "ttsPlayerSlot" not in text:
        text = text.replace(OLD, NEW)
    if "course-audio-player.css" not in text:
        text = text.replace(
            '<link rel="stylesheet" href="narration-editor.css">',
            '<link rel="stylesheet" href="narration-editor.css">\n' + CSS_LINK.strip(),
        )
    path.write_text(encoding="utf-8", data=text)
    print("patched", name)
