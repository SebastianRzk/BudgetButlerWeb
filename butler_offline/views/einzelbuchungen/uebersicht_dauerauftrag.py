from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_to_german
import collections
from butler_offline.viewcore.context.builder import PageContext, \
    generate_transactional_page_context, generate_redirect_page_context
import logging
from butler_offline.core.database.dauerauftraege import Dauerauftraege
from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.requirements import dauerauftrag_needed_decorator


class UbersichtDauerauftragContext:
    def __init__(self, dauerauftraege: Dauerauftraege):
        self._dauerauftraege = dauerauftraege

    def dauerauftraege(self) -> Dauerauftraege:
        return self._dauerauftraege


@dauerauftrag_needed_decorator()
def handle_request(request: Request, context: UbersichtDauerauftragContext) -> PageContext:

    if request.post_action_is('delete'):
        context.dauerauftraege().delete(int(request.values['delete_index']))
        return generate_redirect_page_context('/dauerauftraguebersicht/')

    page_context = generate_transactional_page_context('dauerauftraguebersicht')
    data = collections.OrderedDict()
    data['Aktuelle Daueraufträge'] = _format_dauerauftrag_floatpoint(context.dauerauftraege().aktuelle())
    data['Zukünftige Daueraufträge'] = _format_dauerauftrag_floatpoint(context.dauerauftraege().future())
    data['Vergangene  Daueraufträge'] = _format_dauerauftrag_floatpoint(context.dauerauftraege().past())
    page_context.add('dauerauftraege', data)
    return page_context


def _format_dauerauftrag_floatpoint(dauerauftraege):
    for dauerauftrag in dauerauftraege:
        dauerauftrag['Wert'] = Betrag(dauerauftrag['Wert'])
        dauerauftrag['Startdatum'] = datum_to_german(dauerauftrag['Startdatum'])
        dauerauftrag['Endedatum'] = datum_to_german(dauerauftrag['Endedatum'])
    return dauerauftraege


def index(request):
    return request_handler.handle(
        request=request,
        handle_function=handle_request,
        html_base_page='einzelbuchungen/uebersicht_dauerauftrag.html',
        context_creator=lambda db: UbersichtDauerauftragContext(db.dauerauftraege)
    )
