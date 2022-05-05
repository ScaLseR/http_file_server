"""tests for api """
import unittest
from http_connector import ParamsReq


REFERENCE_DICT = {'id': '',
                  'name': '',
                  'tag': '',
                  'size': '',
                  'mimeType': '',
                  'modificationTime': ''}


class TestEmptyStorage:
    """empty storage tests"""

    #1
    def test_get_without_params(self, fch):
        """get without parameters"""
        assert fch.get_without_param() == {}

    #2
    def test_get_by_id(self, fch):
        """get by id"""
        assert fch.get_by_param(ParamsReq(id='2')) == {}

    #3
    def test_get_by_name(self, fch):
        """get by name"""
        assert fch.get_by_param(ParamsReq(name='test3')) == {}

    #4
    def test_get_by_tag(self, fch):
        """get by tag"""
        assert fch.get_by_param(ParamsReq(tag='test')) == {}

    #4_1
    def test_get_by_mimetype(self, fch):
        """get by mimeType"""
        assert fch.get_by_param(ParamsReq(mimetype='text/plain')) == {}

    #4_2
    def test_get_by_modificationtime(self, fch):
        """get by modificationTime"""
        assert fch.get_by_param(ParamsReq(
            modificationtime='2022-04-29 09:33:45')) == {}

    #5
    def test_get_full_params(self, fch):
        """get by all completed parameters"""
        assert fch.get_by_param(ParamsReq(id='5',
                                          name='test5',
                                          tag='test',
                                          mimetype='text/plain',
                                          modificationtime='2022-04-29 09:33:45')) == {}

    #6
    def test_get_full_empty_params(self, fch):
        """get by all parameters with empty data"""
        assert fch.get_by_param(ParamsReq(id='',
                                          name='',
                                          tag='',
                                          mimetype='',
                                          modificationtime='')) == {}

    #7
    def test_get_several_compound_params(self, fch):
        """get with several compound parameters"""
        assert fch.get_by_param(ParamsReq(id=('7', '7_1'),
                                          name=('test7', 'test7_1'),
                                          tag=('test', 'test1'))) == {}

    #8
    def test_get_wrong_param(self, fch):
        """get by only wrong parameter"""
        assert fch.get_by_param(ParamsReq(param='test8')) == {}

    #9
    def test_get_full_and_wrong_param(self, fch):
        """get by all completed parameters add wrong parameter"""
        assert fch.get_by_param(ParamsReq(id='9',
                                          name='test9',
                                          tag='test',
                                          mimetype='text/plain',
                                          modificationtime='2022-04-29 09:33:45',
                                          param='test8')) == {}

    #10
    def test_delete_without_params(self, fch):
        """delete without parameters"""
        assert fch.delete_by_param(ParamsReq()) == (400, 'отсутствуют условия')

    #11
    def test_delete_by_id(self, fch):
        """delete by id"""
        assert fch.delete_by_param(ParamsReq(id='11')) == '0 files deleted'

    #12
    def test_delete_by_name(self, fch):
        """delete by name"""
        assert fch.delete_by_param(ParamsReq(name='test12')) == '0 files deleted'

    #13
    def test_delete_by_tag(self, fch):
        """delete by tag"""
        assert fch.delete_by_param(ParamsReq(tag='test')) == '0 files deleted'

    #13_2
    def test_delete_by_mimetype(self, fch):
        """delete by mimetype"""
        assert fch.delete_by_param(ParamsReq(mimetype='text/plain')) == '0 files deleted'

    #13_3
    def test_delete_by_modificationtime(self, fch):
        """delete by modification time"""
        assert fch.delete_by_param(ParamsReq(
            modificationtime='2022-04-29 09:33:45')) == '0 files deleted'

    #14
    def test_delete_full_params(self, fch):
        """delete by all completed parameters"""
        assert fch.delete_by_param(ParamsReq(id='14',
                                             name='test14',
                                             tag='test',
                                             mimetype='text/plain',
                                             modificationtime='2022-04-29 09:33:45')) == '0 files deleted'

    #15
    def test_delete_full_empty_params(self, fch):
        """delete by all parameters with empty data"""
        assert fch.delete_by_param(ParamsReq(id='',
                                             name='',
                                             tag='',
                                             mimetype='',
                                             modificationtime='')) == (400, 'отсутствуют условия')

    #16
    def test_delete_several_compound_params(self, fch):
        """delete by several compound parameters"""
        assert fch.delete_by_param(ParamsReq(id=('7', '7_1'),
                                             name=('test7', 'test7_1'),
                                             tag=('test', 'test1'))) == '0 files deleted'

    #17
    def test_delete_only_wrong_param(self, fch):
        """delete by only one wrong parameter"""
        assert fch.delete_by_param(ParamsReq(param='test17')) == (400, 'отсутствуют условия')

    #18
    def test_delete_full_add_wrong_params(self, fch):
        """delete by all completed parameters add one wrong parameter"""
        assert fch.delete_by_param(ParamsReq(id='18',
                                             name='test18',
                                             tag='test',
                                             mimetype='text/plain',
                                             modificationtime='2022-04-29 09:33:45',
                                             param='test18')) == '0 files deleted'

    #19
    def test_download_without_params(self, fch):
        """download without parameters"""
        assert fch.download_without_param() == (400, 'отсутствуют условия')

    #20
    def test_download_by_id(self, fch):
        """download by id"""
        assert fch.download_by_param(ParamsReq(id='20')) == (404, 'файл не существует')

    #21
    def test_download_by_several_id(self, fch):
        """download by several id"""
        assert fch.download_by_param(ParamsReq(id=('21', '21_2'))) == (404, 'файл не существует')

    #22
    def test_download_wrong_param(self, fch):
        """download by one wrong parameter"""
        assert fch.download_by_param(ParamsReq(param='test22')) == (400, 'отсутствуют условия')

    #23
    def test_download_by_id_and_wrong_param(self, fch):
        """download by id and wrong parameter"""
        assert fch.download_by_param(ParamsReq(id='23',
                                               param='test23')) == (404, 'файл не существует')

    #24
    def test_upload_without_param(self, fch):
        """upload without parameters"""
        case = unittest.TestCase()
        case.assertCountEqual(fch.upload_by_param(ParamsReq(), data='test24'),
                              REFERENCE_DICT)

    #25
    def test_upload_by_name(self, fch):
        """upload by name"""
        assert fch.upload_by_param(ParamsReq(name='test25'),
                                   data='test25')['name'] == 'test25'

    #26
    def test_upload_by_id_name(self, fch):
        """upload by id and name"""
        result = fch.upload_by_param(ParamsReq(id='26',
                                               name='test26'),
                                     data='test26')
        assert result['id'] == '26'
        assert result['name'] == 'test26'

    #27
    def test_upload_by_id_name_tag(self, fch):
        """upload by id, name, tag"""
        result = fch.upload_by_param(ParamsReq(id='27',
                                               name='test27',
                                               tag='test'),
                                     data='test27')
        assert result['id'] == '27'
        assert result['name'] == 'test27'
        assert result['tag'] == 'test'

    #28
    def test_upload_by_id(self, fch):
        """upload by id"""
        result = fch.upload_by_param(ParamsReq(id='28'),
                                     data='test28')
        assert result['id'] == result['name']

    #29
    def test_upload_without_param_data(self, fch):
        """upload without parameters and playload"""
        case = unittest.TestCase()
        case.assertCountEqual(fch.upload_by_param(ParamsReq()), REFERENCE_DICT)

    #30
    def test_upload_full_param_add_wrong_param(self, fch):
        """upload all completed parameters add one wrong parameter"""
        case = unittest.TestCase()
        case.assertCountEqual(fch.upload_by_param(ParamsReq(id='30',
                                                            name='test30',
                                                            tag='test',
                                                            param='test30_param'),
                                                  data='test30'), REFERENCE_DICT)

    #30_2
    def test_upload_with_only_wrong_param(self, fch):
        """upload with only one wrong parameter"""
        case = unittest.TestCase()
        case.assertCountEqual(fch.upload_by_param(ParamsReq(param='test30_2')),
                              REFERENCE_DICT)

    #31
    def test_upload_several_id(self, fch):
        """upload with several id"""
        result = fch.upload_by_param(ParamsReq(id=('31', '31_2')),
                                     data='test31')
        assert result['id'] == '31'

    #32
    def test_upload_several_name(self, fch):
        """upload with several name"""
        result = fch.upload_by_param(ParamsReq(name=('test32', 'test32_2')),
                                     data='test32')
        assert result['name'] == 'test32'

    #33
    def test_upload_several_tag(self, fch):
        """upload with several tag"""
        result = fch.upload_by_param(ParamsReq(tag=('test33', 'test33_2')),
                                     data='test33')
        assert result['tag'] == 'test33'


