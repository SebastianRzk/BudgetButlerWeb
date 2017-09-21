'''
Created on 21.09.2017

@author: sebastian
'''
from datetime import datetime

from pandas.core.frame import DataFrame


class Sollzeiten:
    persistent_sollzeiten_columns = ['Startdatum', 'Endedatum', 'Dauer', 'Arbeitgeber']
    content = DataFrame({}, columns=persistent_sollzeiten_columns)

    def parse(self, raw_table):
        raw_table['Startdatum'] = raw_table['Startdatum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())
        raw_table['Endedatum'] = raw_table['Endedatum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())
        raw_table['Dauer'] = raw_table['Dauer'].map(lambda x:  datetime.strptime(x, '%H:%M:%S').time())

        self.content = self.content.append(raw_table, ignore_index=True)

    def add(self, startdatum, endedatum, dauer, arbeitgeber):
        neue_soll_zeit = DataFrame([[startdatum, endedatum, dauer, arbeitgeber]], columns=self.persistent_sollzeiten_columns)
        self.content = self.content.append(neue_soll_zeit, ignore_index=True)

    def edit(self, index, startdatum, endedatum, dauer, arbeitgeber):
        self.content.loc[self.content.index[[index]], 'Startdatum'] = startdatum
        self.content.loc[self.content.index[[index]], 'Endedatum'] = endedatum
        self.content.loc[self.content.index[[index]], 'Dauer'] = dauer
        self.content.loc[self.content.index[[index]], 'Arbeitgeber'] = arbeitgeber

    def get_sollzeiten_liste(self):
        return self.frame_to_list_of_dicts(self.content)

    def frame_to_list_of_dicts(self, dataframe):
        result_list = []
        for index, row_data in dataframe.iterrows():
            row = self._row_to_dict(dataframe.columns, index, row_data)
            result_list.append(row)

        return result_list

    def _row_to_dict(self, columns, index, row_data):
        row = {}
        row['index'] = index
        for key in columns:
            row[key] = row_data[key]
        return row