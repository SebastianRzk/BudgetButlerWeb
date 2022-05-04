from butler_offline.core.database.database_object import DatabaseObject
import pandas as pd


class Depotwerte(DatabaseObject):
    TYP = 'Typ'
    TYP_ETF = 'ETF'
    TYP_FOND = 'Fond'
    TYP_EINZELAKTIE = 'Einzelaktie'
    TYP_CRYPTO = 'Crypto'
    TYP_ROBOT = 'Robot'
    TYP_DEFAULT = TYP_ETF

    TABLE_HEADER = ['Name', 'ISIN', 'Typ']
    TYPES = [TYP_ETF, TYP_FOND, TYP_EINZELAKTIE, TYP_CRYPTO, TYP_ROBOT]

    def __init__(self):
        super().__init__(self.TABLE_HEADER)

    def add(self, name, isin, typ):
        neuer_depotwert = pd.DataFrame([[name, isin, typ]], columns=self.TABLE_HEADER)
        self.content = pd.concat([self.content, neuer_depotwert], ignore_index=True)
        self.taint()
        self._sort()

    def get_all(self):
        return self.content

    def edit(self, index, name, isin, typ):
        self.edit_element(index, {
            'Name': name,
            'ISIN': isin,
            'Typ': typ
        })

    def parse_and_migrate(self, raw_table):
        migrated_raw_table = self.migrate(raw_table)
        self.parse(migrated_raw_table)

    def migrate(self, raw_table):
        if self.TYP not in raw_table.columns:
            raw_table[self.TYP] = self.TYP_DEFAULT
        return raw_table

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

    def get_isin_nach_typ(self):
        content = self.content.copy()
        result_frame = content[['ISIN', 'Typ']].groupby(by='Typ').agg({'ISIN': lambda x: list(x)})
        result = {}

        for depotwert_type, name_list in result_frame.iterrows():
            result[depotwert_type] = name_list['ISIN']

        return result
