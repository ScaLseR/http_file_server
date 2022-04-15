"""HTTP server"""
import json
import uuid
import os
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from datetime import datetime
from sql_db import SqlStorage


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
    def _create_json(data: list) -> json:
        """создание обьекта json из словаря"""
        str_json = json.dumps(data, indent=2)
        return str_json

    @staticmethod
    def _save_file_to_disk(name: str, body: bytes) -> None:
        """запись файла на диск"""
        with open(name, mode="wb") as file:
            file.write(body)

    @staticmethod
    def _load_file_from_disk(name: str) -> bytes:
        """загрузка файла с диска"""
        with open(name, mode="rb") as file:
            body = file.read()
        return body

    @staticmethod
    def _delete_file_from_disk(name: str) -> None:
        """удаление файла с диска"""
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), name)
        os.remove(path)
        print(name + ' файл удален')

    @staticmethod
    def _create_dict(data: list) -> list:
        main_list = []
        for part in data:
            part_dict = {'id': part[0], 'name': part[1], 'tag': part[2],
                         'size': part[3], 'mimeType': part[4], 'modificationTime': part[5]}
            main_list.append(part_dict)
        return main_list

    def do_GET(self):#pylint: disable=invalid-name
        """отработка запросов GET на ендпоинты /api/get и /api/download"""
        storage = SqlStorage('file_server')
        #обрабатываем api/get
        if self.path.startswith('/api/get'):
            params = parse_qs(urlparse(self.path).query)
            #если нет параметров то выводим все файлы
            if len(params) == 0:
                rez = storage.load_from_db({})
                rez_list = self._create_dict(rez)
                self._set_headers(200)
                rez_json = self._create_json(rez_list)
                self.wfile.write(rez_json.encode('utf-8'))
            else:
                rez = storage.load_from_db(params)
                rez_list = self._create_dict(rez)
                self._set_headers(200)
                rez_json = self._create_json(rez_list)
                self.wfile.write(rez_json.encode('utf-8'))
        # обрабатываем api/download
        if self.path.startswith('/api/download'):
            params = parse_qs(urlparse(self.path).query)
            #если нет параметров выводим 400 ошибку
            if len(params) == 0:
                self._set_headers(400)
                self.wfile.write('отсутствуют уловия'.encode('utf-8'))
            else:
                find = {'id': [params['id'][0]]}
                data = storage.load_from_db(find)
                #если файла с заданным id нет в базе
                if len(data) == 0:
                    self._set_headers(404)
                    self.wfile.write('файл не существует'.encode('utf-8'))
                #файл с заданным id присутствует в базе, возвращаем файл клиенту
                else:
                    self.send_response(200)
                    self.send_header('Content-type', data[0][4])
                    self.send_header('Content-Disposition: attachment; filename=', data[0][1])
                    self.send_header('Content-length', data[0][3])
                    self.end_headers()
                    body = self._load_file_from_disk(data[0][0])
                    self.wfile.write(body)
                    print('файл ' + data[0][1] + ' отправлен')

    def do_POST(self):#pylint: disable=invalid-name, too-many-locals
        """отработка запросов POST на ендпоинт /api/upload"""
        storage = SqlStorage('file_server')
        upd = False
        if self.path.startswith('/api/upload'):
            params = parse_qs(urlparse(self.path).query)
            #проверка условий и наличия пареметров в запросе
            if not params.get('id'):
                ids = str(uuid.uuid4())
            else:
                ids = params['id'][0]
                find = {'id': [ids]}
                _rez = storage.load_from_db(find)
                if len(_rez) != 0:
                    name = _rez[0][1]
                    tag = _rez[0][2]
                    upd = True
            if not params.get('name'):
                name = ids
            else:
                name = params['name'][0]
            if not params.get('tag'):
                tag = ''
            else:
                tag = params['tag'][0]
            if not params.get('Content-Type'):
                mime_type = self.headers.get('content-type')
            else:
                mime_type = params['Content-Type'][0]
            content_size = int(self.headers.get('content-length'))
            modification_time = self._date_time_str()
            #сохраняем все параметры загруженного файла в базу
            if upd:
                storage.update_to_db(ids, name, tag, content_size, mime_type, modification_time)
            else:
                storage.save_to_db(ids, name, tag, content_size, mime_type, modification_time)
            #получаем тело файла и сохраняем на диск
            post_body = self.rfile.read(content_size)
            self._save_file_to_disk(ids, post_body)
            #создаем json обьект и возвращаем клиенту
            find = {'id': [ids]}
            rez = storage.load_from_db(find)
            time_dict = self._create_dict(rez)
            rez_json = self._create_json(time_dict)
            self._set_headers(201)
            self.wfile.write(rez_json.encode('utf-8'))

    def do_DELETE(self):#pylint: disable=invalid-name
        """отработка ёзапроса DELETE на ендпоинт /api/delete"""
        storage = SqlStorage('file_server')
        if self.path.startswith('/api/delete'):
            params = parse_qs(urlparse(self.path).query)
            if len(params) == 0:
                self._set_headers(400)
                self.wfile.write('отсутствуют условия'.encode('utf-8'))
            else:
                rez = storage.load_from_db(params)
                if len(rez) == 0:
                    self._set_headers(404)
                    self.wfile.write('файл не найден'.encode('utf-8'))
                else:
                    count = 0
                    for part in rez:
                        storage.del_from_db(id=part[0])
                        self._delete_file_from_disk(part[0])
                        count += 1
                    self._set_headers(200)
                    self.wfile.write((str(count) + ' files deleted').encode('utf-8'))


def run(ip_addr: str, port: int):
    """запуск сервера с переданными параметрами"""
    server = HTTPServer((ip_addr, port), ApiEndpoint)
    server.serve_forever()

if __name__ == "__main__":
    run('localhost', 9876)
