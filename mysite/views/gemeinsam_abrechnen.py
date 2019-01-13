from mysite.viewcore import viewcore
from mysite.viewcore.viewcore import name_of_partner
from mysite.viewcore.viewcore import get_post_parameter_or_default
from mysite.viewcore import request_handler
from mysite.viewcore.converter import datum_to_string
from mysite.viewcore.converter import datum_to_german
from mysite.viewcore.converter import datum_from_german
from mysite.viewcore.converter import datum


def _handle_request(request):
    name_self = viewcore.database_instance().name
    name_partner = viewcore.name_of_partner()

    alle_gemeinsamen_buchungen = viewcore.database_instance().gemeinsamebuchungen

    context = viewcore.generate_base_context('gemeinsamabrechnen')
    if alle_gemeinsamen_buchungen.is_empty():
        context['%Errortext'] = 'Keine gemeinsame Buchungen erfasst'
        return context

    mindate = alle_gemeinsamen_buchungen.min_date()
    maxdate = alle_gemeinsamen_buchungen.max_date()

    set_mindate = get_post_parameter_or_default(request, 'set_mindate', mindate, mapping_function=datum)
    set_maxdate = get_post_parameter_or_default(request, 'set_maxdate', maxdate, mapping_function=datum)
    selected_gemeinsamen_buchungen = alle_gemeinsamen_buchungen.select_range(set_mindate, set_maxdate)



    ausgabe_sebastian = selected_gemeinsamen_buchungen.fuer(name_self)
    ausgabe_maureen = selected_gemeinsamen_buchungen.fuer(name_partner)
    ausgabe_sebastian = _sum(ausgabe_sebastian.Wert)
    ausgabe_maureen = _sum(ausgabe_maureen.Wert)
    ausgabe_gesamt = ausgabe_maureen + ausgabe_sebastian

    dif_sebastian = (ausgabe_gesamt / 2) - ausgabe_sebastian
    dif_maureen = (ausgabe_gesamt / 2) - ausgabe_maureen

    ergebnis = 'Die gemeinsamen Ausgaben sind ausgeglichen.'

    if dif_maureen > 0:
        ergebnis = name_partner + ' bekommt von ' + name_self + ' noch ' + str('%.2f' % dif_maureen) + '€.'

    if dif_sebastian > 0:
        ergebnis = name_self + ' bekommt von ' + name_partner + ' noch ' + str('%.2f' % dif_sebastian) + '€.'


    context['ausgabe_maureen'] = "%.2f" % abs(ausgabe_maureen)
    context['ausgabe_sebastian'] = "%.2f" % abs(ausgabe_sebastian)
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

    return context


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
