from butler_offline.viewcore import request_handler
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.viewcore.context.builder import generate_redirect_page_context, generate_transactional_page_context
from butler_offline.viewcore.converter import datum_to_german
from butler_offline.core.database.sparen.sparbuchungen import Sparbuchungen
from butler_offline.viewcore.requirements import sparbuchungen_needed_decorator


class UebersichtSparbuchungenContext:
    def __init__(self, sparbuchungen: Sparbuchungen):
        self._sparbuchungen = sparbuchungen

    def sparbuchungen(self) -> Sparbuchungen:
        return self._sparbuchungen


@sparbuchungen_needed_decorator()
def handle_request(request: Request, context: UebersichtSparbuchungenContext):
    sparbuchungen = context.sparbuchungen()
    if request.post_action_is('delete'):
        sparbuchungen.delete(int(request.values['delete_index']))
        return generate_redirect_page_context('/uebersicht_sparbuchungen/')

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
            'wert': Betrag(row.Wert),
            'typ': row.Typ,
            'dynamisch': row.Dynamisch})

    if datum_alt:
        sparbuchungen_monatlich["" + str(datum_alt.year) + "." + str(datum_alt.month)] = sparbuchungen_liste

    result_context = generate_transactional_page_context('uebersicht_sparbuchungen')
    result_context.add('alles', sparbuchungen_monatlich)
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='sparen/uebersicht_sparbuchungen.html',
        context_creator=lambda db: UebersichtSparbuchungenContext(
            sparbuchungen=db.sparbuchungen
        )
    )
