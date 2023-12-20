from datetime import date

import pandas as pd

from butler_offline.core.database.database_object import DatabaseObject

COLUMN_KATEGORIE = 'Kategorie'


class Einzelbuchungen(DatabaseObject):
    STATIC_TABLE_HEADER = ['Datum', COLUMN_KATEGORIE, 'Name', 'Wert', 'Tags']
    TABLE_HEADER = STATIC_TABLE_HEADER + ['Dynamisch']
    tmp_kategorie = None
    ausgeschlossene_kategorien = set()

    def __init__(self):
        super().__init__(self.TABLE_HEADER)

    def _sort(self):
        self.content = self.content.sort_values(by=['Datum', COLUMN_KATEGORIE, 'Name', 'Wert'])
        self.content = self.content.reset_index(drop=True)

    def add(self, datum, kategorie, name, wert, dynamisch=False):
        neue_einzelbuchung = pd.DataFrame([[datum, kategorie, name, wert, [], dynamisch]], columns=self.TABLE_HEADER)
        self.content = pd.concat([self.content, neue_einzelbuchung], ignore_index=True)
        self.taint()
        self._sort()

    def get_all(self) -> pd.DataFrame:
        return self.content

    def edit(self, index, buchungs_datum, kategorie, name, wert):
        self.edit_element(index, {
            'Datum': buchungs_datum,
            'Wert': wert,
            'Kategorie': kategorie,
            'Name': name
        })

    def get_jahresausgaben_nach_kategorie_prozentual(self, jahr):
        tabelle = self.select().select_ausgaben().select_year(jahr).content
        return self._berechne_prozentual(tabelle)

    def get_jahreseinnahmen_nach_kategorie_prozentual(self, jahr):
        tabelle = self.select().select_einnahmen().select_year(jahr).content
        return self._berechne_prozentual(tabelle)

    def _berechne_prozentual(self, tabelle):
        if tabelle.empty:
            return {}

        tabelle_gesamtsumme = tabelle.Wert.sum()
        tabelle = tabelle.copy()[[COLUMN_KATEGORIE, 'Wert']].groupby([COLUMN_KATEGORIE]).sum()
        result = {}
        for kategorie, row in tabelle.iterrows():
            result[kategorie] = (row.Wert / tabelle_gesamtsumme) * 100
        return result

    def append_row(self, row: pd.DataFrame):
        self.content = pd.concat([self.content, row], ignore_index=True)
        self._sort()

    def get_monate(self):
        monate = self.content.Datum.copy().map(lambda x: str(x.year) + '_' + str(x.month).rjust(2, '0'))
        return set(monate)

    def get_jahre(self):
        jahre = self.content.Datum.copy().map(lambda x: x.year)
        return set(jahre)

    def get_alle_kategorien(self, hide_ausgeschlossene_kategorien=False):
        return self.get_kategorien_ausgaben(hide_ausgeschlossene_kategorien).union(self.get_kategorien_einnahmen(hide_ausgeschlossene_kategorien))

    def get_kategorien_ausgaben(self, hide_ausgeschlossene_kategorien=False):
        kategorien = set(self.content[self.content.Wert < 0].Kategorie)
        if self.tmp_kategorie:
            kategorien.add(self.tmp_kategorie)

        if hide_ausgeschlossene_kategorien:
            kategorien = kategorien - self.ausgeschlossene_kategorien

        return kategorien

    def get_kategorien_einnahmen(self, hide_ausgeschlossene_kategorien=False):
        kategorien = set(self.content[self.content.Wert > 0].Kategorie)
        if self.tmp_kategorie:
            kategorien.add(self.tmp_kategorie)

        if hide_ausgeschlossene_kategorien:
            kategorien = kategorien - self.ausgeschlossene_kategorien

        return kategorien

    def add_kategorie(self, tmp_kategorie: str):
        self.tmp_kategorie = tmp_kategorie

    def rename_kategorie(self, alter_name: str, neuer_name: str):
        self.content[COLUMN_KATEGORIE].replace(to_replace=alter_name, value=neuer_name, inplace=True)
        self.taint()
        self._sort()

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
            monats_teiler = 13 - min(self.content.Datum).month
        if jahr == today.year:
            data.DatumBackup = data.DatumBackup.map(lambda x: x.month)
            data = data[data.DatumBackup != today.month]
            monats_teiler = monats_teiler - (13 - today.month)
            if monats_teiler == 0:
                return {}
        data.Wert = data.Wert.map(lambda x: abs(x / monats_teiler))
        data = data[['Wert', COLUMN_KATEGORIE]]
        data = data.groupby(by=COLUMN_KATEGORIE).sum()
        data = data.sort_index()
        result = {}
        for kategorie, wert in data.iterrows():
            result[kategorie] = "%.2f" % wert['Wert']
        return result

    def get_static_content(self):
        static_content = self.content.copy()[self.content.Dynamisch == False]
        return static_content[self.STATIC_TABLE_HEADER]
