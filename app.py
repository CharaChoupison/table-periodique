from __future__ import annotations

import json
import mimetypes
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from periodic_table import CLASS_ALIASES, ELEMENTS


HOST = "127.0.0.1"
PORT = int(os.environ.get("PORT", "3000"))
BASE_DIR = Path(__file__).parent
PUBLIC_DIR = BASE_DIR / "public"


def normalize(value: str) -> str:
    return value.strip().lower()


def find_element(identifier: str) -> dict | None:
    value = normalize(unquote(identifier))

    if value.isdigit():
        atomic_number = int(value)
        return next((element for element in ELEMENTS if element["atomicNumber"] == atomic_number), None)

    return next((element for element in ELEMENTS if normalize(element["symbol"]) == value), None)


def find_elements_by_class(class_name: str) -> list[dict]:
    value = normalize(unquote(class_name))
    canonical_class = CLASS_ALIASES.get(value, value)

    return [
        element
        for element in ELEMENTS
        if element["class"] == canonical_class or element["category"] == canonical_class
    ]


class PeriodicTableHandler(BaseHTTPRequestHandler):
    def send_json(self, status_code: int, payload: dict | list) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path: Path) -> None:
        if not path.exists() or not path.is_file():
            self.send_json(404, {"error": "Fichier introuvable"})
            return

        content = path.read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self) -> None:
        parsed_url = urlparse(self.path)
        path = parsed_url.path.strip("/")
        segments = [segment for segment in path.split("/") if segment]

        if not segments:
            self.send_file(PUBLIC_DIR / "index.html")
            return

        if segments == ["elements"]:
            self.send_json(200, {"count": len(ELEMENTS), "data": ELEMENTS})
            return

        if len(segments) == 2 and segments[0] == "elements":
            element = find_element(segments[1])

            if element is None:
                self.send_json(404, {"error": "Aucun element trouve pour ce numero atomique ou ce symbole"})
                return

            self.send_json(200, {"data": element})
            return

        if len(segments) == 2 and segments[0] == "classes":
            elements = find_elements_by_class(segments[1])

            if not elements:
                self.send_json(404, {"error": "Aucun element trouve pour cette classe"})
                return

            self.send_json(200, {"count": len(elements), "data": elements})
            return

        static_path = (PUBLIC_DIR / unquote(path)).resolve()
        if PUBLIC_DIR in static_path.parents or static_path == PUBLIC_DIR:
            self.send_file(static_path)
            return

        self.send_json(404, {"error": "Route introuvable"})


def run() -> None:
    try:
        server = ThreadingHTTPServer((HOST, PORT), PeriodicTableHandler)
    except OSError as error:
        if error.errno in {48, 98, 10048}:
            print(f"Le port {PORT} est deja utilise.")
            print(f"Relance avec un autre port : PORT=4000 python3 app.py")
            sys.exit(1)
        raise

    print(f"API Python lancee sur http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run()
