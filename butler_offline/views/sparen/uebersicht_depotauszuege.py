from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_redirect_page_context, generate_transactional_page_context
from butler_offline.viewcore.converter import datum_to_german
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import depotauszug_needed_decorator


class UebersichtDepotauszuegeContext:
    def __init__(self, depotauszuege: Depotauszuege(), depotwerte: Depotwerte):
        self._depotauszuege = depotauszuege
        self._depotwerte = depotwerte

    def depotauszuege(self) -> Depotauszuege:
        return self._depotauszuege

    def depotwerte(self) -> Depotwerte:
        return self._depotwerte


@depotauszug_needed_decorator()
def handle_request(request: Request, context: UebersichtDepotauszuegeContext):

    if request.post_action_is('delete'):
        delete_index = int(request.values['delete_index'])
        delete_konto = context.depotauszuege().resolve_konto(delete_index)
        delete_datum = context.depotauszuege().resolve_datum(delete_index)
        context.depotauszuege().delete_depotauszug(delete_datum, delete_konto)
        return generate_redirect_page_context('/uebersicht_depotauszuege/')

    db = context.depotauszuege().get_all()

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
        if index_alt is None:
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
            'depotwert': context.depotwerte().get_description_for(row.Depotwert),
            'wert': row.Wert})

    if index_alt:
        gesamt.append({
                'name': '{} vom {}'.format(konto_alt, datum_to_german(datum_alt)),
                'index': index_alt,
                'buchungen': buchungen
            })

    result_context = generate_transactional_page_context('uebersicht_depotauszuege')
    result_context.add('gesamt', gesamt)
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='sparen/uebersicht_depotauszuege.html',
        context_creator=lambda db: UebersichtDepotauszuegeContext(
            depotwerte=db.depotwerte,
            depotauszuege=db.depotauszuege
        )
    )
