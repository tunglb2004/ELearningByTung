# -*- coding: utf-8 -*-
"""Chuyển bài Java Review (tab) sang slide + UI khóa học (giống OOP)."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_CSS = ROOT / "part1_oop_principles.html"

EXTRA_CSS = """
        .comparison-table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 0.95em; }
        .comparison-table th { background: #667eea; color: white; padding: 10px; text-align: left; }
        .comparison-table td { padding: 10px; border-bottom: 1px solid #e2e8f0; }
        .comparison-table tr:hover { background: #f8fafc; }
        .code-block {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 18px;
            border-radius: 10px;
            overflow-x: auto;
            margin: 18px 0;
            font-family: 'Courier New', monospace;
            font-size: 0.88em;
            line-height: 1.6;
            border-left: 5px solid #764ba2;
        }
        .section-body p { margin-bottom: 12px; }
        .section-body ul { margin-left: 28px; margin-bottom: 12px; }
        .flow-diagram {
            background: #f8fafc;
            padding: 18px;
            border-radius: 8px;
            margin: 15px 0;
            border: 2px solid #667eea;
        }
        .flow-arrow { text-align: center; font-size: 1.1em; margin: 8px 0; color: #667eea; }
        .learning-objectives {
            background: #eef2ff;
            padding: 18px;
            border-left: 4px solid #667eea;
            margin: 18px 0;
            border-radius: 8px;
        }
        .learning-objectives h3 { color: #667eea; margin-bottom: 12px; }
        .learning-objectives ul { list-style: none; padding-left: 0; }
        .learning-objectives li {
            padding: 6px 0 6px 28px;
            position: relative;
        }
        .learning-objectives li::before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #667eea;
            font-weight: bold;
        }
        .intro-box-inner {
            background: linear-gradient(135deg, #ede9fe 0%, #f3e8ff 100%);
            color: #4c1d95;
            padding: 18px;
            border-radius: 8px;
            margin-bottom: 18px;
        }
        .intro-box-inner h2 { font-size: 1.3em; margin-bottom: 10px; color: #5b21b6; }
        .recap-box {
            background: #eef2ff;
            padding: 20px;
            border-left: 4px solid #667eea;
            border-radius: 8px;
        }
        .recap-box h3 { color: #667eea; margin-bottom: 10px; }
"""

SLIDE_SCRIPT = """
    <script src="vietnamese-tts.js"></script>
    <script src="narration-editor.js"></script>
    <script src="course-nav.js"></script>
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


def load_base_css() -> str:
    text = TEMPLATE_CSS.read_text(encoding="utf-8")
    m = re.search(r"<style>(.*?)</style>", text, re.DOTALL)
    if not m:
        raise RuntimeError("Khong tim thay CSS trong part1_oop_principles.html")
    return m.group(1) + EXTRA_CSS


def extract_block(src: str, class_name: str) -> str:
    m = re.search(rf'<motion class="{class_name}">(.*?)</motion>', src, re.DOTALL)
    if not m:
        m = re.search(rf'<div class="{class_name}">(.*?)</div>', src, re.DOTALL)
    return m.group(1).strip() if m else ""


def extract_tab(src: str, tab_id: str, next_marker: str) -> str:
    open_m = re.search(rf'<div id="{tab_id}" class="tab-content[^"]*">', src)
    if not open_m:
        return ""
    start = open_m.end()
    end_m = re.search(next_marker, src[start:], re.DOTALL)
    if not end_m:
        return ""
    body = src[start : start + end_m.start()].rstrip()
    body = re.sub(r"</div>\s*$", "", body, count=1)
    return body.strip()


def extract_tabs_ordered(src: str, tab_ids: list[str]) -> list[str]:
    out: list[str] = []
    for i, tid in enumerate(tab_ids):
        if i + 1 < len(tab_ids):
            nxt = rf'(?=<div id="{tab_ids[i + 1]}" class="tab-content)'
        else:
            nxt = r'(?=<motion style="margin-top: 40px)'
        nxt = nxt.replace("<motion", "<div")
        body = extract_tab(src, tid, nxt)
        out.append(body)
    return out


def extract_recap_inner(src: str) -> str:
    m = re.search(
        r'<div style="margin-top: 40px; padding: 20px; background: #f0f4ff[^"]*">(.*?)</div>\s*</div>\s*<div class="sidebar">',
        src,
        re.DOTALL,
    )
    return m.group(1).strip() if m else ""


def fix_content_html(fragment: str) -> str:
    fragment = fragment.replace('class="section-title"', "")
    fragment = fragment.replace('class="section-content"', 'class="section-body"')
    return fragment.strip()


def build_slide(active: bool, body: str, narration: str) -> str:
    cls = "slide active" if active else "slide"
    safe = html.escape(narration.strip(), quote=False)
    return (
        f'                <div class="{cls}">\n'
        f"{body}\n"
        f'                    <motion class="narration-box">🔊 "{safe}"</motion>\n'
        f"                </motion>\n"
    ).replace("<motion ", "<div ").replace("</motion>", "</div>")


def build_sidebar(nav_items: list[str], meta: str, total: int) -> str:
    links = "\n".join(
        f'                        <li><a href="#" onclick="return goToSlide({i})">{html.escape(label, quote=False)}</a></li>'
        for i, label in enumerate(nav_items)
    )
    return f"""            <motion class="sidebar">
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
                <div class="slide-counter"><div id="slideCount">1 / {total}</div></div>
                <div class="progress-bar" style="margin: 20px 0;"><div class="progress-fill" id="sidebarProgress"></div></div>
                <div data-course-nav></div>
                <div class="sidebar-section slide-nav-section" style="max-height: 280px; overflow-y: auto;">
                    <h3 class="slide-nav-heading">📑 Slide trong bài</h3>
                    <ul class="nav-links">
{links}
                    </ul>
                </div>
                <div style="margin-top: auto; padding-top: 20px; border-top: 1px solid #ddd;">
                    <p style="font-size: 0.85em; color: #666; text-align: center;">{meta}</p>
                </div>
            </div>
""".replace("<motion class=", "<div class=").replace("</motion>", "")


def build_lesson(cfg: dict) -> str:
    src = Path(cfg["src"]).read_text(encoding="utf-8")
    intro = extract_block(src, "intro-box")
    objectives = extract_block(src, "learning-objectives")
    tabs = extract_tabs_ordered(src, cfg["tab_ids"])
    recap_inner = extract_recap_inner(src)
    narrations: list[str] = cfg["narrations"]
    nav_labels: list[str] = cfg["nav_labels"]

    slides: list[str] = []
    intro_body = f"""
                    <div class="intro-box-inner">{intro}</div>
                    <div class="learning-objectives">{objectives}</div>
"""
    slides.append(build_slide(True, intro_body, narrations[0]))
    for idx, tab_html in enumerate(tabs):
        slides.append(build_slide(False, fix_content_html(tab_html), narrations[idx + 1]))
    recap_body = f'                    <div class="recap-box">{recap_inner}</motion>'
    recap_body = recap_body.replace("</motion>", "</div>")
    slides.append(build_slide(False, recap_body, narrations[-1]))

    total = len(slides)
    css = load_base_css()
    sidebar = build_sidebar(nav_labels, cfg["sidebar_meta"], total)

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cfg["title"]}</title>
    <style>
{css}
    </style>
    <link rel="stylesheet" href="narration-editor.css">
    <link rel="stylesheet" href="course-audio-player.css">
    <link rel="stylesheet" href="course-code-blocks.css">
    <link rel="stylesheet" href="course-nav.css">
</head>
<body data-tts-page="{cfg["tts_page"]}">
    <div class="container">
        <div class="header">
            <h1>{cfg["header_h1"]}</h1>
            <p>{cfg["header_p"]}</p>
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
{"".join(slides)}
            </div>
{sidebar}
        </div>
        <div class="footer">
            <p>© 2025 Automation Testing & Java Core | {cfg["footer"]} | Tất cả quyền được bảo lưu</p>
        </div>
    </div>
{SLIDE_SCRIPT.strip()}
</body>
</html>
"""


LESSONS = [
    {
        "src": r"c:\Users\ADMIN\Downloads\java_review_phase2_collections.html",
        "out": "java_core_phase2_collections.html",
        "tts_page": "java2",
        "tab_ids": ["list", "set", "map", "comparison"],
        "title": "Phần 2: Collections — Java Core",
        "header_h1": "☕ Phần 2: Collections",
        "header_p": "Java Core — List, Set, Map",
        "footer": "Phần 2: Collections",
        "sidebar_meta": "⏱️ ~40 phút<br>📚 Java Core — Phần 2<br>📦 Collections",
        "nav_labels": ["0. Giới thiệu", "1. List", "2. Set", "3. Map", "4. So sánh", "5. Tóm tắt"],
        "narrations": [
            "Chào mừng đến với phần Collections trong Java Core. Collections Framework giúp bạn lưu trữ và xử lý tập hợp dữ liệu linh hoạt hơn mảng cố định. Trong bài này chúng ta học List cho dữ liệu có thứ tự, Set cho giá trị duy nhất, và Map cho cặp khóa-giá trị.",
            "List là collection có thứ tự, truy cập theo index và cho phép trùng lặp. ArrayList phù hợp truy cập nhanh theo index, LinkedList phù hợp chèn xóa nhiều.",
            "Set không cho phép phần tử trùng. Dùng Set khi cần danh sách browser duy nhất, test ID không trùng, hoặc kiểm tra nhanh phần tử đã tồn tại.",
            "Map lưu cặp key-value với key duy nhất. HashMap tra cứu O(1) phù hợp lưu locator, cấu hình username-password, hoặc map tên test sang trạng thái.",
            "So sánh List, Set và Map: List có thứ tự và cho duplicate; Set unique; Map tra cứu theo key. Trong framework test, thường kết hợp cả ba.",
            "Tóm lại, chọn đúng collection cho đúng bài toán. Tiếp theo học Exception Handling và Streams ở phần 3-4.",
        ],
    },
    {
        "src": r"c:\Users\ADMIN\Downloads\java_review_phase3_4_advanced.html",
        "out": "java_core_phase3_4_advanced.html",
        "tts_page": "java34",
        "tab_ids": ["exception", "streams", "fileio", "strings"],
        "title": "Phần 3–4: Advanced Java — Java Core",
        "header_h1": "☕ Phần 3–4: Advanced Java",
        "header_p": "Exception, Streams, File I/O & String",
        "footer": "Phần 3–4: Advanced Java",
        "sidebar_meta": "⏱️ ~45 phút<br>📚 Java Core — Phần 3–4<br>⚡ Advanced",
        "nav_labels": ["0. Giới thiệu", "1. Exceptions", "2. Streams & Lambda", "3. File I/O", "4. Strings", "5. Tổng kết"],
        "narrations": [
            "Phần Advanced Java bổ sung xử lý lỗi, streams, file I/O và string manipulation — nền tảng trước khi vào automation chuyên sâu.",
            "Exception Handling giúp chương trình không crash. Dùng try-catch-finally để log lỗi, chụp screenshot khi test fail, và cleanup trong finally.",
            "Lambda và Stream API giúp filter, map, reduce trên collection — lọc test fail, group theo status, transform data trước assert.",
            "File I/O đọc CSV test data và ghi báo cáo. Dùng try-with-resources để đóng stream an toàn.",
            "String methods: trim, contains, split, replace khi verify UI; StringBuilder khi nối chuỗi trong vòng lặp.",
            "Bạn đã hoàn thành Java Core. Chuyển sang bài Manual vs Automation để bắt đầu lộ trình automation.",
        ],
    },
]


def main() -> None:
    for cfg in LESSONS:
        out_path = ROOT / cfg["out"]
        html_out = build_lesson(cfg)
        html_out = html_out.replace("<motion ", "<div ").replace("</motion>", "")
        out_path.write_text(html_out, encoding="utf-8")
        n_slides = len(re.findall(r'<div class="slide', html_out))
        n_narr = html_out.count('class="narration-box">🔊')
        print(f"OK {cfg['out']}: slides={n_slides}, narrations={n_narr}")


if __name__ == "__main__":
    main()
