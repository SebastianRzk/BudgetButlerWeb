
from viewcore import viewcore
from viewcore.viewcore import post_action_is
from viewcore import request_handler
import collections


def _handle_request(request):
    dauerauftraege = viewcore.database_instance().dauerauftraege

    if post_action_is(request, 'delete'):
        print("Delete: ", request.POST['delete_index'])
        dauerauftraege.delete(int(request.POST['delete_index']))

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
    return dauerauftraege


def index(request):
    return request_handler.handle_request(request, _handle_request, 'dauerauftraguebersicht.html')
