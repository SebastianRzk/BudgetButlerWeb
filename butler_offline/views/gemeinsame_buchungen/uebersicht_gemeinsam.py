from butler_offline.viewcore.state.persisted_state import database_instance
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import to_descriptive_list
from butler_offline.viewcore.context import generate_transactional_context, generate_redirect_context

def _handle_request(request):
    if post_action_is(request, 'delete'):
        database_instance().gemeinsamebuchungen.delete(int(request.values['delete_index']))
        return generate_redirect_context('/gemeinsameuebersicht/')

    context = generate_transactional_context('gemeinsameuebersicht')
    context['ausgaben'] = to_descriptive_list(
        database_instance().gemeinsamebuchungen.select().to_list())

    return context


# Create your views here.
def index(request):
    return request_handler.handle_request(request, _handle_request, 'gemeinsame_buchungen/uebersicht_gemeinsam.html')

