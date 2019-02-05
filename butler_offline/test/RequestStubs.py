'''
Created on 30.09.2017

@author: sebastian
'''

class GetRequest():
    method = "GET"
    POST = {}


from butler_offline.viewcore import request_handler

CONFIGURED = False

class PostRequest:
    method = "POST"
    def __init__(self, args):
        self.values = args


class VersionedPostRequest(PostRequest):
    def __init__(self, args):
        args["ID"] = request_handler.current_key()
        self.values = args
