'''''
Created on 24.04.2017

@author: sebastian
'''
from butler_offline.core import DBManager
from butler_offline.viewcore import viewcore
from butler_offline.viewcore import configuration_provider
from butler_offline.viewcore.request_handler import current_key
import datetime


DATABASE_INSTANCE = None
DATABASES = []
CONTEXT = {}
EINZELBUCHUNGEN_SUBMENU_NAME = 'Persönliche Finanzen'
TODAY = lambda: datetime.datetime.now().date()


def database_instance():
    '''
    returns the actual database instance
    '''
    if not viewcore.DATABASES:
        viewcore.DATABASES = configuration_provider.get_configuration('DATABASES').split(',')

    if viewcore.DATABASE_INSTANCE is None:
        ausgeschlossene_kategorien =  set(configuration_provider.get_configuration('AUSGESCHLOSSENE_KATEGORIEN').split(','))
        viewcore.DATABASE_INSTANCE = DBManager.read(viewcore.DATABASES[0], ausgeschlossene_kategorien = ausgeschlossene_kategorien)
    return DATABASE_INSTANCE


def _get_context():
    if DATABASE_INSTANCE.name not in CONTEXT.keys():
        CONTEXT[DATABASE_INSTANCE.name] = {}
    return CONTEXT[DATABASE_INSTANCE.name]


def get_changed_einzelbuchungen():
    context = _get_context()
    if "einzelbuchungen_changed" not in context.keys():
        context["einzelbuchungen_changed"] = []
    return context["einzelbuchungen_changed"]


def add_changed_einzelbuchungen(new_changed_einzelbuchung_event):
    context = get_changed_einzelbuchungen()
    context.append(new_changed_einzelbuchung_event)


def add_changed_gemeinsamebuchungen(new_changed_gemeinsamebuchungen_event):
    context = get_changed_gemeinsamebuchungen()
    context.append(new_changed_gemeinsamebuchungen_event)


def get_changed_gemeinsamebuchungen():
    context = _get_context()
    if "gemeinsamebuchungen_changed" not in context.keys():
        context["gemeinsamebuchungen_changed"] = []
    return context["gemeinsamebuchungen_changed"]


def get_changed_dauerauftraege():
    context = _get_context()
    if "dauerauftraege_changed" not in context.keys():
        context["dauerauftraege_changed"] = []
    return context["dauerauftraege_changed"]


def add_changed_dauerauftraege(new_changed_dauerauftraege_event):
    context = get_changed_dauerauftraege()
    context.append(new_changed_dauerauftraege_event)

def switch_database_instance(database_name):
    ausgeschlossene_kategorien =  set(configuration_provider.get_configuration('AUSGESCHLOSSENE_KATEGORIEN').split(','))
    viewcore.DATABASE_INSTANCE = DBManager.read(database_name, ausgeschlossene_kategorien = ausgeschlossene_kategorien)


def get_menu_list():
    main_menu = {}

    menu = []
    menu.append({'url':'/uebersicht/', 'name':'Übersicht Einzelbuchungen', 'icon':'fa fa-list'})
    menu.append({'url':'/dauerauftraguebersicht/', 'name': 'Übersicht Daueraufträge', 'icon':'fa fa-list'})
    menu.append({'url':'/addausgabe/', 'name':'Neue Ausgabe', 'icon':'fa fa-plus'})
    menu.append({'url':'/addeinnahme/', 'name':'Neue Einnahme', 'icon':'fa fa-plus'})
    menu.append({'url':'/adddauerauftrag/', 'name':'Neuer Dauerauftrag', 'icon':'fa fa-plus'})
    menu.append({'url':'/monatsuebersicht/', 'name': 'Monatsübersicht', 'icon':'fa fa-line-chart'})
    menu.append({'url':'/jahresuebersicht/', 'name': 'Jahresübersicht', 'icon':'fa fa-line-chart'})
    menu.append({'url': '/import/', 'name': 'Export / Import', 'icon':'fa fa-cogs'})
    main_menu[EINZELBUCHUNGEN_SUBMENU_NAME] = menu

    menu = []
    menu.append({'url':'/gemeinsameuebersicht/', 'name': 'Übersicht Buchungen', 'icon':'fa fa-list'})
    menu.append({'url':'/addgemeinsam/', 'name':'Neue gemeinsame Ausgabe', 'icon':'fa fa-plus'})
    menu.append({'url': '/gemeinsamabrechnen/', 'name': 'Gemeinsam abrechnen', 'icon':'fa fa-cogs'})
    menu.append({'url': '/import/', 'name': 'Export / Import', 'icon':'fa fa-cogs'})
    main_menu['Gemeinsame Finanzen'] = menu

    menu = []
    menu.append({'url': '/configuration/', 'name': 'Einstellungen', 'icon':'fa fa-cogs'})
    menu.append({'url':'/production/?database=' + viewcore.database_instance().name, 'name':'Datenbank neu laden', 'icon':'fa fa-refresh'})
    for database in DATABASES:
        if database != database_instance().name:
            menu.append({'url':'/production/?database=' + database, 'name':'To ' + database, 'icon':'fa fa-cogs'})

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
        'active_page_url':'/' + pagename + '/',
        'active_name': get_name_from_key(pagename),
        'element_titel':get_name_from_key(pagename),
        'menu' : get_menu_list(),
        'nutzername': database_instance().name,
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


def _save_database():
    if DATABASE_INSTANCE != None:
        DBManager.write(DATABASE_INSTANCE)


def _save_refresh():
    _save_database()
    db_name = viewcore.DATABASE_INSTANCE.name
    viewcore.DATABASE_INSTANCE = None
    viewcore.switch_database_instance(db_name)


def save_tainted():
    db = viewcore.DATABASE_INSTANCE
    if db.is_tainted():
        print('Saving database with', db.taint_number(), 'modifications')
        _save_refresh()
        print('Saved')
        db.de_taint()


def name_of_partner():
    return configuration_provider.get_configuration('PARTNERNAME')


def design_colors():
    return configuration_provider.get_configuration('DESIGN_COLORS').split(',')


def post_action_is(request, action_name):
    if not is_post_parameter_set(request, 'action'):
        return False
    return request.values['action'] == action_name

def get_post_parameter_or_default(request, key, default, mapping_function= lambda x: x):
    if not is_post_parameter_set(request, key):
        return default
    return mapping_function(request.values[key])

def is_post_parameter_set(request, parameter):
    if request.method != 'POST':
        return False
    return parameter in request.values.keys()

def today():
    return viewcore.TODAY()


def stub_today_with(new_today):
    viewcore.TODAY = lambda: new_today


def reset_viewcore_stubs():
    viewcore.TODAY = lambda: datetime.datetime.now().date()
