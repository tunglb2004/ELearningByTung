#!/usr/bin/env python3
"""
Server khóa học + API chỉnh sửa thuyết minh / tạo lại audio.

    pip install -r requirements.txt
    python server.py

Mở: http://localhost:5500  (phải dùng server này, không dùng python -m http.server)
"""
from __future__ import annotations

import asyncio
import json
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler
from pathlib import Path
from socketserver import ThreadingTCPServer
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))

from narration_lib import (  # noqa: E402
    PAGE_FILES,
    PAGE_ORDER,
    build_modules_payload,
    filter_narration_items,
    get_narration,
    list_all_narrations,
    PAGE_LABELS,
    regenerate_all,
    regenerate_audio,
    regenerate_audio_with_retry,
    regenerate_items,
    update_narration_text,
)

PORT = 5500


class ReuseTCPServer(ThreadingTCPServer):
    allow_reuse_address = True


def json_response(handler: SimpleHTTPRequestHandler, status: int, payload: dict) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(body)


def read_json_body(handler: SimpleHTTPRequestHandler) -> dict:
    length = int(handler.headers.get("Content-Length", 0))
    if length <= 0:
        return {}
    raw = handler.rfile.read(length)
    return json.loads(raw.decode("utf-8"))


def run_async(coro):
    return asyncio.run(coro)


class CourseHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, fmt, *args):
        print(f"[{self.log_date_time_string()}] {fmt % args}")

    def do_OPTIONS(self):
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, PUT, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            json_response(
                self,
                200,
                {
                    "ok": True,
                    "pages": list(PAGE_FILES.keys()),
                    "pageOrder": list(PAGE_ORDER),
                    "labels": PAGE_LABELS,
                    "modules": build_modules_payload(list_all_narrations()),
                },
            )
            return
        if path == "/api/narrations":
            try:
                items = list_all_narrations()
                json_response(
                    self,
                    200,
                    {"items": items, "modules": build_modules_payload(items)},
                )
            except Exception as exc:
                json_response(self, 500, {"error": str(exc)})
            return
        if path.startswith("/api/narration/"):
            parts = [p for p in path.split("/") if p]
            if len(parts) == 4:
                _, _, page, key = parts[:4]
                try:
                    text = get_narration(unquote(page), unquote(key))
                    json_response(self, 200, {"page": page, "key": key, "text": text})
                except Exception as exc:
                    json_response(self, 404, {"error": str(exc)})
                return
        return super().do_GET()

    def do_PUT(self):
        path = urlparse(self.path).path
        if path.startswith("/api/narration/"):
            parts = [p for p in path.split("/") if p]
            if len(parts) == 4:
                _, _, page, key = parts[:4]
                page, key = unquote(page), unquote(key)
                try:
                    body = read_json_body(self)
                    text = (body.get("text") or "").strip()
                    if not text:
                        json_response(self, 400, {"error": "text không được rỗng"})
                        return
                    update_narration_text(page, key, text)
                    regenerate = body.get("regenerate", True)
                    if regenerate is False or regenerate == 0:
                        json_response(
                            self,
                            200,
                            {
                                "ok": True,
                                "page": page,
                                "key": key,
                                "text": text,
                                "audioRegenerated": False,
                            },
                        )
                        return
                    audio = run_async(regenerate_audio(page, key, text))
                    json_response(
                        self,
                        200,
                        {
                            "ok": True,
                            "page": page,
                            "key": key,
                            "text": text,
                            "audio": audio,
                            "audioRegenerated": True,
                        },
                    )
                except Exception as exc:
                    json_response(self, 500, {"error": str(exc)})
                return
        json_response(self, 404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path.startswith("/api/regenerate-module/"):
            parts = [p for p in path.split("/") if p]
            if len(parts) == 3:
                module_id = unquote(parts[2])
                try:
                    items = filter_narration_items(
                        list_all_narrations(), module_id=module_id
                    )
                    results = run_async(regenerate_items(items))
                    ok_count = sum(1 for r in results if r.get("status") == "ok")
                    err_count = sum(1 for r in results if r.get("status") == "error")
                    json_response(
                        self,
                        200,
                        {
                            "ok": err_count == 0,
                            "module": module_id,
                            "count": len(results),
                            "okCount": ok_count,
                            "errorCount": err_count,
                            "items": results,
                        },
                    )
                except Exception as exc:
                    json_response(self, 500, {"error": str(exc)})
                return
        if path == "/api/regenerate-all":
            try:
                results = run_async(regenerate_all())
                ok_count = sum(1 for r in results if r.get("status") == "ok")
                err_count = sum(1 for r in results if r.get("status") == "error")
                json_response(
                    self,
                    200,
                    {
                        "ok": err_count == 0,
                        "count": len(results),
                        "okCount": ok_count,
                        "errorCount": err_count,
                        "items": results,
                    },
                )
            except Exception as exc:
                json_response(self, 500, {"error": str(exc)})
            return
        if path.startswith("/api/regenerate/"):
            parts = [p for p in path.split("/") if p]
            if len(parts) == 4:
                _, _, page, key = parts[:4]
                page, key = unquote(page), unquote(key)
                try:
                    result = run_async(regenerate_audio_with_retry(page, key))
                    status = 200 if result["status"] == "ok" else 207
                    json_response(self, status, result)
                except Exception as exc:
                    json_response(self, 500, {"error": str(exc)})
                return
        json_response(self, 404, {"error": "not found"})


def main():
    global PORT
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    for candidate in (5500, 5501):
        try:
            server = ReuseTCPServer(("", candidate), CourseHandler)
            PORT = candidate
            break
        except OSError:
            if candidate == 5501:
                raise
    print(f"Khóa học: http://localhost:{PORT}/index.html")
    print("API: PUT /api/narration/{{page}}/{{key}}  |  POST /api/regenerate-all")
    print("Luu y: dung server nay, KHONG dung python -m http.server")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDa dung server.")
        server.server_close()


if __name__ == "__main__":
    main()
