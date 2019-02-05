from flask import Flask
app = Flask(__name__)
from flask import request

from butler_offline.views import dashboard
from butler_offline.views import adddauerauftrag
from butler_offline.views import addeinnahme
from butler_offline.views import addausgabe
from butler_offline.views import addgemeinsam

from butler_offline.views import uebersicht_dauerauftrag
from butler_offline.views import uebersicht_gemeinsam
from butler_offline.views import uebersicht_jahr
from butler_offline.views import uebersicht_monat
from butler_offline.views import uebersicht_einzelbuchungen

from butler_offline.views import gemeinsam_abrechnen
from butler_offline.views import testmode_switch
from butler_offline.views import import_data


from butler_offline.views import configuration

from butler_offline.views import theme

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


@app.route('/theme/')
def theme_color():
    return theme.index(request)
