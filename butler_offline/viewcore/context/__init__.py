
'''
New implementation
'''
from butler_offline.viewcore.menu import get_key_for_name, get_name_from_key, get_menu_list
from butler_offline.viewcore.state import persisted_state

TRANSACTION_ID_KEY = 'ID'
ERROR_KEY = '%Errortext'
REDIRECT_KEY = 'redirect_to'


class Context:
    def __init__(self, initial_state, error=None, redirect=None):
        self._state = initial_state
        self._error = error
        self._redirect = redirect

    def put(self, key, value):
        self._state[key] = value

    def state(self):
        return self._state

    def is_error(self):
        return not self._error

    def error_text(self):
        return self._error

    def is_redirect(self):
        return not self._redirect

    def is_transactional(self):
        return TRANSACTION_ID_KEY in self._state

    def transaction_id(self):
        return self.state()[TRANSACTION_ID_KEY]

    def redirect_destination(self):
        return self._redirect

    def add_transaction_id(self, transaction_id):
        self.state()['ID'] = transaction_id

    def add_error(self, error_text):
        self._error = error_text

    def contains_key(self, key):
        return key in self._state


'''
Old migration
'''


def is_transactional_request(request):
    return TRANSACTION_ID_KEY in request.values


def get_transaction_id(request):
    return request.values[TRANSACTION_ID_KEY]


def is_error(context):
    return ERROR_KEY in context


def get_error_message(context):
    return context[ERROR_KEY]


def generate_base_context(pagename):
    return {
        'active': get_key_for_name(pagename),
        'active_page_url': '/' + pagename + '/',
        'active_name': get_name_from_key(pagename),
        'element_titel': get_name_from_key(pagename),
        'menu': get_menu_list(),
        'nutzername': persisted_state.database_instance().name,
        'extra_scripts': ''
    }


def generate_transactional_context(pagename):
    context = generate_base_context(pagename)
    context['ID'] = persisted_state.current_database_version()
    return context


def generate_error_context(pagename, errortext):
    context = generate_base_context(pagename)
    context[ERROR_KEY] = errortext
    return context


def generate_redirect_context(url):
    return {
        REDIRECT_KEY: url
    }
