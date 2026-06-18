"""API boundary for local and Cloud Run serving.

If FastAPI is installed, this module exposes an ASGI `app` object for Uvicorn.
If it is not installed, `python -m app.api.main` falls back to a tiny stdlib HTTP
server so the repo remains runnable from a fresh clone.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from typing import Any, Optional

from app.agent.planner import RetailOpsAgent

try:
    from fastapi import FastAPI
    from pydantic import BaseModel
except ImportError:  # pragma: no cover - local stdlib fallback
    FastAPI = None
    BaseModel = object


agent = RetailOpsAgent.from_default_data()


if FastAPI is not None:
    app = FastAPI(title="Retail Ops Agent GCP", version="0.1.0")

    class QueryRequest(BaseModel):
        question: str

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.post("/query")
    def query(request: QueryRequest) -> dict:
        return agent.answer(request.question)
else:
    app = None


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 - stdlib handler API
        if self.path == "/health":
            self._json({"status": "ok"})
            return
        self._json({"error": "not_found"}, status=404)

    def do_POST(self) -> None:  # noqa: N802 - stdlib handler API
        if self.path != "/query":
            self._json({"error": "not_found"}, status=404)
            return
        length = int(self.headers.get("content-length", "0"))
        payload, error = parse_json_object(self.rfile.read(length) or b"{}")
        if error is not None:
            self._json({"error": error}, status=400)
            return
        response = agent.answer(payload.get("question", ""))
        self._json(response)

    def _json(self, payload: dict, status: int = 200) -> None:
        body = json.dumps(payload, indent=2).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def run(host: str = "127.0.0.1", port: int = 8080) -> None:
    HTTPServer((host, port), Handler).serve_forever()


def parse_json_object(raw: bytes) -> tuple[dict[str, Any], Optional[str]]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return {}, "invalid_json"
    if not isinstance(payload, dict):
        return {}, "invalid_json_object"
    return payload, None


if __name__ == "__main__":
    run()
