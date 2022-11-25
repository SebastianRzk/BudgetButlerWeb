from butler_offline.viewcore.routes import EINZELBUCHUNGEN_EINZELBUCHUNGEN_UEBERSICHT, \
    EINZELBUCHUNGEN_DAUERAUFTRAG_UEBERSICHT, \
    EINZELBUCHUNGEN_AUSGABE_ADD, \
    EINZELBUCHUNGEN_EINNAHME_ADD, \
    EINZELBUCHUNGEN_DAUERAUFTRAG_ADD, \
    EINZELBUCHUNGEN_MONATSUEBERSICHT, \
    EINZELBUCHUNGEN_JAHRESUEBERSICHT, \
    CORE_IMPORT, \
    GEMEINSAME_BUCHUNGEN_UEBERSICHT, \
    GEMEINSAME_BUCHUNGEN_ADD, \
    GEMEINSAME_BUCHUNGEN_ABRECHNEN, \
    GEMEINSAME_BUCHUNGEN_ABRECHNUNGEN, \
    SPAREN_UEBERSICHT, \
    SPAREN_SPARBUCHUNG_ADD, \
    SPAREN_SPARKONTO_ADD, \
    SPAREN_DEPOTWERT_ADD, \
    SPAREN_ORDER_ADD, \
    SPAREN_ORDERDAUERAUFTRAG_ADD, \
    SPAREN_ORDERDAUERAUFTRAG_UEBERSICHT, \
    SPAREN_DEPOTAUSZUG_ADD, \
    SPAREN_SPARBUCHUNGEN_UEBERSICHT, \
    SPAREN_SPARKONTO_UEBERSICHT, \
    SPAREN_DEPOTWERT_UEBERSICHT, \
    SPAREN_ORDER_UEBERSICHT, \
    SPAREN_DEPOTAUSZUEGE_UEBERSICHT, \
    SPAREN_UEBERSICHT_ETFS, \
    CORE_CONFIGURATION
from butler_offline.viewcore.template import fa

from butler_offline.viewcore.state import persisted_state

EINZELBUCHUNGEN_SUBMENU_NAME = 'Persönliche Finanzen'


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


def get_menu_list():
    main_menu = {}

    menu = []
    menu.append({'url': EINZELBUCHUNGEN_EINZELBUCHUNGEN_UEBERSICHT, 'name': 'Übersicht Einzelbuchungen', 'icon': (
        fa.fa_list)})
    menu.append({'url': EINZELBUCHUNGEN_DAUERAUFTRAG_UEBERSICHT, 'name': 'Übersicht Daueraufträge', 'icon': (
        fa.fa_list)})
    menu.append({'url': EINZELBUCHUNGEN_AUSGABE_ADD, 'name': 'Neue Ausgabe', 'icon': fa.fa_plus})
    menu.append({'url': EINZELBUCHUNGEN_EINNAHME_ADD, 'name': 'Neue Einnahme', 'icon': fa.fa_plus})
    menu.append({'url': EINZELBUCHUNGEN_DAUERAUFTRAG_ADD, 'name': 'Neuer Dauerauftrag', 'icon': fa.fa_plus})
    menu.append({'url': EINZELBUCHUNGEN_MONATSUEBERSICHT, 'name': 'Monatsübersicht', 'icon': fa.fa_line_chart})
    menu.append({'url': EINZELBUCHUNGEN_JAHRESUEBERSICHT, 'name': 'Jahresübersicht', 'icon': fa.fa_line_chart})
    menu.append({'url': CORE_IMPORT, 'name': 'Export / Import', 'icon': fa.fa_cogs})
    main_menu[EINZELBUCHUNGEN_SUBMENU_NAME] = menu

    menu = []
    menu.append({'url': GEMEINSAME_BUCHUNGEN_UEBERSICHT, 'name': 'Übersicht Buchungen', 'icon': fa.fa_list})
    menu.append({'url': GEMEINSAME_BUCHUNGEN_ADD, 'name': 'Neue gemeinsame Ausgabe', 'icon': fa.fa_plus})
    menu.append({'url': GEMEINSAME_BUCHUNGEN_ABRECHNEN, 'name': 'Gemeinsam abrechnen', 'icon': fa.fa_cogs})
    menu.append({'url': CORE_IMPORT, 'name': 'Export / Import', 'icon': fa.fa_cogs})
    menu.append({'url': GEMEINSAME_BUCHUNGEN_ABRECHNUNGEN, 'name': 'Übersicht Abrechnungen', 'icon': fa.fa_list})
    main_menu['Gemeinsame Finanzen'] = menu

    menu = []
    menu.append({'url': SPAREN_UEBERSICHT, 'name': 'Sparen Übersicht', 'icon': fa.fa_line_chart})
    menu.append({'url': SPAREN_UEBERSICHT_ETFS, 'name': 'ETF Übersicht', 'icon': fa.fa_line_chart})
    menu.append({'url': SPAREN_SPARBUCHUNG_ADD, 'name': 'Neue Sparbuchung', 'icon': fa.fa_plus})
    menu.append({'url': SPAREN_SPARKONTO_ADD, 'name': 'Neues Sparkonto', 'icon': fa.fa_plus})
    menu.append({'url': SPAREN_DEPOTWERT_ADD, 'name': 'Neuer Depotwert', 'icon': fa.fa_plus})
    menu.append({'url': SPAREN_ORDER_ADD, 'name': 'Neue Order', 'icon': fa.fa_plus})
    menu.append({'url': SPAREN_ORDERDAUERAUFTRAG_ADD, 'name': 'Neuer Order-Dauerauftrag', 'icon': fa.fa_plus})
    menu.append({'url': SPAREN_DEPOTAUSZUG_ADD, 'name': 'Neuer Depotauszug', 'icon': fa.fa_plus})
    menu.append({'url': SPAREN_SPARBUCHUNGEN_UEBERSICHT, 'name': 'Übersicht Sparbuchungen', 'icon': fa.fa_list})
    menu.append({'url': SPAREN_SPARKONTO_UEBERSICHT, 'name': 'Übersicht Sparkontos', 'icon': fa.fa_list})
    menu.append({'url': SPAREN_DEPOTWERT_UEBERSICHT, 'name': 'Übersicht Depotwerte', 'icon': fa.fa_list})
    menu.append({'url': SPAREN_ORDER_UEBERSICHT, 'name': 'Übersicht Order', 'icon': fa.fa_list})
    menu.append({'url': SPAREN_ORDERDAUERAUFTRAG_UEBERSICHT, 'name': 'Übersicht Order-Daueraufträge', 'icon': (
        fa.fa_list)})
    menu.append({'url': SPAREN_DEPOTAUSZUEGE_UEBERSICHT, 'name': 'Übersicht Depotauszüge', 'icon': fa.fa_list})

    main_menu['Sparen'] = menu

    menu = []
    menu.append({'url': CORE_CONFIGURATION, 'name': 'Einstellungen', 'icon': fa.fa_cogs})
    menu.append({'url': '/production/?database=' + persisted_state.database_instance().name,
                 'name': 'Datenbank neu laden',
                 'icon':  fa.fa_refresh})
    for database in persisted_state.DATABASES:
        if database != persisted_state.database_instance().name:
            menu.append({'url': '/production/?database=' + database, 'name': 'To ' + database, 'icon': fa.fa_cogs})

    main_menu['Einstellungen'] = menu
    return main_menu
