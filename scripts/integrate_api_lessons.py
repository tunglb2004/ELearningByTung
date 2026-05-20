# -*- coding: utf-8 -*-
"""Tích hợp 3 bài API Testing vào layout chuẩn (giống PHASE/Selenium)."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHASE2 = ROOT / "phase2_selenium_webdriver.html"

API_EXTRA_CSS = """
        .info-box {
            background: #e3f2fd;
            border-left: 4px solid #2196f3;
            padding: 14px;
            margin: 15px 0;
            border-radius: 6px;
            font-size: 0.95em;
            line-height: 1.6;
        }
        .warning-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 14px;
            margin: 15px 0;
            border-radius: 6px;
            font-size: 0.95em;
            line-height: 1.6;
        }
        .success-box {
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 14px;
            margin: 15px 0;
            border-radius: 6px;
            font-size: 0.95em;
            line-height: 1.6;
        }
        .learning-objectives {
            background: #f0f8ff;
            border: 2px solid #2a5298;
            padding: 16px;
            border-radius: 8px;
            margin: 15px 0;
        }
        .learning-objectives h4 {
            color: #1e3c72;
            margin-bottom: 10px;
        }
        .learning-objectives ul {
            margin-left: 20px;
        }
        .recap-box {
            background: #e8f5e9;
            border: 2px solid #4caf50;
            padding: 16px;
            border-radius: 8px;
            margin: 15px 0;
        }
        .intro-box-inner {
            background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .slide h4 {
            color: #2a5298;
            font-size: 1.15em;
            margin-top: 16px;
            margin-bottom: 10px;
        }
"""

LESSONS = [
    {
        "src": Path(r"c:\Users\ADMIN\Downloads\API_Testing_Buoi_1_Lesson_Design.html"),
        "out": "api_testing_buoi1_fundamentals.html",
        "tts": "api1",
        "page_title": "API Testing — Buổi 1: Fundamentals & HTTP",
        "title": "🔌 API Testing — Buổi 1",
        "subtitle": "API Fundamentals · HTTP Protocol · REST · Test Design",
        "footer": "API Testing — Buổi 1: Fundamentals",
        "meta": "⏱️ ~5 giờ<br>📚 API Testing · Buổi 1<br>🌐 HTTP & REST",
    },
    {
        "src": Path(r"c:\Users\ADMIN\Downloads\TUAN_3_4_Advanced_API_Testing_Lesson_Design.html"),
        "out": "api_testing_advanced_auth.html",
        "tts": "api2",
        "page_title": "API Testing — Tuần 3-4: Auth & Security",
        "title": "🔐 API Testing — Tuần 3-4",
        "subtitle": "Authentication · Authorization · JWT · Security Testing",
        "footer": "API Testing — Tuần 3-4: Advanced",
        "meta": "⏱️ ~4 giờ<br>📚 API Testing · Tuần 3-4<br>🛡️ Auth & Security",
    },
    {
        "src": Path(r"c:\Users\ADMIN\Downloads\RESTASSURED_LESSON_DESIGN.html"),
        "out": "api_testing_restassured.html",
        "tts": "api3",
        "page_title": "API Testing — RestAssured Automation",
        "title": "⚡ API Testing — RestAssured",
        "subtitle": "RestAssured Framework · TestNG · POM · Data-Driven",
        "footer": "API Testing — RestAssured",
        "meta": "⏱️ ~4 giờ<br>📚 API Testing · Tuần 5-6<br>🤖 Automation",
    },
]


def extract_phase2_css() -> str:
    t = PHASE2.read_text(encoding="utf-8")
    m = re.search(r"<style>(.*?)</style>", t, re.DOTALL)
    if not m:
        raise RuntimeError("No style in phase2")
    return m.group(1).strip() + API_EXTRA_CSS


def clean_narration_text(raw: str) -> str:
    text = re.sub(r"<br\s*/?>", " ", raw, flags=re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("🔊", "")
    text = re.sub(r"🎤\s*Script[^:]*:\s*", "", text, flags=re.I)
    text = re.sub(r"🎤\s*Script\s+Kết\s+Thúc:\s*", "", text, flags=re.I)
    text = re.sub(r"\s+", " ", text).strip().strip("\"'“”")
    return text


def normalize_narration_boxes(content: str) -> str:
    def repl(m: re.Match[str]) -> str:
        text = clean_narration_text(m.group(2))
        if not text:
            return m.group(0)
        safe = html.escape(text, quote=False)
        return f'<div class="narration-box">🔊 "{safe}"</div>'

    return re.sub(
        r'(<div class="narration-box">)(.*?)(</div>)',
        repl,
        content,
        flags=re.DOTALL | re.IGNORECASE,
    )


def parse_slide_markers(html: str) -> list[tuple[str, str]]:
    """Return [(title, block_html), ...]"""
    markers = list(re.finditer(r"<!--\s*SLIDE\s+(\d+)[:\s]+([^>]+?)\s*-->", html, re.I))
    chunks: list[tuple[str, str]] = []
    for i, m in enumerate(markers):
        num = m.group(1)
        title = m.group(2).strip()
        start = m.start()
        if i + 1 < len(markers):
            end = markers[i + 1].start()
        else:
            tail = html[start:]
            stop = re.search(r'<!--\s*SIDEBAR|<div class="sidebar|<script\s+', tail, re.I)
            end = start + stop.start() if stop else len(html)
        block = html[start:end]
        block = re.split(r'<div class="sidebar', block, maxsplit=1)[0].strip()
        label = f"{int(num) - 1}. {title}" if num.isdigit() else f"{num}. {title}"
        chunks.append((label, block))
    return chunks


def extract_slides(html: str) -> tuple[str, list[str]]:
    chunks = parse_slide_markers(html)
    if not chunks:
        raise ValueError("No SLIDE markers found")
    nav = [t for t, _ in chunks]
    body = "\n\n                ".join(b for _, b in chunks)
    body = normalize_narration_boxes(body)
    if not re.search(r'class="slide active"', body):
        body = body.replace('class="slide"', 'class="slide active"', 1)
    return body, nav


def build_sidebar(nav: list[str], meta: str) -> str:
    links = "\n".join(
        f'                        <li><a href="#" onclick="return goToSlide({i})">{lb}</a></li>'
        for i, lb in enumerate(nav)
    )
    total = len(nav) or 1
    meta_html = meta.replace("<br>", "<br>\n                        ")
    return f"""            <div class="sidebar">
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
                <div class="slide-counter">
                    <div id="slideCount">1 / {total}</div>
                </div>
                <div class="progress-bar" style="margin: 20px 0;">
                    <div class="progress-fill" id="sidebarProgress"></div>
                </div>
                <div data-course-nav></div>
                <div class="slide-nav-section">
                    <h3 class="slide-nav-heading">📑 Slide trong bài</h3>
                    <ul class="nav-links">
{links}
                    </ul>
                </div>
                <div style="margin-top: auto; padding-top: 20px; border-top: 1px solid #ddd;">
                    <p style="font-size: 0.85em; color: #666; text-align: center;">
                        {meta_html}
                    </p>
                </div>
            </div>"""


def build_html(cfg: dict, css: str, slides: str, sidebar: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cfg["page_title"]}</title>
    <style>
{css}
    </style>
    <link rel="stylesheet" href="narration-editor.css">
    <link rel="stylesheet" href="course-audio-player.css">
    <link rel="stylesheet" href="course-code-blocks.css">
    <link rel="stylesheet" href="course-nav.css?v=2">
</head>
<body data-tts-page="{cfg["tts"]}">
    <div class="container">
        <div class="header">
            <h1>{cfg["title"]}</h1>
            <p>{cfg["subtitle"]}</p>
            <p style="margin-top: 14px;"><a href="index.html" style="color: white; text-decoration: none; opacity: 0.95;">🏠 Trang chủ</a></p>
        </div>
        <div style="display: flex; margin-bottom: 20px; padding: 0 30px; padding-top: 20px;">
            <div style="flex: 1;">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
            </div>
        </div>
        <div class="content">
            <div class="slides" id="slidesContainer">
{slides}
            </div>
{sidebar}
        </div>
        <div class="footer">
            <p>© 2025 Automation Testing & Java Core | {cfg["footer"]} | Tất cả quyền được bảo lưu</p>
        </div>
    </div>
    <script src="vietnamese-tts.js"></script>
    <script src="narration-editor.js"></script>
    <script src="course-nav.js?v=4"></script>
    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slides .slide');
        const totalSlides = slides.length;
        const ttsPage = document.body.dataset.ttsPage;
        function updateSlide() {{
            VietnameseTTS.stop();
            slides.forEach((slide, index) => {{
                slide.classList.toggle('active', index === currentSlide);
            }});
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
"""


def main() -> None:
    css = extract_phase2_css()
    for lesson in LESSONS:
        src = lesson["src"]
        if not src.exists():
            print("MISSING", src)
            continue
        raw = src.read_text(encoding="utf-8")
        slides, nav = extract_slides(raw)
        sidebar = build_sidebar(nav, lesson["meta"])
        out_html = build_html(lesson, css, slides, sidebar)
        # fix motion typos from template
        out_html = out_html.replace("<div ", "<div ").replace("</div>", "</div>")
        dest = ROOT / lesson["out"]
        dest.write_text(out_html, encoding="utf-8")
        print("OK", lesson["out"], len(nav), "slides")
    print("done")


if __name__ == "__main__":
    main()
