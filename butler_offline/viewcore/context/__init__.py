from butler_offline.viewcore.menu import get_key_for_name, get_name_from_key, get_menu_list

TRANSACTION_ID_KEY = 'ID'


def is_transactional_request(request):
    return TRANSACTION_ID_KEY in request.values


def get_transaction_id(request):
    return request.values[TRANSACTION_ID_KEY]


def generate_base_context(pagename: str, database_name: str):
    return {
        'active': get_key_for_name(pagename),
        'active_page_url': '/' + pagename + '/',
        'active_name': get_name_from_key(pagename),
        'element_titel': get_name_from_key(pagename),
        'menu': get_menu_list(database_name),
        'nutzername': database_name,
        'extra_scripts': ''
    }
