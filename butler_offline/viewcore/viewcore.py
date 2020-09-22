'''''
Created on 24.04.2017

@author: sebastian
'''
from butler_offline.viewcore import configuration_provider
from butler_offline.viewcore.request_handler import current_key
from butler_offline.viewcore.state import persisted_state

EINZELBUCHUNGEN_SUBMENU_NAME = 'Persönliche Finanzen'


def get_menu_list():
    main_menu = {}

    menu = []
    menu.append({'url': '/uebersicht/', 'name': 'Übersicht Einzelbuchungen', 'icon': 'fa fa-list'})
    menu.append({'url': '/dauerauftraguebersicht/', 'name': 'Übersicht Daueraufträge', 'icon': 'fa fa-list'})
    menu.append({'url': '/addausgabe/', 'name': 'Neue Ausgabe', 'icon': 'fa fa-plus'})
    menu.append({'url': '/addeinnahme/', 'name': 'Neue Einnahme', 'icon': 'fa fa-plus'})
    menu.append({'url': '/adddauerauftrag/', 'name': 'Neuer Dauerauftrag', 'icon': 'fa fa-plus'})
    menu.append({'url': '/monatsuebersicht/', 'name': 'Monatsübersicht', 'icon': 'fa fa-line-chart'})
    menu.append({'url': '/jahresuebersicht/', 'name': 'Jahresübersicht', 'icon': 'fa fa-line-chart'})
    menu.append({'url': '/import/', 'name': 'Export / Import', 'icon': 'fa fa-cogs'})
    main_menu[EINZELBUCHUNGEN_SUBMENU_NAME] = menu

    menu = []
    menu.append({'url': '/gemeinsameuebersicht/', 'name': 'Übersicht Buchungen', 'icon': 'fa fa-list'})
    menu.append({'url': '/addgemeinsam/', 'name': 'Neue gemeinsame Ausgabe', 'icon': 'fa fa-plus'})
    menu.append({'url': '/gemeinsamabrechnen/', 'name': 'Gemeinsam abrechnen', 'icon': 'fa fa-cogs'})
    menu.append({'url': '/import/', 'name': 'Export / Import', 'icon': 'fa fa-cogs'})
    menu.append({'url': '/uebersichtabrechnungen/', 'name': 'Übersicht Abrechnungen', 'icon': 'fa fa-list'})
    main_menu['Gemeinsame Finanzen'] = menu

    menu = []
    menu.append({'url': '/add_sparbuchung/', 'name': 'Neue Sparbuchung', 'icon': 'fa fa-plus'})
    menu.append({'url': '/add_sparkonto/', 'name': 'Neues Sparkonto', 'icon': 'fa fa-plus'})
    menu.append({'url': '/add_depotwert/', 'name': 'Neuer Depotwert', 'icon': 'fa fa-plus'})
    menu.append({'url': '/add_order/', 'name': 'Neue Order', 'icon': 'fa fa-plus'})
    menu.append({'url': '/uebersicht_sparbuchungen/', 'name': 'Übersicht Sparbuchungen', 'icon': 'fa fa-list'})
    menu.append({'url': '/uebersicht_sparkontos/', 'name': 'Übersicht Sparkontos', 'icon': 'fa fa-list'})
    menu.append({'url': '/uebersicht_depotwerte/', 'name': 'Übersicht Depotwerte', 'icon': 'fa fa-list'})
    menu.append({'url': '/uebersicht_order/', 'name': 'Übersicht Order', 'icon': 'fa fa-list'})

    main_menu['Sparen'] = menu

    menu = []
    menu.append({'url': '/configuration/', 'name': 'Einstellungen', 'icon': 'fa fa-cogs'})
    menu.append({'url': '/production/?database=' + persisted_state.database_instance().name, 'name': 'Datenbank neu laden',
                 'icon': 'fa fa-refresh'})
    for database in persisted_state.DATABASES:
        if database != persisted_state.database_instance().name:
            menu.append({'url': '/production/?database=' + database, 'name': 'To ' + database, 'icon': 'fa fa-cogs'})

    main_menu['Einstellungen'] = menu
    return main_menu


def get_name_from_key(pagename):
    for name, menu_items in get_menu_list().items():
        for menu_item in menu_items:
            if menu_item['url'] == "/" + pagename + "/":
                return menu_item['name']
    return 'Übersicht'


def get_key_for_name(pagename):
    if pagename == 'dashboard':
        return EINZELBUCHUNGEN_SUBMENU_NAME

    for name, menu_items in get_menu_list().items():
        for menu_item in menu_items:
            if menu_item['url'] == "/" + pagename + "/":
                return name
    return EINZELBUCHUNGEN_SUBMENU_NAME


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
