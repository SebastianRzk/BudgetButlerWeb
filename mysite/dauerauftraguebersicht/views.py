
from viewcore import viewcore
from viewcore import request_handler

def _handle_request(request):
    dauerauftraege = viewcore.database_instance().dauerauftraege
    if request.method == "POST":
        if "action" in request.POST:
            if request.POST['action'] == "delete":
                print("Delete: ", request.POST['delete_index'])
                dauerauftraege.delete(int(request.POST['delete_index']))
                viewcore.save_refresh()

    context = viewcore.generate_base_context('dauerauftraguebersicht')
    aktuelle_dauerauftraege = dauerauftraege.aktuelle()
    context['aktuelle_dauerauftraege'] = _format_dauerauftrag_floatpoint(aktuelle_dauerauftraege)
    vergangene_dauerauftraege = dauerauftraege.past()
    context['vergangene_dauerauftraege'] = _format_dauerauftrag_floatpoint(vergangene_dauerauftraege)
    zukuenftige_dauerauftraege = dauerauftraege.future()
    context['zukuenftige_dauerauftraege'] = _format_dauerauftrag_floatpoint(zukuenftige_dauerauftraege)
    context['transaction_key'] = 'requested'
    return context

def _format_dauerauftrag_floatpoint(dauerauftraege):
    for dauerauftrag in dauerauftraege:
        dauerauftrag['Wert'] = '%.2f' % dauerauftrag['Wert']
    return dauerauftraege

def index(request):
    return request_handler.handle_request(request, _handle_request, 'dauerauftraguebersicht.html')
