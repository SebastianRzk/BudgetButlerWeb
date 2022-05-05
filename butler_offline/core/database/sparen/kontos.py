from butler_offline.core.database.database_object import DatabaseObject
import pandas as pd


class Kontos(DatabaseObject):
    TYP = 'Kontotyp'
    TYP_SPARKONTO = 'Sparkonto'
    TYP_GENOSSENSCHAFTSANTEILE = 'Genossenschafts-Anteile'
    TYP_DEPOT = 'Depot'

    KONTO_TYPEN = [TYP_SPARKONTO, TYP_GENOSSENSCHAFTSANTEILE, TYP_DEPOT]
    TABLE_HEADER = ['Kontoname', TYP]

    def __init__(self):
        super().__init__(self.TABLE_HEADER)

    def add(self, kontoname, kontotyp):
        neues_konto = pd.DataFrame([[kontoname, kontotyp]], columns=self.TABLE_HEADER)
        self.content = pd.concat([self.content, neues_konto], ignore_index=True)
        self.taint()
        self._sort()

    def get_all(self):
        return self.content

    def edit(self, index, kontoname, kontotyp):
        self.edit_element(index, {
            'Kontoname': kontoname,
            'Kontotyp': kontotyp
        })

    def get_sparfaehige_kontos(self):
        query = '{} == "{}" | {} == "{}"'.format(self.TYP, self.TYP_SPARKONTO, self.TYP, self.TYP_GENOSSENSCHAFTSANTEILE)
        return sorted(list(self.content.query(query).Kontoname))

    def get_depots(self):
        return sorted(list(self.content[self.content.Kontotyp == self.TYP_DEPOT].Kontoname))

    def _sort(self):
        self.content = self.content.sort_values(by=['Kontotyp', 'Kontoname'])
        self.content = self.content.reset_index(drop=True)