class TestOneFileStorage:
    """one file storage tests"""

    #1
    def test_upload_change_name(self, upl_one):
        """change name when loading an existing id with a new name"""
        result = upl_one.upload_by_param(ParamsReq(id='1',
                                                   name='name2'))
        assert result['name'] == 'name2'

    #2
    def test_upload_id_name_change_tag(self, upl_one):
        """change tag when loading an existing id with a new tag"""
        result = upl_one.upload_by_param(ParamsReq(id='1',
                                                   name='name2',
                                                   tag='test2'))
        assert result['tag'] == 'test2'

    #3
    def test_upload_change_data(self, upl_one):
        """change data when loading an existing id with a new data"""
        upl_one.upload_by_param(ParamsReq(id='1',
                                          name='name2',
                                          tag='test'), data='2_name2')
        assert upl_one.download_by_param(ParamsReq(id='1')) == '2_name2'

    #4
    def test_upload_full_param_and_wrong_param(self, upl_one):
        """upload with wrong parameter"""
        case = unittest.TestCase()
        case.assertCountEqual(upl_one.upload_by_param(ParamsReq(id='1',
                                                                name='name2',
                                                                tag='test4',
                                                                param='test4')), REFERENCE_DICT)

    #5
    def test_upload_id_change_tag(self, upl_one):
        """change tag when loading an existing id with a new tag"""
        result = upl_one.upload_by_param(ParamsReq(id='1',
                                                   tag='test5'))
        assert result['tag'] == 'test5'

    #6
    def test_get_without_param(self, upl_one):
        """get without parameters"""
        case = unittest.TestCase()
        case.assertCountEqual(upl_one.get_by_param(ParamsReq()), REFERENCE_DICT)

    #7
    def test_get_wrong_param(self, upl_one):
        """get with only wrong parameter"""
        case = unittest.TestCase()
        case.assertCountEqual(upl_one.get_by_param(ParamsReq(param='test7')), REFERENCE_DICT)

    #8
    def test_get_by_id(self, upl_one):
        """get by id"""
        case = unittest.TestCase()
        result = upl_one.get_by_param(ParamsReq(id='1'))
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '1'

    #9
    def test_get_by_wrong_id(self, upl_one):
        """get by wrong id"""
        assert upl_one.get_by_param(ParamsReq(id='2')) == {}

    #10
    def test_get_by_name(self, upl_one):
        """get by name"""
        case = unittest.TestCase()
        result = upl_one.get_by_param(ParamsReq(name='name1'))
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '1'

    #11
    def test_get_by_wrong_name(self, upl_one):
        """get by wrong name"""
        assert upl_one.get_by_param(ParamsReq(name='name')) == {}

    #12
    def test_get_by_tag(self, upl_one):
        """get by tag"""
        case = unittest.TestCase()
        result = upl_one.get_by_param(ParamsReq(tag='test'))
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '1'

    #13
    def test_get_by_wrong_tag(self, upl_one):
        """get by wrong tag"""
        assert upl_one.get_by_param(ParamsReq(tag='tes')) == {}

    #14
    def test_get_by_size(self, upl_one):
        """get by size"""
        case = unittest.TestCase()
        result = upl_one.get_by_param(ParamsReq(size=7))
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '1'

    #15
    def test_get_by_mimetype(self, upl_one):
        """get by mimetype"""
        case = unittest.TestCase()
        result = upl_one.get_by_param(ParamsReq(mimetype='text/plain'))
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '1'

    #16
    def test_get_by_wrong_mimetype(self, upl_one):
        """get by wrong mimetype"""
        assert upl_one.get_by_param(ParamsReq(mimetype='text')) == {}

    #17
    def test_get_by_id_name(self, upl_one):
        """get by id and name"""
        case = unittest.TestCase()
        result = upl_one.get_by_param(ParamsReq(id='1',
                                                name='name1'))
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '1'

    #18
    def test_get_by_name_tag(self, upl_one):
        """get by name and tag"""
        case = unittest.TestCase()
        result = upl_one.get_by_param(ParamsReq(name='name1',
                                                tag='test'))
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '1'

    #19
    def test_get_full_params(self, upl_one):
        """get with full complete parameters """
        case = unittest.TestCase()
        result = upl_one.get_by_param(ParamsReq(id='1',
                                                name='name1',
                                                tag='test',
                                                size='7',
                                                mimetype='text/plain'))
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '1'

    #20
    def test_get_full_params_without_param_data(self, upl_one):
        """get with full parameters without parameters data"""
        case = unittest.TestCase()
        result = upl_one.get_by_param(ParamsReq(id='',
                                                name='',
                                                tag='',
                                                size='',
                                                mimetype=''))
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '1'

    #21
    def test_get_with_one_compound_params(self, upl_one):
        """get with one compound parameters"""
        case = unittest.TestCase()
        result = upl_one.get_by_param(ParamsReq(id=('1', '2')))
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '1'

    #22
    def test_get_with_several_compound_params(self, upl_one):
        """get with several compound parameters"""
        case = unittest.TestCase()
        result = upl_one.get_by_param(ParamsReq(id=('1', '2'),
                                                name=('name1', 'name2')))
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '1'

    #23
    def test_get_by_id_add_wrong_param(self, upl_one):
        """get by id with wrong parameter"""
        case = unittest.TestCase()
        result = upl_one.get_by_param(ParamsReq(id='1',
                                                param='test23'))
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '1'

    #24
    def test_delete_by_id(self, upl_one):
        """delete by id"""
        assert upl_one.delete_by_param(ParamsReq(id='1')) == '1 files deleted'

    #25
    def test_delete_several_by_one_id(self, upl_one):
        """several delete by one id"""
        assert upl_one.delete_by_param(ParamsReq(id='1')) == '1 files deleted'
        assert upl_one.delete_by_param(ParamsReq(id='1')) == '0 files deleted'

    #26
    def test_delete_by_wrong_id(self, upl_one):
        """delete by wrong id"""
        assert upl_one.delete_by_param(ParamsReq(id='2')) == '0 files deleted'

    #25
    def test_delete_by_name(self, upl_one):
        """delete by name"""
        assert upl_one.delete_by_param(ParamsReq(name='name1')) == '1 files deleted'

    #26
    def test_delete_by_wrong_name(self, upl_one):
        """delete by wrong name"""
        assert upl_one.delete_by_param(ParamsReq(name='name')) == '0 files deleted'

    #27
    def test_delete_by_tag(self, upl_one):
        """delete by tag"""
        assert upl_one.delete_by_param(ParamsReq(tag='test')) == '1 files deleted'

    #28
    def test_delete_by_wrong_tag(self, upl_one):
        """delete by wrong tag"""
        assert upl_one.delete_by_param(ParamsReq(tag='tes')) == '0 files deleted'

    #29
    def test_delete_by_all_params(self, upl_one):
        """delete by all correctly completed parameters """
        assert upl_one.delete_by_param(ParamsReq(id='1',
                                                 name='name1',
                                                 tag='test')) == '1 files deleted'

    #30
    def test_delete_one_incorrect_param(self, upl_one):
        """delete by all parameters where one incorrect data"""
        assert upl_one.delete_by_param(ParamsReq(id='1',
                                                 name='name1',
                                                 tag='tes')) == '0 files deleted'

    #31
    def test_delete_by_id_add_wrong_param(self, upl_one):
        """delete by id with one wrong parameter"""
        assert upl_one.delete_by_param(ParamsReq(id='1',
                                                 param='test31')) == '1 files deleted'

    #32
    def test_download_by_id(self, upl_one):
        """download by id"""
        assert upl_one.download_by_param(ParamsReq(id='1')) == '1_name1'

    #33
    def test_download_several_by_one_id(self, upl_one):
        """several downloads by one id"""
        assert upl_one.download_by_param(ParamsReq(id='1')) == '1_name1'
        assert upl_one.download_by_param(ParamsReq(id='1')) == '1_name1'

    #34
    def test_download_by_wrong_id(self, upl_one):
        """download by wrong id"""
        assert upl_one.download_by_param(ParamsReq(id='2')) == (404, 'файл не существует')

    #35
    def test_download_by_id_add_wrong_param(self, upl_one):
        """download by id and wrong parameter"""
        assert upl_one.download_by_param(ParamsReq(id='1',
                                                   param='test35')) == '1_name1'

    #36
    def test_download_by_several_id(self, upl_one):
        """download by several id"""
        assert upl_one.download_by_param(ParamsReq(id=('1', '2'),
                                                   param='test35')) == '1_name1'

    #37
    def test_download_by_id_check_content_type(self, upl_one):
        """download by id and check content-type"""
        result = upl_one.download_check_param(ParamsReq(id='1'))
        assert result['Content-type'] == 'text/plain'

    #38
    def test_download_by_id_check_filename(self, upl_one):
        """download by id and check filename"""
        result = upl_one.download_check_param(ParamsReq(id='1'))
        assert result['Content-Disposition'][-5:] == 'name1'

    #39
    def test_download_by_id_check_size(self, upl_one):
        """download by id and check size"""
        result = upl_one.download_check_param(ParamsReq(id='1'))
        assert result['Content-length'] == '7'


