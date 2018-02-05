import sys, os
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from viewcore import viewcore
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest




class ViewcoreTest(unittest.TestCase):

    def test_post_action_is_with_get_request_should_return_false(self):
        assert not viewcore.post_action_is(GetRequest(), "delete")

    def test_post_action_is_with_empty_post_request_should_return_false(self):
        assert not viewcore.post_action_is(PostRequest({}), "delete")

    def test_post_action_is_with_post_request_and_other_action_should_return_false(self):
        assert not viewcore.post_action_is(PostRequest({'action': 'add'}), "delete")

    def test_post_action_is_with_post_request_and_and_matching_action_should_return_true(self):
        assert viewcore.post_action_is(PostRequest({'action': 'delete'}), "delete")
