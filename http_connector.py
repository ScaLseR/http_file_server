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

    def download_by_id(self, file_id):
        """download file by id"""
        return self._download({'id': file_id})

    def get_by_param(self, id='', name='', tag='', mimetype='', modificationtime=''):
        """get file by params"""
        response = self._get({'id': id, 'name': name, 'tag': tag,
                              'mimeType': mimetype, 'modificationTime': modificationtime})
        return loads(response)

    def get_by_faulty_param(self, id='', name='', tag='', mimetype='',
                                modificationtime='', param=''):
        """get with faulty parameter"""
        response = self._get({'id': id, 'name': name, 'tag': tag,
                             'mimeType': mimetype,
                              'modificationTime': modificationtime, 'count': param})
        return loads(response)

    def delete_by_param(self, id='', name='', tag='', mimetype='', modificationtime=''):
        """delete file by id"""
        return self._delete({'id': id, 'name': name, 'tag': tag,
                             'mimeType': mimetype, 'modificationTime': modificationtime})

