"""HTTP server"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from sql_db import SqlStorage
from datetime import datetime
import uuid
import os


class ApiEndpoint(BaseHTTPRequestHandler):
    """класс дял получения и обработки запросов на ендпоинты"""

    def _set_headers(self, id_response: int) -> None:
        """формирование хедера с указанным статусом ответа"""
        self.send_response(id_response)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    @staticmethod
    def _date_time_str() -> str:
        """получение текущего времени и даты в формате str"""
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _create_json(data: dict) -> json:
        """создание обьекта json из словаря"""
        str_json = json.dumps(data)
        print('str_json= ', str_json)
        return str_json

    @staticmethod
    def _save_file_to_disk(name: str, body: bytes) -> None:
        """запись файла на диск"""
        with open(name, mode="wb") as file:
            file.write(body)

    def do_GET(self):
        """отработка запросов GET на ендпоинты /api/get и /api/download"""
        #storage = SqlStorage('file_server')
        if self.path.startswith('/api/get'):
            storage = SqlStorage('file_server')
            params = parse_qs(urlparse(self.path).query)
            if len(params) == 0:
                rez = storage.load_from_db()
            print(rez)
        if self.path.startswith('/api/download'):
            params = parse_qs(urlparse(self.path).query)
            print(params)
            print('/api/download')
        self._set_headers(200)
        self.wfile.write(str(params).replace("'", '"').encode('utf-8'))

    def do_POST(self):
        """отработка запросов POST на ендпоинт /api/upload"""
        storage = SqlStorage('file_server')
        time_dict = {}
        if self.path.startswith('/api/upload'):
            params = parse_qs(urlparse(self.path).query)
            print(params)
            if not params.get('id'):
                ids = str(uuid.uuid4())
            else:
                ids = params['id'][0]
            time_dict['id'] = ids
            if not params.get('name'):
                name = ids
            else:
                name = params['name'][0]
            time_dict['name'] = name
            if not params.get('tag'):
                tag = ''
            else:
                tag = params['tag'][0]
            time_dict['tag'] = tag
            content_size = int(self.headers.get('content-length'))
            time_dict['size'] = content_size
            mime_type = self.headers.get('content-type')
            time_dict['mimeType'] = mime_type
            modification_time = self._date_time_str()
            time_dict['modificationTime'] = modification_time
            storage.save_to_db(ids, name, tag, content_size, mime_type, modification_time)
            rez_json = self._create_json(time_dict)
            post_body = self.rfile.read(content_size)
            self._save_file_to_disk(name, post_body)
            self._set_headers(201)
            self.wfile.write(rez_json.encode('utf-8'))

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
