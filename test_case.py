"""юнит тесты для API server.py"""
import unittest
import requests
import re


class TestApi(unittest.TestCase):
    """тестовый класс"""
    api_upload = r"http://127.0.0.1:9876/api/upload"

    def test_api_upload_code_201(self):
        """проверка кода 201 при удачной загрузке файла"""
        response = requests.post(self.api_upload, data="123123awerdaew1234")
        self.assertEqual(response.status_code, 201, "should be code 201")

    def test_api_upload_full_param(self):
        """загрузка файла с корректно заполненными параметрами"""
        response = requests.post(self.api_upload,
                                 params={'id': 2, 'name': 'test2', 'tag': 'test'},
                                 data="qweqwewqedsadzdxfcewqrq34w5rdasf")
        response_body = response.json()
        self.assertEqual(int(response_body[0]['id']), 2,
                         f"should be params['id'] = response_body['id'] = {int(response_body[0]['id'])}")
        self.assertEqual(response_body[0]['name'],
                         'test2', f"should be params['name'] = response_body['name'] = {response_body[0]['name']}")
        self.assertEqual(response_body[0]['tag'],
                         'test', f"should be params['tag'] = response_body['tag'] = {response_body[0]['tag']}")

    def test_api_upload_generate_id_with_name(self):
        """загрузка файла с автоматической генерацией id и заполненным вручную именем файла name"""
        response = requests.post(self.api_upload,
                                 params={'name': 'test3', 'tag': 'test'},
                                 data="123qweqdsadzdxrq34w5rdasf")
        response_body = response.json()
        result = re.match(r'^\w{8}-\w{4}-\w{4}-\w{4}-\w{12}$', response_body[0]['id'])
        generate_id = False
        if result:
            generate_id = True
        self.assertEqual(generate_id, True, "should be generated id ")
        self.assertEqual(response_body[0]['name'],
                         'test3', f"should be params['name'] = response_body['name'] = {response_body[0]['name']}")

    def test_api_upload_generate_id_without_name(self):
        """загрузка файла с автоматической генерацией id и не заполненным именем файла name"""
        response = requests.post(self.api_upload,
                                 params={},
                                 data="123qweqdsadzdxrrdasf")
        response_body = response.json()
        self.assertEqual(response_body[0]['id'], response_body[0]['name'],
                         f"should be response_body['id'] = response_body['name'] = {response_body[0]['id']}")


if __name__ == "__main__":
    unittest.main()
