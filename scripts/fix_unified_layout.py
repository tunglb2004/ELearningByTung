# -*- coding: utf-8 -*-
"""Sửa layout bài học: 2 cột slides + sidebar như Automation PHASE."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PHASE2 = ROOT / "phase2_selenium_webdriver.html"

JAVA_FILES = [
    "part1_oop_principles.html",
    "java_core_phase2_collections.html",
    "java_core_phase3_4_advanced.html",
]

LESSON_FILES = [
    "part1_oop_principles.html",
    "java_core_phase2_collections.html",
    "java_core_phase3_4_advanced.html",
    "video1_manual_vs_automation.html",
    "video2_4_types_testing.html",
    "phase2_selenium_webdriver.html",
    "phase3_testng_pom.html",
    "phase4_advanced_cicd.html",
]


def extract_phase2_css() -> str:
    t = PHASE2.read_text(encoding="utf-8")
    m = re.search(r"<style>(.*?)</style>", t, re.DOTALL)
    if not m:
        raise RuntimeError("No style in phase2")
    return m.group(1).strip()


def extract_slides(html: str) -> str:
    markers = list(re.finditer(r"<!-- SLIDE \d+", html))
    if markers:
        chunks: list[str] = []
        for i, m in enumerate(markers):
            start = m.start()
            if i + 1 < len(markers):
                end = markers[i + 1].start()
            else:
                tail = html[start:]
                stop = re.search(r'<div class="sidebar|<script\s+src=', tail)
                end = start + stop.start() if stop else len(html)
            block = html[start:end]
            block = re.split(r'<div class="sidebar', block, maxsplit=1)[0].strip()
            chunks.append(block)
        return "\n\n                ".join(chunks)

    m = re.search(r'id="slidesContainer"[^>]*>(.*)', html, re.DOTALL)
    if not m:
        return ""
    region = re.split(r'<div class="sidebar', m.group(1), maxsplit=1)[0]
    slides = _extract_slide_divs(region)
    return "\n\n                ".join(slides) if slides else region.strip()


def _extract_slide_divs(region: str) -> list[str]:
    slides: list[str] = []
    pos = 0
    while pos < len(region):
        m = re.search(r'<div class="slide(?:\s+active)?[^>]*>', region[pos:])
        if not m:
            break
        start = pos + m.start()
        if re.match(r'<div class="sidebar', region[start:]):
            break
        depth = 0
        i = start
        while i < len(region):
            if region.startswith('<div class="sidebar', i):
                break
            open_m = re.match(r"<div[^>]*>", region[i:])
            if open_m:
                depth += 1
                i += len(open_m.group(0))
                continue
            if region.startswith("</div>", i):
                depth -= 1
                i += 6
                if depth == 0:
                    slides.append(region[start:i])
                    pos = i
                    break
                continue
            i += 1
        else:
            break
    return slides


def extract_nav_labels(html: str) -> list[str]:
    labels = re.findall(r"goToSlide\(\d+\)[^>]*>([^<]+)</a>", html)
    return [x.strip() for x in labels] if labels else []


def extract_meta(html: str) -> str:
    m = re.search(r'class="sidebar-meta"[^>]*>(.*?)</p>', html, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(
        r'margin-top: auto[^>]*>.*?<p[^>]*>(.*?)</p>\s*</div>\s*</motion>\s*</motion>\s*<div class="footer"',
        html,
        re.DOTALL,
    )
    if m:
        return m.group(1).strip()
    return ""


def build_sidebar(nav: list[str], meta: str, btn_prev: str = "⬅️ Trước", btn_next: str = "Tiếp ➡️") -> str:
    links = "\n".join(
        f'                        <li><a href="#" onclick="return goToSlide({i})">{lb}</a></li>'
        for i, lb in enumerate(nav)
    )
    total = len(nav) or 1
    meta_html = meta.replace("<br>", "<br>\n                        ")
    return f"""            <div class="sidebar">
                <div class="controls">
                    <button class="btn-primary" id="prevBtn">{btn_prev}</button>
                    <button class="btn-primary" id="nextBtn">{btn_next}</button>
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


