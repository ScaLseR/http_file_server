"""HTTP server"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from sql_db import SqlStorage


class ApiEndpoint(BaseHTTPRequestHandler):
    """класс дял получения и обработки запросов на эндпоинты"""

    def _set_headers(self, id_response: int):
        """формирование хедера с указанным статусом ответа"""
        self.send_response(id_response)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """отработка запросов GET на ендпоинты /api/get и /api/download"""
        if self.path.startswith('/api/get'):
            params = parse_qs(urlparse(self.path).query)
            if len(params) == 0:
                rez = storage.load_from_db()
            print(params)
        if self.path.startswith('/api/download'):
            params = parse_qs(urlparse(self.path).query)
            print(params)
            print('/api/download')
        self._set_headers(200)
        self.wfile.write(str(params).replace("'", '"').encode('utf-8'))

    def do_POST(self):
        """отработка запросов POST на ендпоинт /api/upload"""
        if self.path.startswith('/api/upload'):
            self._set_headers(201)
            params = parse_qs(urlparse(self.path).query)
            print(params)
            # content_len = int(self.headers('content-length'))
            # post_body = self.rfile.read(content_len)
            # print(post_body)
            self.wfile.write('POST_forever'.encode('utf-8'))

    def do_DELETE(self):
        """отработка ёзапроса DELETE на ендпоинт /api/delete"""
        if self.path.startswith('/api/delete'):
            params = parse_qs(urlparse(self.path).query)
            if len(params) == 0:
                self._set_headers(400)
                self.wfile.write('отсутствуют условия'.encode('utf-8'))
            else:
                self._set_headers(200)
                self.wfile.write('X files deleted'.encode('utf-8'))


def run(ip_addr: str, port: int):
    server = HTTPServer((ip_addr, port), ApiEndpoint)
    server.serve_forever()

if __name__ == "__main__":
    run('127.0.0.1', 9876)
    storage = SqlStorage('file_storage')
