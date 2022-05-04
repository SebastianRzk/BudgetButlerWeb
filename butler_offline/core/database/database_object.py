import pandas as pd
from datetime import datetime
from butler_offline.core.database.selector import Selektor
from butler_offline.core.database.stated_object import StatedObject

class DatabaseObject(StatedObject):

    def __init__(self, stored_columns=[]):
        super().__init__()
        self.content = pd.DataFrame({}, columns=stored_columns)

    def get(self, db_index):
        row = self.content.loc[db_index]
        return {**row.to_dict(), **{'index': db_index}}

    def edit_element(self, index, new_element_map):
        for column_name in new_element_map.keys():
            self.content.loc[self.content.index[[index]], column_name] = new_element_map[column_name]
        self._sort()
        self.taint()

    def parse(self, raw_table):
        if 'Datum' in raw_table.columns:
            raw_table['Datum'] = raw_table['Datum'].map(lambda x:  datetime.strptime(x, '%Y-%m-%d').date())
        if 'Dynamisch' in self.content.columns:
            raw_table['Dynamisch'] = False
        self.content = pd.concat([self.content, raw_table], ignore_index=True)
        self._sort()

    def delete(self, index):
        self.content = self.content.drop(index)
        self.taint()

    def select(self):
        return Selektor(self.content)

    def get_static_content(self):
        return self.content

    def frame_to_list_of_dicts(self, dataframe):
        result_list = []
        for index, row_data in dataframe.iterrows():
            row = self._row_to_dict(dataframe.columns, index, row_data)
            result_list.append(row)
        return result_list

    def _row_to_dict(self, columns, index, row_data):
        row = {'index': index}
        for key in columns:
            row[key] = row_data[key]
        return row

