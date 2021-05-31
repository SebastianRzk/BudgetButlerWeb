from butler_offline.core.database.database_object import DatabaseObject
import pandas as pd


class Depotwerte(DatabaseObject):
    TABLE_HEADER = ['Name', 'ISIN']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)

    def add(self, name, isin):
        neuer_depotwert = pd.DataFrame([[name, isin]], columns=self.TABLE_HEADER)
        self.content = self.content.append(neuer_depotwert, ignore_index=True)
        self.taint()
        self._sort()

    def get_all(self):
        return self.content

    def edit(self, index, name, isin):
        self.edit_element(index, {
            'Name': name,
            'ISIN': isin
        })

    def get_depotwerte(self):
        return sorted(list(self.content.ISIN))

    def get_depotwerte_descriptions(self):
        result = []
        for isin in self.get_depotwerte():
            result.append({
                'description': self.get_description_for(isin),
                'isin': isin
            })
        return result

    def get_description_for(self, isin):
        name = self.content[self.content.ISIN == isin].Name.to_list()[0]
        return '{} ({})'.format(name, isin)
    
    def get_valid_isins(self):
        isins = sorted(set(self.content.ISIN.to_list()))
        return list(filter(lambda x: len(x) == 12, isins))

    def _sort(self):
        self.content = self.content.sort_values(by=['Name', 'ISIN'])
        self.content = self.content.reset_index(drop=True)
