from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.converter import from_double_to_german


def _handle_request(request):
    sparkontos = persisted_state.database_instance().sparkontos
    if post_action_is(request, 'delete'):
        sparkontos.delete(int(request.values['delete_index']))
        return request_handler.create_redirect_context('/uebersicht_sparkontos/')

    db = sparkontos.get_all()

    gesamt_kontostand = 0
    gesamt_aufbuchungen = 0
    sparkonto_liste = []

    for row_index, row in db.iterrows():
        aktueller_kontostand = 0
        aktueller_kontostand_str = 'noch nicht ermittelt'

        aufbuchungen = 0
        aufbuchungen_str = 'noch nicht ermittelt'

        if row.Kontotyp == sparkontos.TYP_SPARKONTO:
            aktueller_kontostand = persisted_state.database_instance().sparbuchungen.get_kontostand_fuer(row.Kontoname)
            aktueller_kontostand_str = from_double_to_german(aktueller_kontostand)

            aufbuchungen = persisted_state.database_instance().sparbuchungen.get_aufbuchungen_fuer(row.Kontoname)
            aufbuchungen_str = from_double_to_german(aufbuchungen)

        if row.Kontotyp == sparkontos.TYP_DEPOT:
            aufbuchungen = persisted_state.database_instance().order.get_order_fuer(row.Kontoname)
            aufbuchungen_str = from_double_to_german(aufbuchungen)

        gesamt_kontostand += aktueller_kontostand
        gesamt_aufbuchungen += aufbuchungen

        diff = aktueller_kontostand - aufbuchungen

        sparkonto_liste.append({
            'index': row_index,
            'kontoname': row.Kontoname,
            'kontotyp': row.Kontotyp,
            'wert': aktueller_kontostand_str,
            'difference': from_double_to_german(diff),
            'aufbuchungen': aufbuchungen_str,
            'difference_is_negativ': diff < 0
        })

    gesamt_diff = gesamt_kontostand - gesamt_aufbuchungen

    gesamt = {
        'wert': from_double_to_german(gesamt_kontostand),
        'difference': from_double_to_german(gesamt_diff),
        'aufbuchungen': from_double_to_german(gesamt_aufbuchungen),
        'difference_is_negativ': gesamt_diff < 0
    }


    context = viewcore.generate_transactional_context('uebersicht_sparkontos')
    context['sparkontos'] = sparkonto_liste
    context['gesamt'] = gesamt
    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'sparen/uebersicht_sparkontos.html')

