"""fixtures"""
import pytest
from http_connector import ConnectorHttp, ParamsReq


@pytest.fixture(scope="function")
def fch():
    """connection to http server"""
    fch = ConnectorHttp('http://127.0.0.1:9876')
    return fch


@pytest.fixture(scope="function")
def params():
    """created data class for parameters to requests"""
    params = ParamsReq
    return params


@pytest.fixture(scope="function")
def upl_one(fch, params):
    """upload one file to base"""
    fch.upload_by_param(params(id='1',
                                  name='name1',
                                  tag='test'), data='1_name1')
    return fch


@pytest.fixture(scope="function")
def upl_few(fch, params):
    """upload few files to base"""
    fch.upload_by_param(params(id='1',
                                  name='part_3_test',
                                  tag='test1'), data='test')
    fch.upload_by_param(params(id='2',
                                  name='part_3_test_1',
                                  tag='test2'), data='test')
    fch.upload_by_param(params(id='3',
                                  name='part_3_test_2',
                                  tag='test1'), data='test')
    fch.upload_by_param(params(id='4',
                                  name='part_3_test',
                                  tag='test2'), data='test')
    return fch


@pytest.fixture(autouse=True)
def clear(fch, params):
    """clear all files from base before and after test"""
    result = fch.get_without_param()
    if isinstance(result, dict) and len(result) > 0:
        fch.delete_by_param(params(id=result['id']))
    else:
        for part in result:
            fch.delete_by_param(params(id=part['id']))
    yield clear
    result = fch.get_without_param()
    if isinstance(result, dict) and len(result) > 0:
        fch.delete_by_param(params(id=result['id']))
    else:
        for part in result:
            fch.delete_by_param(params(id=part['id']))
