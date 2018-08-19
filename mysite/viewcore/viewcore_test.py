import sys, os
import unittest
import datetime

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from viewcore import viewcore
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from viewcore.converter import datum_from_german as datum



class ViewcoreTest(unittest.TestCase):

    def test_post_action_is_with_get_request_should_return_false(self):
        assert not viewcore.post_action_is(GetRequest(), "delete")

    def test_post_action_is_with_empty_post_request_should_return_false(self):
        assert not viewcore.post_action_is(PostRequest({}), "delete")

    def test_post_action_is_with_post_request_and_other_action_should_return_false(self):
        assert not viewcore.post_action_is(PostRequest({'action': 'add'}), "delete")

    def test_post_action_is_with_post_request_and_and_matching_action_should_return_true(self):
        assert viewcore.post_action_is(PostRequest({'action': 'delete'}), "delete")

    def test_today_should_return_today(self):
        assert viewcore.today() == datetime.datetime.now().date()

    def test_today_with_subbed_today_should_return_stubbed_date(self):
        viewcore.stub_today_with(datum('01.01.2012'))
        assert viewcore.today() == datum('01.01.2012')
        viewcore.reset_viewcore_stubs()

    def test_today_with_resetted_stub_should_return_today(self):
        viewcore.stub_today_with(datum('01.01.2012'))
        viewcore.reset_viewcore_stubs()
        assert viewcore.today() == datetime.datetime.now().date()
