from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.core.database.sparen.orderdauerauftrag import OrderDauerauftrag
from butler_offline.core.frequency import ALL_FREQUENCY_NAMES
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_transactional_page_context
from butler_offline.viewcore.converter import from_double_to_german, datum, datum_to_string, datum_to_german
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.template import fa
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import depots_needed_decorator, depotwerte_needed_decorator


TYP = 'typ'
TYPEN = 'typen'
TYP_KAUF = 'Kauf'
TYP_VERKAUF = 'Verkauf'


class AddOrderDauerauftragContext:
    def __init__(self, depotwerte: Depotwerte, order_dauerauftrag: OrderDauerauftrag, kontos: Kontos):
        self._depotwerte = depotwerte
        self._order_dauerauftrag = order_dauerauftrag
        self._kontos = kontos

    def depotwerte(self) -> Depotwerte:
        return self._depotwerte

    def order_dauerauftrag(self) -> OrderDauerauftrag:
        return self._order_dauerauftrag

    def kontos(self) -> Kontos:
        return self._kontos


@depots_needed_decorator()
@depotwerte_needed_decorator()
def handle_request(request: Request, context: AddOrderDauerauftragContext):
    result_context = generate_transactional_page_context('add_orderdauerauftrag')

    if request.post_action_is('add'):
        startdatum = datum(request.values['startdatum'])
        endedatum = datum(request.values['endedatum'])
        value = request.values['wert'].replace(",", ".")
        value = float(value)

        if request.values[TYP] == TYP_VERKAUF:
            value = value * -1

        if "edit_index" in request.values:
            context.order_dauerauftrag().edit(
                int(request.values['edit_index']),
                startdatum=startdatum,
                endedatum=endedatum,
                rhythmus=request.values['rhythmus'],
                name=request.values['name'],
                wert=value,
                depotwert=request.values['depotwert'],
                konto=request.values['konto'])
            non_persisted_state.add_changed_orderdauerauftrag(
                {
                    'fa': fa.pencil,
                    'startdatum': datum_to_german(startdatum),
                    'endedatum': datum_to_german(endedatum),
                    'rhythmus': request.values['rhythmus'],
                    'wert': from_double_to_german(abs(value)),
                    'name': request.values['name'],
                    TYP: request.values[TYP],
                    'depotwert': request.values['depotwert'],
                    'konto': request.values['konto']
                })

        else:
            context.order_dauerauftrag().add(
                startdatum=startdatum,
                endedatum=endedatum,
                rhythmus=request.values['rhythmus'],
                name=request.values['name'],
                wert=value,
                depotwert=request.values['depotwert'],
                konto=request.values['konto'])
            non_persisted_state.add_changed_orderdauerauftrag(
                {
                    'fa': fa.plus,
                    'startdatum': datum_to_german(startdatum),
                    'endedatum': datum_to_german(endedatum),
                    'rhythmus': request.values['rhythmus'],
                    'wert': from_double_to_german(value),
                    'name': request.values['name'],
                    TYP: request.values[TYP],
                    'value': '%.2f' % abs(value),
                    'depotwert': request.values['depotwert'],
                    'konto': request.values['konto']
                })

    result_context.add('approve_title', 'Order-Dauerauftrag hinzufügen')
    if request.post_action_is('edit'):
        print("Please edit:", request.values['edit_index'])
        db_index = int(request.values['edit_index'])
        db_row = context.order_dauerauftrag().get(db_index)

        if db_row['Wert'] > 0:
            typ = TYP_KAUF
        else:
            typ = TYP_VERKAUF

        default_item = {
            'edit_index': str(db_index),
            'startdatum': datum_to_string(db_row['Startdatum']),
            'endedatum': datum_to_string(db_row['Endedatum']),
            'rhythmus': db_row['Rhythmus'],
            'name': db_row['Name'],
            'wert': from_double_to_german(abs(db_row['Wert'])),
            'depotwert': db_row['Depotwert'],
            'typ': typ,
            'konto': db_row['Konto']
        }

        result_context.add('default_item', default_item)
        result_context.add('bearbeitungsmodus', True)
        result_context.add('edit_index', db_index)
        result_context.add('approve_title', 'Order-Dauerauftrag aktualisieren')

    if not result_context.contains('default_item'):
        result_context.add('default_item', {
            'name': '',
            'wert': '',
            'startdatum': '',
            'endedatum': '',
            'rhythmus': 'monatlich',
            'depotwert': '',
            'konto': ''
        })

    result_context.add('kontos', context.kontos().get_depots())
    result_context.add(TYPEN, [TYP_KAUF, TYP_VERKAUF])
    result_context.add('rhythmen', ALL_FREQUENCY_NAMES)
    result_context.add('depotwerte', context.depotwerte().get_depotwerte_descriptions())
    result_context.add('letzte_erfassung', reversed(non_persisted_state.get_changed_orderdauerauftrag()))
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='sparen/add_orderdauerauftrag.html',
        context_creator=lambda db: AddOrderDauerauftragContext(
            depotwerte=db.depotwerte,
            order_dauerauftrag=db.orderdauerauftrag,
            kontos=db.sparkontos,
        )
    )
