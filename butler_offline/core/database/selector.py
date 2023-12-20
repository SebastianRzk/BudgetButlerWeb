import itertools as it
from datetime import date
from typing import Self, Callable


import pandas as pd
from pandas import DataFrame

from butler_offline.viewcore.converter import datum_to_german


class Selektor:
    content = 0

    def __init__(self, content):
        self.content = content

    def select_year(self, year) -> Self:
        return self._select_date(
            number_extractor=lambda x: x.year,
            number_to_find=year
        )

    def select_month(self, month) -> Self:
        return self._select_date(number_extractor=lambda x: x.month,
                                 number_to_find=month)

    def _select_date(self, number_extractor: Callable[[date], int], number_to_find: int) -> Self:
        data = self.content.copy()
        if data.empty:
            return Selektor(data)
        data['TMP'] = data.Datum.map(number_extractor)
        data = data[data.TMP == number_to_find]
        del data['TMP']
        return Selektor(data)

    def select_einnahmen(self) -> Self:
        return Selektor(self.content[self.content.Wert > 0])

    def select_ausgaben(self) -> Self:
        return Selektor(self.content[self.content.Wert < 0])

    def raw_table(self) -> DataFrame:
        return self.content

    def group_by_kategorie(self):
        return self.content.copy()[['Wert', 'Kategorie']].groupby(by='Kategorie').sum()

    def select_letzte_6_montate(self, today: date) -> Self:
        if today.month > 6:
            mindate = date(day=1, month=(today.month - 6), year=today.year)
        else:
            mindate = date(day=1, month=(today.month + 6), year=today.year - 1)
        tabelle = self.content.copy()
        tabelle = tabelle[tabelle.Datum >= mindate]
        tabelle = tabelle[tabelle.Datum <= date.today()]
        return Selektor(tabelle)

    def inject_zeros_for_last_6_months(self, today: date):
        if today.month > 6:
            return self.inject_zeros_for_year(today.year, today.month)

        first_mapped = self.inject_zeroes_for_year_and_kategories(today.year, today.month)
        return first_mapped.inject_zeroes_for_year_and_kategories(today.year - 1, 12)

    def inject_zeros_for_year(self, year, max_month=12):
        data = self.content.copy()
        for month in range(1, max_month + 1):
            inject_month = date(day=1, month=month, year=year)
            data = pd.concat([data, pd.DataFrame([[inject_month, 0]], columns=['Datum', 'Wert'])], ignore_index=True)
        return Selektor(data)

    def inject_zeroes_for_year_and_kategories(self, year, max_month=12):
        data = self.content.copy()
        kategorien = set(data.Kategorie)

        dates = []
        for month in range(1, max_month + 1):
            dates.append(date(day=1, month=month, year=year))

        injections = it.product(dates, kategorien)
        for injection_date, injection_kategorie in injections:
            data = pd.concat([data,
                              pd.DataFrame([[injection_date, injection_kategorie, 0]],
                                           columns=['Datum', 'Kategorie', 'Wert'])],
                             ignore_index=True)
        return Selektor(data)

    def sum_monthly(self):
        data = self.content.copy()
        data = data[['Datum', 'Wert']]
        data.Datum = data.Datum.map(lambda x: (x.year * 13) + x.month)
        grouped = data.groupby(by='Datum').sum()
        result = []
        for _, reihe in grouped.iterrows():
            result.append("%.2f" % abs(reihe.Wert))
        return result

    def sum_kategorien_monthly(self) -> dict[int, dict[str, str]]:
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

    def sum(self) -> float:
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
                if datum_alt != row.Datum:
                    zusammenfassung.append((datum_alt, tag_liste))
                    tag_liste = []
            tag_liste.append({'kategorie': row.Kategorie, 'name': row.Name, 'summe': row.Wert})
            datum_alt = row.Datum

        if datum_alt:
            zusammenfassung.append([datum_alt, tag_liste])
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
            if (kategorie_alt != row.Kategorie or datum_alt != row.Datum) and kategorie_alt != '':  # next cat or day
                if datum_alt != row.Datum:
                    zusammenfassung.append((datum_to_german(datum_alt), tag_liste))
                    tag_liste = []
                tag_liste.append({'kategorie': kategorie_alt, 'name': name_alt, 'summe': ('%.2f' % summe_alt).replace('.', ',')})
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
                    name_alt = name_alt + ' (' + (('%.2f' % summe_alt).replace('.', ',')) + '€)'
                    more_than_one = True
                name_alt = name_alt + ', ' + row.Name + ' (' + (('%.2f' % row.Wert).replace('.', ',')) + '€)'
                summe_alt += row.Wert

        if datum_alt:
            tag_liste.append({'kategorie': kategorie_alt, 'name': name_alt, 'summe': ('%.2f' % summe_alt).replace('.', ',')})
            zusammenfassung.append([datum_to_german(datum_alt), tag_liste])
        return zusammenfassung

    def faktor(self, faktor):
        data = self.content.copy()
        data.Wert = data.Wert.map(lambda x: x * faktor)
        return Selektor(data)

    def count(self) -> int:
        return len(self.content)

    def to_list(self):
        result = []
        for index, row in self.content.iterrows():
            result.append({**row.to_dict(), **{'index': index}})
        return result

    def get_all_raw(self) -> DataFrame:
        return self.content

    def select_kategorie(self, kategorie: str) -> Self:
        return Selektor(self.content[self.content['Kategorie'] == kategorie])

    def select_statischen_content(self) -> Self:
        return Selektor(self.content[self.content['Dynamisch'] == False])


class GemeinsamSelector(Selektor):

    def __init__(self, content):
        super().__init__(content)

    def fuer(self, person):
        return GemeinsamSelector(self.content[self.content.Person == person])

    def select_range(self, mindate, maxdate):
        data = self.content.copy()
        data = data[data.Datum >= mindate]
        data = data[data.Datum <= maxdate]

        return GemeinsamSelector(data)
