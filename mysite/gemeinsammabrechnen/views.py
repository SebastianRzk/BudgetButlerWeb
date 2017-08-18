from django.shortcuts import render
from django.template.loader import render_to_string

from adddauerauftrag.views import handle_request
from viewcore import viewcore


def __init__(self):
    self.count = 0

def handle_request(request):
    ausgabe_sebastian = viewcore.database_instance().get_gemeinsame_ausgabe_fuer('Sebastian')
    ausgabe_maureen = viewcore.database_instance().get_gemeinsame_ausgabe_fuer('Maureen')
    ausgabe_sebastian = ausgabe_sebastian.Wert.sum()
    ausgabe_maureen = ausgabe_maureen.Wert.sum()
    ausgabe_gesamt = ausgabe_maureen + ausgabe_sebastian
    print("maureen", ausgabe_maureen)
    print('sebastian', ausgabe_sebastian)

    dif_sebastian = (ausgabe_gesamt / 2) - ausgabe_sebastian
    dif_maureen = (ausgabe_gesamt / 2) - ausgabe_maureen

    ergebnis = "No Ergebnis set"


    if dif_maureen > 0:
        ergebnis = "Maureen bekommt von Sebastian noch " + str("%.2f" % dif_maureen) + "€."

    if dif_sebastian > 0:
        ergebnis = "Sebastian bekommt von Maureen noch " + str("%.2f" % dif_sebastian) + "€."
    print("ergebnis:", ergebnis)

    context = viewcore.generate_base_context('gemeinsamabrechnen')

    context['ausgabe_maureen'] = "%.2f" % abs(ausgabe_maureen)
    context['ausgabe_sebastian'] = "%.2f" % abs(ausgabe_sebastian)
    context['ausgabe_gesamt'] = "%.2f" % abs(ausgabe_gesamt)
    context['ergebnis'] = ergebnis
    return context

def index(request):
    context = handle_request(request)
    rendered_content = render_to_string('theme/gemeinsamabrechnen.html', context)

    context['content'] = rendered_content

    return render(request, 'theme/index.html', context)


def abrechnen(request):
    print("Abrechnen")
    context = viewcore.generate_base_context('gemeinsamabrechnen')
    abrechnungs_text = viewcore.database_instance().abrechnen()
    context['abrechnungstext'] = abrechnungs_text.replace('\n', '<br>')
    rendered_content = render_to_string("theme/present_abrechnung.html", context, request)


    context['content'] = rendered_content

    viewcore.save_refresh()
    return render(request, 'theme/index.html', context)
