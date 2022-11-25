from butler_offline.viewcore.state import persisted_state
from butler_offline.core.file_system import write_abrechnung
from butler_offline.core.time import time
from butler_offline.core.export.string_writer import StringWriter
from butler_offline.core.export.text_report import TextReportWriter
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.converter import datum_to_german
import pandas as pd
from pandas import DataFrame


def abrechnen(database,
              mindate,
              maxdate,
              set_ergebnis=None,
              verhaeltnis=50,
              set_self_kategorie=None,
              set_other_kategorie=None):
    selector = database.gemeinsamebuchungen.select().select_range(mindate, maxdate)

    name_self = persisted_state.database_instance().name
    name_partner = viewcore.name_of_partner()
    gemeinsame_buchungen_content = selector.content

    select_partner = selector.fuer(name_partner)
    select_self = selector.fuer(name_self)
    summe_partner = select_partner.sum()
    summe_self = select_self.sum()

    ausgaben_gesamt = selector.sum()

    abrechnunsdatei = StringWriter()
    zeitraum = datum_to_german(mindate) + '-' + datum_to_german(maxdate)
    abrechnunsdatei.write_line('Abrechnung vom ' + datum_to_german(time.today()) + ' (' + zeitraum + ')')
    write_trenner(abrechnunsdatei)
    abrechnunsdatei.write_line('Ergebnis:')

    abrechnunsdatei.write_line(set_ergebnis)

    abrechnunsdatei.write_empty_line()
    write_large_table_row(abrechnunsdatei, 'Ausgaben von ' + name_partner, summe_partner)
    write_large_table_row(abrechnunsdatei, 'Ausgaben von ' + name_self, summe_self)
    abrechnunsdatei.write_line("".ljust(38, "-"))
    write_large_table_row(abrechnunsdatei, "Gesamt", ausgaben_gesamt)

    if verhaeltnis == 50:
        write_into_file(abrechnunsdatei, selector.faktor(0.5).to_list(), 'Gesamtausgaben pro Person ')
    write_into_file(abrechnunsdatei, select_partner.to_list(), 'Ausgaben von ' + name_partner)
    write_into_file(abrechnunsdatei, select_self.to_list(), 'Ausgaben von ' + name_self)

    ausgaben_fuer_partner = DataFrame()
    faktor_partner = compute_faktor_other(verhaeltnis)

    ausgaben_fuer_self = DataFrame()
    faktor_self = compute_faktor_self(verhaeltnis)

    summe_halb = selector.faktor(0.5).sum()

    if set_self_kategorie:
        faktor_self = 0.5

    if set_other_kategorie:
        faktor_partner = 0.5

    for _, row in gemeinsame_buchungen_content.iterrows():
        buchung_partner = berechne_abbuchung(row['Datum'], row['Kategorie'], row['Name'],
                                                   ("%.2f" % (row['Wert'] * faktor_partner)))
        buchung_partner.Dynamisch = False
        ausgaben_fuer_partner = pd.concat([ausgaben_fuer_partner, buchung_partner])

        buchung_self = berechne_abbuchung(row['Datum'], row['Kategorie'], row['Name'],
                                                ("%.2f" % (row['Wert'] * faktor_self)))
        buchung_self.Dynamisch = False
        ausgaben_fuer_self = pd.concat([ausgaben_fuer_self, buchung_self])

    if set_self_kategorie:
        extra_wert = (ausgaben_gesamt * compute_faktor_self(verhaeltnis)) - summe_halb
        extra_ausgleichs_buchung = berechne_abbuchung(maxdate, set_self_kategorie, set_self_kategorie,
                                                            ("%.2f" % extra_wert))
        extra_ausgleichs_buchung.Dynamisch = False
        ausgaben_fuer_self = pd.concat([ausgaben_fuer_self, extra_ausgleichs_buchung])

    if set_other_kategorie:
        extra_wert = (ausgaben_gesamt * compute_faktor_other(verhaeltnis)) - summe_halb
        extra_ausgleichs_buchung = berechne_abbuchung(maxdate, set_other_kategorie, set_other_kategorie,
                                                            ("%.2f" % extra_wert))
        extra_ausgleichs_buchung.Dynamisch = False
        ausgaben_fuer_partner = pd.concat([ausgaben_fuer_partner, extra_ausgleichs_buchung])

    report = TextReportWriter().generate_report(ausgaben_fuer_partner, abrechnunsdatei.to_string())

    database.einzelbuchungen.append_row(ausgaben_fuer_self)
    database.einzelbuchungen.taint()

    database.gemeinsamebuchungen.drop(gemeinsame_buchungen_content.index.tolist())
    database.taint()
    write_abrechnung("Abrechnung_" + str(time.now()), report)
    return report


def write_trenner( abrechnunsdatei):
    return abrechnunsdatei.write("".rjust(40, "#") + "\n ")


def compute_faktor_self(verhaeltnis):
    return verhaeltnis / 100


def compute_faktor_other(verhaeltnis):
    return compute_faktor_self(100 - verhaeltnis)


def write_large_table_row(abrechnunsdatei, name, summe):
    abrechnunsdatei.write_line(name.ljust(30, " ") + str("%.2f" % summe).rjust(7, " "))


def write_into_file(abrechnunsdatei, ausgaben, title):
    abrechnunsdatei.write_empty_line(count=2)
    write_trenner(abrechnunsdatei)
    abrechnunsdatei.write_line(title)
    write_trenner(abrechnunsdatei)
    write_tabelle(abrechnunsdatei, ausgaben)


def write_tabelle(writer, tabelle):
    writer.write_line(
        to_left("Datum", 10) + to_left(" Kategorie", 14) + to_left("Name", 21) + to_right(
            "Wert", 7))
    for row in tabelle:
        writer.write_line(
            datum_to_german(row['Datum']) + "  " + row['Kategorie'].ljust(len("Kategorie   "), " ") + " " + row[
                'Name'].ljust(20, " ") + " " + str("%.2f" % (row['Wert'])).rjust(7, " "))


def to_left(target_string, size):
    return target_string.ljust(size, ' ')


def to_right(target_string, size):
    return target_string.rjust(size, ' ')


def berechne_abbuchung(laufdatum, kategorie, name, wert):
    return DataFrame([[laufdatum, kategorie, name, wert, True]],
                     columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))
