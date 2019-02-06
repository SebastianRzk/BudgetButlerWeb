'''
Created on 28.09.2017

@author: sebastian
'''
from datetime import datetime

from pandas.core.frame import DataFrame
from butler_offline.core.database.DatabaseObject import DatabaseObject
from butler_offline.core.database.Selector import GemeinsamSelector


class Gemeinsamebuchungen(DatabaseObject):

    def __init__(self):
        super().__init__(['Datum', 'Kategorie', 'Name', 'Wert', 'Person'])

    def add(self, ausgaben_datum, kategorie, ausgaben_name, wert, person):
        row = DataFrame([[ausgaben_datum, kategorie, ausgaben_name, wert, person]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Person'))
        self.content = self.content.append(row, ignore_index=True)
        self._sort()
        self.taint()

    def anteil_gemeinsamer_buchungen(self):
        anteil_gemeinsamer_buchungen = DataFrame()
        for _, row in self.content.iterrows():
            einzelbuchung = DataFrame([[row.Datum, row.Kategorie, str(row.Name) + " (noch nicht abgerechnet, von " + str(row.Person) + ")", row.Wert * 0.5, True]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))
            anteil_gemeinsamer_buchungen = anteil_gemeinsamer_buchungen.append(einzelbuchung, ignore_index=True)
        return anteil_gemeinsamer_buchungen

    def drop(self, indices_to_drop):
        print(self.content)
        self.content = self.content.drop(indices_to_drop, axis=0)
        print(self.content)

    def _sort(self):
        self.content = self.content.sort_values(by='Datum')

    def edit(self, index, datum, name, kategorie, wert, person):
        self.edit_element(index, {
            'Datum': datum,
            'Wert': wert,
            'Kategorie': kategorie,
            'Name': name,
            'Person': person
        })

    def rename(self, old_name, new_name):
        self.content.Person = self.content.Person.map(lambda x: self._rename_value(old_name, new_name, x))
        self.taint()

    def _rename_value(self, old, new, x):
        if x == old:
            return new
        return x

    def fuer(self, person):
        return self.content[self.content.Person == person]

    def select_range(self, mindate, maxdate):
        data = self.content.copy()
        data = data[data.Datum >= mindate]
        data = data[data.Datum <= maxdate]

        new_gemeinsame_buchungen = Gemeinsamebuchungen()
        new_gemeinsame_buchungen.content = data

        return new_gemeinsame_buchungen

    def min_date(self):
        return self.content.Datum.min()

    def max_date(self):
        return self.content.Datum.max()

    def is_empty(self):
        return self.content.empty


    def get_content(self):
        result = []
        for index,row in self.content.iterrows():
            result.append({
                'Datum': row.Datum,
                'Name': row.Name,
                'Kategorie': row.Kategorie,
                'Person': row.Person,
                'Wert': row.Wert
            })
        return result


    def select(self):
        return GemeinsamSelector(self.content)
