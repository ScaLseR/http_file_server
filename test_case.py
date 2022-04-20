"""тесты для API server.py"""
import unittest
import re
import os
import requests as rq
from jsonschema import validate


class TestApi(unittest.TestCase):
    """тестовый класс"""

    def setUp(self) -> None:
        """прописываем дефолтные url значения и схему ответа json"""
        self.api_upload = "http://127.0.0.1:9876/api/upload"
        self.api_get = "http://127.0.0.1:9876/api/get"
        self.api_delete = "http://127.0.0.1:9876/api/delete"
        self.api_download = "http://127.0.0.1:9876/api/download"
        self.valid_json_schema = {
                  "properties": {
                    "id": {
                      "type": "string"
                    },
                    "name": {
                      "type": "string"
                    },
                    "tag": {
                      "type": "string"
                    },
                    "size": {
                      "type": "integer"
                    },
                    "mimeType": {
                      "type": "string"
                    },
                    "modificationTime": {
                      "type": "string"
                    }
                  },
                  "required": [
                    "id",
                    "name",
                    "tag",
                    "size",
                    "mimeType",
                    "modificationTime"
                  ]
                }

    def tearDown(self) -> None:
        """чистка файлов и БД после теста"""
        dirname = r"./"
        files = os.listdir(dirname)
        for file in files:
            result = re.match(r'^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$|^\d+$', file)
            if result:
                os.remove(file)
        if os.path.exists('file_server'):
            os.remove('file_server')

    def test_api_upload_code_201(self):
        """api_upload код 201 при удачной загрузке файла"""
        #test1
        response = rq.post(self.api_upload, data="test1")
        self.assertEqual(response.status_code, 201, "should be code 201")

    def test_api_upload_valid_json_schema(self):
        """api_upload соответствие схеме ответа json"""
        #test2
        response = rq.post(self.api_upload, data="test2")
        response_body = response.json()
        validate(response_body, self.valid_json_schema)

    def test_api_upload_correct_content_length(self):
        """api_upload правильное заполнение заголовка Content-Length"""
        # test3
        response = rq.post(self.api_upload, data="test3")
        response_body = response.json()
        self.assertEqual(response_body[0]['size'], 5, "Content-Length should be 5")

    def test_api_upload_full_param(self):
        """api_upload загрузка файла с корректно заполненными параметрами"""
        #test4
        response = rq.post(self.api_upload, params={'id': 4,
                                                    'name': 'test4',
                                                    'tag': 'test'}, data="test4")
        response_body = response.json()
        self.assertEqual(int(response_body[0]['id']), 4,
                         f"should be params['id'] = response_body['id'] "
                         f"= {int(response_body[0]['id'])}")
        self.assertEqual(response_body[0]['name'],
                         'test4', f"should be params['name'] = "
                                  f"response_body['name'] = {response_body[0]['name']}")
        self.assertEqual(response_body[0]['tag'],
                         'test', f"should be params['tag'] = "
                                 f"response_body['tag'] = {response_body[0]['tag']}")

    def test_api_upload_generate_id_with_name(self):
        """api_upload загрузка файла с автоматической генерацией
        id и заполненным вручную именем файла name"""
        #test5
        response = rq.post(self.api_upload, params={'name': 'test5',
                                                    'tag': 'test'}, data="test5")
        response_body = response.json()
        result = re.match(r'^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$', response_body[0]['id'])
        generate_id = False
        if result:
            generate_id = True
        self.assertTrue(generate_id, "should be generated id")
        self.assertEqual(response_body[0]['name'],
                         'test5', f"should be params['name'] = "
                                  f"response_body['name'] = {response_body[0]['name']}")

    def test_api_upload_generate_id_without_name(self):
        """api_upload загрузка файла с автоматической генерацией
        id и не заполненным именем файла name, name = id"""
        #test6
        response = rq.post(self.api_upload, params={}, data="test6")
        response_body = response.json()
        self.assertEqual(response_body[0]['id'], response_body[0]['name'],
                         f"should be response_body['id'] = "
                         f"response_body['name'] = {response_body[0]['id']}")

    #@unittest.expectedFailure
    def test_api_upload_rewrite_file_with_enable_id(self):
        """api_upload изменение файла с уже существующим id(
        перезапись существующего файла)"""
        #test7
        _ = rq.post(self.api_upload, params={'id': 7, 'name': 'test7', 'tag': '123',
                                             'content-type': 'text'}, data="test7")
        response = rq.post(self.api_upload, params={'id': 7,
                                                    'name': 'test7_new', 'tag': '321',
                                                    'content-type': 'text'}, data="test7_new")
        response_body = response.json()
        self.assertEqual(response_body[0]['name'],
                         'test7_new', f"should be response_body['name'] "
                                      f"= name = {response_body[0]['name']}")
        self.assertEqual(response_body[0]['tag'], '321', "should be response_body['tag'] = '321'")

    def test_api_get_code_200(self):
        """api_get код ответа 200 при получении выборки файла"""
        #test8
        _ = rq.post(self.api_upload, params={'id': 8, 'name': 'test8'}, data="test8")
        response = rq.get(self.api_get)
        self.assertEqual(response.status_code, 200, "should be code 200")

    def test_api_get_valid_json_schema(self):
        """api_get соответствие схеме ответа json"""
        #test9
        _ = rq.post(self.api_upload, params={'id': 9, 'name': 'test9'}, data="test9")
        response = rq.get(self.api_get)
        response_body = response.json()
        validate(response_body, self.valid_json_schema)

    def test_api_get_all(self):
        """api_get вывод всех метаданных файлов на
        сервере при пустом условии"""
        #test10
        _ = rq.post(self.api_upload, params={'id': 1,
                                             'name': 'test10_1',
                                             'tag': 'test'}, data="test10_1")
        _ = rq.post(self.api_upload, params={'id': 2,
                                             'name': 'test10_2'}, data="test10_2")
        _ = rq.post(self.api_upload, params={'id': 3}, data="test10_3")
        _ = rq.post(self.api_upload, data="test10_4")
        response = rq.get(self.api_get)
        response_body = response.json()
        self.assertEqual(len(response_body), 4, "should be 4")

    def test_api_get_files_from_params(self):
        """api_get возвращение метаданных файлов удовлетворяющих условию"""
        #test11
        _ = rq.post(self.api_upload, params={'id': 1,
                                             'name': 'test11',
                                             'tag': 'test'}, data="test11_1")
        _ = rq.post(self.api_upload, params={'id': 2,
                                             'name': 'test10'}, data="test11_2")
        _ = rq.post(self.api_upload, params={'id': 3,
                                             'name': 'test11'}, data="test11_3")
        response = rq.get(self.api_get, params={'id': [1, 2, 3], 'name': 'test11'})
        response_body = response.json()
        self.assertEqual(len(response_body), 2, "should be 2")

    def test_api_delete_code_400(self):
        """api_delete код ответа 400 при отсутствии условий"""
        #test12
        response = rq.delete(self.api_delete)
        response.encoding = 'utf-8'
        self.assertEqual(response.status_code, 400, "should be code 400")
        self.assertEqual(response.text, 'отсутствуют условия', "should be 'отсутствуют условия'")

    def test_api_delete_1_file(self):
        """api_delete удаление 1 файла"""
        #test13
        _ = rq.post(self.api_upload, params={'id': 1,
                                             'name': 'test13',
                                             'tag': 'test'}, data="test13")
        response = rq.delete(self.api_delete, params={'id': 1})
        self.assertEqual(response.status_code, 200, "should be code 200")
        self.assertEqual(response.text, '1 files deleted', "should be '1 files deleted'")

    def test_api_delete_few_files_from_params(self):
        """api_delete удаление нескольких файлов"""
        #test14
        _ = rq.post(self.api_upload, params={'id': 1,
                                             'name': 'test14',
                                             'tag': 'test'}, data="test14")
        _ = rq.post(self.api_upload, params={'id': 2, 'name': 'test14_2'}, data="test14_2")
        _ = rq.post(self.api_upload, params={'id': 3, 'name': 'test14_3'}, data="test14_3")
        _ = rq.post(self.api_upload, params={'id': 4, 'name': 'test14'}, data="test14_4")
        response = rq.delete(self.api_delete, params={'id': [1, 2, 3, 4], 'name': 'test14'})
        self.assertEqual(response.status_code, 200, "should be code 200")
        self.assertEqual(response.text, '2 files deleted', "should be '2 files deleted'")

    def test_api_delete_code_404(self):
        """api_delete код ответа 404 при удалении несуществующего файла"""
        #test15
        response = rq.delete(self.api_delete, params={'id': 1})
        response.encoding = 'utf-8'
        self.assertEqual(response.status_code, 404, "should be code 404")
        self.assertEqual(response.text, 'файл не найден', "should be 'файл не найден'")

    def test_api_download_code_400(self):
        """api_download код ответа 400 при загрузке без условий"""
        #test16
        response = rq.get(self.api_download)
        self.assertEqual(response.status_code, 400, "should be code 400")

    def test_api_download_code_404(self):
        """api_download код ответа 404 при загрузке не существующего файла"""
        #test17
        response = rq.get(self.api_download, params={'id': 1})
        self.assertEqual(response.status_code, 404, "should be code 404")

    def test_api_download_file(self):
        """api_download загрузка существующего файла"""
        #test18
        _ = rq.post(self.api_upload, params={'id': 1,
                                             'name': 'test18',
                                             'tag': 'test'}, data="test1818")
        response = rq.get(self.api_download, params={'id': 1})
        self.assertEqual(response.status_code, 200, "should be code 200")
        self.assertEqual(response.text, 'test1818', "should be 'test1818'")

    def test_api_download_content_disposition(self):
        """api_download Content-Disposition == filename = <имя файла>"""
        #test19
        _ = rq.post(self.api_upload, params={'id': 1,
                                             'name': 'test19',
                                             'tag': 'test'}, data="test1919")
        response = rq.get(self.api_download, params={'id': 1})
        self.assertIn('filename=: test19', response.headers['Content-Disposition'],
                      "should be filename=: test19")

    def test_api_download_content_type(self):
        """api_download Content-Type выставляется таким
        же как был при загрузке файла на сервер"""
        # test20
        _ = rq.post(self.api_upload, params={'id': 1,
                                             'name': 'test20',
                                             'tag': 'test', 'content-type': 'text_test_20'}, data="test2020")
        response = rq.get(self.api_download, params={'id': 1})
        self.assertEqual(response.headers['Content-Type'], 'text_test_20', "should be 'text_test_20'")

if __name__ == "__main__":
    unittest.main()
