'''
Created on 10.05.2017

@author: sebastian
'''

import unittest
from requests.exceptions import ConnectionError
from butler_offline.viewcore import request_handler
from butler_offline.test.RequestStubs import PostRequest
from butler_offline.test.FileSystemStub import FileSystemStub
from butler_offline.core import FileSystem
from butler_offline.viewcore import viewcore


class TesteRequestHandler(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        viewcore.database_instance()
        request_handler.stub_me_theme()

    def test_redirect(self):
        self.set_up()
        result = request_handler.handle_request(PostRequest({'redirect': 'test_page'}), lambda x: {}, 'nothing')
        assert result == '/test_page/'

    def test_extra_page(self):
        self.set_up()
        result = request_handler.handle_request(PostRequest({}), lambda x: {'special_page': 'something_special'}, 'something_normal')
        assert result['content'] == 'theme/something_special'

    def test_default_page(self):
        self.set_up()
        result = request_handler.handle_request(PostRequest({}), lambda x: {}, 'something_normal')
        assert result['content'] == 'theme/something_normal'

    def raise_http_error(self):
        raise ConnectionError()

    def raise_error(self):
        raise Exception()

    def test_http_exception(self):
        self.set_up()
        request_handler.stub_me()

        result = request_handler.handle_request(PostRequest({}), lambda x: self.raise_http_error(), 'something_normal')
        assert result['message']
        assert result['message_type'] == 'error'
        assert result['message_content'] == 'Verbindung zum Server konnte nicht aufgebaut werden.'


    def test_exception(self):
        self.set_up()
        request_handler.stub_me()

        result = request_handler.handle_request(PostRequest({}), lambda x: self.raise_error(), 'something_normal')
        print(result['message_content'])
        assert result['message']
        assert result['message_type'] == 'error'
        assert result['message_content'] == 'Ein Fehler ist aufgetreten: <br>\n '
