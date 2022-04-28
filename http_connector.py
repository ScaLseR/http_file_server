from requests import request
from json import loads

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
        print('response= ', response)
        print('response.status_code= ', response.status_code)
        print('response.headers= ', response.headers)
        print('response.content= ', response.content)
        response.raise_for_status()
        return response.content.decode('utf-8')
    return make_request


class ConnectorHttp:
    """class to work with our server"""

    def __init__(self, http_url):
        self._get = request_preparation(http_url, _GET_END_POINT)
        self._upload = request_preparation(http_url, _UPLOAD_END_POINT)
        self._delete = request_preparation(http_url, _DELETE_END_POINT)
        self._download = request_preparation(http_url, _DOWNLOAD_END_POINT)

    def get_without_params(self):
        """api/get without parameters, return the metadata of all files on the server"""
        response = self._get()
        return loads(response)

    def download_by_id(self, file_id):
        """api/download, download file by id"""
        return self._download({'id': file_id})

    def get_by_id(self, file_id):
        """get file by id"""
        response = self._get({'id': file_id})
        return loads(response)

    def delete_by_id(self, file_id):
        """delete file by  id"""
        return self._delete({'id': file_id})
