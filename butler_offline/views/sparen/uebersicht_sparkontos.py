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

        kontoname = row.Kontoname
        kontotyp = row.Kontotyp

        if kontotyp == sparkontos.TYP_SPARKONTO:
            aktueller_kontostand = persisted_state.database_instance().sparbuchungen.get_kontostand_fuer(kontoname)
            aufbuchungen = persisted_state.database_instance().sparbuchungen.get_aufbuchungen_fuer(kontoname)

        if kontotyp == sparkontos.TYP_DEPOT:
            aufbuchungen = persisted_state.database_instance().order.get_order_fuer(kontoname)
            aktueller_kontostand = persisted_state.database_instance().depotauszuege.get_kontostand_by(kontoname)

        gesamt_kontostand += aktueller_kontostand
        gesamt_aufbuchungen += aufbuchungen

        diff = aktueller_kontostand - aufbuchungen

        sparkonto_liste.append({
            'index': row_index,
            'kontoname': kontoname,
            'kontotyp': kontotyp,
            'wert': from_double_to_german(aktueller_kontostand),
            'difference': from_double_to_german(diff),
            'aufbuchungen': from_double_to_german(aufbuchungen),
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

