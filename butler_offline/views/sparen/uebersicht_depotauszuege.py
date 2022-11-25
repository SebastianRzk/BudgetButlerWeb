from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore.converter import datum_to_german
from butler_offline.viewcore.context import generate_transactional_context, generate_redirect_context

def _handle_request(request):
    depotauszuege = persisted_state.database_instance().depotauszuege

    if post_action_is(request, 'delete'):
        delete_index = int(request.values['delete_index'])
        delete_konto = depotauszuege.resolve_konto(delete_index)
        delete_datum = depotauszuege.resolve_datum(delete_index)
        depotauszuege.delete_depotauszug(delete_datum, delete_konto)
        return generate_redirect_context('/uebersicht_depotauszuege/')

    depotwerte = persisted_state.database_instance().depotwerte
    db = depotauszuege.get_all()

    gesamt = []
    datum_alt = None
    konto_alt = None
    index_alt = None
    buchungen = []

    for row_index, row in db.iterrows():
        if not datum_alt:
            datum_alt = row.Datum
        if not konto_alt:
            konto_alt = row.Konto
        if index_alt == None:
            index_alt = row_index

        if datum_alt != row.Datum or konto_alt != row.Konto:
            gesamt.append({
                'name': '{} vom {}'.format(konto_alt, datum_to_german(datum_alt)),
                'index': index_alt,
                'buchungen': buchungen
            })

            buchungen = []
            datum_alt = row.Datum
            konto_alt = row.Konto
            index_alt = row_index

        buchungen.append({
            'depotwert': depotwerte.get_description_for(row.Depotwert),
            'wert': row.Wert})

    if index_alt:
        gesamt.append({
                'name': '{} vom {}'.format(konto_alt, datum_to_german(datum_alt)),
                'index': index_alt,
                'buchungen': buchungen
            })

    context = generate_transactional_context('uebersicht_depotauszuege')
    context['gesamt'] = gesamt
    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'sparen/uebersicht_depotauszuege.html')

