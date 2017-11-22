from django.shortcuts import render
from django.template.loader import render_to_string

from adddauerauftrag.views import handle_request
from viewcore import viewcore
from mysite.viewcore.viewcore import name_of_partner

def handle_request(request):
    name_self = viewcore.database_instance().name
    name_partner = viewcore.name_of_partner()

    ausgabe_sebastian = viewcore.database_instance().gemeinsamebuchungen.fuer(name_self)
    ausgabe_maureen = viewcore.database_instance().gemeinsamebuchungen.fuer(name_partner)
    ausgabe_sebastian = _sum(ausgabe_sebastian.Wert)
    ausgabe_maureen = _sum(ausgabe_maureen.Wert)
    ausgabe_gesamt = ausgabe_maureen + ausgabe_sebastian
    print(viewcore.name_of_partner(), ausgabe_maureen)
    print(viewcore.database_instance().name, ausgabe_sebastian)

    dif_sebastian = (ausgabe_gesamt / 2) - ausgabe_sebastian
    dif_maureen = (ausgabe_gesamt / 2) - ausgabe_maureen

    ergebnis = 'Die gemeinsamen Ausgaben sind ausgeglichen.'

    if dif_maureen > 0:
        ergebnis = name_partner + ' bekommt von ' + name_self + ' noch ' + str('%.2f' % dif_maureen) + '€.'

    if dif_sebastian > 0:
        ergebnis = name_self + ' bekommt von ' + name_partner + ' noch ' + str('%.2f' % dif_sebastian) + '€.'
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

def _sum(data):
    if data.empty:
        return 0
    return data.sum()

def abrechnen(request):
    context = handle_abrechnen_request(request)
    rendered_content = render_to_string("theme/present_abrechnung.html", context, request)
    context['content'] = rendered_content
    return render(request, 'theme/index.html', context)


def handle_abrechnen_request(request):
    print("Abrechnen")
    context = viewcore.generate_base_context('gemeinsamabrechnen')
    abrechnungs_text = viewcore.database_instance().abrechnen()
    context['abrechnungstext'] = abrechnungs_text.replace('\n', '<br>')
    viewcore.save_refresh()

    return context
