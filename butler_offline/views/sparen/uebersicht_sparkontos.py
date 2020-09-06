from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.viewcore import post_action_is
from butler_offline.viewcore import viewcore


def _handle_request(request):
    sparkontos = persisted_state.database_instance().sparkontos
    if post_action_is(request, 'delete'):
        sparkontos.delete(int(request.values['delete_index']))
        return request_handler.create_redirect_context('/uebersicht_sparkontos/')

    db = sparkontos.get_all()
    sparkonto_liste = []
    for row_index, row in db.iterrows():
        sparkonto_liste.append({
            'index': row_index,
            'kontoname': row.Kontoname,
            'kontotyp': row.Kontotyp,
            'wert': 'noch nicht ermittelt'
        })


    context = viewcore.generate_transactional_context('uebersicht_sparkontos')
    context['sparkontos'] = sparkonto_liste
    return context


def index(request):
    return request_handler.handle_request(request, _handle_request, 'sparen/uebersicht_sparkontos.html')

