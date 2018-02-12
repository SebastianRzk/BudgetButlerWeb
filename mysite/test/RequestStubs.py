'''
Created on 30.09.2017

@author: sebastian
'''

class GetRequest():
    method = "GET"
    POST = {}


from django.http import QueryDict
from django.conf import settings
from test import RequestStubs

CONFIGURED = False

class PostRequest:
    method = "POST"
    def __init__(self, args):
        self.POST = RequestStubs.to_query_dict(args)


from viewcore import request_handler


class VersionedPostRequest(PostRequest):
    def __init__(self, args):
        args["ID"] = request_handler.current_key()
        self.POST = RequestStubs.to_query_dict(args)

def to_query_dict(dictionary):
    if not RequestStubs.CONFIGURED:
        settings.configure()
        RequestStubs.CONFIGURED = True
    result = QueryDict('', mutable=True)
    for element in dictionary:
        if isinstance(dictionary[element], list):
            for list_element in dictionary[element]:
                result.update({element: list_element})
        else:
            result.update({element: dictionary[element]})
    return result
