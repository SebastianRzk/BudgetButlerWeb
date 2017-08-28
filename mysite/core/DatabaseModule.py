'''
Created on 17.09.2016

@author: sebastian
'''

from calendar import monthrange
from datetime import datetime, date, timedelta

from core.Frequency import FrequencsFunctions
from core.database.Dauerauftraege import Dauerauftraege
from core.database.Einzelbuchungen import Einzelbuchungen
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
    persitent_stechzeiten_columns = ['Datum', 'Einstechen', 'Ausstechen', 'Arbeitgeber']
    persistent_sollzeiten_columns = ['Startdatum', 'Endedatum', 'Dauer', 'Arbeitgeber']
    '''
    Database
    '''

    def __init__(self, name):
        self.name = name
        self.dauerauftraege = Dauerauftraege()
        self.gemeinsame_buchungen = pd.DataFrame({}, columns=['Datum', 'Kategorie', 'Name', 'Wert', 'Person'])
        self.stechzeiten = pd.DataFrame({}, columns=self.persitent_stechzeiten_columns)
        self.soll_zeiten = pd.DataFrame({}, columns=self.persistent_sollzeiten_columns)
        self.sonder_zeiten = pd.DataFrame({}, columns=['Datum', 'Dauer', 'Typ', 'Arbeitgeber'])
        self.einzelbuchungen = Einzelbuchungen()

    def refresh(self):
        '''
        inits the database
        '''
        print('DATABASE: Erneuere Datenbestand')
        self.gemeinsame_buchungen['Datum'] = self.gemeinsame_buchungen['Datum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())

        self.stechzeiten['Datum'] = self.stechzeiten['Datum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())
        self.stechzeiten['Einstechen'] = self.stechzeiten['Einstechen'].map(lambda x:  datetime.strptime(x, '%H:%M:%S').time())
        self.stechzeiten['Ausstechen'] = self.stechzeiten['Ausstechen'].map(lambda x:  datetime.strptime(x, '%H:%M:%S').time())

        self.soll_zeiten['Startdatum'] = self.soll_zeiten['Startdatum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())
        self.soll_zeiten['Endedatum'] = self.soll_zeiten['Endedatum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())
        self.soll_zeiten['Dauer'] = self.soll_zeiten['Dauer'].map(lambda x:  datetime.strptime(x, '%H:%M:%S').time())

        self.sonder_zeiten['Datum'] = self.sonder_zeiten['Datum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())
        self.sonder_zeiten['Dauer'] = self.sonder_zeiten['Dauer'].map(lambda x:  datetime.strptime(x, '%H:%M:%S').time())

        self.stechzeiten['Arbeitszeit'] = timedelta(seconds=0)
        for index, row in self.stechzeiten.iterrows():
            arbeitszeit = datetime.combine(date.today(), row.Ausstechen) - datetime.combine(date.today(), row.Einstechen)
            arbeitszeit = self._ziehe_pause_ab(arbeitszeit, row.Arbeitgeber)
            self.stechzeiten.loc[self.stechzeiten.index[[index]], 'Arbeitszeit'] = arbeitszeit
            print(f'berechnete Arbeitszeit: {arbeitszeit}')
        self.stechzeiten = self.stechzeiten.sort_values(by=['Datum'])

        alle_dauerauftragsbuchungen = self.dauerauftraege.get_all_einzelbuchungen_until_today()
        self.einzelbuchungen.append_row(alle_dauerauftragsbuchungen)

        for ind, row in self.gemeinsame_buchungen.iterrows():
            einzelbuchung = pd.DataFrame([[row.Datum, row.Kategorie, row.Name + " (noch nicht abrerechnet, von " + row.Person + ")", row.Wert * 0.5, True]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))
            self.einzelbuchungen.append_row(einzelbuchung)

        self.einzelbuchungen.sort()
        print('DATABASE: Datenbestand erneuert')


    def add_stechzeit(self, buchungs_datum, einstechen, ausstechen, arbeitgeber):
        '''
        add a new stechzeit to the database
        '''
        arbeitszeit = datetime.combine(date.today(), ausstechen) - datetime.combine(date.today(), einstechen)
        stechzeit = pd.DataFrame([[buchungs_datum, einstechen, ausstechen, arbeitgeber, self._ziehe_pause_ab(arbeitszeit, arbeitgeber)]], columns=['Datum', 'Einstechen', 'Ausstechen', 'Arbeitgeber', 'Arbeitszeit'])
        self.stechzeiten = self.stechzeiten.append(stechzeit, ignore_index=True)
        print('DATABASE: stechzeit hinzugefügt')

    def edit_stechzeit(self, index, buchungs_datum, einstechen, ausstechen, arbeitgeber):
        '''
        edit an existing stechzeit by tableIndex
        '''
        self.stechzeiten.loc[self.stechzeiten.index[[index]], 'Datum'] = buchungs_datum
        self.stechzeiten.loc[self.stechzeiten.index[[index]], 'Einstechen'] = einstechen
        self.stechzeiten.loc[self.stechzeiten.index[[index]], 'Ausstechen'] = ausstechen
        self.stechzeiten.loc[self.stechzeiten.index[[index]], 'Arbeitgeber'] = arbeitgeber


    def add_soll_zeit(self, startdatum, endedatum, dauer, arbeitgeber):
        neue_soll_zeit = pd.DataFrame([[startdatum, endedatum, dauer, arbeitgeber]], columns=self.persistent_sollzeiten_columns)
        self.soll_zeiten = self.soll_zeiten.append(neue_soll_zeit, ignore_index=True)

        print('DATABASE: sollzeit hinzugefügt')
        print(self.soll_zeiten)

    def edit_sollzeit(self, index, startdatum, endedatum, dauer, arbeitgeber):
        self.soll_zeiten.loc[self.soll_zeiten.index[[index]], 'Startdatum'] = startdatum
        self.soll_zeiten.loc[self.soll_zeiten.index[[index]], 'Endedatum'] = endedatum
        self.soll_zeiten.loc[self.soll_zeiten.index[[index]], 'Dauer'] = dauer
        self.soll_zeiten.loc[self.soll_zeiten.index[[index]], 'Arbeitgeber'] = arbeitgeber


    def add_gemeinsame_einnahmeausgabe(self, ausgaben_datum, kategorie, ausgaben_name, wert, person):
        row = pd.DataFrame([[ausgaben_datum, kategorie, ausgaben_name, wert, person]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Person'))
        self.gemeinsame_buchungen = self.gemeinsame_buchungen.append(row, ignore_index=True)

        self.einzelbuchungen.add(datum=ausgaben_datum,
                                kategorie=kategorie,
                                name=ausgaben_name + " (noch nicht abgerechnet, von " + person + ")",
                                wert=wert * 0.5,
                                dynamisch=True)

    def get_gemeinsame_ausgabe_fuer(self, person):
        return self.gemeinsame_buchungen[self.gemeinsame_buchungen.Person == person]

    def _write_trenner(self, abrechnunsdatei):
        return abrechnunsdatei.write("".rjust(40, "#") + "\n ")

    def abrechnen(self):
        '''
        rechnet gemeinsame ausgaben aus der Datenbank ab
        '''
        self.gemeinsame_buchungen = self.gemeinsame_buchungen.sort_values(by='Datum')
        ausgaben_maureen = self.gemeinsame_buchungen[self.gemeinsame_buchungen.Person == 'Maureen']
        ausgaben_sebastian = self.gemeinsame_buchungen[self.gemeinsame_buchungen.Person == 'Sebastian']

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
        for _, row in self.gemeinsame_buchungen.iterrows():
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
        for _ , row in self.gemeinsame_buchungen.iterrows():
            buchung = self._berechne_abbuchung(row['Datum'], row['Kategorie'], row['Name'], ("%.2f" % (row['Wert'] / 2)))
            buchung.Dynamisch = False
            ausgaben = ausgaben.append(buchung)

        abrechnunsdatei.write("\n\n")
        abrechnunsdatei.write("#######MaschinenimportStart\n")
        abrechnunsdatei.write(ausgaben.to_csv(index=False))
        abrechnunsdatei.write("#######MaschinenimportEnd\n")

        self.einzelbuchungen.append_row(ausgaben)
        self.gemeinsame_buchungen = self.gemeinsame_buchungen[self.gemeinsame_buchungen.Wert == 0]
        viewcore.viewcore.save_refresh()
        f = open("../Abrechnung_" + str(datetime.now()), "w")
        f.write(abrechnunsdatei.to_string())
        return abrechnunsdatei.to_string()

    def delete_gemeinsame_buchung(self, einzelbuchung_index):
        self.gemeinsame_buchungen = self.gemeinsame_buchungen.drop(einzelbuchung_index)

    def _berechne_abbuchung(self, laufdatum, kategorie, name, wert):
        return pd.DataFrame([[laufdatum, kategorie, name, wert, True]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))


    def edit_gemeinsam(self, index, frame):
        print("index", index)
        print("frame:", frame)
        for column_name, column in frame.copy().transpose().iterrows():
            self.gemeinsame_buchungen.ix[index:index, column_name] = max(column)

    def get_arbeitgeber(self):
        return ['DATEV']

    def func_woechentlich(self, buchungs_datum):
        return buchungs_datum.isocalendar()[1]

    def func_monatlich(self, buchungs_datum):
        return buchungs_datum.month

    def get_woechentliche_stechzeiten(self, jahr, function=func_woechentlich):
        print(jahr, 'wird ignoriert')
        wochen_karte = {}
        for index, stechzeit in self.stechzeiten.iterrows():
            woche = function(self, stechzeit.Datum)
            if woche not in wochen_karte:
                wochen_karte[woche] = timedelta(minutes=0)
            print(stechzeit)
            wochen_karte[woche] = wochen_karte[woche] + stechzeit.Arbeitszeit

        for index, sonderzeit in self.sonder_zeiten.iterrows():
            woche = function(self, sonderzeit.Datum)
            if woche not in wochen_karte:
                wochen_karte[woche] = timedelta(minutes=0)
            value = datetime.combine(date.min, sonderzeit.Dauer) - datetime.min
            wochen_karte[woche] = wochen_karte[woche] + value


        return wochen_karte

    def get_soll_ist_uebersicht(self, jahr, function=func_woechentlich):
        startwoche = 1
        print(function)
        if len(self.stechzeiten) != 0:
            startwoche = function(self, min(self.stechzeiten.Datum))
        if len(self.soll_zeiten.Startdatum) != 0:
            startwoche = function(self, min(self.soll_zeiten.Startdatum))

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
        crit1 = self.soll_zeiten.Startdatum.map(lambda x : x <= wochentag)
        crit2 = self.soll_zeiten.Endedatum.map(lambda x : x >= wochentag)

        kopierte_tabelle = self.soll_zeiten.copy()
        kopierte_tabelle = kopierte_tabelle[crit1 & crit2]
        kopierte_tabelle.Dauer = kopierte_tabelle.Dauer.map(lambda x: datetime.combine(date.min, x) - datetime.min)
        if kopierte_tabelle.Dauer.sum() == 0:
            return timedelta(minutes=0)

        return kopierte_tabelle.Dauer.sum()

    def _substract(self, row):
        print(row)
        return  datetime.combine(date.today(), row.Ausstechen) - datetime.combine(date.today(), row.Einstechen)

    def stechzeiten_vorhanden(self):
        return not self.stechzeiten.empty

    def anzahl_stechzeiten(self):
        '''
        returns the anzahl der stechzeiten
        '''
        return len(self.stechzeiten)

    def get_sollzeiten_liste(self):
        return self.frame_to_list_of_dicts(self.soll_zeiten)


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

    def add_sonder_zeit(self, buchungs_datum, dauer, typ, arbeitgeber):
        row = pd.DataFrame([[buchungs_datum, dauer, typ, arbeitgeber]], columns=['Datum', 'Dauer', 'Typ', 'Arbeitgeber'])
        self.sonder_zeiten = self.sonder_zeiten.append(row)

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

