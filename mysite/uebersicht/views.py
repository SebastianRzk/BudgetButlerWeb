
from django.shortcuts import render
from django.template.loader import render_to_string

from viewcore import viewcore

def handle_request(request):
    einzelbuchungen = viewcore.database_instance().einzelbuchungen
    if request.method == "POST":
        if "action" in request.POST:
            if request.POST['action'] == "delete":
                print("Delete: ", request.POST['delete_index'])
                einzelbuchungen.delete(int(request.POST['delete_index']))
                viewcore.save_refresh()

    db = einzelbuchungen.get_all()
    ausgaben_monatlich = {}
    datum_alt = None
    ausgaben_liste = []
    for row_index, row in db.iterrows():
        if datum_alt == None:
            datum_alt = row.Datum
        if datum_alt.month != row.Datum.month:
            ausgaben_monatlich["" + str(datum_alt.year) + "." + str(datum_alt.month)] = ausgaben_liste
            ausgaben_liste = []
            datum_alt = row.Datum

        link = "addeinnahme"
        if row.Wert < 0:
            link = "addeinzelbuchung"
        ausgaben_liste.append((row_index, row.Datum, row.Name, row.Kategorie, '%.2f' % row.Wert, row.Dynamisch, link))

    if datum_alt != None:
        ausgaben_monatlich["" + str(datum_alt.year) + "." + str(datum_alt.month)] = ausgaben_liste

    context = viewcore.generate_base_context('uebersicht')
    context['alles'] = ausgaben_monatlich
    return context

def index(request):

    context = handle_request(request)
    rendered_content = render_to_string('theme/uebersicht.html', context, request=request)

    context['content'] = rendered_content

    return render(request, 'theme/index.html', context)

