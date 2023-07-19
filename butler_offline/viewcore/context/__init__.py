from butler_offline.viewcore.menu import get_key_for_name, get_name_from_key, get_menu_list
from butler_offline.viewcore.state import persisted_state

TRANSACTION_ID_KEY = 'ID'
ERROR_KEY = '%Errortext'
REDIRECT_KEY = 'redirect_to'


def is_transactional_request(request):
    return TRANSACTION_ID_KEY in request.values


def get_transaction_id(request):
    return request.values[TRANSACTION_ID_KEY]


def is_error(context):
    return ERROR_KEY in context


def get_error_message(context):
    return context[ERROR_KEY]


def generate_base_context(pagename: str, database_name: str = None):
    if not database_name:
        database_name = persisted_state.database_instance().name

    return {
        'active': get_key_for_name(pagename),
        'active_page_url': '/' + pagename + '/',
        'active_name': get_name_from_key(pagename),
        'element_titel': get_name_from_key(pagename),
        'menu': get_menu_list(database_name),
        'nutzername': database_name,
        'extra_scripts': ''
    }


def generate_transactional_context(pagename: str, database_name: str = None):
    if not database_name:
        database_name = persisted_state.database_instance().name

    context = generate_base_context(pagename=pagename, database_name=database_name)
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
