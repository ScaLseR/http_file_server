from unittest.case import TestCase
from http_connector import ConnectorHttp


class EmptyStorageTests(TestCase):
    """тесты для пустой базы """

    def setUp(self):
        fsc = ConnectorHttp('http://127.0.0.1:9876')

    def test_download_by_id(self):
        fsc = ConnectorHttp('http://127.0.0.1:9876')
        result = fsc.download_by_id('1')
        print(result)

    def test_get_by_id(self):
        fsc = ConnectorHttp('http://127.0.0.1:9876')
        result = fsc.get_by_id('1')
        print(result)


class OneFileStorageTests(TestCase):
    """тесты для базы содержащей 1 файл"""
    pass


class ManyFilesStorageTests(TestCase):
    """тесты для базы содержащей большое количество файлов"""
    pass
