from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_to_german
import collections

from butler_offline.viewcore.context import generate_transactional_context, generate_redirect_context

def _handle_request(request):
    orderdauerauftrag = persisted_state.database_instance().orderdauerauftrag

    if post_action_is(request, 'delete'):
        print("Delete: ", request.values['delete_index'])
        orderdauerauftrag.delete(int(request.values['delete_index']))
        return generate_redirect_context('/uebersicht_orderdauerauftrag/')

    context = generate_transactional_context('uebersicht_orderdauerauftrag')
    data = collections.OrderedDict()
    data['Aktuelle Daueraufträge'] = _format_dauerauftrag_floatpoint(orderdauerauftrag.aktuelle())
    data['Zukünftige Daueraufträge'] = _format_dauerauftrag_floatpoint(orderdauerauftrag.future())
    data['Vergangene  Daueraufträge'] = _format_dauerauftrag_floatpoint(orderdauerauftrag.past())
    context['dauerauftraege'] = data
    return context


def _format_dauerauftrag_floatpoint(dauerauftraege):
    for dauerauftrag in dauerauftraege:
        dauerauftrag['Wert'] = '%.2f' % dauerauftrag['Wert']
        dauerauftrag['Startdatum'] = datum_to_german(dauerauftrag['Startdatum'])
        dauerauftrag['Endedatum'] = datum_to_german(dauerauftrag['Endedatum'])

    return dauerauftraege


def index(request):
    return request_handler.handle_request(request, _handle_request, 'sparen/uebersicht_orderdauerauftrag.html')
