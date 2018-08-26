
from mysite.viewcore import viewcore
from mysite.viewcore.viewcore import post_action_is
from mysite.viewcore import request_handler
from mysite.viewcore.converter import datum_to_german
import collections


def _handle_request(request):
    dauerauftraege = viewcore.database_instance().dauerauftraege

    if post_action_is(request, 'delete'):
        print("Delete: ", request.values['delete_index'])
        dauerauftraege.delete(int(request.values['delete_index']))

    context = viewcore.generate_base_context('dauerauftraguebersicht')
    data = collections.OrderedDict()
    data['Aktuelle Daueraufträge'] = _format_dauerauftrag_floatpoint(dauerauftraege.aktuelle())
    data['Zukünftige Daueraufträge'] = _format_dauerauftrag_floatpoint(dauerauftraege.future())
    data['Vergangene  Daueraufträge'] = _format_dauerauftrag_floatpoint(dauerauftraege.past())
    context['dauerauftraege'] = data
    context['transaction_key'] = 'requested'
    return context


def _format_dauerauftrag_floatpoint(dauerauftraege):
    for dauerauftrag in dauerauftraege:
        dauerauftrag['Wert'] = '%.2f' % dauerauftrag['Wert']
        dauerauftrag['Startdatum'] = datum_to_german(dauerauftrag['Startdatum'])
        dauerauftrag['Endedatum'] = datum_to_german(dauerauftrag['Endedatum'])

    return dauerauftraege


def index(request):
    return request_handler.handle_request(request, _handle_request, 'uebersicht_dauerauftrag.html')
