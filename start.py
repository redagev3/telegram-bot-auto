import subprocess
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import asyncio
import os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'Bot is running')
    
    def log_message(self, format, *args):
        pass

def run_http_server():
    server = HTTPServer(('0.0.0.0', 8000), Handler)
    server.serve_forever()

# Удаляем старую БД чтобы пересоздалась с ключами
if os.path.exists("users.db"):
    os.remove("users.db")

# Запускаем HTTP сервер в отдельном потоке
http_thread = threading.Thread(target=run_http_server, daemon=True)
http_thread.start()

# Запускаем основной бот в основном потоке
from bot import main
main()
