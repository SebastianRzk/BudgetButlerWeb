from datetime import datetime, date

from butler_offline.core.frequency import get_function_for_name
from butler_offline.core.database.database_object import DatabaseObject
import pandas as pd


class Dauerauftraege(DatabaseObject):

    TABLE_HEADER = ['Endedatum', 'Kategorie', 'Name', 'Rhythmus', 'Startdatum', 'Wert']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)

    def parse(self, raw_table):
        raw_table['Startdatum'] = raw_table['Startdatum'].map(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
        raw_table['Endedatum'] = raw_table['Endedatum'].map(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
        self.content = pd.concat([self.content, raw_table], ignore_index=True)
        self.content = self.content.sort_values(by=['Startdatum'])

    def einnahmenausgaben_until_today(self,
                                      startdatum,
                                      endedatum,
                                      frequenzfunktion,
                                      name,
                                      wert,
                                      kategorie):
        laufdatum = startdatum
        frequency_function = get_function_for_name(frequenzfunktion)
        result = []
        while laufdatum < date.today() and laufdatum < endedatum:
            abbuchung = self._berechne_abbuchung(laufdatum, kategorie, name, wert)
            result.append(abbuchung)
            laufdatum = frequency_function(laufdatum)
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
                row['Kategorie'])
            for buchung in dauerauftrag_buchungen:
                all_rows = pd.concat([all_rows, buchung], ignore_index=True)
        return all_rows

    def add(self, startdatum, endedatum, kategorie, name, rhythmus, wert):
        neuer_dauerauftrag = pd.DataFrame(
            [[endedatum, kategorie, name, rhythmus, startdatum, wert]],
            columns=self.TABLE_HEADER
            )
        self.content = pd.concat([self.content, neuer_dauerauftrag], ignore_index=True)
        self.taint()
        print('DATABASE: Dauerauftrag hinzugefügt')

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

    def _sort(self):
        pass

    def _berechne_abbuchung(self, laufdatum, kategorie, name, wert):
        return pd.DataFrame(
            [[laufdatum, kategorie, name, wert, True]],
            columns=['Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'])
