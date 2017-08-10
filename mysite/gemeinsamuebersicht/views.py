'''
View für Page Gemeinsame Ausgaben Übersicht

'''

from django.shortcuts import render
from django.template.loader import render_to_string

from viewcore import viewcore


def __init__(self):
    self.count = 0

# Create your views here.
def index(request):
    '''
    Show gemeinsame Ausgaben Übersicht
    '''
    if request.method == "POST":
        if "action" in request.POST:
            if request.POST['action'] == "delete":
                print("Delete: ", request.POST['delete_index'])
                viewcore.database_instance().delete_gemeinsame_buchung(int(request.POST['delete_index']))
                viewcore.save_refresh()



    ausgaben_liste = []
    data = viewcore.database_instance().gemeinsame_buchungen.sort_values(by='Datum')
    for row_index, row in data.iterrows():
        ausgaben_liste.append((row_index, row.Datum, row.Name, row.Kategorie, row.Wert, row.Person))

    context = viewcore.generate_base_context('gemeinsameuebersicht')
    context['ausgaben'] = ausgaben_liste

    rendered_content = render_to_string('theme/gemeinsameuebersicht.html', context, request=request)

    context['content'] = rendered_content

    return render(request, 'theme/index.html', context)

