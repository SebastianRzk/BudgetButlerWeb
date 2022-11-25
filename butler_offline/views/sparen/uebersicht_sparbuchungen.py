from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore.context import generate_transactional_context, generate_redirect_context
from butler_offline.viewcore.converter import datum_to_german, from_double_to_german


def _handle_request(request):
    sparbuchungen = persisted_state.database_instance().sparbuchungen
    if post_action_is(request, 'delete'):
        sparbuchungen.delete(int(request.values['delete_index']))
        return generate_redirect_context('/uebersicht_sparbuchungen/')

    db = sparbuchungen.get_all()
    sparbuchungen_monatlich = {}
    datum_alt = None
    sparbuchungen_liste = []
    for row_index, row in db.iterrows():
        if not datum_alt:
            datum_alt = row.Datum
        if datum_alt.month != row.Datum.month or datum_alt.year != row.Datum.year:
            sparbuchungen_monatlich["" + str(datum_alt.year) + "." + str(datum_alt.month)] = sparbuchungen_liste
            sparbuchungen_liste = []
            datum_alt = row.Datum

        sparbuchungen_liste.append({
            'index': row_index,
            'datum': datum_to_german(row.Datum),
            'name': row.Name,
            'konto': row.Konto,
            'wert': from_double_to_german(row.Wert),
            'typ': row.Typ,
            'dynamisch': row.Dynamisch})

    if datum_alt:
        sparbuchungen_monatlich["" + str(datum_alt.year) + "." + str(datum_alt.month)] = sparbuchungen_liste

    context = generate_transactional_context('uebersicht_sparbuchungen')
    context['alles'] = sparbuchungen_monatlich
    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'sparen/uebersicht_sparbuchungen.html')

