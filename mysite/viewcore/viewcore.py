'''
Created on 24.04.2017

@author: sebastian
'''

from core import DBManager
from viewcore import viewcore


DATABASE_INSTANCE = None
DATABASES = []
CONTEXT = {}
FIRED_IDS = set()
ID_COUNT = 1
EINZELBUCHUNGEN_SUBMENU_NAME = 'Persönliche Finanzen'

def database_instance():
    '''
    returns the actual database instance
    '''
    if not viewcore.DATABASES:
        file = open("../config", "r")
        for line in file:
            line = line.strip()
            if line.startswith("DATABASES:"):
                line = line.replace("DATABASES:", "")
                viewcore.DATABASES = line.split(',')
    if viewcore.DATABASE_INSTANCE is None:
        viewcore.DATABASE_INSTANCE = DBManager.read_database(viewcore.DATABASES[0])
    return DATABASE_INSTANCE

def get_next_transaction_id():
    viewcore.ID_COUNT = viewcore.ID_COUNT + 1
    return str(viewcore.ID_COUNT)

def is_transaction_already_fired(id):
    return id in viewcore.FIRED_IDS

def fire(id):
    viewcore.FIRED_IDS.add(id)
    print("VIEWCORE: Fire id", id)
    print("All fired ids:", viewcore.FIRED_IDS)

def _get_context():
    print("CONTEXT:", CONTEXT, "  ", DATABASE_INSTANCE)
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
    menu.append({'url':'/addgemeinsam/', 'name':'Neue gemeinsame Buchung', 'icon':'fa fa-plus'})
    menu.append({'url': '/gemeinsamabrechnen/', 'name': 'Gemeinsam abrechnen', 'icon':'fa fa-cogs'})
    main_menu['Gemeinsame Finanzen'] = menu


    menu = []
    menu.append({'url':'/stechzeituebersicht/', 'name': 'Stechzeituebersicht', 'icon':'fa fa-line-chart'})
    menu.append({'url':'/addstechzeit/', 'name':'Neue Stechzeit', 'icon':'fa fa-plus'})
    menu.append({'url':'/addsollzeit/', 'name':'Sollzeit bearbeiten', 'icon':'fa fa-pencil'})
    main_menu['Stechzeiten'] = menu


    menu = []
    menu.append({'url': '/import/', 'name': 'Datensätze importieren', 'icon':'fa fa-cogs'})
    menu.append({'url': '/configuration/', 'name': 'Konfiguration', 'icon':'fa fa-cogs'})
    menu.append({'url':'/production/?database=' + viewcore.database_instance().name, 'name':'Reload Database', 'icon':'fa fa-refresh'})
    for database in DATABASES:
        if database != database_instance().name:
            menu.append({'url':'/production/?database=' + database, 'name':'To ' + database, 'icon':'fa fa-cogs'})

    main_menu['Einstellungen'] = menu
    print(main_menu)

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

TEST = False

def save_database():
    if viewcore.TEST:
        print('testmode, no database saving')
        return
    if DATABASE_INSTANCE != None:
        DBManager.write(DATABASE_INSTANCE)

def save_refresh():
    if viewcore.TEST:
        print("TESTMODE! save and refresh deaktived")
        return
    save_database()
    db_name = viewcore.DATABASE_INSTANCE.name
    viewcore.DATABASE_INSTANCE = None
    viewcore.switch_database_instance(db_name)

def get_icon_for_categorie(categorie):
    kategorienliste = {
        "Miete_Grundkosten":"fa fa-home",
        "Essen":"fa fa-cutlery",
        "Bus_Bahn":"fa fa-train",
        "Spass":"fa fa-camera-retro",
        "Einrichtung": "fa fa-free-code-camp",
        "Geschenke":"fa fa-gift",
        "Hygiene":"fa fa-bath",
        "Handy":"fa fa-mobile",
        "Alkohol":"fa fa-beer",
        "Spende":"fa fa-leaf",
        "Fahrrad":"fa fa-bicycle",
        "Urlaub":"fa fa-globe",
        "Schreibwaren":"fa fa-pencil",
        "Umzug":"fa fa-truck",
        "Medizin":"fa fa-medkit",
        "Sport":"fa fa-futbol-o",
        "Versicherung":"fa fa-file",
        }

    if categorie in kategorienliste.keys():
        return kategorienliste[categorie]


    for key, item in kategorienliste.items():
        if key in categorie:
            return item
    return "fa fa-archive"

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
