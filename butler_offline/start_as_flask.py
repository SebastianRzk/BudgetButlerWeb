from flask import Flask
from flask import request
import logging

from butler_offline.views.einzelbuchungen import addausgabe, \
    adddauerauftrag, \
    addeinnahme, \
    uebersicht_dauerauftrag, \
    uebersicht_einzelbuchungen, \
    uebersicht_jahr, \
    uebersicht_monat
from butler_offline.views.core import dashboard, \
    configuration, \
    testmode_switch,\
    theme

from butler_offline.views.gemeinsame_buchungen import gemeinsam_abrechnen,\
    uebersicht_abrechnungen,\
    addgemeinsam, \
    uebersicht_gemeinsam

from butler_offline.views.sparen import uebersicht_sparen, \
    add_sparbuchung, \
    add_sparkoto, \
    uebersicht_sparbuchungen, \
    uebersicht_sparkontos,\
    add_depotwert,\
    uebersicht_depotwerte, \
    add_order, \
    uebersicht_order, \
    add_orderdauerauftrag, \
    uebersicht_orderdauerauftrag, \
    add_depotauszug, \
    uebersicht_depotauszuege, \
    uebersicht_etfs

from butler_offline.viewcore import routes

from butler_offline.views.shared import import_data


app = Flask(__name__)

if app.debug:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
else:
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARN)
logging.debug('debug output enabled')


@app.route('/')
def show_dashboard():
    return dashboard.index(request)


@app.route(routes.EINZELBUCHUNGEN_DAUERAUFTRAG_ADD, methods=['GET', 'POST'])
def add_dauerauftrag():
    return adddauerauftrag.index(request)


@app.route(routes.EINZELBUCHUNGEN_EINNAHME_ADD, methods=['GET', 'POST'])
def add_einnahme():
    return addeinnahme.index(request)


@app.route(routes.EINZELBUCHUNGEN_AUSGABE_ADD, methods=['GET', 'POST'])
def add_ausgabe():
    return addausgabe.index(request)


@app.route(routes.GEMEINSAME_BUCHUNGEN_ADD, methods=['GET', 'POST'])
def add_gemeinsam():
    return addgemeinsam.index(request)


@app.route(routes.EINZELBUCHUNGEN_DAUERAUFTRAG_UEBERSICHT, methods=['GET', 'POST'])
def view_uebersicht_dauerauftrag():
    return uebersicht_dauerauftrag.index(request)


@app.route(routes.GEMEINSAME_BUCHUNGEN_UEBERSICHT, methods=['GET', 'POST'])
def view_uebersicht_gemeinsam():
    return uebersicht_gemeinsam.index(request)


@app.route(routes.EINZELBUCHUNGEN_JAHRESUEBERSICHT, methods=['GET', 'POST'])
def view_uebersicht_jahr():
    return uebersicht_jahr.index(request)


@app.route(routes.EINZELBUCHUNGEN_MONATSUEBERSICHT, methods=['GET', 'POST'])
def view_uebersicht_monat():
    return uebersicht_monat.index(request)


@app.route(routes.EINZELBUCHUNGEN_EINZELBUCHUNGEN_UEBERSICHT, methods=['GET', 'POST'])
def view_uebersicht_einzelbuchungen():
    return uebersicht_einzelbuchungen.index(request)


@app.route('/production/', methods=['GET'])
def switch_to_production():
    return testmode_switch.leave_debug(request)


@app.route('/production/testmode/', methods=['GET'])
def switch_to_debug():
    return testmode_switch.enter_testmode(request)


@app.route(routes.GEMEINSAME_BUCHUNGEN_ABRECHNEN, methods=['GET', 'POST'])
def view_gemeinsam_abrechnen():
    return gemeinsam_abrechnen.index(request)


@app.route('/abrechnen/', methods=['GET', 'POST'])
def exec_abrechnen():
    return gemeinsam_abrechnen.abrechnen(request)


@app.route(routes.CORE_IMPORT, methods=['GET', 'POST'])
def view_import():
    return import_data.index(request)


@app.route(routes.CORE_CONFIGURATION, methods=['GET', 'POST'])
def view_configuration():
    return configuration.index(request)


@app.route(routes.GEMEINSAME_BUCHUNGEN_ABRECHNUNGEN, methods=['GET'])
def view_uebersicht_abrechnungen():
    return uebersicht_abrechnungen.index(request)


'''
Sparen:
'''


@app.route(routes.SPAREN_SPARBUCHUNG_ADD, methods=['GET', 'POST'])
def display_add_sparbuchung():
    return add_sparbuchung.index(request)


@app.route(routes.SPAREN_SPARKONTO_ADD, methods=['GET', 'POST'])
def display_add_sparkonto():
    return add_sparkoto.index(request)


@app.route(routes.SPAREN_DEPOTWERT_ADD, methods=['GET', 'POST'])
def display_add_depowert():
    return add_depotwert.index(request)


@app.route(routes.SPAREN_ORDER_ADD, methods=['GET', 'POST'])
def display_add_order():
    return add_order.index(request)


@app.route(routes.SPAREN_ORDERDAUERAUFTRAG_ADD, methods=['GET', 'POST'])
def display_add_orderdauerauftrag():
    return add_orderdauerauftrag.index(request)


@app.route(routes.SPAREN_DEPOTAUSZUG_ADD, methods=['GET', 'POST'])
def display_add_depotauszug():
    return add_depotauszug.index(request)


@app.route(routes.SPAREN_SPARBUCHUNGEN_UEBERSICHT, methods=['GET', 'POST'])
def display_uebersicht_sparbuchung():
    return uebersicht_sparbuchungen.index(request)


@app.route(routes.SPAREN_SPARKONTO_UEBERSICHT, methods=['GET', 'POST'])
def display_uebersicht_sparkontos():
    return uebersicht_sparkontos.index(request)


@app.route(routes.SPAREN_DEPOTWERT_UEBERSICHT, methods=['GET', 'POST'])
def display_uebersicht_depowerte():
    return uebersicht_depotwerte.index(request)


@app.route(routes.SPAREN_ORDER_UEBERSICHT, methods=['GET', 'POST'])
def display_uebersicht_order():
    return uebersicht_order.index(request)


@app.route(routes.SPAREN_ORDERDAUERAUFTRAG_UEBERSICHT, methods=['GET', 'POST'])
def display_uebersicht_orderdauerauftrag():
    return uebersicht_orderdauerauftrag.index(request)


@app.route(routes.SPAREN_DEPOTAUSZUEGE_UEBERSICHT, methods=['GET', 'POST'])
def display_uebersicht_depotauszuege():
    return uebersicht_depotauszuege.index(request)


@app.route(routes.SPAREN_UEBERSICHT, methods=['GET'])
def display_sparen_uebersicht():
    return uebersicht_sparen.index(request)


@app.route(routes.SPAREN_UEBERSICHT_ETFS, methods=['GET', 'POST'])
def display_sparen_uebersicht_etfs():
    return uebersicht_etfs.index(request)


@app.route('/theme/')
def theme_color():
    return theme.index(request)
