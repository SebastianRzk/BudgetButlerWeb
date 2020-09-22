from butler_offline.core.database.database_object import DatabaseObject
import pandas as pd


class Depotauszuege(DatabaseObject):
    TABLE_HEADER = ['Datum', 'Depotwert', 'Konto', 'Wert']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)


    def add(self, datum, depotwert, konto, wert):
        neuer_auszug = pd.DataFrame([[datum, depotwert, konto, wert]], columns=self.TABLE_HEADER)
        self.content = self.content.append(neuer_auszug, ignore_index=True)
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

    def _sort(self):
        self.content = self.content.sort_values(by=['Datum', 'Konto', 'Depotwert'])
        self.content = self.content.reset_index(drop=True)
