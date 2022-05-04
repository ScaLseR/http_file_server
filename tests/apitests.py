"""tests for api """
from unittest.case import TestCase
from http_connector import ConnectorHttp, ParamsReq


REFERENCE_DICT = {'id': '',
                  'name': '',
                  'tag': '',
                  'size': '',
                  'mimeType': '',
                  'modificationTime': ''}


class EmptyStorageTests(TestCase):# pylint: disable=too-many-public-methods
    """empty storage tests"""

    @classmethod
    def setUpClass(cls) -> None:
        """setup for class"""
        cls.fch = ConnectorHttp('http://127.0.0.1:9876')
        result = cls.fch.get_without_param()
        if isinstance(result, dict) and len(result) > 0:
            cls.fch.delete_by_param(ParamsReq(id=result['id']))
        else:
            for part in result:
                cls.fch.delete_by_param(ParamsReq(id=part['id']))

    def tearDown(self) -> None:
        """teardown after tests"""
        result = self.fch.get_without_param()
        if isinstance(result, dict) and len(result) > 0:
            self.fch.delete_by_param(ParamsReq(id=result['id']))
        else:
            for part in result:
                self.fch.delete_by_param(ParamsReq(id=part['id']))

    #1
    def test_get_without_params(self):
        """get without parameters"""
        self.assertEqual(self.fch.get_without_param(), {})

    #2
    def test_get_by_id(self):
        """get by id"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(id='2')), {})

    #3
    def test_get_by_name(self):
        """get by name"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(name='test3')), {})

    #4
    def test_get_by_tag(self):
        """get by tag"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(tag='test')), {})

    #4_1
    def test_get_by_mimetype(self):
        """get by mimeType"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(mimetype='text/plain')), {})

    #4_2
    def test_get_by_modificationtime(self):
        """get by modificationTime"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(
            modificationtime='2022-04-29 09:33:45')), {})

    #5
    def test_get_full_params(self):
        """get by all completed parameters"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(id='5',
                                                         name='test5',
                                                         tag='test',
                                                         mimetype='text/plain',
                                                         modificationtime='2022-04-29 09:33:45')),
                         {})

    #6
    def test_get_full_empty_params(self):
        """get by all parameters with empty data"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(id='',
                                                         name='',
                                                         tag='',
                                                         mimetype='',
                                                         modificationtime='')), {})

    #7
    def test_get_several_compound_params(self):
        """get with several compound parameters"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(id=('7', '7_1'),
                                                         name=('test7', 'test7_1'),
                                                         tag=('test', 'test1'))), {})

    #8
    def test_get_wrong_param(self):
        """get by only wrong parameter"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(param='test8')), {})

    #9
    def test_get_full_and_wrong_param(self):
        """get by all completed parameters add wrong parameter"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(id='9',
                                                         name='test9',
                                                         tag='test',
                                                         mimetype='text/plain',
                                                         modificationtime='2022-04-29 09:33:45',
                                                         param='test8')), {})

    #10
    def test_delete_without_params(self):
        """delete without parameters"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq()),
                         (400, 'отсутствуют условия'))

    #11
    def test_delete_by_id(self):
        """delete by id"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id='11')),
                         '0 files deleted')

    #12
    def test_delete_by_name(self):
        """delete by name"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(name='test12')),
                         '0 files deleted')

    #13
    def test_delete_by_tag(self):
        """delete by tag"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(tag='test')),
                         '0 files deleted')

    #13_2
    def test_delete_by_mimetype(self):
        """delete by mimetype"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(mimetype='text/plain')),
                         '0 files deleted')

    #13_3
    def test_delete_by_modificationtime(self):
        """delete by modification time"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(
            modificationtime='2022-04-29 09:33:45')), '0 files deleted')

    #14
    def test_delete_full_params(self):
        """delete by all completed parameters"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id='14',
                                                            name='test14',
                                                            tag='test',
                                                            mimetype='text/plain',
                                                            modificationtime='2022-04-29 '
                                                                             '09:33:45')),
                         '0 files deleted')

    #15
    def test_delete_full_empty_params(self):
        """delete by all parameters with empty data"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id='',
                                                            name='',
                                                            tag='',
                                                            mimetype='',
                                                            modificationtime='')),
                         (400, 'отсутствуют условия'))

    #16
    def test_delete_several_compound_params(self):
        """delete by several compound parameters"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id=('7', '7_1'),
                                                            name=('test7', 'test7_1'),
                                                            tag=('test', 'test1'))),
                         '0 files deleted')

    #17
    def test_delete_only_wrong_param(self):
        """delete by only one wrong parameter"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(param='test17')),
                         (400, 'отсутствуют условия'))

    #18
    def test_delete_full_add_wrong_params(self):
        """delete by all completed parameters add one wrong parameter"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id='18',
                                                            name='test18',
                                                            tag='test',
                                                            mimetype='text/plain',
                                                            modificationtime='2022-04-29 09:33:45',
                                                            param='test18')), '0 files deleted')

    #19
    def test_download_without_params(self):
        """download without parameters"""
        self.assertEqual(self.fch.download_without_param(),
                         (400, 'отсутствуют условия'))

    #20
    def test_download_by_id(self):
        """download by id"""
        self.assertEqual(self.fch.download_by_param(ParamsReq(id='20')),
                         (404, 'файл не существует'))

    #21
    def test_download_by_several_id(self):
        """download by several id"""
        self.assertEqual(self.fch.download_by_param(ParamsReq(id=('21', '21_2'))),
                         (404, 'файл не существует'))

    #22
    def test_download_wrong_param(self):
        """download by one wrong parameter"""
        self.assertEqual(self.fch.download_by_param(ParamsReq(param='test22')),
                         (400, 'отсутствуют условия'))

    #23
    def test_download_by_id_and_wrong_param(self):
        """download by id and wrong parameter"""
        self.assertEqual(self.fch.download_by_param(ParamsReq(id='23',
                                                              param='test23')),
                         (404, 'файл не существует'))

    #24
    def test_upload_without_param(self):
        """upload without parameters"""
        self.assertCountEqual(self.fch.upload_by_param(ParamsReq(), data='test24'),
                              REFERENCE_DICT)

    #25
    def test_upload_by_name(self):
        """upload by name"""
        self.assertEqual(self.fch.upload_by_param(ParamsReq(name='test25'),
                                                  data='test25')['name'], 'test25')

    #26
    def test_upload_by_id_name(self):
        """upload by id and name"""
        result = self.fch.upload_by_param(ParamsReq(id='26',
                                                    name='test26'), data='test26')
        self.assertEqual(result['id'], '26')
        self.assertEqual(result['name'], 'test26')

    #27
    def test_upload_by_id_name_tag(self):
        """upload by id, name, tag"""
        result = self.fch.upload_by_param(ParamsReq(id='27',
                                                    name='test27',
                                                    tag='test'), data='test27')
        self.assertEqual(result['id'], '27')
        self.assertEqual(result['name'], 'test27')
        self.assertEqual(result['tag'], 'test')

    #28
    def test_upload_by_id(self):
        """upload by id"""
        result = self.fch.upload_by_param(ParamsReq(id='28'), data='test28')
        self.assertEqual(result['id'], result['name'])

    #29
    def test_upload_without_param_data(self):
        """upload without parameters and playload"""
        self.assertCountEqual(self.fch.upload_by_param(ParamsReq()), REFERENCE_DICT)

    #30
    def test_upload_full_param_add_wrong_param(self):
        """upload all completed parameters add one wrong parameter"""
        self.assertCountEqual(self.fch.upload_by_param(ParamsReq(id='30',
                                                                 name='test30',
                                                                 tag='test',
                                                                 param='test30_param'),
                                                       data='test30'), REFERENCE_DICT)

    #30_2
    def test_upload_with_only_wrong_param(self):
        """upload with only one wrong parameter"""
        self.assertCountEqual(self.fch.upload_by_param(ParamsReq(param='test30_2')),
                              REFERENCE_DICT)

    #31
    def test_upload_several_id(self):
        """upload with several id"""
        result = self.fch.upload_by_param(ParamsReq(id=('31', '31_2')),
                                          data='test31')
        self.assertEqual(result['id'], '31')

    #32
    def test_upload_several_name(self):
        """upload with several name"""
        result = self.fch.upload_by_param(ParamsReq(name=('test32', 'test32_2')),
                                          data='test32')
        self.assertEqual(result['name'], 'test32')

    #33
    def test_upload_several_tag(self):
        """upload with several tag"""
        result = self.fch.upload_by_param(ParamsReq(tag=('test33', 'test33_2')),
                                          data='test33')
        self.assertEqual(result['tag'], 'test33')


class OneFileStorageTests(TestCase):# pylint: disable=too-many-public-methods
    """one file storage tests"""

    @classmethod
    def setUpClass(cls) -> None:
        """setup for class"""
        cls.fch = ConnectorHttp('http://127.0.0.1:9876')

    def setUp(self) -> None:
        self.fch.upload_by_param(ParamsReq(id='1',
                                           name='name1',
                                           tag='test'), data='1_name1')

    def tearDown(self) -> None:
        """teardown for tests"""
        result = self.fch.get_without_param()
        if isinstance(result, dict) and len(result) > 0:
            self.fch.delete_by_param(ParamsReq(id=result['id']))
        else:
            for part in result:
                self.fch.delete_by_param(ParamsReq(id=part['id']))

    #1
    def test_upload_change_name(self):
        """change name when loading an existing id with a new name"""
        result = self.fch.upload_by_param(ParamsReq(id='1', name='name2'))
        self.assertEqual(result['name'], 'name2')

    #2
    def test_upload_id_name_change_tag(self):
        """change tag when loading an existing id with a new tag"""
        result = self.fch.upload_by_param(ParamsReq(id='1',
                                                    name='name2',
                                                    tag='test2'))
        self.assertEqual(result['tag'], 'test2')

    #3
    def test_upload_change_data(self):
        """change data when loading an existing id with a new data"""
        self.fch.upload_by_param(ParamsReq(id='1',
                                           name='name2',
                                           tag='test'), data='2_name2')
        self.assertEqual(self.fch.download_by_param(ParamsReq(id='1')), '2_name2')

    #4
    def test_upload_full_param_and_wrong_param(self):
        """upload with wrong parameter"""
        self.assertCountEqual(self.fch.upload_by_param(ParamsReq(id='1',
                                                                 name='name2',
                                                                 tag='test4',
                                                                 param='test4')), REFERENCE_DICT)

    #5
    def test_upload_id_change_tag(self):
        """change tag when loading an existing id with a new tag"""
        result = self.fch.upload_by_param(ParamsReq(id='1',
                                                    tag='test5'))
        self.assertEqual(result['tag'], 'test5')

    #6
    def test_get_without_param(self):
        """get without parameters"""
        self.assertCountEqual(self.fch.get_by_param(ParamsReq()), REFERENCE_DICT)

    #7
    def test_get_wrong_param(self):
        """get with only wrong parameter"""
        self.assertCountEqual(self.fch.get_by_param(ParamsReq(param='test7')), REFERENCE_DICT)

    #8
    def test_get_by_id(self):
        """get by id"""
        result = self.fch.get_by_param(ParamsReq(id='1'))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '1')

    #9
    def test_get_by_wrong_id(self):
        """get by wrong id"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(id='2')), {})

    #10
    def test_get_by_name(self):
        """get by name"""
        result = self.fch.get_by_param(ParamsReq(name='name1'))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '1')

    #11
    def test_get_by_wrong_name(self):
        """get by wrong name"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(name='name')), {})

    #12
    def test_get_by_tag(self):
        """get by tag"""
        result = self.fch.get_by_param(ParamsReq(tag='test'))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '1')

    #13
    def test_get_by_wrong_tag(self):
        """get by wrong tag"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(tag='tes')), {})

    #14
    def test_get_by_size(self):
        """get by size"""
        result = self.fch.get_by_param(ParamsReq(size=7))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '1')

    #15
    def test_get_by_mimetype(self):
        """get by mimetype"""
        result = self.fch.get_by_param(ParamsReq(mimetype='text/plain'))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '1')

    #16
    def test_get_by_wrong_mimetype(self):
        """get by wrong mimetype"""
        self.assertEqual(self.fch.get_by_param(ParamsReq(mimetype='text')), {})

    #17
    def test_get_by_id_name(self):
        """get by id and name"""
        result = self.fch.get_by_param(ParamsReq(id='1',
                                                 name='name1'))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '1')

    #18
    def test_get_by_name_tag(self):
        """get by name and tag"""
        result = self.fch.get_by_param(ParamsReq(name='name1',
                                                 tag='test'))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '1')

    #19
    def test_get_full_params(self):
        """get with full complete parameters """
        result = self.fch.get_by_param(ParamsReq(id='1',
                                                 name='name1',
                                                 tag='test',
                                                 size='7',
                                                 mimetype='text/plain'))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '1')

    #20
    def test_get_full_params_without_param_data(self):
        """get with full parameters without parameters data"""
        result = self.fch.get_by_param(ParamsReq(id='',
                                       name='',
                                       tag='',
                                       size='',
                                       mimetype=''))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '1')

    #21
    def test_get_with_one_compound_params(self):
        """get with one compound parameters"""
        result = self.fch.get_by_param(ParamsReq(id=('1', '2')))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '1')

    #22
    def test_get_with_several_compound_params(self):
        """get with several compound parameters"""
        result = self.fch.get_by_param(ParamsReq(id=('1', '2'),
                                       name=('name1', 'name2')))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '1')

    #23
    def test_get_by_id_add_wrong_param(self):
        """get by id with wrong parameter"""
        result = self.fch.get_by_param(ParamsReq(id='1',
                                       param='test23'))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '1')

    #24
    def test_delete_by_id(self):
        """delete by id"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id='1')),
                         '1 files deleted')

    #25
    def test_delete_several_by_one_id(self):
        """several delete by one id"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id='1')),
                         '1 files deleted')
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id='1')),
                         '0 files deleted')

    #26
    def test_delete_by_wrong_id(self):
        """delete by wrong id"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id='2')),
                         '0 files deleted')

    #25
    def test_delete_by_name(self):
        """delete by name"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(name='name1')),
                         '1 files deleted')

    #26
    def test_delete_by_wrong_name(self):
        """delete by wrong name"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(name='name')),
                         '0 files deleted')

    #27
    def test_delete_by_tag(self):
        """delete by tag"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(tag='test')),
                         '1 files deleted')

    #28
    def test_delete_by_wrong_tag(self):
        """delete by wrong tag"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(tag='tes')),
                         '0 files deleted')

    #29
    def test_delete_by_all_params(self):
        """delete by all correctly completed parameters """
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id='1',
                                                            name='name1',
                                                            tag='test')),
                         '1 files deleted')

    #30
    def test_delete_one_incorrect_param(self):
        """delete by all parameters where one incorrect data"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id='1',
                                                            name='name1',
                                                            tag='tes')),
                         '0 files deleted')

    #31
    def test_delete_by_id_add_wrong_param(self):
        """delete by id with one wrong parameter"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id='1',
                                                            param='test31')),
                         '1 files deleted')

    #32
    def test_download_by_id(self):
        """download by id"""
        self.assertEqual(self.fch.download_by_param(ParamsReq(id='1')),
                         '1_name1')

    #33
    def test_download_several_by_one_id(self):
        """several downloads by one id"""
        self.assertEqual(self.fch.download_by_param(ParamsReq(id='1')),
                         '1_name1')
        self.assertEqual(self.fch.download_by_param(ParamsReq(id='1')),
                         '1_name1')

    #34
    def test_download_by_wrong_id(self):
        """download by wrong id"""
        self.assertEqual(self.fch.download_by_param(ParamsReq(id='2')),
                         (404, 'файл не существует'))

    #35
    def test_download_by_id_add_wrong_param(self):
        """download by id and wrong parameter"""
        self.assertEqual(self.fch.download_by_param(ParamsReq(id='1',
                                                              param='test35')),
                         '1_name1')

    #36
    def test_download_by_several_id(self):
        """download by several id"""
        self.assertEqual(self.fch.download_by_param(ParamsReq(id=('1', '2'),
                                                              param='test35')),
                         '1_name1')

    #37
    def test_download_by_id_check_content_type(self):
        """download by id and check content-type"""
        result = self.fch.download_check_param(ParamsReq(id='1'))
        self.assertMultiLineEqual(result['Content-type'], 'text/plain')

    #38
    def test_download_by_id_check_filename(self):
        """download by id and check filename"""
        result = self.fch.download_check_param(ParamsReq(id='1'))
        self.assertMultiLineEqual(result['Content-Disposition'][-5:], 'name1')

    #39
    def test_download_by_id_check_size(self):
        """download by id and check size"""
        result = self.fch.download_check_param(ParamsReq(id='1'))
        self.assertMultiLineEqual(result['Content-length'], '7')


class ManyFilesStorageTests(TestCase):
    """many files storage tests"""

    @classmethod
    def setUpClass(cls) -> None:
        """setup for class"""
        cls.fch = ConnectorHttp('http://127.0.0.1:9876')

    def setUp(self) -> None:
        """setup for tests"""
        self.fch.upload_by_param(ParamsReq(id='1',
                                           name='part_3_test',
                                           tag='test1'), data='test')
        self.fch.upload_by_param(ParamsReq(id='2',
                                           name='part_3_test_1',
                                           tag='test2'), data='test')
        self.fch.upload_by_param(ParamsReq(id='3',
                                           name='part_3_test_2',
                                           tag='test1'), data='test')
        self.fch.upload_by_param(ParamsReq(id='4',
                                           name='part_3_test',
                                           tag='test2'), data='test')

    def tearDown(self) -> None:
        """teardown for tests"""
        result = self.fch.get_without_param()
        for ids in result:
            self.fch.delete_by_param(ParamsReq(id=ids['id']))

    #1
    def test_upload_by_params(self):
        """upload new file by all parameters"""
        result = self.fch.upload_by_param(ParamsReq(id='5',
                                                    name='part_3_test_5',
                                                    tag='test5'), data='test5')
        self.assertCountEqual(result, REFERENCE_DICT)

    #2
    def test_upload_several_files_by_same_params(self):
        """upload several files with the same parameters"""
        result = self.fch.upload_by_param(ParamsReq(id='5',
                                                    name='part_3_test_5',
                                                    tag='test5'), data='test5')
        self.assertCountEqual(result, REFERENCE_DICT)
        result = self.fch.upload_by_param(ParamsReq(id='5',
                                                    name='part_3_test_5',
                                                    tag='test5'), data='test5')
        self.assertCountEqual(result, REFERENCE_DICT)
        result = self.fch.upload_by_param(ParamsReq(id='5',
                                                    name='part_3_test_5',
                                                    tag='test5'), data='test5')
        self.assertCountEqual(result, REFERENCE_DICT)

    #3
    def test_upload_only_playload(self):
        """upload file without parameters only playload"""
        result = self.fch.upload_by_param(ParamsReq(), data='test3')
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], result['name'])

    #4
    def test_get_without_params(self):
        """get without parameters"""
        self.assertEqual(len(self.fch.get_without_param()), 4)

    #5
    def test_get_full_params(self):
        """get by full correctly completed parameters"""
        result = self.fch.get_by_param(ParamsReq(id='2',
                                                 name='part_3_test_1',
                                                 tag='test2'))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '2')

    #6
    def test_get_by_name_tag(self):
        """get by name and tag"""
        result = self.fch.get_by_param(ParamsReq(name='part_3_test_1',
                                                 tag='test2'))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '2')

    #7
    def test_get_files_by_name_tag(self):
        """get few files by name and tag"""
        self.fch.upload_by_param(ParamsReq(name='part_3_test_7',
                                           tag='test'), data='test7')
        self.fch.upload_by_param(ParamsReq(name='part_3_test_7',
                                           tag='test'), data='test7')
        self.fch.upload_by_param(ParamsReq(name='part_3_test_7',
                                           tag='test'), data='test7')
        self.assertEqual(len(self.fch.get_by_param(ParamsReq(name='part_3_test_7',
                                                             tag='test'))), 3)

    #8
    def test_get_few_files_by_name_tag(self):
        """get few files by name and tag"""
        self.fch.upload_by_param(ParamsReq(id='5',
                                           name='part_3_test',
                                           tag='test1'), data='test')
        self.assertEqual(len(self.fch.get_by_param(ParamsReq(name='part_3_test',
                                                             tag='test1'))), 2)

    #9
    def test_get_several_id_name(self):
        """get by several compound parameters id, name and one tag"""
        result = self.fch.get_by_param(ParamsReq(id=('1', '2', '3', '4'),
                                                 name=('part_3_test', 'part_3_test_1'),
                                                 tag='test1'))
        self.assertCountEqual(result, REFERENCE_DICT)
        self.assertEqual(result['id'], '1')

    #10
    def test_get_several_id_name_tag(self):
        """get by several compound parameters id, name and tag"""
        self.assertEqual(len(self.fch.get_by_param(ParamsReq(id=('1', '2', '3', '4'),
                                                             name=('part_3_test',
                                                                   'part_3_test_1'),
                                                             tag=('test1', 'test2')))), 3)

    #11
    def test_delete_name_tag(self):
        """delete by name and tag parameters"""
        self.fch.upload_by_param(ParamsReq(name='part_3_test_11',
                                           tag='test'), data='test11')
        self.fch.upload_by_param(ParamsReq(name='part_3_test_11',
                                           tag='test'), data='test11')
        self.fch.upload_by_param(ParamsReq(name='part_3_test_11',
                                           tag='test'), data='test11')
        self.assertEqual(self.fch.delete_by_param(ParamsReq(name='part_3_test_11',
                                                            tag='test')), '3 files deleted')

    #12
    def test_delete_name_several_tag(self):
        """delete by name and several tag"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(name='part_3_test',
                                                            tag=('test1', 'test2'))),
                         '2 files deleted')

    #13
    def test_delete_several_name_id(self):
        """delete by several id, name and one tag"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id=('1', '2', '3', '4'),
                                                            name=('part_3_test', 'part_3_test_1'),
                                                            tag='test1')), '1 files deleted')

    #14
    def test_delete_several_id_name_tag(self):
        """delete by several id, name and tag"""
        self.assertEqual(self.fch.delete_by_param(ParamsReq(id=('1', '2', '3', '4'),
                                                            name=('part_3_test',
                                                                  'part_3_test_1'),
                                                            tag=('test1', 'test'))),
                         '1 files deleted')
