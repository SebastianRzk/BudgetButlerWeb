'''
Created on 10.08.2017

@author: sebastian
'''
from calendar import monthrange
from datetime import date
from datetime import datetime

import pandas as pd
from viewcore import viewcore


class Einzelbuchungen:
    tmp_kategorie = None
    content = pd.DataFrame({}, columns=['Datum', 'Kategorie', 'Name', 'Wert', 'Tags', 'Dynamisch'])

    def refresh(self):
        self.content['Datum'] = self.content['Datum'].map(lambda x:  datetime.strptime(x, '%Y-%m-%d').date())
        self.content['Dynamisch'] = False
        self.sort()


    def parse(self, raw_table):
        raw_table['Datum'] = raw_table['Datum'].map(lambda x:  datetime.strptime(x, '%Y-%m-%d').date())
        raw_table['Dynamisch'] = False
        self.content = self.content.append(raw_table, ignore_index=True)
        self.sort()

    def sort(self):
        print('DATABASE: Sortiere Einzelbuchungen')
        self.content = self.content.sort_values(by=['Datum', 'Kategorie', 'Name', 'Wert'])
        self.content = self.content.reset_index(drop=True)

    def _row_to_dict(self, columns, index, row_data):
        row = {}
        row['index'] = index
        for key in columns:
            row[key] = row_data[key]
        return row

    def add(self, datum, kategorie, name, wert, dynamisch=False):
        neue_einzelbuchung = pd.DataFrame([[datum, kategorie, name, wert, [], dynamisch]], columns=['Datum', 'Kategorie', 'Name', 'Wert', 'Tags', 'Dynamisch'])
        self.content = self.content.append(neue_einzelbuchung, ignore_index=True)
        self.sort()

    def get(self, db_index):
        row = self.content.iloc[db_index]
        return self._row_to_dict(self.content.columns, db_index, row)

    def get_all(self):
        return self.content

    def delete(self, einzelbuchung_index):
        self.content = self.content.drop(einzelbuchung_index)

    def edit(self, index, buchungs_datum, kategorie, name, wert):
        self.content.loc[self.content.index[[index]], 'Datum'] = buchungs_datum
        self.content.loc[self.content.index[[index]], 'Wert'] = wert
        self.content.loc[self.content.index[[index]], 'Kategorie'] = kategorie
        self.content.loc[self.content.index[[index]], 'Name'] = name
        self.sort()

    def anzahl(self):
        return len(self.content)

    def get_aktuellen_monat(self):
        nov_mask = self.content['Datum'].map(lambda x: x.month) == date.today().month
        return self.content[nov_mask]


    def get_letzte_6_monate_ausgaben(self):
        '''
        Get die ausgaben der letzten 6 Monate nach Monat sortiert
        '''

        tabelle = self.content.copy()
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

        # return gruppiert.tolist()
        return ([0] * 6 + gruppiert.tolist())[-6:]

    def get_letzte_6_monate_einnahmen(self):
        tabelle = self.content.copy()[['Datum', 'Wert']]

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

       # return gruppiert.tolist()
        return ([0] * 6 + gruppiert.tolist())[-6:]

    def _nur_positiv(self, wert):
        if wert > 0:
            return wert
        return 0

    def _nur_negativ(self, wert):
        if wert < 0:
            return wert * -1
        return 0

    def get_ausgabe_pro_monat(self, monat_rueckwaerts):
        today = date.today()

        jahr = today.year
        monat = today.month
        if monat <= monat_rueckwaerts:
            jahr = jahr - 1
            monat = 12 + monat - monat_rueckwaerts
        else:
            monat = monat - monat_rueckwaerts


        crit1 = self.content['Datum'].map(lambda x : x.year == jahr)
        crit2 = self.content['Datum'].map(lambda x : x.month == monat)

        monatsausgaben = self.content[crit1 & crit2]
        print(monatsausgaben)
        summe = monatsausgaben.Wert.sum()

        pro_tag = summe / max(monthrange(jahr, monat))
        print('PRO TAG', pro_tag)
        return '%.2f' % (pro_tag * -1)

    def get_month_summary(self, monat, jahr):
        kopierte_tabelle = self.content.copy()[['Datum', 'Wert', 'Kategorie', 'Name']]

        crit1 = kopierte_tabelle['Datum'].map(lambda x : x.year == jahr)
        crit2 = kopierte_tabelle['Datum'].map(lambda x : x.month == monat)

        kopierte_tabelle = kopierte_tabelle[crit1 & crit2]
        kopierte_tabelle = kopierte_tabelle.sort_values(by=['Datum', 'Kategorie'])

        zusammenfassung = []
        kategorie_alt = ''
        summe_alt = 0
        name_alt = ''
        datum_alt = ''
        tag_liste = []
        more_than_one = False
        for _, row in kopierte_tabelle.iterrows():
            if(kategorie_alt != row.Kategorie or datum_alt != row.Datum) and kategorie_alt != '':  # next cat or day
                if datum_alt != row.Datum :
                    print('push:', [datum_alt, tag_liste])
                    zusammenfassung.append((datum_alt, tag_liste))
                    print(zusammenfassung)
                    tag_liste = []
                tag_liste.append({'kategorie':kategorie_alt, 'name':name_alt, 'summe':'%.2f' % summe_alt})
                datum_alt = row.Datum
                summe_alt = row.Wert
                kategorie_alt = row.Kategorie
                name_alt = row.Name
                more_than_one = False
            elif kategorie_alt == '':  # initial state
                datum_alt = row.Datum
                kategorie_alt = row.Kategorie
                summe_alt = row.Wert
                name_alt = row.Name
            else:
                if not more_than_one:
                    name_alt = name_alt + '(' + str(summe_alt) + '€)'
                    more_than_one = True
                name_alt = name_alt + ', ' + row.Name + '(' + str(row.Wert) + '€)'
                summe_alt += row.Wert


        tag_liste.append({'kategorie':kategorie_alt, 'name':name_alt, 'summe':'%.2f' % summe_alt})
        print('push:', [datum_alt, tag_liste])
        zusammenfassung.append([datum_alt, tag_liste])
        print('Zusammenfassung:')
        print(zusammenfassung)
        return zusammenfassung

    def get_jahresausgaben_nach_monat(self, jahr):
        tabelle = self.content.copy()

        crit1 = tabelle['Datum'].map(lambda x : x.year == jahr)
        tabelle = tabelle[crit1]

        if set(tabelle.index) == set():
            return pd.DataFrame()
        del tabelle['Dynamisch']
        tabelle.Datum = tabelle.Datum.map(lambda x:x.month)
        tabelle = tabelle.groupby(['Datum', 'Kategorie']).sum()
        return tabelle

    def get_gesamtbuchungen_jahr(self, jahr):
        tabelle = self.content.copy()

        crit1 = tabelle['Datum'].map(lambda x : x.year == jahr)

        if tabelle.empty:
            return pd.DataFrame()

        tabelle = tabelle[crit1]
        tabelle.Datum = tabelle.Datum.map(lambda x:x.year)
        del tabelle['Dynamisch']
        del tabelle['Datum']
        tabelle = tabelle.groupby(['Kategorie']).sum()
        return tabelle

    def get_jahresausgaben(self, jahr):
        ausgaben = self.content[self.content.Wert < 0]
        crit1 = ausgaben['Datum'].map(lambda x : x.year == jahr)
        tabelle = ausgaben[crit1]
        if tabelle.empty:
            return 0
        return tabelle.Wert.sum()

    def get_jahreseinnahmen(self, jahr):
        ausgaben = self.content[self.content.Wert > 0]
        crit1 = ausgaben['Datum'].map(lambda x : x.year == jahr)
        tabelle = ausgaben[crit1]
        if tabelle.empty:
            return 0
        return tabelle.Wert.sum()

    def get_gesamtausgaben_jahr(self, jahr):
        tabelle = self.content[self.content.Wert < 0]

        crit1 = tabelle['Datum'].map(lambda x : x.year == jahr)
        tabelle = tabelle[crit1]

        if tabelle.empty:
            return pd.DataFrame()

        del tabelle['Datum']
        tabelle = tabelle.groupby(['Kategorie']).sum()
        return tabelle

    def get_gesamtausgaben_nach_kategorie(self):
        tabelle = self.content.copy()
        tabelle = tabelle[tabelle.Wert < 0]
        tabelle = tabelle.groupby(['Kategorie']).sum()
        result = {}
        for kategorie, row in tabelle.iterrows():
            result[kategorie] = row.Wert
        return result

    def get_gesamtausgaben_nach_kategorie_prozentual(self):
        tabelle = self.content[self.content.Wert < 0]
        tabelle_gesamtsumme = tabelle.Wert.sum()
        tabelle = tabelle.groupby(['Kategorie']).sum()
        result = {}
        for kategorie, row in tabelle.iterrows():
            result[kategorie] = (row.Wert / tabelle_gesamtsumme) * 100
        return result

    def get_jahresausgaben_nach_kategorie_prozentual(self, jahr):
        tabelle = self.content.copy()
        tabelle = tabelle[tabelle.Wert < 0]
        crit1 = tabelle['Datum'].map(lambda x : x.year == jahr)
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
        colors = viewcore.design_colors()
        kategorien = sorted(set(self.content.Kategorie))
        kategorie_farb_mapping = {}
        color_index = 0
        for kategorie in kategorien:
            kategorie_farb_mapping[kategorie] = colors[color_index % len(colors)]
            color_index = color_index + 1

        if not input_kategorie in kategorie_farb_mapping:
            return '00c0ef'
        return kategorie_farb_mapping[input_kategorie]

    def append_row(self, row):
        self.content = self.content.append(row, ignore_index=True)

    def get_vorangegangenen_monat(self, index):
        '''
        gets vorangegangener monat
        '''
        nov_mask = self.content['Datum'].map(lambda x: x.month) == date.today().month - index
        return self.content[nov_mask]

    def get_monate(self):
        '''
        Alle in der Datenbank eingetragenen Monate als set
        '''
        monate = self.content.Datum.copy().map(lambda x: str(x.year) + '_' + str(x.month).rjust(2, '0'))
        return set(monate)

    def get_jahre(self):
        jahre = self.content.Datum.copy().map(lambda x: str(x.year))
        return set(jahre)

    def get_sortierter_monat_fuer(self, year, imonth, kopierte_tabelle, crit):
        kopierte_tabelle = kopierte_tabelle[crit]
        kopierte_tabelle.Datum = kopierte_tabelle.Datum.map(lambda x:str(x.year) + '_' + str(x.month))
        str_date = str(imonth) + '_' + str(year)
        kopierte_tabelle = kopierte_tabelle[kopierte_tabelle.Datum == str_date]
        gemergte_tabelle = kopierte_tabelle.groupby(['Kategorie']).sum()
        gemergte_tabelle = gemergte_tabelle.sort_index()
        return gemergte_tabelle

    def get_monatseinnahmen_nach_kategorie(self, year, imonth):
        kopierte_tabelle = self.content.copy()
        crit = kopierte_tabelle.Wert > 0
        return self.get_sortierter_monat_fuer(year, imonth, kopierte_tabelle, crit)

    def get_monatsausgaben_nach_kategorie(self, year, imonth):
        kopierte_tabelle = self.content.copy()
        crit = kopierte_tabelle.Wert < 0
        return self.get_sortierter_monat_fuer(year, imonth, kopierte_tabelle, crit)

    def get_alle_kategorien(self):
        return self.get_kategorien_ausgaben().union(self.get_kategorien_einnahmen())

    def get_kategorien_ausgaben(self):
        '''
        returns all imported kategorien
        '''
        kategorien = set(self.content[self.content.Wert < 0].Kategorie)
        if self.tmp_kategorie:
            kategorien.add(self.tmp_kategorie)
        return kategorien

    def get_kategorien_einnahmen(self):
        '''
        returns all imported kategorien
        '''
        kategorien = set(self.content[self.content.Wert > 0].Kategorie)
        if self.tmp_kategorie:
            kategorien.add(self.tmp_kategorie)
        return kategorien

    def add_kategorie(self, tmp_kategorie):
        self.tmp_kategorie = tmp_kategorie

