from butler_offline.viewcore.requester import Requester


def test_decode():
    requester = Requester()
    response = FakeReponse(content=str.encode('test'))

    assert requester.decode(response) == 'test'


class FakeReponse:
    def __init__(self, content: bytes):
        self.content = content
