from datetime import date

from butler_offline.core.database.sparen.orderdauerauftrag import OrderDauerauftrag
from butler_offline.core.time import today
from butler_offline.viewcore import request_handler, routes
from butler_offline.viewcore.context.builder import generate_transactional_page_context, \
    TransactionalPageContext, generate_redirect_page_context
from butler_offline.viewcore.converter import datum_to_string, datum_to_german, dezimal_float, datum
from butler_offline.viewcore.http import Request
from butler_offline.views.sparen.orderdauerauftrag.split import (split_dauerauftrag,
                                                                 get_ausführungszeitpunkte_fuer_orderdauerauftrag)


class SplitOrderDauerauftraegeContext:
    def __init__(self,
                 orderdauerauftraege: OrderDauerauftrag,
                 today: date):
        self._orderdauerauftraege = orderdauerauftraege
        self._today = today

    def orderdauerauftraege(self) -> OrderDauerauftrag:
        return self._orderdauerauftraege

    def today(self) -> date:
        return self._today


def handle_request(request: Request, context: SplitOrderDauerauftraegeContext):
    orderdauerauftrag_id: int = int(request.values['orderdauerauftrag_id'])

    if request.post_action_is('preset_values'):

        result_context: TransactionalPageContext = generate_transactional_page_context('addorderdauerauftrag')

        preset_datum = get_ausführungszeitpunkte_fuer_orderdauerauftrag(orderdauerauftraege=context.orderdauerauftraege(),
                                                                        orderdauerauftrag_id=orderdauerauftrag_id,
                                                                        today=context.today())
        preset_datum_formatted = []

        if len(preset_datum) <= 2:
            raise ValueError('Can not be edited')

        for i in range(0, len(preset_datum)):
            current_date = preset_datum[i]
            preset_datum_formatted.append({
                'datum': datum_to_string(current_date),
                'datum_german': datum_to_german(current_date),
                'can_be_chosen': True
            })

        if len(preset_datum_formatted) > 0:
            preset_datum_formatted[0]['can_be_chosen'] = False
            preset_datum_formatted[-1]['can_be_chosen'] = False

        result_context.add('datum', preset_datum_formatted)
        result_context.add('wert', context.orderdauerauftraege().get(orderdauerauftrag_id)['Wert'])
        result_context.add('orderdauerauftrag_id', orderdauerauftrag_id)
        return result_context

    if request.post_action_is('split'):
        wert = dezimal_float(request.values['wert'])
        aenderungsdatum = datum(request.values['datum'])
        split_dauerauftrag(
            orderdauerauftraege=context.orderdauerauftraege(),
            orderdauerauftrag_id=orderdauerauftrag_id,
            split_date=aenderungsdatum,
            wert=wert)
        return generate_redirect_page_context(routes.SPAREN_ORDERDAUERAUFTRAG_ADD)

    raise FileNotFoundError('post action unknown')


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        context_creator=lambda db: SplitOrderDauerauftraegeContext(
            orderdauerauftraege=db.orderdauerauftrag,
            today=today()
        ),
        html_base_page='sparen/split_orderdauerauftrag.html'
    )
