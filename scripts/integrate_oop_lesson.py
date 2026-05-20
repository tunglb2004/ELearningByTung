#!/usr/bin/env python3
"""Tích hợp part1_oop_principles.html vào khóa học."""
from __future__ import annotations

import html
import re
from pathlib import Path

SRC = Path(r"c:\Users\ADMIN\Downloads\part1_oop_principles.html")
OUT = Path(__file__).resolve().parent.parent / "part1_oop_principles.html"

SIDEBAR = """
            <motion class="sidebar">
                <div class="controls">
                    <button class="btn-primary" id="prevBtn">⬅️ Trước</button>
                    <button class="btn-primary" id="nextBtn">Tiếp ➡️</button>
                    <button class="btn-secondary" id="speakBtn">🔊 Đọc thuyết minh</button>
                    <div id="ttsPlayerSlot" class="tts-player-slot" hidden>
                        <audio id="courseAudio" controls preload="metadata"></audio>
                        <div class="tts-rate-row">
                            <label for="ttsRateSelect">Tốc độ</label>
                            <select id="ttsRateSelect" aria-label="Tốc độ đọc">
                                <option value="0.75">0.75×</option>
                                <option value="1" selected>1× Bình thường</option>
                                <option value="1.25">1.25×</option>
                                <option value="1.5">1.5×</option>
                                <option value="1.75">1.75×</option>
                                <option value="2">2×</option>
                            </select>
                        </div>
                    </div>
                    <button class="btn-secondary" id="resetBtn">🔄 Đặt lại</button>
                    <button class="btn-secondary" id="toggleEditBtn" type="button">✏️ Sửa script</button>
                </div>
                <div class="slide-counter"><div id="slideCount">1 / 6</div></div>
                <motion class="progress-bar" style="margin: 20px 0;"><motion class="progress-fill" id="sidebarProgress"></div></div>
                <div style="background: #f0f0f0; padding: 15px; border-radius: 8px; max-height: 420px; overflow-y: auto;">
                    <h3 style="font-size: 0.95em; margin-bottom: 15px; color: #667eea;">📑 Điều hướng</h3>
                    <ul class="nav-links">
                        <li><a href="#" onclick="return goToSlide(0)">0. Giới thiệu OOP</a></li>
                        <li><a href="#" onclick="return goToSlide(1)">1. Encapsulation</a></li>
                        <li><a href="#" onclick="return goToSlide(2)">2. Inheritance</a></li>
                        <li><a href="#" onclick="return goToSlide(3)">3. Polymorphism</a></li>
                        <li><a href="#" onclick="return goToSlide(4)">4. Abstraction</a></li>
                        <li><a href="#" onclick="return goToSlide(5)">5. Tóm tắt</a></li>
                    </ul>
                </div>
                <div style="margin-top: auto; padding-top: 20px; border-top: 1px solid #ddd;">
                    <p style="font-size: 0.85em; color: #666; text-align: center;">⏱️ ~35 phút<br>📚 Java Core — Phần 1<br>☕ OOP Principles</p>
                </div>
            </motion>
""".replace("<motion ", "<div ").replace("</motion>", "</div>")

SCRIPT = """
    <script src="vietnamese-tts.js"></script>
    <script src="narration-editor.js"></script>
    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        const ttsPage = document.body.dataset.ttsPage;
        function updateSlide() {
            VietnameseTTS.stop();
            slides.forEach((slide, index) => {
                slide.classList.toggle('active', index === currentSlide);
            });
            document.getElementById('slideCount').textContent = `${currentSlide + 1} / ${totalSlides}`;
            const progress = ((currentSlide + 1) / totalSlides) * 100;
            document.getElementById('progressFill').style.width = progress + '%';
            document.getElementById('sidebarProgress').style.width = progress + '%';
            document.getElementById('prevBtn').disabled = currentSlide === 0;
            document.getElementById('nextBtn').disabled = currentSlide === totalSlides - 1;
            document.getElementById('slidesContainer').scrollTop = 0;
        }
        function nextSlide() { if (currentSlide < totalSlides - 1) { currentSlide++; updateSlide(); } }
        function prevSlide() { if (currentSlide > 0) { currentSlide--; updateSlide(); } }
        function goToSlide(index) {
            if (index >= 0 && index < totalSlides) { currentSlide = index; updateSlide(); }
            return false;
        }
        function speak() {
            if (!slides[currentSlide].querySelector('.narration-box')) return;
            VietnameseTTS.speakSlide(ttsPage, currentSlide);
        }
        function reset() { currentSlide = 0; updateSlide(); }
        document.getElementById('nextBtn').addEventListener('click', nextSlide);
        document.getElementById('prevBtn').addEventListener('click', prevSlide);
        document.getElementById('speakBtn').addEventListener('click', speak);
        document.getElementById('resetBtn').addEventListener('click', reset);
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight') nextSlide();
            if (e.key === 'ArrowLeft') prevSlide();
        });
        updateSlide();
    </script>
"""


