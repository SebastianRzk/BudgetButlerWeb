from butler_offline.viewcore.requester import Requester


def test_decode():
    requester = Requester()
    response = TestReponse()
    response.content = str.encode('test')

    assert requester.decode(response) == 'test'


class TestReponse:
    pass

