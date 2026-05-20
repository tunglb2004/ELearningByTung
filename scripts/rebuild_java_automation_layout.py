# -*- coding: utf-8 -*-
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LESSONS = [
    {
        "file": "part1_oop_principles.html",
        "tts": "oop1",
        "title": "☕ Java Core — Phần 1: OOP Principles",
        "subtitle": "Encapsulation · Inheritance · Polymorphism · Abstraction",
        "footer": "Java Core — Phần 1: OOP Principles",
        "meta": "⏱️ ~35 phút<br>📚 Java Core — Phần 1<br>☕ OOP Principles",
    },
    {
        "file": "java_core_phase2_collections.html",
        "tts": "java2",
        "title": "☕ Java Core — Phần 2: Collections",
        "subtitle": "List · Set · Map — Collections Framework",
        "footer": "Java Core — Phần 2: Collections",
        "meta": "⏱️ ~40 phút<br>📚 Java Core — Phần 2<br>📦 Collections",
    },
    {
        "file": "java_core_phase3_4_advanced.html",
        "tts": "java34",
        "title": "☕ Java Core — Phần 3–4: Advanced Java",
        "subtitle": "Exception · Streams · File I/O · Strings",
        "footer": "Java Core — Phần 3–4: Advanced Java",
        "meta": "⏱️ ~45 phút<br>📚 Java Core — Phần 3–4<br>⚡ Advanced",
    },
]


def extract_slides(html: str) -> str:
    m = re.search(
        r'id="slidesContainer">(.*?)<\/motion>\s*<div class="sidebar',
        html,
        re.DOTALL,
    )
    if not m:
        m = re.search(
            r'id="slidesContainer">(.*?)<\/div>\s*<div class="sidebar',
            html,
            re.DOTALL,
        )
    return (m.group(1).strip() if m else "").replace(
        'class="code-block"', 'class="code-example"'
    )


def extract_nav_labels(html: str) -> list[str]:
    labels = re.findall(r"goToSlide\(\d+\)[^>]*>([^<]+)</a>", html)
    if labels:
        return [x.strip() for x in labels]
    n = len(re.findall(r'<div class="slide(?:\s+active)?"', html))
    return [f"Slide {i}" for i in range(n)]


def build_sidebar(nav_labels: list[str], meta: str) -> str:
    links = "\n".join(
        f'                        <li><a href="#" onclick="return goToSlide({i})">{label}</a></li>'
        for i, label in enumerate(nav_labels)
    )
    total = len(nav_labels)
    return f"""            <div class="sidebar lesson-sidebar">
                <motion class="controls">
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
                <div class="slide-counter"><div id="slideCount">1 / {total}</div></div>
                <div class="progress-bar"><div class="progress-fill" id="sidebarProgress"></motion></div>
                <div data-course-nav></div>
                <div class="sidebar-section slide-nav-section">
                    <h3 class="slide-nav-heading">📑 Slide trong bài</h3>
                    <ul class="nav-links">
{links}
                    </ul>
                </div>
                <p class="sidebar-meta">{meta}</p>
            </div>""".replace("<motion ", "<div ").replace("</motion>", "")


def build_html(cfg: dict, slides_html: str, sidebar_html: str) -> str:
    page_title = cfg["title"].replace("☕ ", "")
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{page_title}</title>
    <link rel="stylesheet" href="lesson-slide-layout.css">
    <link rel="stylesheet" href="narration-editor.css">
    <link rel="stylesheet" href="course-audio-player.css">
    <link rel="stylesheet" href="course-code-blocks.css">
    <link rel="stylesheet" href="course-nav.css">
</head>
<body class="lesson-page" data-tts-page="{cfg["tts"]}">
    <div class="container">
        <div class="header">
            <h1>{cfg["title"]}</h1>
            <p>{cfg["subtitle"]}</p>
            <p style="margin-top: 14px;"><a href="index.html" style="color: white; text-decoration: none; opacity: 0.95;">🏠 Trang chủ</a></p>
        </div>
        <div class="top-progress">
            <div style="flex: 1;">
                <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
            </div>
        </div>
        <div class="content">
            <div class="slides" id="slidesContainer">
{slides_html}
            </div>
{sidebar_html}
        </div>
        <div class="footer">
            <p>© 2025 Automation Testing & Java Core | {cfg["footer"]} | Tất cả quyền được bảo lưu</p>
        </motion>
    </div>
    <script src="vietnamese-tts.js"></script>
    <script src="narration-editor.js"></script>
    <script src="course-nav.js?v=2"></script>
    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        const ttsPage = document.body.dataset.ttsPage;
        function updateSlide() {{
            VietnameseTTS.stop();
            slides.forEach((slide, index) => slide.classList.toggle('active', index === currentSlide));
            document.getElementById('slideCount').textContent = `${{currentSlide + 1}} / ${{totalSlides}}`;
            const progress = ((currentSlide + 1) / totalSlides) * 100;
            document.getElementById('progressFill').style.width = progress + '%';
            document.getElementById('sidebarProgress').style.width = progress + '%';
            document.getElementById('prevBtn').disabled = currentSlide === 0;
            document.getElementById('nextBtn').disabled = currentSlide === totalSlides - 1;
            document.getElementById('slidesContainer').scrollTop = 0;
            if (window.CourseNav && CourseNav.setActiveSlide) CourseNav.setActiveSlide(currentSlide);
        }}
        function nextSlide() {{ if (currentSlide < totalSlides - 1) {{ currentSlide++; updateSlide(); }} }}
        function prevSlide() {{ if (currentSlide > 0) {{ currentSlide--; updateSlide(); }} }}
        function goToSlide(index) {{
            if (index >= 0 && index < totalSlides) {{ currentSlide = index; updateSlide(); }}
            return false;
        }}
        function speak() {{
            if (!slides[currentSlide].querySelector('.narration-box')) return;
            VietnameseTTS.speakSlide(ttsPage, currentSlide);
        }}
        function reset() {{ currentSlide = 0; updateSlide(); }}
        document.getElementById('nextBtn').addEventListener('click', nextSlide);
        document.getElementById('prevBtn').addEventListener('click', prevSlide);
        document.getElementById('speakBtn').addEventListener('click', speak);
        document.getElementById('resetBtn').addEventListener('click', reset);
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowRight') nextSlide();
            if (e.key === 'ArrowLeft') prevSlide();
        }});
        updateSlide();
    </script>
</body>
</html>
""".replace("</motion>", "</div>").replace("<motion ", "<div ")


def main() -> None:
    for cfg in LESSONS:
        path = ROOT / cfg["file"]
        old = path.read_text(encoding="utf-8")
        slides = extract_slides(old)
        nav = extract_nav_labels(old)
        if not slides:
            print("FAIL", cfg["file"])
            continue
        out = build_html(cfg, slides, build_sidebar(nav, cfg["meta"]))
        path.write_text(out, encoding="utf-8")
        print("OK", cfg["file"], "slides", len(re.findall(r'<motion class="slide', out.replace("<div class=", "<div class="))))


if __name__ == "__main__":
    main()
