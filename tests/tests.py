from unittest.case import TestCase
from http_connector import ConnectorHttp
from requests import HTTPError


class EmptyStorageTests(TestCase):
    """empty storage tests"""

    @classmethod
    def setUpClass(cls) -> None:
        """setup for class"""
        cls.fch = ConnectorHttp('http://127.0.0.1:9876')

    def setUp(self) -> None:
        """setup for tests"""
        result = self.fch.get_by_param()
        if isinstance(result, dict) and len(result) > 0:
            self.fch.delete_by_param(id=result['id'])
        else:
            for part in result:
                self.fch.delete_by_param(id=part['id'])

    def tearDown(self) -> None:
        """teardown for tests"""
        result = self.fch.get_by_param()
        if isinstance(result, dict) and len(result) > 0:
            self.fch.delete_by_param(id=result['id'])
        else:
            for part in result:
                self.fch.delete_by_param(id=part['id'])

    #1
    def test_get_without_params(self):
        self.assertEqual(self.fch.get_by_param(), {})

    #2
    def test_get_by_id(self):
        self.assertEqual(self.fch.get_by_param(id='2'), {})

    #3
    def test_get_by_name(self):
        self.assertEqual(self.fch.get_by_param(name='test3'), {})

    #4
    def test_get_by_tag(self):
        self.assertEqual(self.fch.get_by_param(tag='test'), {})

    #4_1
    def test_get_by_mimeType(self):
        self.assertEqual(self.fch.get_by_param(mimetype='text/plain'), {})

    #4_2
    def test_get_by_modificationTime(self):
        self.assertEqual(self.fch.get_by_param(modificationtime='2022-04-29 09:33:45'), {})

    #5
    def test_get_full_parameters(self):
        self.assertEqual(self.fch.get_by_param(id='5',
                                               name='test5', tag='test', mimetype='text/plain',
                                               modificationtime='2022-04-29 09:33:45'), {})

    #6
    def test_get_full_empty_parameters(self):
        self.assertEqual(self.fch.get_by_param(id='',
                                               name='', tag='', mimetype='',
                                               modificationtime=''), {})

    #7
    def test_get_several_similar_parameters(self):
        self.assertEqual(self.fch.get_by_param(id=[7, 7_1], name=['test7', 'test7_1'],
                                               tag=['test', 'test1']), {})

    #8
    def test_get_faulty_parameter(self):
        self.assertEqual(self.fch.get_by_faulty_param(param='test8'), {})

    #9
    def test_get_full_and_faulty_parameters(self):
        self.assertEqual(self.fch.get_by_faulty_param(id='9',
                                                      name='test9',
                                                      tag='test',
                                                      mimetype='text/plain',
                                                      modificationtime='2022-04-29 09:33:45',
                                                      param='test8'), {})

    #10
    def test_delete_without_params(self):
        with self.assertRaises(HTTPError):
            self.fch.delete_by_param()

    #11
    def test_delete_by_id(self):
        self.assertEqual(self.fch.delete_by_param(id='11'), '0 files deleted')

    #12
    def test_delete_by_name(self):
        self.assertEqual(self.fch.delete_by_param(name='test12'), '0 files deleted')

    #13
    def test_delete_by_tag(self):
        self.assertEqual(self.fch.delete_by_param(tag='test'), '0 files deleted')

    #13_2
    def test_delete_by_mimetype(self):
        self.assertEqual(self.fch.delete_by_param(mimetype='text/plain'), '0 files deleted')






class OneFileStorageTests(TestCase):
    """one file storage tests"""

    @classmethod
    def setUpClass(cls) -> None:
        """setup for class"""
        cls.fch = ConnectorHttp('http://127.0.0.1:9876')

    def tearDown(self) -> None:
        """teardown for tests"""
        result = self.fch.get_by_param()
        for ids in result:
            self.fch.delete_by_param(id=ids['id'])


class ManyFilesStorageTests(TestCase):
    """many files storage tests"""

    @classmethod
    def setUpClass(cls) -> None:
        """setup for class"""
        cls.fch = ConnectorHttp('http://127.0.0.1:9876')

    def tearDown(self) -> None:
        """teardown for tests"""
        result = self.fch.get_by_param()
        for ids in result:
            self.fch.delete_by_param(id=ids['id'])
