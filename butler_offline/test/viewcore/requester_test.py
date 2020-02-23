import unittest
from butler_offline.viewcore.requester import Requester


class RequesterTest(unittest.TestCase):

    def test_decode(self):
        requester = Requester()
        response = TestReponse()
        response.content = str.encode('test')

        assert requester.decode(response) == 'test'


class TestReponse():
    pass

