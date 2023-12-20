from datetime import datetime, date
from typing import List
import pandas as pd
import logging

from butler_offline.core.frequency import get_function_for_name
from butler_offline.core.database.database_object import DatabaseObject, map_column_types


class Dauerauftraege(DatabaseObject):

    _TABLE_HEADER_START_DATUM: str = 'Startdatum'
    _TABLE_HEADER_ENDE_DATUM: str = 'Endedatum'
    _TABLE_HEADER_KATEGORIE: str = 'Kategorie'
    _TABLE_HEADER_NAME: str = 'Name'
    _TABLE_HEADER_WERT: str = 'Wert'
    _TABLE_HEADER_RHYTHUMS: str = 'Rhythmus'

    SORT_ORDER: List[str] = [
        _TABLE_HEADER_START_DATUM,
        _TABLE_HEADER_ENDE_DATUM,
        _TABLE_HEADER_KATEGORIE,
        _TABLE_HEADER_NAME,
        _TABLE_HEADER_WERT,
        _TABLE_HEADER_RHYTHUMS
    ]

    TABLE_HEADER: List[str] = ['Endedatum', 'Kategorie', 'Name', 'Rhythmus', 'Startdatum', 'Wert']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)

    def parse(self, raw_table) -> None:
        raw_table[self._TABLE_HEADER_START_DATUM] = raw_table[self._TABLE_HEADER_START_DATUM]\
            .map(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
        raw_table[self._TABLE_HEADER_ENDE_DATUM] = raw_table[self._TABLE_HEADER_ENDE_DATUM]\
            .map(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
        self.content = pd.concat([self.content, raw_table], ignore_index=True)
        self._sort()

    def einnahmenausgaben_until_today(self,
                                      startdatum,
                                      endedatum,
                                      frequenzfunktion,
                                      name,
                                      wert,
                                      kategorie):
        laufdatum = startdatum
        iteration = 0
        frequency_function = get_function_for_name(frequenzfunktion)
        result = []
        while laufdatum < date.today() and laufdatum < endedatum:
            abbuchung = self._berechne_abbuchung(laufdatum, kategorie, name, wert)
            result.append(abbuchung)
            iteration += 1
            laufdatum = startdatum + frequency_function(iteration)
        return result

    def get_all_einzelbuchungen_until_today(self):
        all_rows = pd.DataFrame()
        for _, row in self.content.iterrows():
            dauerauftrag_buchungen = self.einnahmenausgaben_until_today(
                row['Startdatum'],
                row['Endedatum'],
                row['Rhythmus'],
                row['Name'],
                row['Wert'],
                row['Kategorie'],
            )
            for buchung in dauerauftrag_buchungen:
                all_rows = pd.concat([all_rows, buchung], ignore_index=True)
        return map_column_types(all_rows)

    def add(self, startdatum, endedatum, kategorie, name, rhythmus, wert):
        neuer_dauerauftrag = pd.DataFrame(
            [[endedatum, kategorie, name, rhythmus, startdatum, wert]],
            columns=self.TABLE_HEADER
            )
        self.content = pd.concat([self.content, neuer_dauerauftrag], ignore_index=True)
        self.taint()
        self._sort()
        logging.info('DATABASE: Dauerauftrag hinzugefügt')

    def aktuelle(self):
        dauerauftraege = self.content.copy()
        dauerauftraege = dauerauftraege[dauerauftraege.Endedatum > date.today()]
        dauerauftraege = dauerauftraege[dauerauftraege.Startdatum < date.today()]
        return self.frame_to_list_of_dicts(dauerauftraege)

    def past(self):
        dauerauftraege = self.content.copy()
        dauerauftraege = dauerauftraege[dauerauftraege.Endedatum < date.today()]
        return self.frame_to_list_of_dicts(dauerauftraege)

    def future(self):
        dauerauftraege = self.content.copy()
        dauerauftraege = dauerauftraege[dauerauftraege.Startdatum > date.today()]
        return self.frame_to_list_of_dicts(dauerauftraege)

    def edit(self, index, startdatum, endedatum, kategorie, name, rhythmus, wert):
        self.edit_element(index, {
            'Startdatum': startdatum,
            'Endedatum': endedatum,
            'Wert': wert,
            'Kategorie': kategorie,
            'Name': name,
            'Rhythmus': rhythmus
        })
        self._sort()

    def _sort(self):
        self.content = self.content.sort_values(by=self.SORT_ORDER)
        self.content = self.content.reset_index(drop=True)

    def rename_kategorie(self, alter_name: str, neuer_name: str):
        self.content[self._TABLE_HEADER_KATEGORIE].replace(to_replace=alter_name, value=neuer_name, inplace=True)
        self.taint()
        self._sort()

    def _berechne_abbuchung(self, laufdatum, kategorie, name, wert):
        return pd.DataFrame(
            [[laufdatum, kategorie, name, wert, True, []]],
            columns=['Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch', 'Tags'])
