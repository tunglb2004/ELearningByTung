"""Thư viện đọc/ghi script thuyết minh và tạo file MP3 (Edge TTS)."""
from __future__ import annotations

import asyncio
import hashlib
import html
import json
import re
from pathlib import Path

import edge_tts
from edge_tts.exceptions import NoAudioReceived

from bilingual_text import segment_text

ROOT = Path(__file__).resolve().parent.parent
AUDIO_DIR = ROOT / "audio"
MANIFEST_PATH = AUDIO_DIR / "manifest.json"
VOICE_VI = "vi-VN-HoaiMyNeural"
VOICE_EN = "en-US-AriaNeural"
VOICE = VOICE_VI
MAX_RETRIES = 4
MAX_CONCURRENT_REGENERATE = 4
HASHES_PATH = AUDIO_DIR / "narration-hashes.json"

PAGE_FILES: dict[str, str] = {
    "index": "index.html",
    "oop1": "part1_oop_principles.html",
    "java2": "java_core_phase2_collections.html",
    "java34": "java_core_phase3_4_advanced.html",
    "video1": "video1_manual_vs_automation.html",
    "video2": "video2_4_types_testing.html",
    "phase2": "phase2_selenium_webdriver.html",
    "phase3": "phase3_testng_pom.html",
    "phase4": "phase4_advanced_cicd.html",
    "api1": "api_testing_buoi1_fundamentals.html",
    "api2": "api_testing_advanced_auth.html",
    "api3": "api_testing_restassured.html",
}

PAGE_ORDER: tuple[str, ...] = (
    "index",
    "oop1",
    "java2",
    "java34",
    "video1",
    "video2",
    "phase2",
    "phase3",
    "phase4",
    "api1",
    "api2",
    "api3",
)

PAGE_LABELS: dict[str, str] = {
    "index": "Trang chủ",
    "oop1": "Java Core — Phần 1: OOP Principles",
    "java2": "Java Core — Phần 2: Collections",
    "java34": "Java Core — Phần 3–4: Advanced Java",
    "video1": "PHASE 1 — Bài 1: Manual vs Automation",
    "video2": "PHASE 1 — Bài 2: 4 Loại Test",
    "phase2": "PHASE 2 — Selenium WebDriver",
    "phase3": "PHASE 3 — TestNG & POM",
    "phase4": "PHASE 4 — Advanced & CI/CD",
    "api1": "API Testing — Buổi 1: Fundamentals & HTTP",
    "api2": "API Testing — Tuần 3-4: Auth & Security",
    "api3": "API Testing — RestAssured Automation",
}

MODULES: tuple[dict, ...] = (
    {"id": "java", "title": "☕ Java Core", "pages": ("oop1", "java2", "java34")},
    {"id": "api", "title": "🔌 API Testing", "pages": ("api1", "api2", "api3")},
    {
        "id": "auto",
        "title": "🤖 Automation",
        "pages": ("video1", "video2", "phase2", "phase3", "phase4"),
    },
)

PAGE_MODULE: dict[str, str] = {
    "index": "intro",
    "oop1": "java",
    "java2": "java",
    "java34": "java",
    "video1": "auto",
    "video2": "auto",
    "phase2": "auto",
    "phase3": "auto",
    "phase4": "auto",
    "api1": "api",
    "api2": "api",
    "api3": "api",
}

SLIDE_SPLIT = re.compile(r'(?=<div class="slide(?:\s|"|>))')
SLIDE_OPEN = re.compile(r'^<div class="slide(?:\s|"|>)')
NARRATION_BOX = re.compile(
    r'(<div class="narration-box">)(.*?)(</div>)',
    re.DOTALL | re.IGNORECASE,
)
INTRO_BOX = re.compile(
    r'(id="introNarration"[^>]*>)(.*?)(</div>)',
    re.DOTALL | re.IGNORECASE,
)
SCRIPT_GIANG = re.compile(
    r'<strong>\s*🎤\s*Script Giảng:\s*</strong>\s*["\u201c](.*?)["\u201d]',
    re.DOTALL | re.IGNORECASE,
)
SCRIPT_BOX_BLOCK = re.compile(
    r'<div class="script-box">\s*<strong>\s*🎤\s*Script Giảng:\s*</strong>\s*["\u201c].*?["\u201d]\s*</div>',
    re.DOTALL | re.IGNORECASE,
)


def clean_narration(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw)
    text = text.replace("🔊", "")
    text = re.sub(r"\s+", " ", text).strip()
    return text.strip("\"'“”")


def format_narration_html(text: str) -> str:
    safe = html.escape(text.strip(), quote=False)
    return f'🔊 "{safe}"'


