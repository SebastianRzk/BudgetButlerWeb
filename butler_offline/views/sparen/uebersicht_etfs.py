from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore import viewcore
from butler_offline.views.sparen.language import NO_VALID_ISIN_IN_DB

PAGE_NAME = 'uebersicht_etfs'

def _handle_request(request):
    if not persisted_state.database_instance().depotwerte.get_valid_isins():
        return viewcore.generate_error_context(PAGE_NAME, NO_VALID_ISIN_IN_DB)

    context = viewcore.generate_transactional_context(PAGE_NAME)


    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'sparen/uebersicht_sparen.html')

