from flask import Flask
app = Flask(__name__)
from flask import request

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

from butler_offline.views.sparen import add_sparbuchung, \
    add_sparkoto, \
    uebersicht_sparbuchungen, \
    uebersicht_sparkontos

from butler_offline.views.shared import import_data


@app.route('/')
def show_dashboard():
    return dashboard.index(request)


@app.route('/adddauerauftrag/', methods=['GET', 'POST'])
def add_dauerauftrag():
    return adddauerauftrag.index(request)


@app.route('/addeinnahme/', methods=['GET', 'POST'])
def add_einnahme():
    return addeinnahme.index(request)


@app.route('/addausgabe/', methods=['GET', 'POST'])
def add_ausgabe():
    return addausgabe.index(request)


@app.route('/addgemeinsam/', methods=['GET', 'POST'])
def add_gemeinsam():
    return addgemeinsam.index(request)


@app.route('/dauerauftraguebersicht/', methods=['GET', 'POST'])
def view_uebersicht_dauerauftrag():
    return uebersicht_dauerauftrag.index(request)


@app.route('/gemeinsameuebersicht/', methods=['GET', 'POST'])
def view_uebersicht_gemeinsam():
    return uebersicht_gemeinsam.index(request)


@app.route('/jahresuebersicht/', methods=['GET', 'POST'])
def view_uebersicht_jahr():
    return uebersicht_jahr.index(request)


@app.route('/monatsuebersicht/', methods=['GET', 'POST'])
def view_uebersicht_monat():
    return uebersicht_monat.index(request)


@app.route('/uebersicht/', methods=['GET', 'POST'])
def view_uebersicht_einzelbuchungen():
    return uebersicht_einzelbuchungen.index(request)


@app.route('/monatsuebersicht/abrechnung/', methods=['GET', 'POST'])
def view_abrechnung_monat():
    return uebersicht_monat.abrechnen(request)


@app.route('/production/', methods=['GET'])
def switch_to_production():
    return testmode_switch.leave_debug(request)


@app.route('/production/testmode/', methods=['GET'])
def switch_to_debug():
    return testmode_switch.enter_testmode(request)


@app.route('/gemeinsamabrechnen/', methods=['GET', 'POST'])
def view_gemeinsam_abrechnen():
    return gemeinsam_abrechnen.index(request)


@app.route('/abrechnen/', methods=['GET', 'POST'])
def exec_abrechnen():
    return gemeinsam_abrechnen.abrechnen(request)


@app.route('/import/', methods=['GET', 'POST'])
def view_import():
    return import_data.index(request)


@app.route('/configuration/', methods=['GET', 'POST'])
def view_configuration():
    return configuration.index(request)


@app.route('/uebersichtabrechnungen/', methods=['GET'])
def view_uebersicht_abrechnungen():
    return uebersicht_abrechnungen.index(request)


'''
Sparen:
'''
@app.route('/add_sparbuchung/', methods=['GET', 'POST'])
def display_add_sparbuchung():
    return add_sparbuchung.index(request)

@app.route('/add_sparkonto/', methods=['GET', 'POST'])
def display_add_sparkonto():
    return add_sparkoto.index(request)

@app.route('/uebersicht_sparbuchungen/', methods=['GET', 'POST'])
def display_uebersicht_sparbuchung():
    return uebersicht_sparbuchungen.index(request)

@app.route('/uebersicht_sparkontos/', methods=['GET', 'POST'])
def display_uebersicht_sparkontos():
    return uebersicht_sparkontos.index(request)








@app.route('/theme/')
def theme_color():
    return theme.index(request)