def read_html(page: str) -> str:
    if page not in PAGE_FILES:
        raise ValueError(f"Trang không hợp lệ: {page}")
    return (ROOT / PAGE_FILES[page]).read_text(encoding="utf-8")


def write_html(page: str, content: str) -> None:
    (ROOT / PAGE_FILES[page]).write_text(content, encoding="utf-8")


def _extract_slide_narration(chunk: str) -> str:
    m = NARRATION_BOX.search(chunk)
    if m:
        text = clean_narration(m.group(2))
        if text:
            return text
    sg = SCRIPT_GIANG.search(chunk)
    if sg:
        text = clean_narration(sg.group(1))
        if text:
            return text
    return ""


def extract_slides_narrations(html: str) -> dict[int, str]:
    narrations: dict[int, str] = {}
    slide_idx = -1
    for chunk in SLIDE_SPLIT.split(html):
        if not SLIDE_OPEN.match(chunk):
            continue
        slide_idx += 1
        text = _extract_slide_narration(chunk)
        if text:
            narrations[slide_idx] = text
    return narrations


def extract_index_intro(html: str) -> str:
    m = INTRO_BOX.search(html)
    return clean_narration(m.group(2)) if m else ""


def get_narration(page: str, key: str) -> str:
    html_content = read_html(page)
    if page == "index":
        if key != "intro":
            raise ValueError("index chỉ có key intro")
        return extract_index_intro(html_content)
    slide_idx = int(key)
    narrations = extract_slides_narrations(html_content)
    if slide_idx not in narrations:
        raise KeyError(f"Không có thuyết minh slide {key} trên {page}")
    return narrations[slide_idx]


def replace_slide_narration(html_content: str, slide_idx: int, new_text: str) -> str:
    """Ghi script vào đúng slide theo chỉ số (khớp với currentSlide trên UI)."""
    inner = "\n                        " + format_narration_html(new_text) + "\n                    "
    parts = SLIDE_SPLIT.split(html_content)
    slide_num = -1
    rebuilt: list[str] = []
    for part in parts:
        if SLIDE_OPEN.match(part):
            slide_num += 1
            if slide_num == slide_idx:
                part, count = re.subn(
                    r'(<div class="narration-box">)(.*?)(</div>)',
                    lambda m: m.group(1) + inner + m.group(3),
                    part,
                    count=1,
                    flags=re.DOTALL | re.IGNORECASE,
                )
                if count == 0:
                    box_html = (
                        "\n                    <div class=\"narration-box\">"
                        + format_narration_html(new_text)
                        + "</div>\n                "
                    )
                    part, count = SCRIPT_BOX_BLOCK.subn(box_html, part, count=1)
                if count == 0:
                    part, count = re.subn(
                        r'<strong>\s*🎤\s*Script Giảng:\s*</strong>\s*["\u201c].*?["\u201d]',
                        format_narration_html(new_text),
                        part,
                        count=1,
                        flags=re.DOTALL | re.IGNORECASE,
                    )
                if count == 0:
                    part = (
                        part.rstrip()
                        + "\n                    <div class=\"narration-box\">"
                        + format_narration_html(new_text)
                        + "</div>\n                "
                    )
        rebuilt.append(part)
    if slide_num < slide_idx:
        raise IndexError(f"Slide {slide_idx} không tồn tại")
    return "".join(rebuilt)


def replace_index_intro(html_content: str, new_text: str) -> str:
    m = INTRO_BOX.search(html_content)
    if not m:
        raise ValueError("Không tìm thấy introNarration")
    inner = "\n                    " + format_narration_html(new_text) + "\n                "
    return html_content[: m.start(2)] + inner + html_content[m.end(2) :]


def update_narration_text(page: str, key: str, new_text: str) -> None:
    new_text = new_text.strip()
    if not new_text:
        raise ValueError("Nội dung thuyết minh không được rỗng")
    html_content = read_html(page)
    if page == "index":
        updated = replace_index_intro(html_content, new_text)
    else:
        updated = replace_slide_narration(html_content, int(key), new_text)
    write_html(page, updated)


def audio_relative_path(page: str, key: str) -> str:
    if page == "index":
        return "audio/index/intro.mp3"
    return f"audio/{page}/{key}.mp3"


def segment_relative_path(page: str, key: str, index: int) -> str:
    if page == "index":
        return f"audio/index/intro-seg-{index}.mp3"
    return f"audio/{page}/{key}-seg-{index}.mp3"


def audio_absolute_path(page: str, key: str) -> Path:
    return ROOT / audio_relative_path(page, key)


