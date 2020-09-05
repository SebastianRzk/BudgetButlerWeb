from butler_offline.core.database.database_object import DatabaseObject
import pandas as pd


class Sparbuchungen(DatabaseObject):
    TYP_MANUELLER_AUFTRAG = 'Manueller Auftrag'

    AUFTRAGS_TYPEN = [TYP_MANUELLER_AUFTRAG]
    TABLE_HEADER = ['Datum', 'Name', 'Wert', 'Typ', 'Konto' , 'Dynamisch']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)


    def add(self, datum, name, wert, typ, konto, dynamisch=False):
        neue_sparbuchung = pd.DataFrame([[datum, name, wert, typ, konto, dynamisch]], columns=self.TABLE_HEADER)
        self.content = self.content.append(neue_sparbuchung, ignore_index=True)
        self.taint()
        self._sort()

    def get_all(self):
        return self.content

    def edit(self, index, datum, name, wert, typ, konto,):
        self.edit_element(index, {
            'Datum': datum,
            'Wert': wert,
            'Typ': typ,
            'Konto': konto,
            'Name': name
        })

    def _sort(self):
        self.content = self.content.sort_values(by=['Datum', 'Konto', 'Name'])
        self.content = self.content.reset_index(drop=True)

    def get_static_content(self):
        static_content = self.content.copy()[self.content.Dynamisch==False]
        return static_content[['Datum', 'Name', 'Wert', 'Typ', 'Konto']]
