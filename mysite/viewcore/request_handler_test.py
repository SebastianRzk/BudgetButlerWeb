'''
Created on 10.05.2017

@author: sebastian
'''

import unittest
from mysite.viewcore import request_handler
from mysite.test.RequestStubs import PostRequest


class TesteRequestHanlder(unittest.TestCase):

    def test_redirect(self):
        request_handler.stub_me()

        result = request_handler.handle_request(PostRequest({'redirect': 'test_page'}), lambda x: {}, 'nothing')

        assert result == '/test_page/'

