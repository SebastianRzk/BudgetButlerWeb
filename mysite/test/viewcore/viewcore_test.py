import sys, os
import unittest
import datetime

from mysite.viewcore import viewcore
from mysite.test.RequestStubs import GetRequest
from mysite.test.RequestStubs import PostRequest
from mysite.viewcore.converter import datum_from_german as datum



class ViewcoreTest(unittest.TestCase):

    def test_post_action_is_with_get_request_should_return_false(self):
        assert not viewcore.post_action_is(GetRequest(), "delete")

    def test_post_action_is_with_empty_post_request_should_return_false(self):
        assert not viewcore.post_action_is(PostRequest({}), "delete")

    def test_post_action_is_with_post_request_and_other_action_should_return_false(self):
        assert not viewcore.post_action_is(PostRequest({'action': 'add'}), "delete")

    def test_post_action_is_with_post_request_and_and_matching_action_should_return_true(self):
        assert viewcore.post_action_is(PostRequest({'action': 'delete'}), "delete")

    def test_today_with_subbed_today_should_return_stubbed_date(self):
        viewcore.stub_today_with(datum('01.01.2012'))
        assert viewcore.today() == datum('01.01.2012')
        viewcore.reset_viewcore_stubs()

    def test_today_with_resetted_stub_should_return_today(self):
        viewcore.stub_today_with(datum('01.01.2012'))
        viewcore.reset_viewcore_stubs()
        assert viewcore.today() == datetime.datetime.now().date()

    def test_getPostParameterOrDefault_withGetRequest_shouldReturnDefault(self):
        assert viewcore.get_post_parameter_or_default(GetRequest(), 'test', 'default') == 'default'

    def test_getPostParameterOrDefault_withPostRequestAndNoMatchingParameter_shouldReturnDefault(self):
        assert viewcore.get_post_parameter_or_default(PostRequest({}), 'test', 'default') == 'default'

    def test_getPostParameterOrDefault_withPostRequestAndMatchingParameter_shouldReturnValue(self):
        request = PostRequest({'test' : 'value'})
        assert viewcore.get_post_parameter_or_default(request, 'test', 'default') == 'value'
        
