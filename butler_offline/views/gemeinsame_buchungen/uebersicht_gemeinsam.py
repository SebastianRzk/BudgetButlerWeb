from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import to_descriptive_list
from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen
from butler_offline.viewcore.context.builder import generate_transactional_page_context, generate_redirect_page_context
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import gemeinsame_buchung_needed_decorator


class UebersichtGemeinsamContext:
    def __init__(self, gemeinsamebuchungen: Gemeinsamebuchungen):
        self._gemeinsamebuchungen = gemeinsamebuchungen

    def gemeinsamebuchungen(self) -> Gemeinsamebuchungen:
        return self._gemeinsamebuchungen


@gemeinsame_buchung_needed_decorator()
def handle_request(request: Request, context: UebersichtGemeinsamContext):
    if request.post_action_is('delete'):
        context.gemeinsamebuchungen().delete(int(request.values['delete_index']))
        return generate_redirect_page_context('/gemeinsameuebersicht/')

    result_context = generate_transactional_page_context('gemeinsameuebersicht')
    result_context.add('ausgaben', to_descriptive_list(context.gemeinsamebuchungen().select().to_list()))

    return result_context


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='gemeinsame_buchungen/uebersicht_gemeinsam.html',
        context_creator=lambda db: UebersichtGemeinsamContext(
            gemeinsamebuchungen=db.gemeinsamebuchungen,
        )
    )