def normalize_narrations(text: str) -> str:
    pat = re.compile(r'<motion class="narration-box">\s*(.*?)\s*</div>', re.DOTALL | re.I)
    pat = re.compile(r'<div class="narration-box">\s*(.*?)\s*</div>', re.DOTALL | re.I)

    def repl(m: re.Match) -> str:
        raw = re.sub(r"<[^>]+>", " ", m.group(1))
        raw = re.sub(r"\s+", " ", raw.replace("🔊", "").strip().strip("\"'“”")).strip()
        return f'<div class="narration-box">🔊 "{html.escape(raw, quote=False)}"</motion>'

    out = pat.sub(repl, text)
    return out.replace("</motion>", "</div>")


def main() -> None:
    t = SRC.read_text(encoding="utf-8")
    for a, b in [
        ("#1e40af", "#667eea"),
        ("#7c3aed", "#764ba2"),
        ("linear-gradient(135deg, #1e40af 0%, #7c3aed 100%)", "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"),
        ("linear-gradient(90deg, #1e40af 0%, #7c3aed 100%)", "linear-gradient(90deg, #667eea 0%, #764ba2 100%)"),
        ("max-width: 1500px", "max-width: 1400px"),
        ("height: 800px", "height: 600px"),
        ("border-right: 2px solid #e0e0e0", "border-right: 1px solid #ddd"),
        ("border-left: 2px solid #e0e0e0", "border-left: 1px solid #ddd"),
        ("flex: 0 0 320px", "flex: 0 0 300px"),
        ("border-bottom: 4px solid #764ba2", "border-bottom: 3px solid #667eea"),
        (".btn-secondary {\n            background: #10b981;", ".btn-secondary {\n            background: #764ba2;"),
        (".btn-secondary:hover {\n            background: #059669;", ".btn-secondary:hover {\n            background: #663a8b;"),
        (".nav-links a:hover {\n            background: #764ba2;", ".nav-links a:hover {\n            background: #667eea;"),
    ]:
        t = t.replace(a, b)

    t = re.sub(
        r"\.narration-box \{.*?\n        \}",
        """        .narration-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
            font-style: italic;
            color: #333;
            line-height: 1.6;
        }""",
        t,
        count=1,
        flags=re.DOTALL,
    )
    t = t.replace("<title>PHẦN 1: OOP Principles - Java Core Concepts</title>", "<title>Phần 1: OOP Principles — Java Core</title>")
    t = re.sub(
        r"<h1>🎓 PHẦN 1: OOP Principles</h1>\s*<p>Làm Chủ 4 Trụ Cột Của Lập Trình Hướng Đối Tượng</p>\s*"
        r'<p style="margin-top: 14px; font-size: 0\.95em;">Encapsulation • Inheritance • Polymorphism • Abstraction</p>',
        '<h1>☕ Phần 1: OOP Principles</h1>\n            <p>Java Core — 4 trụ cột lập trình hướng đối tượng</p>\n'
        '<p style="margin-top: 14px;"><a href="index.html" style="color: white; text-decoration: none; opacity: 0.95;">🏠 Trang chủ</a></p>',
        t,
        count=1,
    )
    t = t.replace(
        "</style>\n</head>\n<body>",
        '</style>\n    <link rel="stylesheet" href="narration-editor.css">\n'
        '    <link rel="stylesheet" href="course-audio-player.css">\n'
        '    <link rel="stylesheet" href="course-code-blocks.css">\n'
        '</head>\n<body data-tts-page="oop1">',
    )
    t = normalize_narrations(t)
    t = re.sub(
        r'<div class="sidebar">.*?</div>\s*\n\s*<div class="footer">',
        SIDEBAR + "\n        <div class=\"footer\">",
        t,
        count=1,
        flags=re.DOTALL,
    )
    t = re.sub(r"<script>.*?</script>\s*</body>", SCRIPT.strip() + "\n</body>", t, count=1, flags=re.DOTALL)
    t = t.replace(
        "© 2025 Java Core Concepts Tutorial | PHẦN 1: OOP Principles",
        "© 2025 Automation Testing & Java Core | Phần 1: OOP Principles",
    )
    OUT.write_text(t, encoding="utf-8")
    print("OK", OUT.name, "slides", len(re.findall(r'<div class="slide', t)), "narr", t.count("narration-box"))


if __name__ == "__main__":
    main()
