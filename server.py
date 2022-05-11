"""HTTP server"""
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from datetime import datetime
from json import dumps
import magic
from sql_db import SqlStorage
from file_operation import save_file_to_disk, load_file_from_disk, delete_file_from_disk


class ApiEndpoint(BaseHTTPRequestHandler):
    """class for receiving and processing requests for enddpoints"""
    _storage = SqlStorage('file_server')

    def _set_headers(self, *args) -> None:
        """forming a header with the specified response status"""
        if len(args) == 1:
            self.send_response(args[0])
        else:
            self.send_response(args[0], args[1])
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    @staticmethod
    def _date_time_str() -> str:
        """get the current time and date in the format: str"""
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _create_dict(data: list) -> list:
        main_list = []
        for part in data:
            part_dict = {'id': part[0], 'name': part[1], 'tag': part[2],
                         'size': part[3], 'mimeType': part[4], 'modificationTime': part[5]}
            main_list.append(part_dict)
        return main_list

    def do_GET(self):  # pylint: disable=invalid-name
        """processing GET requests to endpoints /api/get and /api/download"""
        # обрабатываем api/get
        if self.path.startswith('/api/get'):
            params = parse_qs(urlparse(self.path).query)
            # если нет параметров то выводим все файлы
            if len(params) == 0 or ('id' not in params) and ('name' not in params) \
                    and ('tag' not in params) and ('mimetype' not in params) \
                    and ('modificationtime' not in params):
                rez = ApiEndpoint._storage.load_from_db({})
            else:
                #если есть параметры то делаем запрос в базу
                rez = ApiEndpoint._storage.load_from_db(params)
            rez_list = self._create_dict(rez)
            # if len(rez_list) == 1:
            #     rez_json = dumps(rez_list[0])
            # else:
            #     rez_json = dumps(rez_list)
            self._set_headers(200)
            # if len(rez_json) == 2:
            #     rez_json = dumps({})
            rez_json = dumps(rez_list)
            self.wfile.write(rez_json.encode('utf-8'))
        # обрабатываем api/download
        elif self.path.startswith('/api/download'):
            params = parse_qs(urlparse(self.path).query)
            # если нет параметров выводим 400 ошибку
            if len(params) == 0 or ('id' not in params):
                self._set_headers(400)
                self.wfile.write('отсутствуют условия'.encode('utf-8'))
            else:
                find = {'id': [params['id'][0]]}
                data = ApiEndpoint._storage.load_from_db(find)
                # если файла с заданным id нет в базе
                if len(data) == 0:
                    self._set_headers(404)
                    self.wfile.write('файл не существует'.encode('utf-8'))
                # файл с заданным id присутствует в базе, возвращаем файл клиенту
                else:
                    self.send_response(200)
                    self.send_header('Content-type', data[0][4])
                    self.send_header('Content-Disposition: attachment; filename=', data[0][1])
                    self.send_header('Content-length', data[0][3])
                    self.end_headers()
                    body = load_file_from_disk(data[0][0])
                    self.wfile.write(body)
                    print('файл ' + data[0][1] + ' отправлен')
        else:
            self._set_headers(501)

    def do_POST(self):  # pylint: disable=invalid-name, too-many-locals
        """processing POST requests to endpoint /api/upload"""
        upd = False
        if self.path.startswith('/api/upload'):
            params = parse_qs(urlparse(self.path).query)
            # проверка условий и наличия пареметров в запросе
            if not params.get('id'):
                ids = str(uuid.uuid4())
            else:
                ids = params['id'][0]
                find = {'id': [ids]}
                _rez = ApiEndpoint._storage.load_from_db(find)
                if len(_rez) != 0:
                    name = _rez[0][1]
                    if len(_rez[0][2]) == 0:
                        tag = ''
                    else:
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
            # получаем тело файла и сохраняем на диск
            content_size = int(self.headers.get('content-length'))
            post_body = self.rfile.read(content_size)
            save_file_to_disk(ids, post_body)
            if not params.get('content-type'):
                mime_type = self.headers.get('content-type')
                if not mime_type:
                    mime_type = magic.from_buffer(post_body, mime=True)
            else:
                mime_type = params['content-type'][0]
            modification_time = self._date_time_str()
            # сохраняем все параметры загруженного файла в базу
            if upd:
                ApiEndpoint._storage.update_to_db(ids, name, tag,
                                                  content_size, mime_type, modification_time)
            else:
                ApiEndpoint._storage.save_to_db(ids, name, tag, content_size,
                                                mime_type, modification_time)
            # создаем json обьект и возвращаем клиенту
            find = {'id': [ids]}
            rez = ApiEndpoint._storage.load_from_db(find)
            time_dict = self._create_dict(rez)
            rez_json = dumps(time_dict[0])
            self._set_headers(201)
            self.wfile.write(rez_json.encode('utf-8'))
        else:
            self._set_headers(501)

    def do_DELETE(self):  # pylint: disable=invalid-name
        """DELETE request processing on the endpoint /api/delete"""
        if self.path.startswith('/api/delete'):
            params = parse_qs(urlparse(self.path).query)
            print(params)
            if len(params) == 0 or ('id' not in params) and ('name' not in params) \
                    and ('tag' not in params) and ('mimetype' not in params) \
                    and ('modificationtime' not in params):
                self._set_headers(400)
                self.wfile.write('отсутствуют условия'.encode('utf-8'))
            else:
                rez = ApiEndpoint._storage.load_from_db(params)
                if len(rez) == 0:
                    self._set_headers(200, '0 files deleted')
                    self.wfile.write('0 files deleted'.encode('utf-8'))
                else:
                    count = 0
                    for part in rez:
                        ApiEndpoint._storage.del_from_db(id=part[0])
                        delete_file_from_disk(part[0])
                        count += 1
                    self._set_headers(200, str(count) + ' files deleted')
                    self.wfile.write((str(count) + ' files deleted').encode('utf-8'))
        else:
            self._set_headers(501)


def run(ip_addr: str, port: int) -> None:
    """running the server with the passed parameters"""
    server = HTTPServer((ip_addr, port), ApiEndpoint)
    print('server started')
    server.serve_forever()


if __name__ == "__main__":
    run('localhost', 9876)
