from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.core.database.sparen.order import Order
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_transactional_page_context, generate_redirect_page_context
from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import depotwerte_needed_decorator


class UebersichtDepotwerteContext:
    def __init__(self, depotwerte: Depotwerte, order: Order, depotauszuege: Depotauszuege):
        self._depotwerte = depotwerte
        self._order = order
        self._depotauszuege = depotauszuege

    def depotwerte(self) -> Depotwerte:
        return self._depotwerte

    def order(self) -> Order:
        return self._order

    def depotauszuege(self) -> Depotauszuege:
        return self._depotauszuege


@depotwerte_needed_decorator()
def handle_request(request: Request, context: UebersichtDepotwerteContext):
    result_context = generate_transactional_page_context('uebersicht_depotwerte')
    depotwerte = context.depotwerte()
    order = context.order()
    depotauszuege = context.depotauszuege()

    if request.post_action_is('delete'):
        depotwerte.delete(int(request.values['delete_index']))
        return generate_redirect_page_context('/uebersicht_depotwerte/')

    db = depotwerte.get_all()
    depotwerte_liste = []
    gesamt_buchungen = 0
    gesamt_wert = 0

    for row_index, row in db.iterrows():
        isin = row.ISIN
        buchungen = order.get_order_fuer_depotwert(isin)
        wert = depotauszuege.get_depotwert_by(isin)
        differenz = wert - buchungen
        typ = row.Typ

        depotwerte_liste.append({
            'index': row_index,
            'name': row.Name,
            'isin': isin,
            'typ': typ,
            'buchung': Betrag(buchungen),
            'difference': Betrag(differenz),
            'difference_is_negativ': differenz < 0,
            'wert': Betrag(wert)
        })
        gesamt_buchungen += buchungen
        gesamt_wert += wert

    gesamt_difference = gesamt_wert - gesamt_buchungen
    gesamt = {
        'wert': Betrag(gesamt_wert),
        'difference': Betrag(gesamt_difference),
        'difference_is_negativ': gesamt_difference < 0,
        'buchung': Betrag(gesamt_buchungen)
    }

    result_context.add('depotwerte', depotwerte_liste)
    result_context.add('gesamt', gesamt)
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='sparen/uebersicht_depotwerte.html',
        context_creator=lambda db: UebersichtDepotwerteContext(
            depotwerte=db.depotwerte,
            depotauszuege=db.depotauszuege,
            order=db.order
        )
    )
