
'''
New implementation
'''

TRANSACTION_ID_KEY = 'ID'
ERROR_KEY = '%Errortext'

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
