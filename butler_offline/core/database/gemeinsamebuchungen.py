from pandas.core.frame import DataFrame
from butler_offline.core.database.database_object import DatabaseObject
from butler_offline.core.database.selector import GemeinsamSelector
import pandas as pd


class Gemeinsamebuchungen(DatabaseObject):
    TABLE_HEADER = ['Datum', 'Kategorie', 'Name', 'Wert', 'Person']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)

    def add(self, ausgaben_datum, kategorie, ausgaben_name, wert, person):
        row = DataFrame([[ausgaben_datum, kategorie, ausgaben_name, wert, person]], columns=self.TABLE_HEADER)
        self.content = pd.concat([self.content, row], ignore_index=True)
        self._sort()
        self.taint()

    def anteil_gemeinsamer_buchungen(self):
        anteil_gemeinsamer_buchungen = DataFrame()
        for _, row in self.content.iterrows():
            einzelbuchung = DataFrame([[row.Datum, row.Kategorie, str(row.Name) + " (noch nicht abgerechnet, von " + str(row.Person) + ")", row.Wert * 0.5, True]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))
            anteil_gemeinsamer_buchungen = pd.concat([anteil_gemeinsamer_buchungen, einzelbuchung], ignore_index=True)
        return anteil_gemeinsamer_buchungen

    def drop(self, indices_to_drop):
        self.content = self.content.drop(indices_to_drop, axis=0)

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

    def get_renamed_list(self, old_username, new_username, old_partnername, new_partnername):
        data = self.content.copy()
        data.Person = data.Person.map(lambda x: self._rename_person(x, {old_username: new_username, old_partnername: new_partnername}))
        result = []

        for index, row in data.iterrows():
            result.append({
            'Datum': row.Datum,
            'Wert': row.Wert,
            'Kategorie': row.Kategorie,
            'Name': row.Name,
            'Person': row.Person
        })
        return result

    def drop_all(self):
        self.content = self.content.iloc[0:0]
        self.taint()

    def _rename_person(self, person_name, mapping):
        if person_name in mapping:
            return mapping[person_name]
        return person_name

    def _rename_value(self, old, new, x):
        if x == old:
            return new
        return x

    def min_date(self):
        return self.content.Datum.min()

    def max_date(self):
        return self.content.Datum.max()

    def is_empty(self):
        return self.content.empty

    def select(self):
        return GemeinsamSelector(self.content)