class TestManyFilesStorage:
    """many files storage tests"""

    #1
    def test_upload_by_params(self, upl_few):
        """upload new file by all parameters"""
        case = unittest.TestCase()
        result = upl_few.upload_by_param(ParamsReq(id='5',
                                                   name='part_3_test_5',
                                                   tag='test5'), data='test5')
        case.assertCountEqual(result, REFERENCE_DICT)

    #2
    def test_upload_several_files_by_same_params(self, upl_few):
        """upload several files with the same parameters"""
        case = unittest.TestCase()
        result = upl_few.upload_by_param(ParamsReq(id='5',
                                                   name='part_3_test_5',
                                                   tag='test5'), data='test5')
        case.assertCountEqual(result, REFERENCE_DICT)
        result = upl_few.upload_by_param(ParamsReq(id='5',
                                                   name='part_3_test_5',
                                                   tag='test5'), data='test5')
        case.assertCountEqual(result, REFERENCE_DICT)
        result = upl_few.upload_by_param(ParamsReq(id='5',
                                                   name='part_3_test_5',
                                                   tag='test5'), data='test5')
        case.assertCountEqual(result, REFERENCE_DICT)

    #3
    def test_upload_only_playload(self, upl_few):
        """upload file without parameters only playload"""
        case = unittest.TestCase()
        result = upl_few.upload_by_param(ParamsReq(), data='test3')
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == result['name']

    #4
    def test_get_without_params(self, upl_few):
        """get without parameters"""
        assert len(upl_few.get_without_param()) == 4

    #5
    def test_get_full_params(self, upl_few):
        """get by full correctly completed parameters"""
        result = upl_few.get_by_param(ParamsReq(id='2',
                                                name='part_3_test_1',
                                                tag='test2'))
        case = unittest.TestCase()
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '2'

    #6
    def test_get_by_name_tag(self, upl_few):
        """get by name and tag"""
        result = upl_few.get_by_param(ParamsReq(name='part_3_test_1',
                                                tag='test2'))
        case = unittest.TestCase()
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '2'

    #7
    def test_get_files_by_name_tag(self, upl_few):
        """get few files by name and tag"""
        upl_few.upload_by_param(ParamsReq(name='part_3_test_7', tag='test'), data='test7')
        upl_few.upload_by_param(ParamsReq(name='part_3_test_7', tag='test'), data='test7')
        upl_few.upload_by_param(ParamsReq(name='part_3_test_7', tag='test'), data='test7')
        assert len(upl_few.get_by_param(ParamsReq(name='part_3_test_7',
                                                  tag='test'))) == 3

    #8
    def test_get_few_files_by_name_tag(self, upl_few):
        """get few files by name and tag"""
        upl_few.upload_by_param(ParamsReq(id='5',
                                          name='part_3_test',
                                          tag='test1'), data='test')
        assert len(upl_few.get_by_param(ParamsReq(name='part_3_test',
                                                  tag='test1'))) == 2

    #9
    def test_get_several_id_name(self, upl_few):
        """get by several compound parameters id, name and one tag"""
        result = upl_few.get_by_param(ParamsReq(id=('1', '2', '3', '4'),
                                                name=('part_3_test', 'part_3_test_1'),
                                                tag='test1'))
        case = unittest.TestCase()
        case.assertCountEqual(result, REFERENCE_DICT)
        assert result['id'] == '1'

    #10
    def test_get_several_id_name_tag(self, upl_few):
        """get by several compound parameters id, name and tag"""
        assert len(upl_few.get_by_param(ParamsReq(id=('1', '2', '3', '4'),
                                                  name=('part_3_test', 'part_3_test_1'),
                                                  tag=('test1', 'test2')))) == 3

    #11
    def test_delete_name_tag(self, upl_few):
        """delete by name and tag parameters"""
        upl_few.upload_by_param(ParamsReq(name='part_3_test_11', tag='test'), data='test11')
        upl_few.upload_by_param(ParamsReq(name='part_3_test_11', tag='test'), data='test11')
        upl_few.upload_by_param(ParamsReq(name='part_3_test_11', tag='test'), data='test11')
        assert upl_few.delete_by_param(ParamsReq(name='part_3_test_11', tag='test')) == '3 files deleted'

    #12
    def test_delete_name_several_tag(self, upl_few):
        """delete by name and several tag"""
        assert upl_few.delete_by_param(ParamsReq(name='part_3_test',
                                                 tag=('test1', 'test2'))) == '2 files deleted'

    #13
    def test_delete_several_name_id(self, upl_few):
        """delete by several id, name and one tag"""
        assert upl_few.delete_by_param(ParamsReq(id=('1', '2', '3', '4'),
                                                 name=('part_3_test', 'part_3_test_1'),
                                                 tag='test1')) == '1 files deleted'

    #14
    def test_delete_several_id_name_tag(self, upl_few):
        """delete by several id, name and tag"""
        assert upl_few.delete_by_param(ParamsReq(id=('1', '2', '3', '4'),
                                                 name=('part_3_test', 'part_3_test_1'),
                                                 tag=('test1', 'test'))) == '1 files deleted'
