'''
Created on 17.09.2016

@author: sebastian
'''
import butler_offline.core.time
from butler_offline.core.database.Dauerauftraege import Dauerauftraege
from butler_offline.core.database.Einzelbuchungen import Einzelbuchungen
from butler_offline.core.database.Gemeinsamebuchungen import Gemeinsamebuchungen
from butler_offline.viewcore import viewcore
from butler_offline.core.FileSystem import write_abrechnung
from butler_offline.core import time
from butler_offline.viewcore.converter import datum_to_german
from butler_offline.core.export.string_writer import StringWriter
from butler_offline.core.export.text_report import TextReportWriter

from pandas import DataFrame


class Database:
    def __init__(self, name, ausgeschlossene_kategorien=set()):
        self.name = name
        self.dauerauftraege = Dauerauftraege()
        self.gemeinsamebuchungen = Gemeinsamebuchungen()
        self.einzelbuchungen = Einzelbuchungen()
        self.einzelbuchungen.ausgeschlossene_kategorien = ausgeschlossene_kategorien
        self.tainted = 0

    def taint(self):
        self.tainted = self.tainted + 1

    def is_tainted(self):
        return self.taint_number() != 0

    def taint_number(self):
        return self.tainted + self.dauerauftraege.taint_number() + self.einzelbuchungen.taint_number() + self.gemeinsamebuchungen.taint_number()

    def de_taint(self):
        self.tainted = 0
        self.dauerauftraege.de_taint()
        self.einzelbuchungen.de_taint()
        self.gemeinsamebuchungen.de_taint()

    def refresh(self):
        print('DATABASE: Erneuere Datenbestand')
        alle_dauerauftragsbuchungen = self.dauerauftraege.get_all_einzelbuchungen_until_today()
        self.einzelbuchungen.append_row(alle_dauerauftragsbuchungen)

        anteil_gemeinsamer_buchungen = self.gemeinsamebuchungen.anteil_gemeinsamer_buchungen()
        self.einzelbuchungen.append_row(anteil_gemeinsamer_buchungen)

        print('DATABASE: Datenbestand erneuert')

    def _write_trenner(self, abrechnunsdatei):
        return abrechnunsdatei.write("".rjust(40, "#") + "\n ")

    def abrechnen(self, mindate=None, maxdate=None, set_ergebnis=None, verhaeltnis=50, set_self_kategorie=None,
                  set_other_kategorie=None):
        '''
        rechnet gemeinsame ausgaben aus der Datenbank ab
        '''

        if mindate == None:
            mindate = self.gemeinsamebuchungen.min_date()

        if maxdate == None:
            maxdate = self.gemeinsamebuchungen.max_date()

        selector = self.gemeinsamebuchungen.select().select_range(mindate, maxdate)

        name_self = viewcore.database_instance().name
        name_partner = viewcore.name_of_partner()
        gemeinsame_buchungen_content = selector.content

        select_maureen = selector.fuer(name_partner)
        select_sebastian = selector.fuer(name_self)
        summe_maureen = select_maureen.sum()
        summe_sebastian = select_sebastian.sum()

        ausgaben_gesamt = selector.sum()

        abrechnunsdatei = StringWriter()
        zeitraum = datum_to_german(mindate) + '-' + datum_to_german(maxdate)
        abrechnunsdatei.write_line('Abrechnung vom ' + datum_to_german(time.today()) + ' (' + zeitraum + ')')
        self._write_trenner(abrechnunsdatei)
        abrechnunsdatei.write_line('Ergebnis:')

        abrechnunsdatei.write_line(set_ergebnis)

        abrechnunsdatei.write_empty_line()
        self._write_large_table_row(abrechnunsdatei, 'Ausgaben von ' + name_partner, summe_maureen)
        self._write_large_table_row(abrechnunsdatei, 'Ausgaben von ' + name_self, summe_sebastian)
        abrechnunsdatei.write_line("".ljust(38, "-"))
        self._write_large_table_row(abrechnunsdatei, "Gesamt", ausgaben_gesamt)

        if verhaeltnis == 50:
            self.write_into_file(abrechnunsdatei, selector.faktor(0.5).to_list(), 'Gesamtausgaben pro Person ')
        self.write_into_file(abrechnunsdatei, select_maureen.to_list(), 'Ausgaben von ' + name_partner)
        self.write_into_file(abrechnunsdatei, select_sebastian.to_list(), 'Ausgaben von ' + name_self)

        ausgaben_fuer_maureen = DataFrame()
        faktor_maureen = self._faktor_other(verhaeltnis)

        ausgaben_fuer_sebastian = DataFrame()
        faktor_sebastian = self._faktor_self(verhaeltnis)

        summe_halb = selector.faktor(0.5).sum()

        if set_self_kategorie:
            faktor_sebastian = 0.5

        if set_other_kategorie:
            faktor_maureen = 0.5

        for _, row in gemeinsame_buchungen_content.iterrows():
            buchung_maureen = self._berechne_abbuchung(row['Datum'], row['Kategorie'], row['Name'],
                                                       ("%.2f" % (row['Wert'] * faktor_maureen)))
            buchung_maureen.Dynamisch = False
            ausgaben_fuer_maureen = ausgaben_fuer_maureen.append(buchung_maureen)

            buchung_sebastian = self._berechne_abbuchung(row['Datum'], row['Kategorie'], row['Name'],
                                                         ("%.2f" % (row['Wert'] * faktor_sebastian)))
            buchung_sebastian.Dynamisch = False
            ausgaben_fuer_sebastian = ausgaben_fuer_sebastian.append(buchung_sebastian)

        if set_self_kategorie:
            extra_wert = (ausgaben_gesamt * self._faktor_self(verhaeltnis)) - summe_halb
            extra_ausgleichs_buchung = self._berechne_abbuchung(maxdate, set_self_kategorie, set_self_kategorie,
                                                                ("%.2f" % extra_wert))
            extra_ausgleichs_buchung.Dynamisch = False
            ausgaben_fuer_sebastian = ausgaben_fuer_sebastian.append(extra_ausgleichs_buchung)

        if set_other_kategorie:
            extra_wert = (ausgaben_gesamt * self._faktor_other(verhaeltnis)) - summe_halb
            extra_ausgleichs_buchung = self._berechne_abbuchung(maxdate, set_other_kategorie, set_other_kategorie,
                                                                ("%.2f" % extra_wert))
            extra_ausgleichs_buchung.Dynamisch = False
            ausgaben_fuer_maureen = ausgaben_fuer_maureen.append(extra_ausgleichs_buchung)

        report = TextReportWriter().generate_report(ausgaben_fuer_maureen, abrechnunsdatei.to_string())

        self.einzelbuchungen.append_row(ausgaben_fuer_sebastian)
        self.einzelbuchungen.taint()

        self.gemeinsamebuchungen.drop(gemeinsame_buchungen_content.index.tolist())
        self.taint()
        write_abrechnung("Abrechnung_" + str(time.now()), report)
        return report

    def _faktor_self(self, verhaeltnis):
        return verhaeltnis / 100

    def _faktor_other(self, verhaeltnis):
        return self._faktor_self(100 - verhaeltnis)

    def _write_large_table_row(self, abrechnunsdatei, name, summe_sebastian):
        abrechnunsdatei.write_line(name.ljust(30, " ") + str("%.2f" % summe_sebastian).rjust(7, " "))

    def write_into_file(self, abrechnunsdatei, ausgaben_sebastian, title):
        abrechnunsdatei.write_empty_line(count=2)
        self._write_trenner(abrechnunsdatei)
        abrechnunsdatei.write_line(title)
        self._write_trenner(abrechnunsdatei)
        self._write_tabelle(abrechnunsdatei, ausgaben_sebastian)

    def _write_tabelle(self, writer, tabelle):
        writer.write_line(
            self._to_left("Datum", 10) + self._to_left(" Kategorie", 14) + self._to_left("Name", 21) + self._to_right(
                "Wert", 7))
        for row in tabelle:
            writer.write_line(
                datum_to_german(row['Datum']) + "  " + row['Kategorie'].ljust(len("Kategorie   "), " ") + " " + row[
                    'Name'].ljust(20, " ") + " " + str("%.2f" % (row['Wert'])).rjust(7, " "))

    def _to_left(self, target_string, size):
        return target_string.ljust(size, ' ')

    def _to_right(self, target_string, size):
        return target_string.rjust(size, ' ')

    def _berechne_abbuchung(self, laufdatum, kategorie, name, wert):
        return DataFrame([[laufdatum, kategorie, name, wert, True]],
                         columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))

    def func_woechentlich(self, buchungs_datum):
        return buchungs_datum.isocalendar()[1]

    def func_monatlich(self, buchungs_datum):
        return buchungs_datum.month

    def _row_to_dict(self, columns, index, row_data):
        row = {}
        row['index'] = index
        for key in columns:
            row[key] = row_data[key]
        return row

    def frame_to_list_of_dicts(self, dataframe):
        result_list = []
        for index, row_data in dataframe.iterrows():
            row = self._row_to_dict(dataframe.columns, index, row_data)
            result_list.append(row)

        return result_list
