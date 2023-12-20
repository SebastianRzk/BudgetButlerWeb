from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.core.database.sparen.order import Order
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_transactional_page_context, generate_redirect_page_context
from butler_offline.viewcore.converter import datum_to_german
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.viewcore.requirements import order_needed_decorator
from butler_offline.views.sparen.add_order import TYP_KAUF, TYP_VERKAUF


class UebersichtOrderContext:
    def __init__(self, depotwerte: Depotwerte, order: Order):
        self._depotwerte = depotwerte
        self._order = order

    def order(self) -> Order:
        return self._order

    def depotwerte(self) -> Depotwerte:
        return self._depotwerte


@order_needed_decorator()
def handle_request(request: Request, context: UebersichtOrderContext):
    order = context.order()
    depotwerte = context.depotwerte()

    if request.post_action_is('delete'):
        order.delete(int(request.values['delete_index']))
        return generate_redirect_page_context('/uebersicht_order/')

    db = order.get_all()
    order_liste = []
    for row_index, row in db.iterrows():
        if row.Wert > 0:
            typ = TYP_KAUF
        else:
            typ = TYP_VERKAUF

        order_liste.append({
            'index': row_index,
            'Datum': datum_to_german(row.Datum),
            'Name': row.Name,
            'Konto': row.Konto,
            'Typ': typ,
            'Depotwert': depotwerte.get_description_for(row.Depotwert),
            'Wert': Betrag(abs(row.Wert)),
            'Dynamisch': row.Dynamisch
        })

    result_context = generate_transactional_page_context('uebersicht_order')
    result_context.add('order', order_liste)
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='sparen/uebersicht_order.html',
        context_creator=lambda db: UebersichtOrderContext(
            depotwerte=db.depotwerte,
            order=db.order
        )
    )
