import pytest
from http_connector import ConnectorHttp, ParamsReq


@pytest.fixture()
def fch():
    fch = ConnectorHttp('http://127.0.0.1:9876')
    return fch


@pytest.fixture()
def upl_one(fch):
    fch.upload_by_param(ParamsReq(id='1',
                                  name='name1',
                                  tag='test'), data='1_name1')
    return fch


@pytest.fixture()
def upl_few(fch):
    fch.upload_by_param(ParamsReq(id='1',
                                  name='part_3_test',
                                  tag='test1'), data='test')
    fch.upload_by_param(ParamsReq(id='2',
                                  name='part_3_test_1',
                                  tag='test2'), data='test')
    fch.upload_by_param(ParamsReq(id='3',
                                  name='part_3_test_2',
                                  tag='test1'), data='test')
    fch.upload_by_param(ParamsReq(id='4',
                                  name='part_3_test',
                                  tag='test2'), data='test')
    return fch


@pytest.fixture(autouse=True)
def clear(fch):
    result = fch.get_without_param()
    if isinstance(result, dict) and len(result) > 0:
        fch.delete_by_param(ParamsReq(id=result['id']))
    else:
        for part in result:
            fch.delete_by_param(ParamsReq(id=part['id']))
