from butler_offline.viewcore import request_handler
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.context.builder import generate_transactional_page_context
from butler_offline.viewcore.template import fa
from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.viewcore.http import Request


class AddDepotwertContext:
    def __init__(self, depotwerte: Depotwerte):
        self._depotwerte = depotwerte

    def depotwerte(self) -> Depotwerte:
        return self._depotwerte


def handle_request(request: Request, context: AddDepotwertContext):
    result_context = generate_transactional_page_context('add_depotwert')

    if request.post_action_is('add'):
        isin = request.values['isin']
        if '_' in isin:
            return result_context.throw_error('ISIN darf kein Unterstrich "_" enthalten.')
        name = request.values['name']
        typ = request.values['typ']

        if "edit_index" in request.values:
            context.depotwerte().edit(int(request.values['edit_index']),
                                      name=name,
                                      isin=isin,
                                      typ=typ)
            non_persisted_state.add_changed_depotwerte(
                {
                    'fa': fa.pencil,
                    'Name': name,
                    'Isin': isin,
                    'Typ': typ
                })
        else:
            context.depotwerte().add(
                name=name,
                isin=isin,
                typ=typ)
            non_persisted_state.add_changed_depotwerte(
                {
                    'fa': fa.plus,
                    'Name': name,
                    'Isin': isin,
                    'Typ': typ
                })

    result_context.add('approve_title', 'Depotwert hinzufügen')

    if request.post_action_is('edit'):
        db_index = int(request.values['edit_index'])
        db_row = context.depotwerte().get(db_index)

        default_item = {
            'edit_index': str(db_index),
            'name': db_row['Name'],
            'isin': db_row['ISIN'],
            'typ': db_row['Typ']
        }

        result_context.add('default_item', default_item)
        result_context.add('bearbeitungsmodus', True)
        result_context.add('edit_index', db_index)
        result_context.add('approve_title', 'Depotwert aktualisieren')

    if not result_context.contains('default_item'):
        result_context.add('default_item', {
            'name': '',
            'isin': '',
            'typ': context.depotwerte().TYP_ETF
        })

    result_context.add('letzte_erfassung', reversed(non_persisted_state.get_changed_depotwerte()))
    result_context.add('types', context.depotwerte().TYPES)
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='sparen/add_depotwert.html',
        context_creator=lambda db: AddDepotwertContext(
            depotwerte=db.depotwerte
        )
    )
