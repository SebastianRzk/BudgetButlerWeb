'''
Created on 30.09.2017

@author: sebastian
'''

class GetRequest():
    method = "GET"
    values = {}
    POST = {}


from butler_offline.viewcore.state import persisted_state

CONFIGURED = False


class PostRequest:
    method = 'POST'

    def __init__(self, args):
        self.values = args


class PostRequestAction(PostRequest):
    def __init__(self, action, args):
        args['action'] = action
        self.values = args


class VersionedPostRequest(PostRequest):
    def __init__(self, args):
        args['ID'] = persisted_state.current_database_version()
        self.values = args


class VersionedPostRequestAction(VersionedPostRequest):
    def __init__(self, action, args):
        args['action'] = action
        self.values = args