import butler_offline.viewcore.menu
import butler_offline.viewcore.routes
from butler_offline.viewcore import viewcore
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import PostRequest


def test_post_action_is_with_get_request_should_return_false():
    assert not viewcore.post_action_is(GetRequest(), "delete")


def test_post_action_is_with_empty_post_request_should_return_false():
    assert not viewcore.post_action_is(PostRequest({}), "delete")


def test_post_action_is_with_post_request_and_other_action_should_return_false():
    assert not viewcore.post_action_is(PostRequest({'action': 'add'}), "delete")


def test_post_action_is_with_post_request_and_and_matching_action_should_return_true():
    assert viewcore.post_action_is(PostRequest({'action': 'delete'}), "delete")


def test__get_post_parameter_or_default__with_get_request__should_return_default():
    assert viewcore.get_post_parameter_or_default(GetRequest(), 'test', 'default') == 'default'


def test__get_post_parameter_or_default__with_post_request_and_no_matching_parameter__should_return_default():
    assert viewcore.get_post_parameter_or_default(PostRequest({}), 'test', 'default') == 'default'


def test__get_post_parameter_or_default__with_post_request_and_matching_parameter__should_return_value():
    request = PostRequest({'test': 'value'})
    assert viewcore.get_post_parameter_or_default(request, 'test', 'default') == 'value'


def test_def_get_menu_list():
    menu_list = butler_offline.viewcore.menu.get_menu_list()
    assert 'Persönliche Finanzen' in menu_list
    assert 'Gemeinsame Finanzen' in menu_list
    assert 'Sparen' in menu_list
    assert 'Einstellungen' in menu_list
