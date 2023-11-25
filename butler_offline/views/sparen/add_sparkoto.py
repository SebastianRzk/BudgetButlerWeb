from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_transactional_page_context
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.state import non_persisted_state
from butler_offline.viewcore.template import fa


class AddSparkontoContext:
    def __init__(self, kontos: Kontos):
        self._kontos = kontos

    def kontos(self) -> Kontos:
        return self._kontos


def handle_request(request: Request, context: AddSparkontoContext):
    result_context = generate_transactional_page_context('add_sparkonto')

    if request.post_action_is('add'):
        kontoname = request.values['kontoname']
        if '_' in kontoname:
            return result_context.throw_error('Kontoname darf kein Unterstrich "_" enthalten.')
        kontotyp = request.values['kontotyp']

        if "edit_index" in request.values:
            context.kontos().edit(int(request.values['edit_index']),
                                  kontoname=kontoname,
                                  kontotyp=kontotyp)
            non_persisted_state.add_changed_sparkontos(
                {
                    'fa': fa.pencil,
                    'Kontoname': kontoname,
                    'Kontotyp': kontotyp
                })

        else:
            context.kontos().add(
                kontoname=kontoname,
                kontotyp=kontotyp)
            non_persisted_state.add_changed_sparkontos(
                {
                    'fa': fa.plus,
                    'Kontoname': kontoname,
                    'Kontotyp': kontotyp
                })

    result_context.add('approve_title', 'Sparkonto hinzufügen')
    if request.post_action_is('edit'):
        print("Please edit:", request.values['edit_index'])
        db_index = int(request.values['edit_index'])
        db_row = context.kontos().get(db_index)

        default_item = {
            'edit_index': str(db_index),
            'kontotyp': db_row['Kontotyp'],
            'kontoname': db_row['Kontoname']
        }

        result_context.add('default_item', default_item)
        result_context.add('bearbeitungsmodus', True)
        result_context.add('edit_index', db_index)
        result_context.add('approve_title', 'Sparkonto aktualisieren')

    if not result_context.contains('default_item'):
        result_context.add('default_item',
                           {
                               'kontoname': '',
                               'kontotyp': ''
                           })
        result_context.add('kontotypen', context.kontos().KONTO_TYPEN)
        result_context.add('letzte_erfassung', reversed(non_persisted_state.get_changed_sparkontos()))
    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='sparen/add_sparkonto.html',
        context_creator=lambda db: AddSparkontoContext(
            kontos=db.sparkontos,
        )
    )
