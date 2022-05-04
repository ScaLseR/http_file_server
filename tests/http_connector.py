"""connector for http server"""
from json import loads
from dataclasses import dataclass, asdict
from requests import request


@dataclass
class ParamsReq:
    """structure for requests parameters """
    id: any = ''
    tag: any = ''
    name: any = ''
    size: any = ''
    mimetype: any = ''
    modificationtime: any = ''
    param: any = ''

    def to_dict(self):
        """convert to dict structure ParamsReq"""
        return asdict(self)


_GET_END_POINT = '/api/get'
_UPLOAD_END_POINT = '/api/upload'
_DELETE_END_POINT = '/api/delete'
_DOWNLOAD_END_POINT = '/api/download'
ENDPOINTS = {_GET_END_POINT: 'get', _UPLOAD_END_POINT: 'post',
             _DELETE_END_POINT: 'delete', _DOWNLOAD_END_POINT: 'get'}


def request_preparation(base_url, endpoint):
    """request representation"""
    method = ENDPOINTS[endpoint]
    url = base_url + endpoint

    def make_request(params=None, headers=None, data=None):
        response = request(method=method, url=url,
                           headers=headers, params=params, data=data)
        # #response.raise_for_status()
        return response
    return make_request


class ConnectorHttp:
    """class to work with our server"""

    def __init__(self, http_url):
        self._get = request_preparation(http_url, _GET_END_POINT)
        self._upload = request_preparation(http_url, _UPLOAD_END_POINT)
        self._delete = request_preparation(http_url, _DELETE_END_POINT)
        self._download = request_preparation(http_url, _DOWNLOAD_END_POINT)

    def download_by_param(self, params: ParamsReq):
        """download file by id"""
        response = self._download(params.to_dict())
        if response.status_code == 200:
            return response.content.decode('utf-8')
        return response.status_code, response.content.decode('utf-8')

    def download_without_param(self):
        """download file without parameters"""
        response = self._download()
        return response.status_code, response.content.decode('utf-8')

    def download_check_param(self, params: ParamsReq):
        """download check wile output parameters"""
        return self._download(params.to_dict()).headers

    def get_without_param(self):
        """get without parameters"""
        return loads(self._get().content.decode('utf-8'))

    def get_by_param(self, params: ParamsReq):
        """get file by parameters"""
        response = self._get(params.to_dict())
        return loads(response.content.decode('utf-8'))

    def delete_by_param(self, params: ParamsReq):
        """delete file by parameters"""
        response = self._delete(params.to_dict())
        if response.status_code == 200:
            return response.content.decode('utf-8')
        return response.status_code, response.content.decode('utf-8')

    def upload_by_param(self, params: ParamsReq, data=''):
        """upload by parameters"""
        response = self._upload(params.to_dict(), data=data)
        return loads(response.content.decode('utf-8'))
