import unittest

import butler_offline.viewcore.menu
import butler_offline.viewcore.routes
from butler_offline.viewcore import viewcore
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import PostRequest



class ViewcoreTest(unittest.TestCase):

    def test_post_action_is_with_get_request_should_return_false(self):
        assert not viewcore.post_action_is(GetRequest(), "delete")

    def test_post_action_is_with_empty_post_request_should_return_false(self):
        assert not viewcore.post_action_is(PostRequest({}), "delete")

    def test_post_action_is_with_post_request_and_other_action_should_return_false(self):
        assert not viewcore.post_action_is(PostRequest({'action': 'add'}), "delete")

    def test_post_action_is_with_post_request_and_and_matching_action_should_return_true(self):
        assert viewcore.post_action_is(PostRequest({'action': 'delete'}), "delete")

    def test_getPostParameterOrDefault_withGetRequest_shouldReturnDefault(self):
        assert viewcore.get_post_parameter_or_default(GetRequest(), 'test', 'default') == 'default'

    def test_getPostParameterOrDefault_withPostRequestAndNoMatchingParameter_shouldReturnDefault(self):
        assert viewcore.get_post_parameter_or_default(PostRequest({}), 'test', 'default') == 'default'

    def test_getPostParameterOrDefault_withPostRequestAndMatchingParameter_shouldReturnValue(self):
        request = PostRequest({'test' : 'value'})
        assert viewcore.get_post_parameter_or_default(request, 'test', 'default') == 'value'
        
    def test_def_get_menu_list(self):
        menu_list = butler_offline.viewcore.menu.get_menu_list()
        assert 'Persönliche Finanzen' in menu_list
        assert 'Gemeinsame Finanzen' in menu_list
        assert 'Sparen' in menu_list
        assert 'Einstellungen' in menu_list