from requests import request
from json import loads
from collections import namedtuple
from typing import get_type_hints


_GET_END_POINT = '/api/get'
_UPLOAD_END_POINT = '/api/upload'
_DELETE_END_POINT = '/api/delete'
_DOWNLOAD_END_POINT = '/api/download'
ENDPOINTS = {_GET_END_POINT: 'get', _UPLOAD_END_POINT: 'post',
             _DELETE_END_POINT: 'delete', _DOWNLOAD_END_POINT: 'get'}


# class ParToDict(namedtuple):
#     """namedtuple class for convert parameters to dict"""
#     id: str
#     tag: str
#     name: str
#     size: int
#     location: str
#     mimeType: str
#     modificationTime: str
#
#     def par_to_json(self):
#         """convert params to dict"""
#         hints = get_type_hints(self)
#         return {
#             key: hints[key](value)
#             for key, value in self.asdict().items()
#             if not key.startswith('')
#         }


def request_preparation(base_url, endpoint):
    """request representation"""
    method = ENDPOINTS[endpoint]
    url = base_url + endpoint

    def make_request(params=None, headers=None, data=None):
        response = request(method=method, url=url,
                           headers=headers, params=params, data=data)
        # #response.raise_for_status()
        #return response.content.decode('utf-8')
        return response
    return make_request


class ConnectorHttp:
    """class to work with our server"""

    def __init__(self, http_url):
        self._get = request_preparation(http_url, _GET_END_POINT)
        self._upload = request_preparation(http_url, _UPLOAD_END_POINT)
        self._delete = request_preparation(http_url, _DELETE_END_POINT)
        self._download = request_preparation(http_url, _DOWNLOAD_END_POINT)

    def download_by_param(self, id='', param=''):
        """download file by id"""
        response = self._download({'id': id, 'param': param})
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            return response.status_code, response.content.decode('utf-8')

    def download_without_param(self):
        """download file without parameters"""
        response = self._download()
        return response.status_code, response.content.decode('utf-8')

    def download_check_param(self, id=''):
        """download check wile output parameters"""
        return self._download({'id': id}).headers

    def get_by_param(self, id='', name='', tag='', size='', mimetype='', modificationtime='', param=''):
        """get file by parameters"""
        response = self._get({'id': id, 'name': name, 'tag': tag, 'size': size,
                              'mimetype': mimetype, 'modificationtime': modificationtime, 'param': param})
        return loads(response.content.decode('utf-8'))

    def delete_by_param(self, id='', name='', tag='', size='', mimetype='', modificationtime='', param=''):
        """delete file by parameters"""
        response = self._delete({'id': id, 'name': name, 'tag': tag, 'size': size,
                             'mimetype': mimetype, 'modificationtime': modificationtime, 'param': param})
        if response.status_code == 200:
            return response.content.decode('utf-8')
        else:
            return response.status_code, response.content.decode('utf-8')

    def upload_by_param(self, id='', name='', tag='', param='', data=''):
        response = self._upload({'id': id, 'name': name, 'tag': tag, 'param': param}, data=data)
        return loads(response.content.decode('utf-8'))
