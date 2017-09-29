'''
Created on 17.09.2016

@author: sebastian
'''

from datetime import datetime, date, timedelta

from core.Frequency import FrequencsFunctions
from core.database.Dauerauftraege import Dauerauftraege
from core.database.Einzelbuchungen import Einzelbuchungen
from core.database.Gemeinsamebuchungen import Gemeinsamebuchungen
from core.database.Sollzeiten import Sollzeiten
from core.database.Sonderzeiten import Sonderzeiten
from core.database.Stechzeiten import Stechzeiten
import pandas as pd
import viewcore
from viewcore.converter import datum


class StringWriter():
    '''
    Shadowes file
    '''
    def __init__(self):
        self.value = ""


    def write(self, new_line):
        '''write line into virtual file'''
        self.value = self.value + new_line

    def to_string(self):
        ''' get filecontent'''
        return self.value


class Database:
    '''
    Database
    '''

    def __init__(self, name):
        self.name = name
        self.dauerauftraege = Dauerauftraege()
        self.gemeinsamebuchungen = Gemeinsamebuchungen()
        self.stechzeiten = Stechzeiten()
        self.sollzeiten = Sollzeiten()
        self.sonderzeiten = Sonderzeiten()
        self.einzelbuchungen = Einzelbuchungen()

    def refresh(self):
        print('DATABASE: Erneuere Datenbestand')
        alle_dauerauftragsbuchungen = self.dauerauftraege.get_all_einzelbuchungen_until_today()
        self.einzelbuchungen.append_row(alle_dauerauftragsbuchungen)


        anteil_gemeinsamer_buchungen = self.gemeinsamebuchungen.anteil_gemeinsamer_buchungen()
        self.einzelbuchungen.append_row(anteil_gemeinsamer_buchungen)

        self.einzelbuchungen.sort()
        print('DATABASE: Datenbestand erneuert')


    def _write_trenner(self, abrechnunsdatei):
        return abrechnunsdatei.write("".rjust(40, "#") + "\n ")

    def abrechnen(self):
        '''
        rechnet gemeinsame ausgaben aus der Datenbank ab
        '''
        ausgaben_maureen = self.gemeinsamebuchungen.content[self.gemeinsamebuchungen.content.Person == 'Maureen']
        ausgaben_sebastian = self.gemeinsamebuchungen.content[self.gemeinsamebuchungen.content.Person == 'Sebastian']

        summe_maureen = ausgaben_maureen['Wert'].sum()
        summe_sebastian = ausgaben_sebastian['Wert'].sum()

        ausgaben_gesamt = summe_maureen + summe_sebastian

        dif_maureen = (ausgaben_gesamt / 2) - summe_maureen

        abrechnunsdatei = StringWriter()
        abrechnunsdatei.write("Abrechnung vom " + str(date.today()) + "\n")
        self._write_trenner(abrechnunsdatei)
        abrechnunsdatei.write("Ergebnis: \n")

        if dif_maureen > 0:
            abrechnunsdatei.write("Sebastian muss an Maureen noch " + str(dif_maureen) + "€ überweisen.\n")
        else:
            abrechnunsdatei.write("Maureen muss an Sebastian noch " + str("%.2f" % (dif_maureen * -1)) + "€ überweisen.\n")

        abrechnunsdatei.write("\n")
        abrechnunsdatei.write("Ausgaben von Maureen".ljust(30, " ") + str("%.2f" % (summe_maureen * -1)).rjust(7, " ") + "\n")
        abrechnunsdatei.write("Ausgaben von Sebastian".ljust(30, " ") + str("%.2f" % (summe_sebastian * -1)).rjust(7, " ") + "\n")
        abrechnunsdatei.write("".ljust(38, "-") + "\n")
        abrechnunsdatei.write("Gesamt".ljust(31, " ") + str("%.2f" % ausgaben_gesamt).ljust(7, " ") + "\n \n \n")

        self._write_trenner(abrechnunsdatei)
        abrechnunsdatei.write("Gesamtausgaben pro Person \n")
        self._write_trenner(abrechnunsdatei)

        abrechnunsdatei.write("Datum".ljust(10, " ") + " Kategorie    " + "Name".ljust(20, " ") + " " + "Wert".rjust(7, " ") + "\n")
        for _, row in self.gemeinsamebuchungen.content.iterrows():
            abrechnunsdatei.write(str(row['Datum']) + "  " + row['Kategorie'].ljust(len("Kategorie   "), " ") + " " + row['Name'].ljust(20, " ") + " " + str("%.2f" % (row['Wert'] / 2)).rjust(7, " ") + "\n")

        abrechnunsdatei.write("\n")
        self._write_trenner(abrechnunsdatei)
        abrechnunsdatei.write("Ausgaben von Maureen \n")
        self._write_trenner(abrechnunsdatei)

        abrechnunsdatei.write("Datum".ljust(10, " ") + " Kategorie    " + "Name".ljust(20, " ") + " " + "Wert".rjust(7, " ") + "\n")
        for _ , row in ausgaben_maureen.iterrows():
            abrechnunsdatei.write(str(row['Datum']) + "  " + row['Kategorie'].ljust(len("Kategorie   "), " ") + " " + row['Name'].ljust(20, " ") + " " + str("%.2f" % (row['Wert'])).rjust(7, " ") + "\n")

        abrechnunsdatei.write("\n")
        self._write_trenner(abrechnunsdatei)
        abrechnunsdatei.write("Ausgaben von Sebastian \n")
        self._write_trenner(abrechnunsdatei)

        abrechnunsdatei.write("Datum".ljust(10, " ") + " Kategorie    " + "Name".ljust(20, " ") + " " + "Wert".rjust(7, " ") + "\n")
        for _ , row in ausgaben_sebastian.iterrows():
            abrechnunsdatei.write(str(row['Datum']) + "  " + row['Kategorie'].ljust(len("Kategorie   "), " ") + " " + row['Name'].ljust(20, " ") + " " + str("%.2f" % (row['Wert'])).rjust(7, " ") + "\n")

        ausgaben = pd.DataFrame()
        for _ , row in self.gemeinsamebuchungen.content.iterrows():
            buchung = self._berechne_abbuchung(row['Datum'], row['Kategorie'], row['Name'], ("%.2f" % (row['Wert'] / 2)))
            buchung.Dynamisch = False
            ausgaben = ausgaben.append(buchung)

        abrechnunsdatei.write("\n\n")
        abrechnunsdatei.write("#######MaschinenimportStart\n")
        abrechnunsdatei.write(ausgaben.to_csv(index=False))
        abrechnunsdatei.write("#######MaschinenimportEnd\n")

        self.einzelbuchungen.append_row(ausgaben)
        self.gemeinsamebuchungen.empty()
        viewcore.viewcore.save_refresh()
        self.abrechnungs_write_function("../Abrechnung_" + str(datetime.now()), abrechnunsdatei.to_string())
        return abrechnunsdatei.to_string()


    def _write_to_file(self, filename, content):
        f = open(filename, "w")
        f.write(content)

    abrechnungs_write_function = _write_to_file

    def _berechne_abbuchung(self, laufdatum, kategorie, name, wert):
        return pd.DataFrame([[laufdatum, kategorie, name, wert, True]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))

    def get_arbeitgeber(self):
        return ['DATEV']

    def func_woechentlich(self, buchungs_datum):
        return buchungs_datum.isocalendar()[1]

    def func_monatlich(self, buchungs_datum):
        return buchungs_datum.month

    def get_woechentliche_stechzeiten(self, jahr, function=func_woechentlich):
        print(jahr, 'wird ignoriert')
        wochen_karte = {}
        for index, stechzeit in self.stechzeiten.content.iterrows():
            woche = function(self, stechzeit.Datum)
            if woche not in wochen_karte:
                wochen_karte[woche] = timedelta(minutes=0)
            print(stechzeit)
            wochen_karte[woche] = wochen_karte[woche] + stechzeit.Arbeitszeit

        for index, sonderzeit in self.sonderzeiten.content.iterrows():
            woche = function(self, sonderzeit.Datum)
            if woche not in wochen_karte:
                wochen_karte[woche] = timedelta(minutes=0)
            value = datetime.combine(date.min, sonderzeit.Dauer) - datetime.min
            wochen_karte[woche] = wochen_karte[woche] + value


        return wochen_karte

    def get_soll_ist_uebersicht(self, jahr, function=func_woechentlich):
        startwoche = 1
        print(function)
        if len(self.stechzeiten.content) != 0:
            startwoche = function(self, min(self.stechzeiten.content.Datum))
        if len(self.sollzeiten.content.Startdatum) != 0:
            startwoche = function(self, min(self.sollzeiten.content.Startdatum))

        ist_map = self.get_woechentliche_stechzeiten(jahr, function)
        result_map = {}

        for woche in range(startwoche, function(self, date.today()) + 1):
            ist_wert = timedelta(minutes=0)
            if woche in ist_map:
                ist_wert = ist_map[woche]
            if function == Database.func_woechentlich:
                result_map[woche] = (ist_wert, self._get_soll_wert_fuer_woche(woche))
            elif function == Database.func_monatlich:
                result_map[woche] = (ist_wert, self._get_soll_wert_fuer_monat(woche))
            else:
                result_map[woche] = (ist_wert, 0)

        return result_map

    def _get_soll_wert_fuer_woche(self, woche):
        sonntag = datetime.strptime(str(date.today().year) + "-" + str(woche) + "-0", '%Y-%W-%w')
        tag = sonntag - timedelta(days=6)

        zeit = timedelta(minutes=0)
        for wochentag in range(0, 5):
            zeit = zeit + self._get_zeit_from_tag((tag + timedelta(days=wochentag)).date())
        return zeit

    def _get_soll_wert_fuer_monat(self, monat):
        erster_tag = datum('01/' + str(monat) + "/2017")

        zeit = timedelta(minutes=0)
        ein_tag = timedelta(days=1)
        tag = erster_tag
        while tag.month == monat:
            if tag.weekday() < 5:
                zeit = zeit + self._get_zeit_from_tag(tag)
            tag = tag + ein_tag
        return zeit


    def _get_zeit_from_tag(self, wochentag):
        print("berechne tag: ", wochentag)
        crit1 = self.sollzeiten.content.Startdatum.map(lambda x : x <= wochentag)
        crit2 = self.sollzeiten.content.Endedatum.map(lambda x : x >= wochentag)

        kopierte_tabelle = self.sollzeiten.content.copy()
        kopierte_tabelle = kopierte_tabelle[crit1 & crit2]
        kopierte_tabelle.Dauer = kopierte_tabelle.Dauer.map(lambda x: datetime.combine(date.min, x) - datetime.min)
        if kopierte_tabelle.Dauer.sum() == 0:
            return timedelta(minutes=0)

        return kopierte_tabelle.Dauer.sum()

    def _substract(self, row):
        print(row)
        return  datetime.combine(date.today(), row.Ausstechen) - datetime.combine(date.today(), row.Einstechen)

    def stechzeiten_vorhanden(self):
        return not self.stechzeiten.content.empty

    def anzahl_stechzeiten(self):
        '''
        returns the anzahl der stechzeiten
        '''
        return len(self.stechzeiten.content)

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


    def _ziehe_datev_ab(self, value):
        print("value", value)
        if value <= timedelta(hours=2):
            return value

        if value <= timedelta(hours=2, minutes=14):
            return timedelta(hours=2)

        if value <= timedelta(hours=4, minutes=45):
            return value - timedelta(minutes=15)

        if value <= timedelta(hours=4, minutes=59):
            return timedelta(hours=4, minutes=30)

        if value <= timedelta(hours=6, minutes=30):
            return value - timedelta(minutes=30)

        if value <= timedelta(hours=6, minutes=44):
            return timedelta(hours=6)

        return value - timedelta(minutes=45)

    def _ziehe_pause_ab(self, value, arbeitgeber):
        if arbeitgeber == "DATEV":
            return self._ziehe_datev_ab(value)
        return value


