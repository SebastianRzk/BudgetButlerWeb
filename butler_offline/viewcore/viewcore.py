from butler_offline.core import configuration_provider
from butler_offline.viewcore.colors import GenericDesignColorChooser


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
