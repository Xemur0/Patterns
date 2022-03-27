import os
import quopri
from helper.content_types import CONTENT_TYPES_MAP
from concert_framework.concert_requests import Post_Requests, Get_Requests


class PageNotFound404:
    def __call__(self, request):
        return '404', '404 Page not found'


class ConcertFramework:
    """Основной класс для фреймворка"""

    def __init__(self, settings, routes):
        self.routes = routes
        self.settings = settings

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = Post_Requests().get_request_params(environ)
            request['data'] = data

        if method == 'GET':
            request_params = Get_Requests().get_request_params(environ)
            request['request_params'] = request_params


        if path in self.routes:
            view = self.routes[path]
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')

        elif path.startswith(self.settings.STATIC_URL):

            file_path = path[len(self.settings.STATIC_URL):len(path) - 1]

            content_type = self.get_content_type(file_path)

            code, body = self.get_static(self.settings.STATIC_FILES_DIR,
                                         file_path)

        else:
            view = PageNotFound404()
            content_type = self.get_content_type(path)
            code, body = view(request)
            body = body.encode('utf-8')
        start_response(code, [('Content-Type', content_type)])

        return [body]

    @staticmethod
    def get_content_type(file_path, content_types_map=CONTENT_TYPES_MAP):
        file_name = os.path.basename(file_path).lower()
        extension = os.path.splitext(file_name)[1]

        return content_types_map.get(extension, "text/html")

    @staticmethod
    def get_static(static_dir, file_path):
        path_to_file = os.path.join(static_dir, file_path)
        with open(path_to_file, 'rb') as f:
            file_content = f.read()
        status_code = '200 OK'
        return status_code, file_content

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = quopri.decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
