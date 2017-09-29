'''
Created on 23.09.2017

@author: sebastian
'''
from datetime import datetime
from pandas.core.frame import DataFrame

class Sonderzeiten:
    content = DataFrame({}, columns=['Datum', 'Dauer', 'Typ', 'Arbeitgeber'])



    def parse(self, raw_table):

        raw_table['Datum'] = raw_table['Datum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())
        raw_table['Dauer'] = raw_table['Dauer'].map(lambda x:  datetime.strptime(x, '%H:%M:%S').time())
        self.content = self.content.append(raw_table)

    def add(self, buchungs_datum, dauer, typ, arbeitgeber):
        row = DataFrame([[buchungs_datum, dauer, typ, arbeitgeber]], columns=['Datum', 'Dauer', 'Typ', 'Arbeitgeber'])
        self.content = self.content.append(row, ignore_index=True)
