"""юнит тесты для API server.py"""
import unittest
import re
import os
import requests as rq
from jsonschema import validate


class TestApi(unittest.TestCase):
    """тестовый класс"""

    @classmethod
    def setUpClass(cls) -> None:
        dirname = r"./"
        files = os.listdir(dirname)
        for file in files:
            result = re.match(r'^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$', file)
            if result:
                os.remove(file)
            result2 = re.match(r'^\w$', file)
            if result2:
                os.remove(file)
        os.remove('file_server')
        print('файлы удалены, база очищена')

    def setUp(self) -> None:
        """прописываем дефолтные url значения и схему ответа json"""
        self.api_upload = "http://127.0.0.1:9876/api/upload"
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

    def test_api_upload_code_201(self):
        """проверка кода 201 при удачной загрузке файла"""
        #test1
        response = rq.post(self.api_upload, data="test1")
        self.assertEqual(response.status_code, 201, "should be code 201")

    def test_api_upload_valid_json_schema(self):
        """проверка ответа json на соответствие схеме"""
        #test2
        response = rq.post(self.api_upload, data="test2")
        response_body = response.json()
        validate(response_body, self.valid_json_schema)

    def test_api_upload_correct_content_length(self):
        """проверка правильного заполнения заголовка Content-Length"""
        # test3
        response = rq.post(self.api_upload, data="test3")
        response_body = response.json()
        self.assertEqual(response_body[0]['size'], 5, "Content-Length should be 5")

    def test_api_upload_full_param(self):
        """загрузка файла с корректно заполненными параметрами"""
        #test4
        response = rq.post(self.api_upload, params={'id': 4,
                                                    'name': 'test4', 'tag': 'test'}, data="test4")
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
        """загрузка файла с автоматической генерацией id и заполненным вручную именем файла name"""
        #test5
        response = rq.post(self.api_upload, params={'name': 'test5', 'tag': 'test'}, data="test5")
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
        """загрузка файла с автоматической генерацией
        id и не заполненным именем файла name, name = id"""
        #test6
        response = rq.post(self.api_upload, params={}, data="test6")
        response_body = response.json()
        self.assertEqual(response_body[0]['id'], response_body[0]['name'],
                         f"should be response_body['id'] = "
                         f"response_body['name'] = {response_body[0]['id']}")

    @unittest.expectedFailure
    def test_api_upload_rewrite_file_with_enable_id(self):
        """загрузка файла с уже существующим id, перезапись существующего файла"""
        #test7
        response = rq.post(self.api_upload, params={'id': 4, 'name': 'test7'}, data="test7")
        response_body = response.json()
        self.assertEqual(response_body[0]['name'],
                         'test7', f"should be response_body['name'] "
                                  f"= name = {response_body[0]['name']}")
        self.assertEqual(response_body[0]['tag'], '', "should be response_body['tag'] = ''")


if __name__ == "__main__":
    unittest.main()
