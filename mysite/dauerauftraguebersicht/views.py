
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
    if request.method == "POST":
        if "action" in request.POST:
            if request.POST['action'] == "delete":
                print("Delete: ", request.POST['delete_index'])
                viewcore.database_instance().delete_dauerauftrag(int(request.POST['delete_index']))
                viewcore.save_refresh()

    context = viewcore.generate_base_context('dauerauftraguebersicht')
    context['aktuelle_dauerauftraege'] = viewcore.database_instance().aktuelle_dauerauftraege()
    context['vergangene_dauerauftraege'] = viewcore.database_instance().past_dauerauftraege()
    context['zukuenftige_dauerauftraege'] = viewcore.database_instance().future_dauerauftraege()
    return context