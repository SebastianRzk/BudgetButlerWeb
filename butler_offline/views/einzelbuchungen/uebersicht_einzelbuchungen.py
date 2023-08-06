from butler_offline.viewcore import request_handler
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore.converter import datum_to_german, from_double_to_german
from butler_offline.viewcore.context.builder import generate_transactional_page_context, generate_redirect_page_context
from butler_offline.core.time import today
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen


class UebersichtEinzelbuchungenContext:
    def __init__(self, einzelbuchungen: Einzelbuchungen):
        self._einzelbuchungen = einzelbuchungen

    def einzelbuchungen(self) -> Einzelbuchungen:
        return self._einzelbuchungen


def handle_request(request, context: UebersichtEinzelbuchungenContext):
    year = today().year
    years = sorted(context.einzelbuchungen().get_jahre(), reverse=True)
    if years:
        year = years[0]

    if request.method == 'POST' and 'date' in request.values:
        year = int(float(request.values['date']))
    einzelbuchungen_filtered = context.einzelbuchungen().select().select_year(year).get_all_raw()

    if post_action_is(request, 'delete'):
        context.einzelbuchungen().delete(int(request.values['delete_index']))
        return generate_redirect_page_context('/uebersicht/')

    ausgaben_monatlich = {}
    datum_alt = None
    ausgaben_liste = []
    for row_index, row in einzelbuchungen_filtered.iterrows():
        if not datum_alt:
            datum_alt = row.Datum
        if datum_alt.month != row.Datum.month or datum_alt.year != row.Datum.year:
            ausgaben_monatlich["" + str(datum_alt.year) + "." + str(datum_alt.month)] = ausgaben_liste
            ausgaben_liste = []
            datum_alt = row.Datum

        link = 'addeinnahme'
        if row.Wert < 0:
            link = 'addausgabe'
        ausgaben_liste.append({
            'index': row_index,
            'datum': datum_to_german(row.Datum),
            'name': row.Name,
            'kategorie': row.Kategorie,
            'wert': from_double_to_german(row.Wert),
            'dynamisch': row.Dynamisch,
            'link': link,
            'tags': str(row.Tags)})

    if datum_alt:
        ausgaben_monatlich["" + str(datum_alt.year) + "." + str(datum_alt.month)] = ausgaben_liste

    result_context = generate_transactional_page_context('uebersicht')
    result_context.add('alles', ausgaben_monatlich)
    result_context.add('jahre', years)
    result_context.add('selected_date', year)
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='einzelbuchungen/uebersicht.html',
        context_creator=lambda db: UebersichtEinzelbuchungenContext(db.einzelbuchungen)
    )
