'''
Created on 10.08.2017

@author: sebastian
'''
from datetime import date
from datetime import datetime

import itertools as it
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
        row = self.content.loc[db_index]
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

    def get_jahresausgaben_nach_kategorie_prozentual(self, jahr):
        tabelle = self.select().select_ausgaben().select_year(jahr).content
        return self._berechne_prozentual(tabelle)

    def get_jahreseinnahmen_nach_kategorie_prozentual(self, jahr):
        tabelle = self.select().select_einnahmen().select_year(jahr).content
        return self._berechne_prozentual(tabelle)


    def _berechne_prozentual(self, tabelle):
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

    def select_letzte_6_montate(self):
        if date.today().month > 6:
            mindate = date(day=1, month=(date.today().month - 6), year=date.today().year)
        else:
            mindate = date(day=1, month=(date.today().month + 6), year=date.today().year - 1)
        tabelle = self.content.copy()
        tabelle = tabelle[tabelle.Datum >= mindate]
        tabelle = tabelle[tabelle.Datum <= date.today()]
        return EinzelbuchungsSelektor(tabelle)

    def inject_zeros_for_last_6_months(self):
        today = date.today()
        if today.month > 6:
            return self.inject_zeros_for_year(today.year, today.month)

        first_mapped = self.inject_zeroes_for_year_and_kategories(today.year, today.month)
        return first_mapped.inject_zeroes_for_year_and_kategories(today.year - 1, 12)

    def inject_zeros_for_year(self, year, max_month=12):
        data = self.content.copy()
        for month in range(1, max_month + 1):
            inject_month = date(day=1, month=month, year=year)
            data = data.append(pd.DataFrame([[inject_month, 0]], columns=['Datum', 'Wert']), ignore_index=True)
        return EinzelbuchungsSelektor(data)

    def inject_zeroes_for_year_and_kategories(self, year, max_month=12):
        data = self.content.copy()
        kategorien = set(data.Kategorie)

        dates = []
        for month in range(1, max_month + 1):
            dates.append(date(day=1, month=month, year=year))

        injections = it.product(dates, kategorien)
        for injection_date, injection_kategorie in injections:
            data = data.append(pd.DataFrame([[injection_date, injection_kategorie, 0]], columns=['Datum', 'Kategorie', 'Wert']), ignore_index=True)
        return EinzelbuchungsSelektor(data)


    def sum_monthly(self):
        data = self.content.copy()
        data = data[['Datum', 'Wert']]
        data.Datum = data.Datum.map(lambda x: (x.year * 13) + x.month)
        print(data)
        grouped = data.groupby(by='Datum').sum()
        result = []
        for monat, reihe in grouped.iterrows():
            result.append("%.2f" % abs(reihe.Wert))
        return result

    def sum_kategorien_monthly(self):
        data = self.content.copy()
        data = data[['Datum', 'Kategorie', 'Wert']]
        data.Datum = data.Datum.map(lambda x: x.month)
        grouped = data.groupby(by=['Datum', 'Kategorie']).sum()
        result = {}

        for (monat, kategorie), reihe in grouped.iterrows():
            if monat not in result:
                result[monat] = {}
            result[monat][kategorie] = "%.2f" % abs(reihe.Wert)
        return result


    def sum(self):
        if self.content.empty:
            return 0
        return self.content.Wert.sum()

    def zusammenfassung(self):
        kopierte_tabelle = self.content.copy()[['Datum', 'Wert', 'Kategorie', 'Name']]

        kopierte_tabelle = kopierte_tabelle.sort_values(by=['Datum', 'Kategorie'])

        zusammenfassung = []
        tag_liste = []
        datum_alt = None
        for _, row in kopierte_tabelle.iterrows():
            if datum_alt and datum_alt != row.Datum:  # next cat or day
                if datum_alt != row.Datum :
                    zusammenfassung.append((datum_alt, tag_liste))
                    tag_liste = []
            tag_liste.append({'kategorie':row.Kategorie, 'name':row.Name, 'summe': row.Wert})
            datum_alt = row.Datum

        if datum_alt:
            zusammenfassung.append([datum_alt, tag_liste])
        print('Zusammenfassung:')
        print(zusammenfassung)
        return zusammenfassung

    def get_month_summary(self):
        kopierte_tabelle = self.content.copy()[['Datum', 'Wert', 'Kategorie', 'Name']]

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