def segment_absolute_path(page: str, key: str, index: int) -> Path:
    return ROOT / segment_relative_path(page, key, index)


def _clear_audio_for_key(page: str, key: str) -> None:
    if page == "index":
        pattern = "intro*.mp3"
        folder = AUDIO_DIR / "index"
    else:
        pattern = f"{key}*.mp3"
        folder = AUDIO_DIR / page
    if folder.exists():
        for f in folder.glob(pattern):
            f.unlink()


def load_manifest() -> dict:
    if MANIFEST_PATH.exists():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return {}


def save_manifest(manifest: dict) -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_hashes() -> dict:
    if HASHES_PATH.exists():
        return json.loads(HASHES_PATH.read_text(encoding="utf-8"))
    return {}


def save_hashes(hashes: dict) -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    HASHES_PATH.write_text(
        json.dumps(hashes, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def update_manifest_entry(page: str, key: str, segment_paths: list[str] | None = None) -> None:
    manifest = load_manifest()
    if page not in manifest:
        manifest[page] = {}
    if segment_paths and len(segment_paths) > 1:
        manifest[page][str(key)] = {"segments": segment_paths}
    elif segment_paths:
        manifest[page][str(key)] = segment_paths[0]
    else:
        manifest[page][str(key)] = audio_relative_path(page, key)
    save_manifest(manifest)


def get_manifest_audio_paths(page: str, key: str) -> list[str]:
    manifest = load_manifest()
    entry = manifest.get(page, {}).get(str(key))
    if isinstance(entry, dict) and entry.get("segments"):
        return entry["segments"]
    if isinstance(entry, str):
        return [entry]
    return [audio_relative_path(page, key)]


def narration_hash(text: str) -> str:
    normalized = clean_narration(text)
    return hashlib.sha1(normalized.encode("utf-8")).hexdigest()


def get_hash_entry(page: str, key: str) -> str | None:
    hashes = load_hashes()
    return hashes.get(page, {}).get(str(key))


def update_hash_entry(page: str, key: str, text: str) -> None:
    hashes = load_hashes()
    if page not in hashes:
        hashes[page] = {}
    hashes[page][str(key)] = narration_hash(text)
    save_hashes(hashes)


def audio_paths_exist(paths: list[str]) -> bool:
    return all((ROOT / p).exists() for p in paths)


def remove_manifest_entry(page: str, key: str) -> None:
    manifest = load_manifest()
    if page in manifest and str(key) in manifest[page]:
        del manifest[page][str(key)]
        if not manifest[page]:
            del manifest[page]
        save_manifest(manifest)


async def _synthesize_voice(text: str, voice: str, out_path: Path) -> None:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(str(out_path))
            return
        except NoAudioReceived:
            if attempt == MAX_RETRIES:
                raise
            await asyncio.sleep(attempt * 2)


async def synthesize_bilingual(page: str, key: str, text: str) -> list[str]:
    """Tạo MP3 theo đoạn Việt/Anh; trả về danh sách đường dẫn (phát tuần tự trên trình duyệt)."""
    parts = segment_text(text)
    if not parts:
        raise ValueError("Không có nội dung để đọc")

    rel_paths: list[str] = []
    for i, (lang, seg) in enumerate(parts):
        voice = VOICE_EN if lang == "en" else VOICE_VI
        out = segment_absolute_path(page, key, i)
        out.parent.mkdir(parents=True, exist_ok=True)
        await _synthesize_voice(seg, voice, out)
        rel_paths.append(segment_relative_path(page, key, i))

    if len(parts) == 1:
        single = audio_absolute_path(page, key)
        single.write_bytes(segment_absolute_path(page, key, 0).read_bytes())
        rel_paths = [audio_relative_path(page, key)]

    return rel_paths


async def regenerate_audio(
    page: str, key: str, text: str | None = None, persist_manifest: bool = True
) -> str | list[str]:
    if text is None:
        text = get_narration(page, key)
    current_hash = narration_hash(text)
    saved_hash = get_hash_entry(page, key)
    existing_paths = get_manifest_audio_paths(page, key)
    if saved_hash == current_hash and audio_paths_exist(existing_paths):
        return existing_paths[0] if len(existing_paths) == 1 else existing_paths
    _clear_audio_for_key(page, key)
    rel_paths = await synthesize_bilingual(page, key, text)
    if persist_manifest:
        update_manifest_entry(page, key, rel_paths)
        update_hash_entry(page, key, text)
    return rel_paths if len(rel_paths) > 1 else rel_paths[0]


def list_all_narrations() -> list[dict]:
    items: list[dict] = []
    html_index = read_html("index")
    intro = extract_index_intro(html_index)
    if intro:
        items.append(
            {
                "page": "index",
                "key": "intro",
                "text": intro,
                "label": PAGE_LABELS.get("index", "index"),
                "module": PAGE_MODULE.get("index", "intro"),
            }
        )
    for page in PAGE_ORDER:
        if page == "index":
            continue
        for idx, text in extract_slides_narrations(read_html(page)).items():
            items.append(
                {
                    "page": page,
                    "key": str(idx),
                    "text": text,
                    "label": f"{PAGE_LABELS.get(page, page)} — slide {idx + 1}",
                    "module": PAGE_MODULE.get(page, ""),
                }
            )
    return items


def build_modules_payload(items: list[dict]) -> list[dict]:
    """Thống kê số slide/bài theo module cho UI."""
    by_page: dict[str, int] = {}
    for item in items:
        by_page[item["page"]] = by_page.get(item["page"], 0) + 1

    modules: list[dict] = [
        {
            "id": "all",
            "title": "📚 Toàn khóa học",
            "pages": list(PAGE_ORDER),
            "lessonCount": len([p for p in PAGE_ORDER if p != "index"]),
            "slideCount": len(items),
        },
        {
            "id": "intro",
            "title": "🏠 Trang chủ",
            "pages": ["index"],
            "lessonCount": 1,
            "slideCount": by_page.get("index", 0),
        },
    ]
    for mod in MODULES:
        pages = list(mod["pages"])
        modules.append(
            {
                "id": mod["id"],
                "title": mod["title"],
                "pages": pages,
                "lessonCount": len(pages),
                "slideCount": sum(by_page.get(p, 0) for p in pages),
            }
        )
    return modules


def filter_narration_items(
    items: list[dict], *, module_id: str | None = None, page: str | None = None
) -> list[dict]:
    if page:
        return [i for i in items if i["page"] == page]
    if not module_id or module_id == "all":
        return list(items)
    if module_id == "intro":
        return [i for i in items if i["page"] == "index"]
    return [i for i in items if i.get("module") == module_id]


async def regenerate_items(items: list[dict]) -> list[dict]:
    results: list[dict | None] = [None] * len(items)
    manifest: dict = load_manifest()
    hashes = load_hashes()
    item_lookup = {(i["page"], i["key"]): i for i in items}
    sem = asyncio.Semaphore(MAX_CONCURRENT_REGENERATE)

    async def run_one(i: int, item: dict) -> None:
        page, key, text = item["page"], item["key"], item["text"]
        async with sem:
            results[i] = await regenerate_audio_with_retry(
                page, key, text, persist_manifest=False
            )

    await asyncio.gather(*(run_one(i, item) for i, item in enumerate(items)))

    for result in results:
        if result is None:
            continue
        if result["status"] == "ok":
            if result["page"] not in manifest:
                manifest[result["page"]] = {}
            manifest[result["page"]][result["key"]] = result["audio"]
            src = item_lookup.get((result["page"], result["key"]))
            if src:
                if result["page"] not in hashes:
                    hashes[result["page"]] = {}
                hashes[result["page"]][result["key"]] = narration_hash(src["text"])
    save_manifest(manifest)
    save_hashes(hashes)
    return [r for r in results if r is not None]


async def regenerate_audio_with_retry(
    page: str,
    key: str,
    text: str | None = None,
    attempts: int = 2,
    persist_manifest: bool = True,
) -> dict:
    """Xóa MP3 cũ, tạo mới từ script hiện có; thử lại nếu lỗi."""
    if text is None:
        text = get_narration(page, key)
    label = f"{PAGE_LABELS.get(page, page)} — slide {key}" if page != "index" else PAGE_LABELS.get(page, page)
    last_error: str | None = None
    for attempt in range(1, attempts + 1):
        try:
            rel = await regenerate_audio(
                page, key, text, persist_manifest=persist_manifest
            )
            return {
                "page": page,
                "key": key,
                "label": label,
                "status": "ok",
                "audio": rel,
                "attempts": attempt,
            }
        except Exception as exc:
            last_error = str(exc)
            if attempt < attempts:
                await asyncio.sleep(attempt * 2)
    return {
        "page": page,
        "key": key,
        "label": label,
        "status": "error",
        "error": last_error or "Không tạo được audio",
        "attempts": attempts,
    }


async def regenerate_all() -> list[dict]:
    """Tạo lại toàn bộ audio (có retry từng mục, bỏ qua mục lỗi)."""
    return await regenerate_items(list_all_narrations())
