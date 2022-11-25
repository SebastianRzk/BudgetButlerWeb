from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore.converter import from_double_to_german, datum_to_german
from butler_offline.views.sparen.add_order import TYP_KAUF, TYP_VERKAUF
from butler_offline.viewcore.context import generate_transactional_context, generate_redirect_context

def _handle_request(request):
    order = persisted_state.database_instance().order
    depotwerte = persisted_state.database_instance().depotwerte

    if post_action_is(request, 'delete'):
        order.delete(int(request.values['delete_index']))
        return generate_redirect_context('/uebersicht_order/')

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
            'Wert': from_double_to_german(abs(row.Wert)),
            'Dynamisch': row.Dynamisch
        })

    context = generate_transactional_context('uebersicht_order')
    context['order'] = order_liste
    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'sparen/uebersicht_order.html')

