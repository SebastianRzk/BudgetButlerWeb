from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.converter import from_double_to_german


def _handle_request(request):
    depotwerte = persisted_state.database_instance().depotwerte
    order = persisted_state.database_instance().order
    if post_action_is(request, 'delete'):
        depotwerte.delete(int(request.values['delete_index']))
        return request_handler.create_redirect_context('/uebersicht_depotwerte/')

    db = depotwerte.get_all()
    depotwerte_liste = []
    gesamt_buchungen = 0
    gesamt_wert = 0

    for row_index, row in db.iterrows():
        buchungen = order.get_order_fuer_depotwert(row.ISIN)
        wert = 0
        differenz = wert - buchungen

        depotwerte_liste.append({
            'index': row_index,
            'name': row.Name,
            'isin': row.ISIN,
            'buchung': from_double_to_german(buchungen),
            'difference': from_double_to_german(differenz),
            'difference_is_negativ': differenz < 0,
            'wert': 'noch nicht ermittelt'
        })
        gesamt_buchungen += buchungen
        gesamt_wert += wert

    gesamt_difference = gesamt_wert - gesamt_buchungen
    gesamt = {
        'wert': from_double_to_german(gesamt_wert),
        'difference': from_double_to_german(gesamt_difference),
        'difference_is_negativ': gesamt_difference < 0,
        'buchung': from_double_to_german(gesamt_buchungen)
    }

    context = viewcore.generate_transactional_context('uebersicht_depotwerte')
    context['depotwerte'] = depotwerte_liste
    context['gesamt'] = gesamt
    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'sparen/uebersicht_depotwerte.html')

