
import datetime

from django.shortcuts import render
from django.template.loader import render_to_string

from core.DatabaseModule import Database
from viewcore import viewcore


def handle_request():
    context = viewcore.generate_base_context('stechzeituebersicht')

    if not viewcore.database_instance().stechzeiten_vorhanden():
        return context

    soll_ist_uebersicht = viewcore.database_instance().get_soll_ist_uebersicht(2017)

    stechzeiten_label = []
    ist_werte = []
    soll_werte = []

    for woche, (ist, soll) in soll_ist_uebersicht.items():
        stechzeiten_label.append(woche)
        ist_werte.append("%.2f" % (ist.total_seconds() / (60 * 60)))
        soll_werte.append("%.2f" % (soll.total_seconds() / (60 * 60)))

    context["ist_data"] = ist_werte
    context['soll_data'] = soll_werte
    context["stechzeiten_label"] = stechzeiten_label

    stechzeiten_label_monatlich = []
    ist_werte_monatlich = []
    soll_werte_monatlich = []
    soll_ist_uebersicht_monatlich = viewcore.database_instance().get_soll_ist_uebersicht(2017, Database.func_monatlich)
    for monat, (ist, soll) in soll_ist_uebersicht_monatlich.items():
        stechzeiten_label_monatlich.append(datetime.date(1900, monat, 1).strftime('%B'))
        ist_werte_monatlich.append("%.2f" % (ist.total_seconds() / (60 * 60)))
        soll_werte_monatlich.append("%.2f" % (soll.total_seconds() / (60 * 60)))
    context["ist_data_monatlich"] = ist_werte_monatlich
    context['soll_data_monatlich'] = soll_werte_monatlich
    context["stechzeiten_label_monatlich"] = stechzeiten_label_monatlich



    stechzeiten = []

    for rowindex, row in viewcore.database_instance().stechzeiten.iterrows():
        stechzeiten.append([rowindex, row.Datum, row.Arbeitgeber, row.Einstechen, row.Ausstechen, row.Arbeitszeit])

    context['stechzeiten'] = stechzeiten
    return context

def index(request):
    context = handle_request()
    rendered_content = render_to_string('theme/stechzeituebersicht.html', context)
    context['content'] = rendered_content
    return render(request, 'theme/index.html', context)

