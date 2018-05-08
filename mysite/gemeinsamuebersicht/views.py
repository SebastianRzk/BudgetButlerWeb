from viewcore import viewcore
from viewcore.viewcore import post_action_is
from viewcore import request_handler


def _handle_request(request):
    if post_action_is(request, 'delete'):
        print("Delete: ", request.POST['delete_index'])
        viewcore.database_instance().gemeinsamebuchungen.delete(int(request.POST['delete_index']))

    ausgaben_liste = []
    data = viewcore.database_instance().gemeinsamebuchungen.content.sort_values(by='Datum')
    for row_index, row in data.iterrows():
        ausgaben_liste.append((row_index, row.Datum, row.Name, row.Kategorie, '%.2f' % row.Wert, row.Person))

    context = viewcore.generate_base_context('gemeinsameuebersicht')
    context['ausgaben'] = ausgaben_liste
    context['transaction_key'] = 'requested'
    return context


# Create your views here.
def index(request):
    return request_handler.handle_request(request, _handle_request, 'gemeinsameuebersicht.html')

