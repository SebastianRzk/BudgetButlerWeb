
class GetRequest:
    method = "GET"
    values = {}
    POST = {}


class PostRequest:
    method = 'POST'

    def __init__(self, args):
        self.values = args


class PostRequestAction(PostRequest):
    def __init__(self, action: str, args):
        super().__init__(args)
        args['action'] = action
