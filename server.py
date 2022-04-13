"""HTTP server"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


class ApiEndpoint(BaseHTTPRequestHandler):
    """класс дял получения и обработки запросов на эндпоинты"""

    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        print(params)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(str(params).replace("'", '"').encode('utf-8'))

server = HTTPServer(("127.0.0.1", 9876), ApiEndpoint)
server.serve_forever()