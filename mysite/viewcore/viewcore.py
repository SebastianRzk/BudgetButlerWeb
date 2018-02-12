'''
Created on 24.04.2017

@author: sebastian
'''

from core import DBManager
from viewcore import viewcore
from viewcore import configuration_provider
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
        viewcore.DATABASE_INSTANCE = DBManager.read_database(viewcore.DATABASES[0])
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

def get_changed_stechzeiten():
    context = _get_context()
    if "stechzeiten_changed" not in context.keys():
        context["stechzeiten_changed"] = []
    return context["stechzeiten_changed"]

def add_changed_stechzeiten(new_changed_stechzeiten_element):
    context = get_changed_stechzeiten()
    context.append(new_changed_stechzeiten_element)

def switch_database_instance(database_name):
    viewcore.DATABASE_INSTANCE = DBManager.read_database(database_name)

def get_menu_list():
    main_menu = {}

    menu = []
    menu.append({'url':'/uebersicht/', 'name':'Alle Einzelbuchungen', 'icon':'fa fa-list'})
    menu.append({'url':'/dauerauftraguebersicht/', 'name': 'Alle Daueraufträge', 'icon':'fa fa-list'})
    menu.append({'url':'/addeinzelbuchung/', 'name':'Neue Ausgabe', 'icon':'fa fa-plus'})
    menu.append({'url':'/addeinnahme/', 'name':'Neue Einnahme', 'icon':'fa fa-plus'})
    menu.append({'url':'/adddauerauftrag/', 'name':'Neuer Dauerauftrag', 'icon':'fa fa-plus'})
    menu.append({'url':'/monatsuebersicht/', 'name': 'Monatsübersicht', 'icon':'fa fa-line-chart'})
    menu.append({'url':'/jahresuebersicht/', 'name': 'Jahresübersicht', 'icon':'fa fa-line-chart'})
    main_menu[EINZELBUCHUNGEN_SUBMENU_NAME] = menu


    menu = []
    menu.append({'url':'/gemeinsameuebersicht/', 'name': 'Alle gem. Buchungen', 'icon':'fa fa-list'})
    menu.append({'url':'/addgemeinsam/', 'name':'Neue gemeinsame Ausgabe', 'icon':'fa fa-plus'})
    menu.append({'url': '/gemeinsamabrechnen/', 'name': 'Gemeinsam abrechnen', 'icon':'fa fa-cogs'})
    main_menu['Gemeinsame Finanzen'] = menu


    menu = []
    menu.append({'url': '/import/', 'name': 'Datensätze importieren', 'icon':'fa fa-cogs'})
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
    '''
    Generate the base context for site
    '''
    print('###########################################################################################')
    print('#################################Generatring new page######################################')
    print('###########################################################################################')
    context = {
        'active': get_key_for_name(pagename),
        'active_page_url':'/' + pagename + '/',
        'active_name': get_name_from_key(pagename),
        'element_titel':get_name_from_key(pagename),
        'menu' : get_menu_list(),
        'nutzername': 'Sebastian',
        'extra_scripts':"",
    }
    context['nutzername'] = database_instance().name
    return context

def generate_error_context(pagename, errortext):
    context = generate_base_context(pagename)
    context['%Errortext'] = errortext
    return context

def save_database():
    if DATABASE_INSTANCE != None:
        DBManager.write(DATABASE_INSTANCE)

def save_refresh():
    save_database()
    db_name = viewcore.DATABASE_INSTANCE.name
    viewcore.DATABASE_INSTANCE = None
    viewcore.switch_database_instance(db_name)

def name_of_partner():
    return configuration_provider.get_configuration('PARTNERNAME')

def design_colors():
    colors = {}
    colors[0] = ("3c8dbc")
    colors[1] = ("f56954")
    colors[2] = ("00a65a")
    colors[3] = ("00c0ef")
    colors[4] = ("f39c12")
    colors[5] = ("d2d6de")
    colors[6] = ("001F3F")
    colors[7] = ("39CCCC")
    colors[8] = ("3D9970")
    colors[9] = ("01FF70")
    colors[10] = ("FF851B")
    colors[11] = ("F012BE")
    colors[12] = ("8E24AA")
    colors[13] = ("D81B60")
    colors[14] = ("222222")
    colors[15] = ("d2d6de")
    return colors

def post_action_is(request, action_name):
    if request.method != 'POST':
        return False
    if 'action' not in request.POST:
        return False
    return request.POST['action'] == action_name

def today():
    return viewcore.TODAY()

def stub_today_with(new_today):
    viewcore.TODAY = lambda: new_today

def reset_viewcore_stubs():
    viewcore.TODAY = lambda: datetime.datetime.now().date()