JAVA_META = {
    "part1_oop_principles.html": {
        "tts": "oop1",
        "title": "☕ Java Core — Phần 1: OOP Principles",
        "subtitle": "Encapsulation · Inheritance · Polymorphism · Abstraction",
        "footer": "Java Core — Phần 1: OOP Principles",
        "meta": "⏱️ ~35 phút<br>📚 Java Core — Phần 1<br>☕ OOP Principles",
        "page_title": "Java Core — Phần 1: OOP Principles",
    },
    "java_core_phase2_collections.html": {
        "tts": "java2",
        "title": "☕ Java Core — Phần 2: Collections",
        "subtitle": "List · Set · Map — Collections Framework",
        "footer": "Java Core — Phần 2: Collections",
        "meta": "⏱️ ~40 phút<br>📚 Java Core — Phần 2<br>📦 Collections",
        "page_title": "Java Core — Phần 2: Collections",
    },
    "java_core_phase3_4_advanced.html": {
        "tts": "java34",
        "title": "☕ Java Core — Phần 3–4: Advanced Java",
        "subtitle": "Exception · Streams · File I/O · Strings",
        "footer": "Java Core — Phần 3–4: Advanced Java",
        "meta": "⏱️ ~45 phút<br>📚 Java Core — Phần 3–4<br>⚡ Advanced",
        "page_title": "Java Core — Phần 3–4: Advanced Java",
    },
}


def build_java_html(cfg: dict, css: str, slides: str, sidebar: str) -> str:
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
    <link rel="stylesheet" href="course-nav.css">
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
    <script src="course-nav.js?v=3"></script>
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


def fix_broken_progress(html: str) -> str:
    return re.sub(
        r'(<div class="progress-bar"[^>]*>)\s*<div class="progress-fill" id="sidebarProgress"></div>\s*(?=<div data-course-nav)',
        r'\1<div class="progress-fill" id="sidebarProgress"></div></div>\n                ',
        html,
        count=1,
    )


def patch_automation_files() -> None:
    for name in [
        "video1_manual_vs_automation.html",
        "video2_4_types_testing.html",
        "phase2_selenium_webdriver.html",
        "phase3_testng_pom.html",
        "phase4_advanced_cicd.html",
    ]:
        path = ROOT / name
        t = path.read_text(encoding="utf-8")
        orig = t
        t = t.replace('class="sidebar lesson-sidebar"', 'class="sidebar"')
        t = t.replace(
            'class="sidebar-section slide-nav-section"',
            'class="slide-nav-section"',
        )
        t = re.sub(
            r'<p class="sidebar-meta">(.*?)</p>',
            r'<div style="margin-top: auto; padding-top: 20px; border-top: 1px solid #ddd;">\n'
            r'                    <p style="font-size: 0.85em; color: #666; text-align: center;">\1</p>\n'
            r"                </div>",
            t,
            flags=re.DOTALL,
        )
        if "querySelectorAll('.slides .slide')" not in t:
            t = t.replace(
                "document.querySelectorAll('.slide')",
                "document.querySelectorAll('.slides .slide')",
            )
        if t != orig:
            path.write_text(t, encoding="utf-8")
            print("patched", name)


def main() -> None:
    css = extract_phase2_css()
    for fname, cfg in JAVA_META.items():
        path = ROOT / fname
        old = path.read_text(encoding="utf-8")
        slides = extract_slides(old)
        if not slides:
            print("FAIL slides", fname)
            continue
        slides = slides.replace('class="code-block"', 'class="code-example"')
        nav = extract_nav_labels(old) or [f"Slide {i}" for i in range(len(re.findall(r'<div class="slide', slides)))]
        meta = cfg["meta"]
        sidebar = build_sidebar(nav, meta)
        out = build_java_html(cfg, css, slides, sidebar)
        path.write_text(out, encoding="utf-8")
        print("rebuilt", fname)

    patch_automation_files()
    print("done")


if __name__ == "__main__":
    main()
