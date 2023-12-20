import pandas as pd
from datetime import datetime
from butler_offline.core.database.selector import Selektor
from butler_offline.core.database.stated_object import StatedObject


def map_column_types(content: pd.DataFrame):
    if 'Dynamisch' in content.columns:
        content['Dynamisch'] = content['Dynamisch'].astype('bool')
    if 'Wert' in content.columns:
        content['Wert'] = content['Wert'].astype('float')
    return content


class DatabaseObject(StatedObject):

    def __init__(self, stored_columns: list[str]):
        super().__init__()
        self.content = pd.DataFrame({}, columns=stored_columns)
        self.content = map_column_types(self.content)

    def get(self, db_index):
        row = self.content.loc[db_index]
        return {**row.to_dict(), **{'index': db_index}}

    def edit_element(self, index, new_element_map):
        for column_name in new_element_map.keys():
            self.content.loc[self.content.index[[index]], column_name] = new_element_map[column_name]
        self._sort()
        self.taint()

    def parse(self, raw_table: pd.DataFrame):
        if 'Datum' in raw_table.columns:
            raw_table['Datum'] = raw_table['Datum'].map(lambda x:  datetime.strptime(x, '%Y-%m-%d').date())
        if 'Dynamisch' in self.content.columns:
            raw_table['Dynamisch'] = False
        raw_table = map_column_types(raw_table)
        self.content = pd.concat([self.content, raw_table], ignore_index=True)
        self._sort()

    def delete(self, index):
        self.content = self.content.drop(index)
        self.taint()

    def select(self) -> Selektor:
        return Selektor(self.content.copy(deep=True))

    def get_static_content(self) -> pd.DataFrame:
        return self.content

    def frame_to_list_of_dicts(self, dataframe):
        result_list = []
        for index, row_data in dataframe.iterrows():
            row = row_to_dict(dataframe.columns, index, row_data)
            result_list.append(row)
        return result_list

    def _sort(self):
        raise Exception('not implemented')


def row_to_dict(columns, index, row_data):
    row = {'index': index}
    for key in columns:
        row[key] = row_data[key]
    return row

