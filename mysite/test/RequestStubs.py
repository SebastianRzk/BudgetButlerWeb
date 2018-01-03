'''
Created on 30.09.2017

@author: sebastian
'''

class GetRequest():
    method = "GET"
    POST = {}

class PostRequest:
    method = "POST"
    def __init__(self, args):
        self.POST = args

from viewcore import request_handler

class VersionedPostRequest:
    method = "POST"
    def __init__(self, args):
        self.POST = args
        self.POST["ID"] = request_handler.current_key()
