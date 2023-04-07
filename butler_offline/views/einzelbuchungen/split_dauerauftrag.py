from butler_offline.core.database import Dauerauftraege
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore.context import generate_transactional_context, generate_redirect_context
from butler_offline.views.einzelbuchungen.dauerauftrag.split import split_dauerauftrag, get_ausführungszeitpunkte
from butler_offline.viewcore.converter import datum_to_string, datum_to_german, dezimal_float, datum


class SplitDauerauftraegeContext:
    def __init__(self,
                 dauerauftraege: Dauerauftraege):
        self._dauerauftraege = dauerauftraege

    def dauerauftraege(self) -> Dauerauftraege:
        return self._dauerauftraege


def handle_request(request, context: SplitDauerauftraegeContext):
    dauerauftrag_id: int = int(request.values['dauerauftrag_id'])

    if post_action_is(request, 'preset_values'):

        result_context = generate_transactional_context('adddauerauftrag')

        preset_datum = get_ausführungszeitpunkte(dauerauftraege=context.dauerauftraege(),
                                                 dauerauftrag_id=dauerauftrag_id)
        preset_datum_formatted = []

        if len(preset_datum) <= 2:
            raise ValueError('Can not be edited')

        for i in range(0, len(preset_datum)):
            can_be_chosen = True
            current_date = preset_datum[i]
            if i == 0:
                can_be_chosen = False
            preset_datum_formatted.append({
                'datum': datum_to_string(current_date),
                'datum_german': datum_to_german(current_date),
                'can_be_chosen': can_be_chosen
            })

        result_context['datum'] = preset_datum_formatted
        result_context['wert'] = context.dauerauftraege().get(dauerauftrag_id)['Wert']
        result_context['dauerauftrag_id'] = dauerauftrag_id
        return result_context

    if post_action_is(request, 'split'):
        wert = dezimal_float(request.values['wert'])
        aenderungsdatum = datum(request.values['datum'])
        split_dauerauftrag(
            dauerauftraege=context.dauerauftraege(),
            dauerauftrag_id=dauerauftrag_id,
            split_date=aenderungsdatum,
            wert=wert)
        return generate_redirect_context('/adddauerauftrag')

    raise FileNotFoundError('post action unknown')


def index(request):
    def handle_request_migration(r):
        return handle_request(r, SplitDauerauftraegeContext(
            dauerauftraege=persisted_state.database_instance().dauerauftraege
        ))

    return request_handler.handle_request(request, handle_request_migration, 'einzelbuchungen/split_dauerauftrag.html')
