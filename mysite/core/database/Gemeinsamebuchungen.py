'''
Created on 28.09.2017

@author: sebastian
'''
from datetime import datetime

from pandas.core.frame import DataFrame


class Gemeinsamebuchungen:
    content = DataFrame({}, columns=['Datum', 'Kategorie', 'Name', 'Wert', 'Person'])


    def parse(self, raw_table):
        raw_table['Datum'] = raw_table['Datum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())
        self.content = self.content.append(raw_table, ignore_index=True)
        self.sort()

    def add(self, ausgaben_datum, kategorie, ausgaben_name, wert, person):
        row = DataFrame([[ausgaben_datum, kategorie, ausgaben_name, wert, person]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Person'))
        self.content = self.content.append(row, ignore_index=True)
        self.sort()

    def anteil_gemeinsamer_buchungen(self):
        anteil_gemeinsamer_buchungen = DataFrame()
        for ind, row in self.content.iterrows():
            einzelbuchung = DataFrame([[row.Datum, row.Kategorie, row.Name + " (noch nicht abgerechnet, von " + row.Person + ")", row.Wert * 0.5, True]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))
            anteil_gemeinsamer_buchungen = anteil_gemeinsamer_buchungen.append(einzelbuchung, ignore_index=True)
        return anteil_gemeinsamer_buchungen

    def empty(self):
        self.content = self.content[self.content.Wert == 0]

    def sort(self):
        self.content = self.content.sort_values(by='Datum')

    def delete(self, einzelbuchung_index):
        self.content = self.content.drop(einzelbuchung_index)

    def edit(self, index, frame):
        for column_name, column in frame.copy().transpose().iterrows():
            self.content.ix[index:index, column_name] = max(column)

    def fuer(self, person):
        return self.content[self.content.Person == person]

