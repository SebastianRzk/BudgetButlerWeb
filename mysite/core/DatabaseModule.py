'''
Created on 17.09.2016

@author: sebastian
'''

from calendar import monthrange
from datetime import datetime, date, timedelta

from core.Frequency import FrequencsFunctions
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

    def _initial_einzelbuchungen_table(self):
        return pd.DataFrame({}, columns=['Datum', 'Kategorie', 'Name', 'Wert', 'Tags', 'Dynamisch'])

    def __init__(self, name):
        self.name = name
        self.kategorien_liste = set()
        self.einzelbuchungen = self._initial_einzelbuchungen_table()
        self.dauerauftraege = pd.DataFrame({}, columns=['Endedatum', 'Kategorie', 'Name', 'Rhythmus', 'Startdatum', 'Wert'])
        self.gemeinsame_buchungen = pd.DataFrame({}, columns=['Datum', 'Kategorie', 'Name', 'Wert', 'Person'])
        self.stechzeiten = pd.DataFrame({}, columns=self.persitent_stechzeiten_columns)
        self.soll_zeiten = pd.DataFrame({}, columns=self.persistent_sollzeiten_columns)
        self.sonder_zeiten = pd.DataFrame({}, columns=['Datum', 'Dauer', 'Typ', 'Arbeitgeber'])

        self.tmp_kategorie = None

    def refresh(self):
        '''
        inits the database
        '''
        print('DATABASE: Erneuere Datenbestand')

        if 'Tags' not in self.einzelbuchungen.columns:
            print("DATABASE: MIGRATE: START: Softmigrate Einzelbuchungen. Adding Tags!")
            self.einzelbuchungen['Tags'] = self.einzelbuchungen.Datum.map(lambda x: [])
            print("DATABASE: MIGRATE: END: migrated:", len(self.einzelbuchungen.Datum))

        self.gemeinsame_buchungen['Datum'] = self.gemeinsame_buchungen['Datum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())

        self.einzelbuchungen['Datum'] = self.einzelbuchungen['Datum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())
        self.einzelbuchungen["Dynamisch"] = False

        self.dauerauftraege['Startdatum'] = self.dauerauftraege['Startdatum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())
        self.dauerauftraege['Endedatum'] = self.dauerauftraege['Endedatum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())

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

        for _, row in self.dauerauftraege.iterrows():
            dauerauftrag_buchungen = self.einnahmenausgaben_until_today(row['Startdatum'], row['Endedatum'], row['Rhythmus'], row['Name'], row['Wert'], row['Kategorie'])
            for buchung in dauerauftrag_buchungen:
                self.einzelbuchungen = self.einzelbuchungen.append(buchung, ignore_index=True)
                print("DATABASE: Neuer Dauerauftrag-Einzelposten hinzugefügt: ", buchung)
        self.einzelbuchungen = self.einzelbuchungen.sort_values(by='Datum')

        for ind, row in self.gemeinsame_buchungen.iterrows():
            einzelbuchung = pd.DataFrame([[row.Datum, row.Kategorie, row.Name + " (noch nicht abrerechnet, von " + row.Person + ")", row.Wert * 0.5, True]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))
            self.einzelbuchungen = self.einzelbuchungen.append(einzelbuchung, ignore_index=True)

        print('DATABASE: REFRESH: Sortiere Einzelbuchungen')
        self._sortiere_einzelbuchungen()
        print('DATABASE: Datenbestand erneuert')


    def get_colors(self):
        '''returns list of colors '''
        colors = {}
        colors[0] = ("f56954")
        colors[1] = ("00a65a")
        colors[2] = ("f39c12")
        colors[3] = ("00c0ef")
        colors[4] = ("3c8dbc")
        colors[5] = ("d2d6de")

        colors = {**colors, **colors}
        colors = {**colors, **colors}
        return colors

    def get_alle_kategorien(self):
        return self.get_kategorien_ausgaben().union(self.get_kategorien_einnahmen())

    def get_kategorien_ausgaben(self):
        '''
        returns all imported kategorien
        '''
        kategorien = set(self.einzelbuchungen[self.einzelbuchungen.Wert < 0].Kategorie)
        if self.tmp_kategorie:
            kategorien.add(self.tmp_kategorie)
        return kategorien


    def get_kategorien_einnahmen(self):
        '''
        returns all imported kategorien
        '''
        kategorien = set(self.einzelbuchungen[self.einzelbuchungen.Wert > 0].Kategorie)
        if self.tmp_kategorie:
            kategorien.add(self.tmp_kategorie)
        return kategorien


    def add_dauerauftrag(self, startdatum, endedatum, kategorie, name, rhythmus, wert):
        '''
        add new dauerauftrag to the database
        '''
        neuer_dauerauftrag = pd.DataFrame(
            [[endedatum, kategorie, name, rhythmus, startdatum, wert]],
            columns=['Endedatum', 'Kategorie', 'Name', 'Rhythmus', 'Startdatum', 'Wert']
            )
        self.dauerauftraege = self.dauerauftraege.append(neuer_dauerauftrag, ignore_index=True)
        print('DATABASE: Dauerauftrag hinzugefügt')


    def edit_dauerauftrag(self, index, startdatum, endedatum, kategorie, name, rhythmus, wert):
        '''
        edit dauerauftrag for given index
        '''
        self.dauerauftraege.loc[self.dauerauftraege.index[[index]], 'Startdatum'] = startdatum
        self.dauerauftraege.loc[self.dauerauftraege.index[[index]], 'Endedatum'] = endedatum
        self.dauerauftraege.loc[self.dauerauftraege.index[[index]], 'Wert'] = wert
        self.dauerauftraege.loc[self.dauerauftraege.index[[index]], "Kategorie"] = kategorie
        self.dauerauftraege.loc[self.dauerauftraege.index[[index]], 'Name'] = name
        self.dauerauftraege.loc[self.dauerauftraege.index[[index]], 'Rhythmus'] = rhythmus

    def add_einzelbuchung(self, buchungs_datum, kategorie, name, wert):
        '''
        add a new einzelbuchung to the database
        '''
        neue_einzelbuchung = pd.DataFrame([[buchungs_datum, kategorie, name, wert, [], False]], columns=['Datum', 'Kategorie', 'Name', 'Wert', 'Tags', 'Dynamisch'])
        self.einzelbuchungen = self.einzelbuchungen.append(neue_einzelbuchung, ignore_index=True)
        self._sortiere_einzelbuchungen()

    def edit_einzelbuchung(self, index, buchungs_datum, kategorie, name, wert):
        '''
        edit an existing einzelbuchung by tableindex
        '''
        self.einzelbuchungen.loc[self.einzelbuchungen.index[[index]], 'Datum'] = buchungs_datum
        self.einzelbuchungen.loc[self.einzelbuchungen.index[[index]], 'Wert'] = wert
        self.einzelbuchungen.loc[self.einzelbuchungen.index[[index]], 'Kategorie'] = kategorie
        self.einzelbuchungen.loc[self.einzelbuchungen.index[[index]], 'Name'] = name
        self._sortiere_einzelbuchungen()

    def _add_einnahmeausgabe(self, einnahme_ausgabe):
        '''
        add new einnahmeausgabe to the database (with pandas DataFrame)
        '''
        self.einzelbuchungen = self.einzelbuchungen.append(einnahme_ausgabe, ignore_index=True)
        print('DATABASE: EinnahmeAusgabe hinzugefügt')

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


    def add_gemeinsame_einnahmeausgabe(self, einnahme_ausgabe):
        self.gemeinsame_buchungen = self.gemeinsame_buchungen.append(einnahme_ausgabe.copy(), ignore_index=True)
        name = einnahme_ausgabe.Name + " (noch nicht abgerechnet, von " + einnahme_ausgabe.Person + ")"

        neue_einzelbuchung = einnahme_ausgabe.copy()
        neue_einzelbuchung.Wert = neue_einzelbuchung.Wert * 0.5
        neue_einzelbuchung.Name = name
        neue_einzelbuchung['Dynamisch'] = True

        self.einzelbuchungen = self.einzelbuchungen.append(neue_einzelbuchung, ignore_index=True)

    def get_aktuellen_monat(self):
        nov_mask = self.einzelbuchungen['Datum'].map(lambda x: x.month) == date.today().month
        return self.einzelbuchungen[nov_mask]

    def get_vorangegangenen_monat(self, index):
        '''
        gets vorangegangener monat
        '''
        nov_mask = self.einzelbuchungen['Datum'].map(lambda x: x.month) == date.today().month - index
        return self.einzelbuchungen[nov_mask]

    def get_letzte_6_monate_ausgaben(self):
        '''
        Get die ausgaben der letzten 6 Monate nach Monat sortiert
        '''

        tabelle = self.einzelbuchungen.copy()
        del tabelle['Name']
        del tabelle['Kategorie']
        del tabelle['Dynamisch']


        if date.today().month > 6:
            mindate = date(day=1, month=(date.today().month - 6), year=date.today().year)
        else:
            mindate = date(day=1, month=(date.today().month + 6), year=date.today().year - 1)



        tabelle = tabelle[tabelle.Datum >= mindate]
        tabelle = tabelle[tabelle.Datum <= date.today()]
        tabelle.Datum = tabelle.Datum.apply(lambda x: str(x.month) + str(x.year))
        tabelle.Wert = tabelle.Wert.apply(self._nur_negativ)

        gruppiert = tabelle.Wert.groupby(tabelle.Datum).sum()
        gruppiert = gruppiert.sort_index()

        return gruppiert.tolist()


    def get_letzte_6_monate_einnahmen(self):
        '''
        Get die ausgaben der letzten 6 Monate nach Monat sortiert
        '''

        tabelle = self.einzelbuchungen.copy()
        del tabelle['Name']
        del tabelle['Kategorie']
        del tabelle['Dynamisch']

        if date.today().month > 6:
            mindate = date(day=1, month=(date.today().month - 6), year=date.today().year)
        else:
            mindate = date(day=1, month=(date.today().month + 6), year=date.today().year - 1)

        tabelle = tabelle[tabelle.Datum >= mindate]
        tabelle = tabelle[tabelle.Datum <= date.today()]
        tabelle.Datum = tabelle.Datum.apply(lambda x: str(x.month) + str(x.year))
        tabelle.Wert = tabelle.Wert.map(self._nur_positiv)
        gruppiert = tabelle.Wert.groupby(tabelle.Datum).sum()
        gruppiert = gruppiert.sort_index()

        return gruppiert.tolist()

    def _nur_positiv(self, wert):
        if wert > 0:
            return wert
        return 0

    def _nur_negativ(self, wert):
        if wert < 0:
            return wert * -1
        return 0

    def get_monate(self):
        '''
        Alle in der Datenbank eingetragenen Monate als set
        '''
        monate = self.einzelbuchungen.Datum.copy().map(lambda x: str(x.year) + "_" + str(x.month).rjust(2, '0'))
        return set(monate)

    def get_jahre(self):
        jahre = self.einzelbuchungen.Datum.copy().map(lambda x: str(x.year))
        return set(jahre)

    def get_sortierter_monat_fuer(self, year, imonth, kopierte_tabelle, crit):
        kopierte_tabelle = kopierte_tabelle[crit]
        kopierte_tabelle.Datum = kopierte_tabelle.Datum.map(lambda x:str(x.year) + "_" + str(x.month))
        str_date = str(imonth) + "_" + str(year)
        kopierte_tabelle = kopierte_tabelle[kopierte_tabelle.Datum == str_date]
        gemergte_tabelle = kopierte_tabelle.groupby(['Kategorie']).sum()
        gemergte_tabelle = gemergte_tabelle.sort_index()
        return gemergte_tabelle

    def get_monatseinnahmen_nach_kategorie(self, year, imonth):
        kopierte_tabelle = self.einzelbuchungen.copy()
        crit = kopierte_tabelle.Wert > 0
        return self.get_sortierter_monat_fuer(year, imonth, kopierte_tabelle, crit)

    def get_monatsausgaben_nach_kategorie(self, year, imonth):
        kopierte_tabelle = self.einzelbuchungen.copy()
        crit = kopierte_tabelle.Wert < 0
        return self.get_sortierter_monat_fuer(year, imonth, kopierte_tabelle, crit)


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

        self._add_einnahmeausgabe(ausgaben)
        self.gemeinsame_buchungen = self.gemeinsame_buchungen[self.gemeinsame_buchungen.Wert == 0]
        viewcore.viewcore.save_refresh()
        f = open("../Abrechnung_" + str(datetime.now()), "w")
        f.write(abrechnunsdatei.to_string())
        return abrechnunsdatei.to_string()

    def _berechne_abbuchung(self, laufdatum, kategorie, name, wert):
        return pd.DataFrame([[laufdatum, kategorie, name, wert, True]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))


    def einnahmenausgaben_until_today(self, startdatum,
                                      endedatum, frequenzfunktion, name, wert, kategorie):
        '''
        compute all einnahmenausgaben until today
        '''
        laufdatum = startdatum
        frequency_function = FrequencsFunctions().get_function_for_name(frequenzfunktion)
        print("  Init alle Buchungen für die Den DauerauftragModule. Startdatum:", laufdatum)
        result = []
        while laufdatum < date.today() and laufdatum < endedatum:
            abbuchung = self._berechne_abbuchung(laufdatum, kategorie, name, wert)
            result.append(abbuchung)
            laufdatum = frequency_function(laufdatum)
        return result

    def get_ausgabe_pro_monat(self, monat_rueckwaerts):
        today = date.today()

        jahr = today.year
        monat = today.month
        if monat <= monat_rueckwaerts:
            jahr = jahr - 1
            monat = 12 + monat - monat_rueckwaerts
        else:
            monat = monat - monat_rueckwaerts


        crit1 = self.einzelbuchungen['Datum'].map(lambda x : x.year == jahr)
        crit2 = self.einzelbuchungen['Datum'].map(lambda x : x.month == monat)

        monatsausgaben = self.einzelbuchungen[crit1 & crit2]
        print(monatsausgaben)
        summe = monatsausgaben.Wert.sum()

        pro_tag = summe / max(monthrange(jahr, monat))
        print("PRO TAG", pro_tag)
        return "%.2f" % (pro_tag * -1)

    def delete_dauerauftrag(self, dauerauftrag_index):
        self.dauerauftraege = self.dauerauftraege.drop(dauerauftrag_index)

    def delete_einzelbuchung(self, einzelbuchung_index):
        self.einzelbuchungen = self.einzelbuchungen.drop(einzelbuchung_index)

    def delete_gemeinsame_buchung(self, einzelbuchung_index):
        self.gemeinsame_buchungen = self.gemeinsame_buchungen.drop(einzelbuchung_index)

    def edit_gemeinsam(self, index, frame):
        print("index", index)
        print("frame:", frame)
        for column_name, column in frame.copy().transpose().iterrows():
            self.gemeinsame_buchungen.ix[index:index, column_name] = max(column)

    def get_month_summary(self, monat, jahr):
        '''
        prints the values, storted and merged by day
        '''
        print(self.einzelbuchungen)
        kopierte_tabelle = pd.DataFrame({})
        kopierte_tabelle['Datum'] = self.einzelbuchungen['Datum'].copy()
        kopierte_tabelle['Wert'] = self.einzelbuchungen['Wert'].copy()
        kopierte_tabelle['Kategorie'] = self.einzelbuchungen['Kategorie'].copy()
        kopierte_tabelle['Name'] = self.einzelbuchungen['Name']

        crit1 = self.einzelbuchungen['Datum'].map(lambda x : x.year == jahr)
        crit2 = self.einzelbuchungen['Datum'].map(lambda x : x.month == monat)

        kopierte_tabelle = kopierte_tabelle[crit1 & crit2]
        kopierte_tabelle = kopierte_tabelle.sort_values(by=['Datum', 'Kategorie'])

        zusammenfassung = []
        kategorie_alt = ""
        summe_alt = 0
        name_alt = ""
        datum_alt = ""
        tag_liste = []
        for _, row in kopierte_tabelle.iterrows():
            if(kategorie_alt != row.Kategorie or datum_alt != row.Datum) and kategorie_alt != "":
                if datum_alt != row.Datum :
                    print("push:", [datum_alt, tag_liste])
                    zusammenfassung.append([datum_alt, tag_liste])
                    print(zusammenfassung)
                    tag_liste = []
                tag_liste.append((kategorie_alt, name_alt, "%.2f" % summe_alt))
                datum_alt = row.Datum
                summe_alt = row.Wert
                kategorie_alt = row.Kategorie
                name_alt = row.Name + "(" + str(row.Wert) + "€)"
            elif kategorie_alt == "":
                datum_alt = row.Datum
                kategorie_alt = row.Kategorie
                summe_alt = row.Wert
                name_alt = row.Name + "(" + str(row.Wert) + "€)"
            else:
                summe_alt += row.Wert
                name_alt = name_alt + ", " + row.Name + "(" + str(row.Wert) + "€)"

        tag_liste.append([kategorie_alt, name_alt, "%.2f" % summe_alt])
        print("push:", [datum_alt, tag_liste])
        zusammenfassung.append([datum_alt, tag_liste])
        print("Zusammenfassung:")
        print(zusammenfassung)
        return zusammenfassung

    def add_kategorie(self, tmp_kategorie):
        self.tmp_kategorie = tmp_kategorie

    def get_jahresausgaben_nach_monat(self, jahr):
        tabelle = self.einzelbuchungen.copy()

        crit1 = self.einzelbuchungen['Datum'].map(lambda x : x.year == jahr)
        tabelle = tabelle[crit1]

        if set(tabelle.index) == set():
            return pd.DataFrame()
        del tabelle['Dynamisch']
        tabelle.Datum = tabelle.Datum.map(lambda x:x.month)
        tabelle = tabelle.groupby(['Datum', 'Kategorie']).sum()
        return tabelle

    def get_gesamtbuchungen_jahr(self, jahr):
        tabelle = self.einzelbuchungen.copy()

        crit1 = self.einzelbuchungen['Datum'].map(lambda x : x.year == jahr)

        if tabelle.empty:
            return pd.DataFrame()

        tabelle = tabelle[crit1]
        tabelle.Datum = tabelle.Datum.map(lambda x:x.year)
        del tabelle['Dynamisch']
        del tabelle['Datum']
        tabelle = tabelle.groupby(['Kategorie']).sum()
        return tabelle

    def get_jahresausgaben(self, jahr):
        ausgaben = self.einzelbuchungen[self.einzelbuchungen.Wert < 0]
        crit1 = self.einzelbuchungen['Datum'].map(lambda x : x.year == jahr)
        tabelle = ausgaben[crit1]
        if tabelle.empty:
            return 0
        return tabelle.Wert.sum()

    def get_jahreseinnahmen(self, jahr):
        ausgaben = self.einzelbuchungen[self.einzelbuchungen.Wert > 0]
        crit1 = self.einzelbuchungen['Datum'].map(lambda x : x.year == jahr)
        tabelle = ausgaben[crit1]
        if tabelle.empty:
            return 0
        return tabelle.Wert.sum()

    def get_gesamtausgaben_jahr(self, jahr):
        tabelle = self.einzelbuchungen[self.einzelbuchungen.Wert < 0]

        crit1 = self.einzelbuchungen['Datum'].map(lambda x : x.year == jahr)
        tabelle = tabelle[crit1]

        if tabelle.empty:
            return pd.DataFrame()

        del tabelle['Datum']
        tabelle = tabelle.groupby(['Kategorie']).sum()
        return tabelle

    def get_gesamtausgaben_nach_kategorie(self):
        tabelle = self.einzelbuchungen.copy()
        tabelle = tabelle[tabelle.Wert < 0]
        tabelle = tabelle.groupby(['Kategorie']).sum()
        result = {}
        for kategorie, row in tabelle.iterrows():
            result[kategorie] = row.Wert
        return result

    def get_gesamtausgaben_nach_kategorie_prozentual(self):
        tabelle = self.einzelbuchungen[self.einzelbuchungen.Wert < 0]
        tabelle_gesamtsumme = tabelle.Wert.sum()
        tabelle = tabelle.groupby(['Kategorie']).sum()
        result = {}
        for kategorie, row in tabelle.iterrows():
            result[kategorie] = (row.Wert / tabelle_gesamtsumme) * 100
        return result

    def get_jahresausgaben_nach_kategorie_prozentual(self, jahr):
        tabelle = self.einzelbuchungen.copy()
        tabelle = tabelle[tabelle.Wert < 0]
        crit1 = self.einzelbuchungen['Datum'].map(lambda x : x.year == jahr)
        tabelle = tabelle[crit1]

        if len(tabelle) == 0:
            return {}

        tabelle_gesamtsumme = tabelle.Wert.sum()
        tabelle = tabelle.groupby(['Kategorie']).sum()
        result = {}
        for kategorie, row in tabelle.iterrows():
            result[kategorie] = (row.Wert / tabelle_gesamtsumme) * 100
        return result



    def get_farbe_fuer(self, input_kategorie):
        colors = self.get_colors()
        kategorien = sorted(set(self.einzelbuchungen.Kategorie))
        kategorie_farb_mapping = {}
        color_index = 0
        for kategorie in kategorien:
            kategorie_farb_mapping[kategorie] = colors[color_index % len(colors)]
            color_index = color_index + 1

        if not input_kategorie in kategorie_farb_mapping:
            return "00c0ef"
        return kategorie_farb_mapping[input_kategorie]

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

    def aktuelle_dauerauftraege(self):
        '''
        return aktuelle dauerauftraege
        '''
        dauerauftraege = self.dauerauftraege.copy()
        dauerauftraege = dauerauftraege[dauerauftraege.Endedatum > date.today()]
        dauerauftraege = dauerauftraege[dauerauftraege.Startdatum < date.today()]
        return self.frame_to_list_of_dicts(dauerauftraege)

    def past_dauerauftraege(self):
        '''
        return vergangene dauerauftraege
        '''
        dauerauftraege = self.dauerauftraege.copy()
        dauerauftraege = dauerauftraege[dauerauftraege.Endedatum < date.today()]
        return self.frame_to_list_of_dicts(dauerauftraege)

    def future_dauerauftraege(self):
        '''
        return dauerauftraege aus der zukunft
        '''
        dauerauftraege = self.dauerauftraege.copy()
        dauerauftraege = dauerauftraege[dauerauftraege.Startdatum > date.today()]
        return self.frame_to_list_of_dicts(dauerauftraege)


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

    def get_single_einzelbuchung(self, db_index):
        row = self.einzelbuchungen.iloc[db_index]
        return self._row_to_dict(self.einzelbuchungen.columns, db_index, row)


    def get_single_dauerauftrag(self, db_index):
        db_row = self.dauerauftraege.iloc[db_index]
        return self._row_to_dict(self.dauerauftraege.columns, db_index, db_row)

    def _sortiere_einzelbuchungen(self):
        print("DATABASE: Sortiere Einzelbuchungen")
        print(self.einzelbuchungen)
        self.einzelbuchungen = self.einzelbuchungen.sort_values(by=['Datum', 'Kategorie', 'Name', 'Wert'])
        self.einzelbuchungen = self.einzelbuchungen.reset_index(drop=True)
        print(self.einzelbuchungen)

    def get_sortierte_einzelbuchungen(self):
        return self.einzelbuchungen

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

