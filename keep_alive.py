"""
keep_alive.py — Render Free Tier Keep-Alive Server
====================================================
Render's free tier spins down services after ~15 minutes of inactivity.
This module starts a lightweight HTTP server so Render keeps the process alive.
Use an external pinger (UptimeRobot / cron-job.org) to ping /health every 5 min.
"""

import threading
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler

logger = logging.getLogger(__name__)


class HealthHandler(BaseHTTPRequestHandler):
    """Minimal HTTP handler — responds to GET / and GET /health."""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK - Bot is alive")

    # Suppress default access logs to keep console clean
    def log_message(self, format, *args):
        pass


def start_keep_alive(port: int = 8080):
    """Start the keep-alive server in a background daemon thread."""
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    logger.info(f"✅ Keep-alive server running on port {port}")
