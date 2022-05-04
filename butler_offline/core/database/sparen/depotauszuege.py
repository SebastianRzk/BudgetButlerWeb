from butler_offline.core.database.database_object import DatabaseObject
import pandas as pd
from butler_offline.core.time import today


class Depotauszuege(DatabaseObject):
    TABLE_HEADER = ['Datum', 'Depotwert', 'Konto', 'Wert']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)

    def add(self, datum, depotwert, konto, wert):
        neuer_auszug = pd.DataFrame([[datum, depotwert, konto, wert]], columns=self.TABLE_HEADER)
        self.content = pd.concat([self.content, neuer_auszug], ignore_index=True)
        self.taint()
        self._sort()

    def get_all(self):
        return self.content

    def edit(self, index, datum, depotwert, konto, wert):
        self.edit_element(index, {
            'Datum': datum,
            'Depotwert': depotwert,
            'Konto': konto,
            'Wert': wert
        })

    def get_by(self, datum, konto):
        auszuege = self.content[self.content.Konto == konto].copy()
        auszuege = auszuege[auszuege.Datum == datum]
        return auszuege

    def get_latest_datum_by(self, konto):
        auszuege = self.content[self.content.Konto == konto].copy()
        if len(auszuege) == 0:
            return None
        return auszuege.Datum.max()

    def resolve_index(self, datum, konto, depotwert):
        auszuege = self.get_by(datum, konto)
        result_frame = auszuege[auszuege.Depotwert == depotwert]
        if len(result_frame) == 0:
            return None
        return result_frame.index[0]

    def exists_wert(self, konto, depotwert):
        frame = self.content[self.content.Konto == konto].copy()
        frame = frame[frame.Depotwert == depotwert]
        return len(frame) != 0

    def get_kontostand_by(self, konto):
        latest_datum = self.get_latest_datum_by(konto)
        if not latest_datum:
            return 0
        auszuege = self.content[self.content.Konto == konto].copy()
        auszug = auszuege[auszuege.Datum == latest_datum]
        return auszug.Wert.sum()

    def get_depotwert_by(self, depotwert):
        auszuege = self.content[self.content.Depotwert == depotwert].copy()
        if len(auszuege) == 0:
            return 0

        kontos = set(auszuege.Konto.tolist())
        gesamt = 0

        for konto in kontos:
            konto_auszuege = auszuege[auszuege.Konto == konto].copy()
            datum_max = konto_auszuege.Datum.max()
            gesamt += konto_auszuege[konto_auszuege.Datum == datum_max].Wert.sum()

        return gesamt

    def delete_depotauszug(self, datum, konto):
        index = self._resolve_indices(konto, datum)
        for i in index:
            self.delete(i)

    def _resolve_indices(self, konto, datum):
        values = self.content[self.content.Konto == konto].copy()
        return values[values.Datum == datum].index.tolist()

    def get_all(self):
        return self.content

    def resolve_konto(self, index):
        return self.content.loc[index, 'Konto']

    def resolve_datum(self, index):
        return self.content.loc[index, 'Datum']

    def _sort(self):
        self.content = self.content.sort_values(by=['Datum', 'Konto', 'Depotwert'])
        self.content = self.content.reset_index(drop=True)

    def select_max_year(self, year):
        include = self.content.copy()
        include['datum_filter'] = include.Datum.map(lambda x: x.year)
        include = include[include.datum_filter <= year].copy()
        del include['datum_filter']
        selected = Depotauszuege()
        selected.content = include
        return selected

    def get_isins_invested_by(self, date=None):
        if not date:
            date = today()
        values = self.content[['Datum', 'Depotwert', 'Wert']].copy()
        values.Depotwert = values.Depotwert.astype(str)
        values = values[values.Depotwert.str.len() == 12]
        values = values[values.Datum <= date]
        values = values.sort_values(by='Datum', ascending=True)
        values = values.groupby('Depotwert').last()
        values = values[values.Wert > 0]
        values = values.sort_values('Wert', ascending=False)
        return values.index.to_list()


