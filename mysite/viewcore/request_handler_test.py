'''
Created on 10.05.2017

@author: sebastian
'''

import sys, os
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from viewcore import request_handler
from test.RequestStubs import PostRequest




class TesteRequestHanlder(unittest.TestCase):

    def test_redirect(self):
        request_handler.stub_me()

        result = request_handler.handle_request(PostRequest({'redirect': 'test_page'}), lambda x: {}, 'nothing')

        assert result == '/test_page/'

if __name__ == '__main__':
    unittest.main()
