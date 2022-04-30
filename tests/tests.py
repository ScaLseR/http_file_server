from unittest.case import TestCase
from http_connector import ConnectorHttp
from jsonschema import validate
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
                                               name='test5',
                                               tag='test',
                                               mimetype='text/plain',
                                               modificationtime='2022-04-29 09:33:45'), {})

    #6
    def test_get_full_empty_parameters(self):
        self.assertEqual(self.fch.get_by_param(id='',
                                               name='',
                                               tag='',
                                               mimetype='',
                                               modificationtime=''), {})

    #7
    def test_get_several_similar_parameters(self):
        self.assertEqual(self.fch.get_by_param(id=[7, 7_1],
                                               name=['test7', 'test7_1'],
                                               tag=['test', 'test1']), {})

    #8
    def test_get_faulty_parameter(self):
        self.assertEqual(self.fch.get_by_param(param='test8'), {})

    #9
    def test_get_full_and_faulty_parameters(self):
        self.assertEqual(self.fch.get_by_param(id='9',
                                               name='test9',
                                               tag='test',
                                               mimetype='text/plain',
                                               modificationtime='2022-04-29 09:33:45',
                                               param='test8'), {})

    #10
    def test_delete_without_params(self):
        self.assertEqual(self.fch.delete_by_param(), (400, 'отсутствуют условия'))

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

    #13_3
    def test_delete_by_modificationtime(self):
        self.assertEqual(self.fch.delete_by_param(modificationtime='2022-04-29 09:33:45'),
                         '0 files deleted')

    #14
    def test_delete_full_parameters(self):
        self.assertEqual(self.fch.delete_by_param(id='14',
                                                  name='test14',
                                                  tag='test',
                                                  mimetype='text/plain',
                                                  modificationtime='2022-04-29 09:33:45'), '0 files deleted')

    #15
    def test_delete_full_empty_params(self):
        self.assertEqual(self.fch.delete_by_param(id='',
                                                  name='',
                                                  tag='',
                                                  mimetype='',
                                                  modificationtime=''), (400, 'отсутствуют условия'))

    #16
    def test_delete_several_similar_parameters(self):
        self.assertEqual(self.fch.delete_by_param(id=[7, 7_1],
                                                  name=['test7', 'test7_1'],
                                                  tag=['test', 'test1']), '0 files deleted')

    #17
    def test_delete_faulty_parameter(self):
        self.assertEqual(self.fch.delete_by_param(param='test17'), (400, 'отсутствуют условия'))

    #18
    def test_delete_full_and_faulty_parameters(self):
        self.assertEqual(self.fch.delete_by_param(id='18',
                                                  name='test18',
                                                  tag='test',
                                                  mimetype='text/plain',
                                                  modificationtime='2022-04-29 09:33:45',
                                                  param='test18'), '0 files deleted')

    #19
    def test_download_without_params(self):
        self.assertEqual(self.fch.download_without_param(), (400, 'отсутствуют условия'))

    #20
    def test_download_by_id(self):
        self.assertEqual(self.fch.download_by_param(id='20'), (404, 'файл не существует'))

    #21
    def test_download_by_several_id(self):
        self.assertEqual(self.fch.download_by_param(id=['21', '21_2']), (404, 'файл не существует'))

    #22
    def test_download_faulty_parameter(self):
        self.assertEqual(self.fch.download_by_param(param='test22'), (400, 'отсутствуют условия'))

    #23
    def test_download_by_id_and_fault_param(self):
        self.assertEqual(self.fch.download_by_param(id='23', param='test23'), (404, 'файл не существует'))

    #24
    def test_upload_without_param(self):
        self.assertCountEqual(self.fch.upload_by_param(data='test24'), {'id': '',
                                                                        'name': '',
                                                                        'tag': '',
                                                                        'size': '',
                                                                        'mimeType': '',
                                                                        'modificationTime': ''})

    #25
    def test_upload_by_name(self):
        self.assertEqual(self.fch.upload_by_param(name='test25', data='test25')['name'], 'test25')

    #26
    def test_upload_by_id_name(self):
        result = self.fch.upload_by_param(id='26', name='test26', data='test26')
        self.assertEqual(result['id'], '26')
        self.assertEqual(result['name'], 'test26')

    #27
    def test_upload_by_id_name_tag(self):
        result = self.fch.upload_by_param(id='27', name='test27', tag='test', data='test27')
        self.assertEqual(result['id'], '27')
        self.assertEqual(result['name'], 'test27')
        self.assertEqual(result['tag'], 'test')

    #28
    def test_upload_by_id(self):
        result = self.fch.upload_by_param(id='28', data='test28')
        self.assertEqual(result['id'], result['name'])

    #29
    def test_upload_without_param_data(self):
        self.assertCountEqual(self.fch.upload_by_param(), {'id': '',
                                                           'name': '',
                                                           'tag': '',
                                                           'size': '',
                                                           'mimeType': '',
                                                           'modificationTime': ''})

    #30
    def test_upload_full_param_and_faulty_param(self):
        self.assertCountEqual(self.fch.upload_by_param(id='30',
                                                       name='test30',
                                                       tag='test',
                                                       param='test30_param',
                                                       data='test30'), {'id': '',
                                                                        'name': '',
                                                                        'tag': '',
                                                                        'size': '',
                                                                        'mimeType': '',
                                                                        'modificationTime': ''})

    #30_2
    def test_upload_without_param_plus_faulty_param(self):
        self.assertCountEqual(self.fch.upload_by_param(param='test30_2'), {'id': '',
                                                                           'name': '',
                                                                           'tag': '',
                                                                           'size': '',
                                                                           'mimeType': '',
                                                                           'modificationTime': ''})

    #31
    def test_upload_several_id(self):
        result = self.fch.upload_by_param(id=['31', '31_2'], data='test31')
        self.assertEqual(result['id'], '31')

    #32
    def test_upload_several_name(self):
        result = self.fch.upload_by_param(name=['test32', 'test32_2'], data='test32')
        self.assertEqual(result['name'], 'test32')

    #33
    def test_upload_several_tag(self):
        result = self.fch.upload_by_param(tag=['test33', 'test33_2'], data='test33')
        self.assertEqual(result['tag'], 'test33')


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
