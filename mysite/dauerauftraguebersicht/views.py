
from django.shortcuts import render
from django.template.loader import render_to_string

from viewcore import viewcore


def __init__(self):
    self.count = 0

# Create your views here.
def index(request):

    context = handle_request(request)
    rendered_content = render_to_string('theme/dauerauftraguebersicht.html', context, request=request)

    context['content'] = rendered_content

    return render(request, 'theme/index.html', context)

def handle_request(request):
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
    return context

def _format_dauerauftrag_floatpoint(dauerauftraege):
    for dauerauftrag in dauerauftraege:
        dauerauftrag['Wert'] = '%.2f' % dauerauftrag['Wert']
    return dauerauftraege
