from requests.cookies import cookiejar_from_dict

from butler_offline.online_services.butler_online.session import OnlineAuth
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.context.builder import generate_page_context
from butler_offline.viewcore.state import non_persisted_state


class ErrorContext:
    pass


def handle_request_error(_, __):
    context = generate_page_context('dashboard')
    return context.throw_error('Es konnte kein Import-/Export Befehl ermittelt werden')


def index(request):
    authenticated_function = non_persisted_state.CONTEXT.butler_online_function
    if not authenticated_function:
        return request_handler.handle(
            request=request,
            handle_function=handle_request_error,
            context_creator=lambda db: ErrorContext(),
            html_base_page='core/error.html'
        )
    online_name = request.values['user']
    session = request.values['session'].split("=")
    cookie = {session[0]: session[1]}

    auth_container = OnlineAuth(online_name=online_name, cookies=cookiejar_from_dict(cookie))
    context = authenticated_function(auth_container)
    non_persisted_state.CONTEXT.butler_online_function = None
    return request_handler.handle_for_context_created(request=request, context=context,
                                                      html_base_page='shared/import.html',
                                                      overwrite_taint_mode=True)
