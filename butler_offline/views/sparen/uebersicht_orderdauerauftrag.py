import collections

from butler_offline.core.database.sparen.orderdauerauftrag import OrderDauerauftrag
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_transactional_page_context, generate_redirect_page_context
from butler_offline.viewcore.converter import datum_to_german
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.viewcore.requirements import order_dauerauftrag_needed_decorator


class UbersichtOrderDauerauftragContext:
    def __init__(self, orderdauerauftrag: OrderDauerauftrag):
        self._orderdauerauftrag = orderdauerauftrag

    def orderdauerauftrag(self) -> OrderDauerauftrag:
        return self._orderdauerauftrag


@order_dauerauftrag_needed_decorator()
def handle_request(request: Request, context: UbersichtOrderDauerauftragContext):
    orderdauerauftrag = context.orderdauerauftrag()

    if request.post_action_is('delete'):
        print("Delete: ", request.values['delete_index'])
        orderdauerauftrag.delete(int(request.values['delete_index']))
        return generate_redirect_page_context('/uebersicht_orderdauerauftrag/')

    result_context = generate_transactional_page_context('uebersicht_orderdauerauftrag')
    data = collections.OrderedDict()
    data['Aktuelle Daueraufträge'] = _format_dauerauftrag_floatpoint(orderdauerauftrag.aktuelle())
    data['Zukünftige Daueraufträge'] = _format_dauerauftrag_floatpoint(orderdauerauftrag.future())
    data['Vergangene  Daueraufträge'] = _format_dauerauftrag_floatpoint(orderdauerauftrag.past())
    result_context.add('dauerauftraege', data)
    return result_context


def _format_dauerauftrag_floatpoint(dauerauftraege):
    for dauerauftrag in dauerauftraege:
        dauerauftrag['Wert'] = Betrag(dauerauftrag['Wert'])
        dauerauftrag['Startdatum'] = datum_to_german(dauerauftrag['Startdatum'])
        dauerauftrag['Endedatum'] = datum_to_german(dauerauftrag['Endedatum'])

    return dauerauftraege


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='sparen/uebersicht_orderdauerauftrag.html',
        context_creator=lambda db: UbersichtOrderDauerauftragContext(
            orderdauerauftrag=db.orderdauerauftrag
        )
    )
