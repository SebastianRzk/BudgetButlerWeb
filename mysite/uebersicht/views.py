

from viewcore import request_handler
from viewcore.viewcore import post_action_is
from viewcore import viewcore

def _handle_request(request):
    einzelbuchungen = viewcore.database_instance().einzelbuchungen
    if post_action_is(request, 'delete'):
        print("Delete: ", request.POST['delete_index'])
        einzelbuchungen.delete(int(request.POST['delete_index']))

    db = einzelbuchungen.get_all()
    ausgaben_monatlich = {}
    datum_alt = None
    ausgaben_liste = []
    for row_index, row in db.iterrows():
        if datum_alt == None:
            datum_alt = row.Datum
        if datum_alt.month != row.Datum.month or datum_alt.year != row.Datum.year:
            ausgaben_monatlich["" + str(datum_alt.year) + "." + str(datum_alt.month)] = ausgaben_liste
            ausgaben_liste = []
            datum_alt = row.Datum

        link = "addeinnahme"
        if row.Wert < 0:
            link = "addeinzelbuchung"
        ausgaben_liste.append({
            'index':row_index,
            'datum':row.Datum,
            'name':row.Name,
            'kategorie':row.Kategorie,
            'wert':'%.2f' % row.Wert,
            'dynamisch':row.Dynamisch,
            'link':link,
            'tags':str(row.Tags)})

    if datum_alt != None:
        ausgaben_monatlich["" + str(datum_alt.year) + "." + str(datum_alt.month)] = ausgaben_liste

    context = viewcore.generate_base_context('uebersicht')
    context['alles'] = ausgaben_monatlich
    context['transaction_key'] = 'requested'
    return context

def index(request):
    return request_handler.handle_request(request, _handle_request, 'uebersicht.html')

