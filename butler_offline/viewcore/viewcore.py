from butler_offline.core import configuration_provider
from butler_offline.viewcore.colors import GenericDesignColorChooser


def name_of_partner():
    return configuration_provider.get_configuration('PARTNERNAME')


def design_colors():
    return configuration_provider.get_configuration('DESIGN_COLORS').split(',')


def get_generic_color_chooser(values):
    return GenericDesignColorChooser(values, design_colors())
