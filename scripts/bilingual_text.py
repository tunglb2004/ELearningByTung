"""Tách câu hỗn hợp Việt–Anh để đọc bằng đúng giọng."""
from __future__ import annotations

import re

VI_CHARS = re.compile(
    r"[àáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ]",
    re.IGNORECASE,
)

EN_HINT = re.compile(
    r"\b("
    r"selenium|webdriver|chromedriver|maven|junit|testng|restassured|"
    r"automation|testing|manual|browser|driver|element|elements|"
    r"locator|locators|click|type|clear|submit|verify|assert|test|tests|"
    r"api|e2e|roi|ci|cd|framework|html|xpath|css|selector|"
    r"integration|unit|pom|testng|page|object|model|annotation|annotations|"
    r"parallel|execution|data|driven|xml|suite|suites|"
    r"sendkeys|findelement|nosuchelementexception|implicit|explicit|fluent|"
    r"actions|switchto|java|python|javascript|chrome|edge|firefox|"
    r"google|facebook|amazon|login|shopping|setup|dependency|"
    r"webdriver|web|ui|ux|phase|video|grid|docker|headless"
    r")\b",
    re.IGNORECASE,
)

EN_PARTICLE = re.compile(
    r"^(to|by|of|or|and|in|on|at|is|it|the|a|an|for|with|as|from)$",
    re.IGNORECASE,
)


def _strip_token(token: str) -> str:
    return re.sub(r"^[^\w#/.+\-]+|[^\w#/.+\-]+$", "", token)


def _classify_token(token: str) -> str:
    if not token.strip():
        return "neutral"
    if VI_CHARS.search(token):
        return "vi"
    core = _strip_token(token)
    if not core:
        return "neutral"
    if re.match(r"^[A-Za-z][A-Za-z0-9#/.+\-_]*$", core):
        if re.match(r"^(by|driver|actions)\.", core, re.I):
            return "en"
        if EN_HINT.search(core):
            return "en"
        if re.match(r"^[A-Z]{2,}$", core):
            return "en"
        if re.search(r"[a-z][A-Z]", core):
            return "en"
        return "vi"
    return "neutral"


def segment_text(text: str) -> list[tuple[str, str]]:
    """Trả về [('vi'|'en', 'đoạn text'), ...]."""
    tokens = re.findall(r"\s+|[^\s]+", text.strip())
    if not tokens:
        return []

    segments: list[tuple[str, str]] = []
    current_lang: str | None = None
    parts: list[str] = []

    def flush() -> None:
        nonlocal current_lang, parts
        joined = "".join(parts).strip()
        if joined and current_lang:
            segments.append((current_lang, joined))
        parts = []
        current_lang = None

    for token in tokens:
        lang = _classify_token(token)
        if lang == "neutral":
            parts.append(token)
            continue
        if current_lang is not None and current_lang != lang:
            flush()
        current_lang = lang
        parts.append(token)

    flush()
    return segments
