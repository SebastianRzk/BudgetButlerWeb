from butler_offline.core import configuration_provider
from butler_offline.viewcore.request_handler import current_key
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.colors import GenericDesignColorChooser
from butler_offline.viewcore.menu import get_key_for_name, get_name_from_key, get_menu_list


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
    context['ID'] = current_key()
    return context


def generate_error_context(pagename, errortext):
    context = generate_base_context(pagename)
    context['%Errortext'] = errortext
    return context


def name_of_partner():
    return configuration_provider.get_configuration('PARTNERNAME')


def design_colors():
    return configuration_provider.get_configuration('DESIGN_COLORS').split(',')

def get_generic_color_chooser(values):
    return GenericDesignColorChooser(values, design_colors())


def post_action_is(request, action_name):
    if not is_post_parameter_set(request, 'action'):
        return False
    return request.values['action'] == action_name


def get_post_parameter_or_default(request, key, default, mapping_function=lambda x: x):
    if not is_post_parameter_set(request, key):
        return default
    return mapping_function(request.values[key])


def is_post_parameter_set(request, parameter):
    if request.method != 'POST':
        return False
    return parameter in request.values.keys()
