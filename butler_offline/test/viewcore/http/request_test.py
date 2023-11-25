from butler_offline.viewcore.http import Request


def test_is_post_request():
    assert Request(values={}, args={}, method='POST').is_post_request()
    assert not Request(values={}, args={}, method='GET').is_post_request()


def test_post_action_is():
    assert Request(values={'action': 'match'}, args={}, method='POST').post_action_is('match')
    assert not Request(values={'action': 'match'}, args={}, method='POST').post_action_is('no-match')
    assert not Request(values={'action': 'match'}, args={}, method='GET').post_action_is('match')
    assert not Request(values={}, args={}, method='GET').post_action_is('match')


def test_get_post_parameter_or_default():
    request = Request(values={'key': 'value'}, args={}, method='POST')
    assert request.get_post_parameter_or_default(default='default', key='key') == 'value'
    assert request.get_post_parameter_or_default(default='default', key='key',
                                                 mapping_function=lambda x: x + "2") == 'value2'
    assert request.get_post_parameter_or_default(default='default', key='key2') == 'default'


def test_is_post_parameter_set():
    assert Request(values={'key': 'value'}, args={}, method='POST').is_post_parameter_set('key')
    assert not Request(values={'key': 'value'}, args={}, method='GET').is_post_parameter_set('key')
    assert not Request(values={'key': 'value'}, args={}, method='POST').is_post_parameter_set('key2')
