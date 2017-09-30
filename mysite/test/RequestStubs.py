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