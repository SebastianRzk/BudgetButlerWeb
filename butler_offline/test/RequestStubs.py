from butler_offline.viewcore.http import Request


class GetRequest(Request):
    def __init__(self):
        super().__init__(values={}, args={}, method='GET')


class PostRequest(Request):
    def __init__(self, args):
        super().__init__(values=args, args={}, method='POST')


class PostRequestAction(PostRequest):
    def __init__(self, action: str, args):
        super().__init__(args)
        args['action'] = action
