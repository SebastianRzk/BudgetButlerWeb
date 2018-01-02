from adddauerauftrag.views import handle_request
from viewcore import viewcore
from viewcore.viewcore import name_of_partner
from viewcore import request_handler

def _handle_request(_):
    name_self = viewcore.database_instance().name
    name_partner = viewcore.name_of_partner()

    ausgabe_sebastian = viewcore.database_instance().gemeinsamebuchungen.fuer(name_self)
    ausgabe_maureen = viewcore.database_instance().gemeinsamebuchungen.fuer(name_partner)
    ausgabe_sebastian = _sum(ausgabe_sebastian.Wert)
    ausgabe_maureen = _sum(ausgabe_maureen.Wert)
    ausgabe_gesamt = ausgabe_maureen + ausgabe_sebastian
    print(viewcore.name_of_partner(), ausgabe_maureen)
    print(viewcore.database_instance().name, ausgabe_sebastian)

    dif_sebastian = (ausgabe_gesamt / 2) - ausgabe_sebastian
    dif_maureen = (ausgabe_gesamt / 2) - ausgabe_maureen

    ergebnis = 'Die gemeinsamen Ausgaben sind ausgeglichen.'

    if dif_maureen > 0:
        ergebnis = name_partner + ' bekommt von ' + name_self + ' noch ' + str('%.2f' % dif_maureen) + '€.'

    if dif_sebastian > 0:
        ergebnis = name_self + ' bekommt von ' + name_partner + ' noch ' + str('%.2f' % dif_sebastian) + '€.'
    print("ergebnis:", ergebnis)

    context = viewcore.generate_base_context('gemeinsamabrechnen')

    context['ausgabe_maureen'] = "%.2f" % abs(ausgabe_maureen)
    context['ausgabe_sebastian'] = "%.2f" % abs(ausgabe_sebastian)
    context['ausgabe_gesamt'] = "%.2f" % abs(ausgabe_gesamt)
    context['ergebnis'] = ergebnis
    return context

def index(request):
    return request_handler.handle_request(request, _handle_request, 'dauerauftraguebersicht.html')

def _sum(data):
    if data.empty:
        return 0
    return data.sum()

def abrechnen(request):
    return request_handler.handle_request(request, _handle_abrechnen_request, 'present_abrechnung.html')


def _handle_abrechnen_request(_):
    print("Abrechnen")
    context = viewcore.generate_base_context('gemeinsamabrechnen')
    abrechnungs_text = viewcore.database_instance().abrechnen()
    context['abrechnungstext'] = abrechnungs_text.replace('\n', '<br>')
    viewcore.save_refresh()

    return context
