"""юнит тесты для API server.py"""
import unittest
import requests
import re


class TestApi(unittest.TestCase):
    """тестовый класс"""

    def setUp(self) -> None:
        """прописываем дефолтные url значения для ендпоинтов"""
        self.api_upload = "http://127.0.0.1:9876/api/upload"

    def test_api_upload_code_201(self):
        """проверка кода 201 при удачной загрузке файла"""
        #test1
        response = requests.post(self.api_upload, data="test1")
        self.assertEqual(response.status_code, 201, "should be code 201")

    def test_api_upload_correct_content_length(self):
        """проверка правильного заполнения заголовка Content-Length"""
        # test2
        response = requests.post(self.api_upload, data="test2")
        response_body = response.json()
        self.assertEqual(response_body[0]['size'], 5, "Content-Length should be 5")

    def test_api_upload_full_param(self):
        """загрузка файла с корректно заполненными параметрами"""
        #test3
        response = requests.post(self.api_upload,
                                 params={'id': 3, 'name': 'test3', 'tag': 'test'},
                                 data="test3")
        response_body = response.json()
        self.assertEqual(int(response_body[0]['id']), 3,
                         f"should be params['id'] = response_body['id'] = {int(response_body[0]['id'])}")
        self.assertEqual(response_body[0]['name'],
                         'test3', f"should be params['name'] = response_body['name'] = {response_body[0]['name']}")
        self.assertEqual(response_body[0]['tag'],
                         'test', f"should be params['tag'] = response_body['tag'] = {response_body[0]['tag']}")

    def test_api_upload_generate_id_with_name(self):
        """загрузка файла с автоматической генерацией id и заполненным вручную именем файла name"""
        #test4
        response = requests.post(self.api_upload,
                                 params={'name': 'test4', 'tag': 'test'},
                                 data="test4")
        response_body = response.json()
        result = re.match(r'^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$', response_body[0]['id'])
        generate_id = False
        if result:
            generate_id = True
        self.assertTrue(generate_id, "should be generated id")
        self.assertEqual(response_body[0]['name'],
                         'test4', f"should be params['name'] = response_body['name'] = {response_body[0]['name']}")

    def test_api_upload_generate_id_without_name(self):
        """загрузка файла с автоматической генерацией id и не заполненным именем файла name, name = id"""
        #test5
        response = requests.post(self.api_upload,
                                 params={},
                                 data="test5")
        response_body = response.json()
        self.assertEqual(response_body[0]['id'], response_body[0]['name'],
                         f"should be response_body['id'] = response_body['name'] = {response_body[0]['id']}")

    def test_api_upload_rewrite_file_with_enable_id(self):
        """загрузка файла с уже существующим id, перезапись существующего файла"""
        #test6
        response = requests.post(self.api_upload,
                                 params={'id': 3, 'name': 'test6'},
                                 data="test6")
        response_body = response.json()
        self.assertEqual(response_body[0]['name'],
                         'test6', f"should be response_body['name'] "
                                  f"= name = {response_body[0]['name']}")
        self.assertEqual(response_body[0]['tag'], '', "should be response_body['tag'] = ''")


if __name__ == "__main__":
    unittest.main()
