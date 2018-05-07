'''
Created on 28.09.2017

@author: sebastian
'''
from datetime import datetime

from pandas.core.frame import DataFrame
from core.database.DatabaseObject import DatabaseObject


class Gemeinsamebuchungen(DatabaseObject):
    content = DataFrame({}, columns=['Datum', 'Kategorie', 'Name', 'Wert', 'Person'])

    def parse(self, raw_table):
        raw_table['Datum'] = raw_table['Datum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())
        self.content = self.content.append(raw_table, ignore_index=True)
        self._sort()

    def add(self, ausgaben_datum, kategorie, ausgaben_name, wert, person):
        row = DataFrame([[ausgaben_datum, kategorie, ausgaben_name, wert, person]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Person'))
        self.content = self.content.append(row, ignore_index=True)
        self._sort()
        self.taint()

    def anteil_gemeinsamer_buchungen(self):
        anteil_gemeinsamer_buchungen = DataFrame()
        for ind, row in self.content.iterrows():
            einzelbuchung = DataFrame([[row.Datum, row.Kategorie, str(row.Name) + " (noch nicht abgerechnet, von " + str(row.Person) + ")", row.Wert * 0.5, True]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))
            anteil_gemeinsamer_buchungen = anteil_gemeinsamer_buchungen.append(einzelbuchung, ignore_index=True)
        return anteil_gemeinsamer_buchungen

    def empty(self):
        self.content = self.content[self.content.Wert == 0]

    def _sort(self):
        self.content = self.content.sort_values(by='Datum')

    def delete(self, einzelbuchung_index):
        self.content = self.content.drop(einzelbuchung_index)
        self.taint()

    def edit(self, index, datum, name, kategorie, wert, person):
        self.content.loc[self.content.index[[index]], 'Datum'] = datum
        self.content.loc[self.content.index[[index]], 'Wert'] = wert
        self.content.loc[self.content.index[[index]], 'Kategorie'] = kategorie
        self.content.loc[self.content.index[[index]], 'Name'] = name
        self.content.loc[self.content.index[[index]], 'Person'] = person
        self._sort()
        self.taint()

    def rename(self, old_name, new_name):
        self.content.Person = self.content.Person.map(lambda x: self._rename_value(old_name, new_name, x))

    def _rename_value(self, old, new, x):
        if x == old:
            return new
        return x

    def fuer(self, person):
        return self.content[self.content.Person == person]

