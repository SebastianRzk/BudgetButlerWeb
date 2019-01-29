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

    def taint(self):
        self.tainted = self.tainted + 1

    def taint_number(self):
        return self.tainted

    def de_taint(self):
        self.tainted = 0
