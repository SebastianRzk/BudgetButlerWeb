'''
Created on 03.05.2018

@author: sebastian
'''
import pandas as pd

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

    def taint(self):
        self.tainted = self.tainted + 1

    def taint_number(self):
        return self.tainted

    def de_taint(self):
        self.tainted = 0
