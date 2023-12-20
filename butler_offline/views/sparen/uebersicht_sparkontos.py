from butler_offline.viewcore import request_handler
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.viewcore.context.builder import generate_redirect_page_context, generate_transactional_page_context
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.core.database.sparen.sparbuchungen import Sparbuchungen
from butler_offline.core.database.sparen.order import Order
from butler_offline.viewcore.requirements import sparkontos_needed_decorator


class UebersichtSparkontosContext:
    def __init__(self, kontos: Kontos, depotauszuege: Depotauszuege, sparbuchungen: Sparbuchungen, order: Order):
        self._kontos = kontos
        self._depotauszuege = depotauszuege
        self._sparbuchungen = sparbuchungen
        self._order = order

    def kontos(self) -> Kontos:
        return self._kontos

    def depotauszuege(self) -> Depotauszuege:
        return self._depotauszuege

    def sparbuchungen(self) -> Sparbuchungen:
        return self._sparbuchungen

    def order(self) -> Order:
        return self._order


@sparkontos_needed_decorator()
def handle_request(request: Request, context: UebersichtSparkontosContext):
    sparkontos = context.kontos()
    if request.post_action_is('delete'):
        sparkontos.delete(int(request.values['delete_index']))
        return generate_redirect_page_context('/uebersicht_sparkontos/')

    db = sparkontos.get_all()

    gesamt_kontostand = 0
    gesamt_aufbuchungen = 0
    sparkonto_liste = []

    for row_index, row in db.iterrows():
        aktueller_kontostand = 0
        aufbuchungen = 0

        kontoname = row.Kontoname
        kontotyp = row.Kontotyp

        if kontotyp == sparkontos.TYP_SPARKONTO or kontotyp == sparkontos.TYP_GENOSSENSCHAFTSANTEILE:
            aktueller_kontostand = context.sparbuchungen().get_kontostand_fuer(kontoname)
            aufbuchungen = context.sparbuchungen().get_aufbuchungen_fuer(kontoname)

        if kontotyp == sparkontos.TYP_DEPOT:
            aufbuchungen = context.order().get_order_fuer(kontoname)
            aktueller_kontostand = context.depotauszuege().get_kontostand_by(kontoname)

        gesamt_kontostand += aktueller_kontostand
        gesamt_aufbuchungen += aufbuchungen

        diff = aktueller_kontostand - aufbuchungen

        sparkonto_liste.append({
            'index': row_index,
            'kontoname': kontoname,
            'kontotyp': kontotyp,
            'wert': Betrag(aktueller_kontostand),
            'difference': Betrag(diff),
            'aufbuchungen': Betrag(aufbuchungen),
            'difference_is_negativ': diff < 0
        })

    gesamt_diff = gesamt_kontostand - gesamt_aufbuchungen

    gesamt = {
        'wert': Betrag(gesamt_kontostand),
        'difference': Betrag(gesamt_diff),
        'aufbuchungen': Betrag(gesamt_aufbuchungen),
        'difference_is_negativ': gesamt_diff < 0
    }

    result_context = generate_transactional_page_context('uebersicht_sparkontos')
    result_context.add('sparkontos', sparkonto_liste)
    result_context.add('gesamt', gesamt)
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        context_creator=lambda db: UebersichtSparkontosContext(
            order=db.order,
            sparbuchungen=db.sparbuchungen,
            depotauszuege=db.depotauszuege,
            kontos=db.sparkontos,
        ),
        html_base_page='sparen/uebersicht_sparkontos.html'
    )
