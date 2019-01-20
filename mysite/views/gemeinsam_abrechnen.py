from mysite.viewcore import viewcore
from mysite.viewcore.viewcore import name_of_partner
from mysite.viewcore.viewcore import get_post_parameter_or_default
from mysite.viewcore.viewcore import is_post_parameter_set
from mysite.viewcore import request_handler
from mysite.viewcore.converter import datum_to_string
from mysite.viewcore.converter import datum_to_german
from mysite.viewcore.converter import datum_from_german
from mysite.viewcore.converter import datum


def _handle_request(request):
    context = viewcore.generate_base_context('gemeinsamabrechnen')
    db = viewcore.database_instance()
    alle_gemeinsamen_buchungen = db.gemeinsamebuchungen

    if alle_gemeinsamen_buchungen.is_empty():
        context['%Errortext'] = 'Keine gemeinsame Buchungen erfasst'
        return context

    name_self = db.name
    name_partner = name_of_partner()

    mindate = alle_gemeinsamen_buchungen.min_date()
    maxdate = alle_gemeinsamen_buchungen.max_date()

    set_mindate = get_post_parameter_or_default(request, 'set_mindate', mindate, mapping_function=datum)
    set_maxdate = get_post_parameter_or_default(request, 'set_maxdate', maxdate, mapping_function=datum)
    selected_gemeinsamen_buchungen = alle_gemeinsamen_buchungen.select_range(set_mindate, set_maxdate)

    replay_value_if_defined(context, 'set_verhaeltnis', request, default=50)
    set_verhaeltnis = int(context['set_verhaeltnis'])
    replay_value_if_defined(context, 'set_limit', request)
    replay_value_if_defined(context, 'set_limit_value', request, default=50)
    replay_value_if_defined(context, 'set_limit_fuer', request)
    replay_value_if_defined(context, 'set_self_kategorie', request)
    replay_value_if_defined(context, 'set_self_kategorie_value', request)
    replay_value_if_defined(context, 'set_other_kategorie', request)
    replay_value_if_defined(context, 'set_other_kategorie_value', request, 'Korrekturbuchung')


    ausgabe_sebastian = selected_gemeinsamen_buchungen.fuer(name_self)
    ausgabe_maureen = selected_gemeinsamen_buchungen.fuer(name_partner)
    ausgabe_sebastian = _sum(ausgabe_sebastian.Wert)
    ausgabe_maureen = _sum(ausgabe_maureen.Wert)
    ausgabe_gesamt = ausgabe_maureen + ausgabe_sebastian

    ergebnis = ''

    if is_post_parameter_set(request, 'set_limit'):
        ergebnis_satz = '''Durch das Limit bei {name} von {limit_value} EUR wurde das Verhältnis von {verhaeltnis_alt} auf {verhaeltnis_neu} aktualisiert<br>'''
        verhaeltnis_alt = set_verhaeltnis
        limited_person = request.values['set_limit_fuer']
        limit_value = int(request.values['set_limit_value'])
        print('here', limited_person, limit_value)

        if limited_person == name_partner:
            maureen_soll = abs(ausgabe_gesamt * ((100 - set_verhaeltnis) / 100))
            print('Maureen soll', maureen_soll)
            if maureen_soll > limit_value:
                set_verhaeltnis = 100 - abs((limit_value / ausgabe_gesamt) * 100)
                print('Neu berechnet')
                ergebnis += ergebnis_satz.format(name=name_partner, limit_value = limit_value, verhaeltnis_alt=verhaeltnis_alt, verhaeltnis_neu=set_verhaeltnis)
        else:
            sebastian_soll = abs(ausgabe_gesamt * (set_verhaeltnis / 100))
            if sebastian_soll > limit_value:
                set_verhaeltnis = abs((limit_value / ausgabe_gesamt) * 100)
                ergebnis += ergebnis_satz.format(name=name_self, limit_value = limit_value, verhaeltnis_alt=verhaeltnis_alt, verhaeltnis_neu=set_verhaeltnis)

    sebastian_soll = (ausgabe_gesamt * (set_verhaeltnis / 100))
    sebastian_dif = sebastian_soll - ausgabe_sebastian
    maureen_soll = (ausgabe_gesamt * ((100 - set_verhaeltnis) / 100))
    maureen_dif = maureen_soll - ausgabe_maureen

    ergebnis_satz = 'Die gemeinsamen Ausgaben sind ausgeglichen.'
    if maureen_dif > 0 or sebastian_dif < 0:
        ergebnis_satz = name_partner + ' bekommt von ' + name_self + ' noch ' + str('%.2f' % maureen_dif) + '€.'

    if sebastian_dif > 0 or maureen_dif < 0:
        ergebnis_satz = name_self + ' bekommt von ' + name_partner + ' noch ' + str('%.2f' % sebastian_dif) + '€.'
    ergebnis += ergebnis_satz

    context['ausgabe_maureen'] = "%.2f" % abs(ausgabe_maureen)
    context['ausgabe_sebastian'] = "%.2f" % abs(ausgabe_sebastian)
    context['sebastian_diff'] = "%.2f" % sebastian_dif
    context['maureen_diff'] = "%.2f" % maureen_dif
    context['sebastian_soll'] = "%.2f" % abs(sebastian_soll)
    context['maureen_soll'] = "%.2f" % abs(maureen_soll)
    context['ausgabe_gesamt'] = "%.2f" % abs(ausgabe_gesamt)
    context['ergebnis'] = ergebnis
    context['myname'] = name_self
    context['partnername'] = name_partner

    context['mindate'] = datum_to_german(mindate)
    context['maxdate'] = datum_to_german(maxdate)
    context['count'] = len(alle_gemeinsamen_buchungen.get_content())

    context['set_mindate_rfc'] = datum_to_string(set_mindate)
    context['set_maxdate_rfc'] = datum_to_string(set_maxdate)
    context['set_mindate'] = datum_to_german(set_mindate)
    context['set_maxdate'] = datum_to_german(set_maxdate)
    context['set_count'] = len(selected_gemeinsamen_buchungen.get_content())

    context['kategorien'] = db.einzelbuchungen.get_alle_kategorien(hide_ausgeschlossene_kategorien=True)

    return context


def replay_value_if_defined(context, replay_name, request, default=False):
    if is_post_parameter_set(request, replay_name):
        context[replay_name] = request.values[replay_name]
    elif default:
        context[replay_name] = default


def index(request):
    return request_handler.handle_request(request, _handle_request, 'gemeinsamabrechnen.html')


def _sum(data):
    if data.empty:
        return 0
    return data.sum()


def abrechnen(request):
    return request_handler.handle_request(request, _handle_abrechnen_request, 'present_abrechnung.html')


def _handle_abrechnen_request(request):
    context = viewcore.generate_base_context('gemeinsamabrechnen')

    set_mindate = get_post_parameter_or_default(request, 'set_mindate', None, mapping_function=datum_from_german)
    set_maxdate = get_post_parameter_or_default(request, 'set_maxdate', None, mapping_function=datum_from_german)

    abrechnungs_text = viewcore.database_instance().abrechnen(mindate=set_mindate, maxdate=set_maxdate)
    context['abrechnungstext'] = abrechnungs_text.replace('\n', '<br>')

    return context
