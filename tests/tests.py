from unittest.case import TestCase
from http_connector import ConnectorHttp


class EmptyStorageTests(TestCase):
    """тесты для пустой базы """

    @classmethod
    def setUpClass(cls) -> None:
        cls.fch = ConnectorHttp('http://127.0.0.1:9876')

    def tearDown(self) -> None:
        result = self.fch.get_without_params()
        for ids in result:
            self.fch.delete_by_id(ids['id'])

    def test_get_without_params(self):
        self.assertEqual(self.fch.get_without_params(), {})

    def test_get_by_id(self):
        self.assertEqual(self.fch.get_by_id('1'), {'id': '1', 'name': 'test1', 'tag': 'test2'})

    def test_download_by_id(self):
        self.assertEqual(self.fch.download_by_id('1'), '2_name2')

    def test_delete_by_id(self):
        self.assertEqual(self.fch.delete_by_id('11'), '1 files deleted')




class OneFileStorageTests(TestCase):
    """тесты для базы содержащей 1 файл"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.fch = ConnectorHttp('http://127.0.0.1:9876')

    def tearDown(self) -> None:
        result = self.fch.get_without_params()
        for ids in result:
            self.fch.delete_by_id(ids['id'])


class ManyFilesStorageTests(TestCase):
    """тесты для базы содержащей большое количество файлов"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.fch = ConnectorHttp('http://127.0.0.1:9876')

    def tearDown(self) -> None:
        result = self.fch.get_without_params()
        for ids in result:
            self.fch.delete_by_id(ids['id'])
