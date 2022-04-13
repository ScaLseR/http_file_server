"""HTTP server"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse


class ApiEndpoint(BaseHTTPRequestHandler):
    """класс дял получения и обработки запросов на эндпоинты"""

    def do_GET(self):
        if self.path.startswith('/api/get'):
            params = parse_qs(urlparse(self.path).query)
            print(params)
            print('/api/get')
        if self.path.startswith('/api/download'):
            params = parse_qs(urlparse(self.path).query)
            print(params)
            print('/api/download')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(str(params).replace("'", '"').encode('utf-8'))

    def do_POST(self):
        params = parse_qs(urlparse(self.path).query)
        print(params)
        print('/api/upload')
        if self.path.startswith('/api/upload'):
            self.send_response(201)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write('POST_forever'.encode('utf-8'))

    def do_DELETE(self):
        if self.path.startswith('/api/delete'):
            params = parse_qs(urlparse(self.path).query)
            if len(params) == 0:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write('No conditions'.encode('utf-8'))
            else:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write('X files deleted'.encode('utf-8'))

server = HTTPServer(("127.0.0.1", 9876), ApiEndpoint)
server.serve_forever()