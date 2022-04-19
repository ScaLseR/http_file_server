"""юнит тесты для API server.py"""
import unittest
import requests


class TestApi(unittest.TestCase):
    """тестовый класс"""
    def test_api_upload_code_201(self):
        """проверка кода 201 при удачной загрузке файла"""
        response = requests.post("http://127.0.0.1:9876/api/upload")
        self.assertEqual(response.status_code, 201, "should be code 201")

    def test_api_upload_full_param(self):
        """загрузка файла с корректно заполненными параметрами"""



if __name__ == "__main__":
    unittest.main()
