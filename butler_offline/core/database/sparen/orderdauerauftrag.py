from butler_offline.core.database.database_object import DatabaseObject
from butler_offline.core.frequency import get_function_for_name
from datetime import datetime
import pandas as pd
from datetime import date


class OrderDauerauftrag(DatabaseObject):
    TABLE_HEADER = ['Startdatum', 'Endedatum', 'Rhythmus', 'Name', 'Konto', 'Depotwert', 'Wert']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)

    def add(self, startdatum, endedatum, rhythmus, name, konto, depotwert, wert):
        neue_order = pd.DataFrame(
            [[startdatum, endedatum, rhythmus, name, konto, depotwert, wert]],
            columns=self.TABLE_HEADER)
        self.content = pd.concat([self.content, neue_order], ignore_index=True)
        self.taint()
        self._sort()

    def get_all(self):
        return self.content

    def parse(self, raw_table):
        raw_table['Startdatum'] = raw_table['Startdatum'].map(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
        raw_table['Endedatum'] = raw_table['Endedatum'].map(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
        self.content = pd.concat([self.content, raw_table], ignore_index=True)
        self.content = self.content.sort_values(by=['Startdatum'])

    def edit(self, index, startdatum, endedatum, rhythmus, name, konto, depotwert, wert):
        self.edit_element(index, {
            'Startdatum': startdatum,
            'Endedatum': endedatum,
            'Rhythmus': rhythmus,
            'Name': name,
            'Konto': konto,
            'Depotwert': depotwert,
            'Wert': wert
        })

    def get_all_order_until_today(self):
        all_rows = pd.DataFrame()
        for _, row in self.content.iterrows():
            dauerauftrag_buchungen = self._order_until_today(
                row['Startdatum'],
                row['Endedatum'],
                row['Rhythmus'],
                row['Name'],
                row['Konto'],
                row['Depotwert'],
                row['Wert'])
            for buchung in dauerauftrag_buchungen:
                all_rows = pd.concat([all_rows, buchung], ignore_index=True)
        return all_rows

    def _order_until_today(self,
                           startdatum,
                           endedatum,
                           frequenzfunktion,
                           name,
                           konto,
                           depotwert,
                           wert,):
        laufdatum = startdatum
        iteration = 0
        frequency_function = get_function_for_name(frequenzfunktion)
        result = []
        while laufdatum < date.today() and laufdatum < endedatum:
            abbuchung = self._berechne_order(laufdatum, konto, depotwert, name, wert)
            result.append(abbuchung)
            iteration += 1
            laufdatum = startdatum + frequency_function(iteration)
        return result

    def _berechne_order(self, laufdatum, konto, depotwert, name, wert):
        return pd.DataFrame([[laufdatum, konto, depotwert, name, wert, True]],
                            columns=['Datum', 'Konto', 'Depotwert', 'Name', 'Wert', 'Dynamisch'])

    def _sort(self):
        self.content = self.content.sort_values(by=['Startdatum', 'Endedatum', 'Name'])
        self.content = self.content.reset_index(drop=True)

    def aktuelle_raw(self):
        dauerauftraege = self.content.copy()
        dauerauftraege = dauerauftraege[dauerauftraege.Endedatum > date.today()]
        return dauerauftraege[dauerauftraege.Startdatum < date.today()]

    def aktuelle(self):
        return self.frame_to_list_of_dicts(self.aktuelle_raw())

    def past(self):
        dauerauftraege = self.content.copy()
        dauerauftraege = dauerauftraege[dauerauftraege.Endedatum < date.today()]
        return self.frame_to_list_of_dicts(dauerauftraege)

    def future(self):
        dauerauftraege = self.content.copy()
        dauerauftraege = dauerauftraege[dauerauftraege.Startdatum > date.today()]
        return self.frame_to_list_of_dicts(dauerauftraege)
