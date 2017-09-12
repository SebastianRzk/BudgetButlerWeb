'''
Created on 10.08.2017

@author: sebastian
'''
from datetime import date
from datetime import datetime

import pandas as pd
from viewcore import viewcore


class Einzelbuchungen:
    tmp_kategorie = None
    content = pd.DataFrame({}, columns=['Datum', 'Kategorie', 'Name', 'Wert', 'Tags', 'Dynamisch'])

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
        tabelle = tabelle[tabelle.Wert < 0]

        crit1 = tabelle['Datum'].map(lambda x : x.year == jahr)
        tabelle = tabelle[crit1]

        if set(tabelle.index) == set():
            return pd.DataFrame()
        del tabelle['Dynamisch']
        tabelle.Datum = tabelle.Datum.map(lambda x:x.month)
        tabelle = tabelle.groupby(['Datum', 'Kategorie']).sum()
        return tabelle

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

    def get_monate(self):
        '''
        Alle in der Datenbank eingetragenen Monate als set
        '''
        monate = self.content.Datum.copy().map(lambda x: str(x.year) + '_' + str(x.month).rjust(2, '0'))
        return set(monate)

    def get_jahre(self):
        jahre = self.content.Datum.copy().map(lambda x: str(x.year))
        return set(jahre)

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

    def durchschnittliche_ausgaben_pro_monat(self, jahr, today=date.today()):
        data = self.content.copy()
        if data.empty:
            return {}
        data = data[data.Wert < 0]
        if data.empty:
            return {}
        data['DatumBackup'] = data.Datum
        data.Datum = data.Datum.map(lambda x: x.year)
        min_year = min(data.Datum)
        data = data[data.Datum == jahr]
        if data.empty:
            return {}
        monats_teiler = 12
        if min_year == jahr:
            monats_teiler = 13 - (min(self.content.Datum).month)
        if jahr == today.year:
            data.DatumBackup = data.DatumBackup.map(lambda x: x.month)
            data = data[data.DatumBackup != today.month]
            monats_teiler = monats_teiler - (13 - today.month)
            if monats_teiler == 0:
                return {}
        print('#############Teiler', monats_teiler)
        data.Wert = data.Wert.map(lambda x: abs(x / monats_teiler))
        data = data[['Wert', 'Kategorie']]
        data = data.groupby(by='Kategorie').sum()
        data = data.sort_index()
        result = {}
        for kategorie, wert in data.iterrows():
            result[kategorie] = "%.2f" % wert
        return result

    def select(self):
        return EinzelbuchungsSelektor(self.content)

class EinzelbuchungsSelektor:
    content = 0
    def __init__(self, content):
        self.content = content

    def select_year(self, year):
        data = self.content.copy()
        if data.empty:
            return EinzelbuchungsSelektor(data)
        data['TMP'] = data.Datum.map(lambda x: x.year)
        data = data[data.TMP == year]
        del data['TMP']
        return EinzelbuchungsSelektor(data)

    def select_month(self, month):
        data = self.content.copy()
        if data.empty:
            return EinzelbuchungsSelektor(data)
        data['TMP'] = data.Datum.map(lambda x: x.month)
        data = data[data.TMP == month]
        del data['TMP']
        return EinzelbuchungsSelektor(data)


    def select_einnahmen(self):
        return EinzelbuchungsSelektor(self.content[self.content.Wert > 0])

    def select_ausgaben(self):
        return EinzelbuchungsSelektor(self.content[self.content.Wert < 0])

    def select_aktueller_monat(self):
        selector = self.select_year(date.today().year)
        return selector.select_month(date.today().month)

    def raw_table(self):
        return self.content

    def sort_index(self):
        return EinzelbuchungsSelektor(self.content.sort_index())

    def group_by_kategorie(self):
        return self.content.groupby(by='Kategorie').sum()

    def sum(self):
        return self.content.Wert.sum()
