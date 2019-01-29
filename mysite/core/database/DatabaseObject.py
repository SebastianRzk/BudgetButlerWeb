'''
Created on 03.05.2018

@author: sebastian
'''
import pandas as pd
from datetime import datetime

class DatabaseObject:

    def __init__(self, stored_columns=[]):
        self.tainted = 0
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
        raw_table['Datum'] = raw_table['Datum'].map(lambda x:  datetime.strptime(x, '%Y-%m-%d').date())
        if 'Dynamisch' in self.content.columns:
            raw_table['Dynamisch'] = False
        self.content = self.content.append(raw_table, ignore_index=True)
        self._sort()

    def delete(self, index):
        self.content = self.content.drop(index)
        self.taint()

    def taint(self):
        self.tainted = self.tainted + 1

    def taint_number(self):
        return self.tainted

    def de_taint(self):
        self.tainted = 0
