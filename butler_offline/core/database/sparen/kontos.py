from butler_offline.core.database.database_object import DatabaseObject
import pandas as pd


class Kontos(DatabaseObject):
    TYP_SPARKONTO = 'Sparkonto'

    KONTO_TYPEN = [TYP_SPARKONTO]
    TABLE_HEADER = ['Kontoname', 'Kontotyp']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)


    def add(self, kontoname, kontotyp):
        neues_konto = pd.DataFrame([[kontoname, kontotyp]], columns=self.TABLE_HEADER)
        self.content = self.content.append(neues_konto, ignore_index=True)
        self.taint()
        self._sort()

    def get_all(self):
        return self.content

    def edit(self, index, kontoname, kontotyp):
        self.edit_element(index, {
            'Kontoname': kontoname,
            'Kontotyp': kontotyp
        })

    def _sort(self):
        self.content = self.content.sort_values(by=['Kontotyp', 'Kontoname'])
        self.content = self.content.reset_index(drop=True)
