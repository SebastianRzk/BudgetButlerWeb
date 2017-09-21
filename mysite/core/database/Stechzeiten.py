'''
Created on 19.09.2017

@author: sebastian
'''
from datetime import date, datetime, timedelta

from pandas.core.frame import DataFrame


class Stechzeiten:
    persitent_stechzeiten_columns = ['Datum', 'Einstechen', 'Ausstechen', 'Arbeitgeber']
    content = DataFrame({}, columns=persitent_stechzeiten_columns)

    def parse(self, raw_table):
        raw_table['Datum'] = raw_table['Datum'].map(lambda x:  datetime.strptime(x, "%Y-%m-%d").date())
        raw_table['Einstechen'] = raw_table['Einstechen'].map(lambda x:  datetime.strptime(x, '%H:%M:%S').time())
        raw_table['Ausstechen'] = raw_table['Ausstechen'].map(lambda x:  datetime.strptime(x, '%H:%M:%S').time())
        
        raw_table['Arbeitszeit'] = timedelta(seconds=0)
        for index, row in raw_table.iterrows():
            arbeitszeit = datetime.combine(date.today(), row.Ausstechen) - datetime.combine(date.today(), row.Einstechen)
            arbeitszeit = self._ziehe_pause_ab(arbeitszeit, row.Arbeitgeber)
            raw_table.loc[raw_table.index[[index]], 'Arbeitszeit'] = arbeitszeit
            print(f'berechnete Arbeitszeit: {arbeitszeit}')
        raw_table = raw_table.sort_values(by=['Datum'])
        self.content = self.content.append(raw_table, ignore_index=True)



    def add(self, buchungs_datum, einstechen, ausstechen, arbeitgeber):
        '''
        add a new stechzeit to the database
        '''
        arbeitszeit = datetime.combine(date.today(), ausstechen) - datetime.combine(date.today(), einstechen)
        stechzeit = DataFrame([[buchungs_datum, einstechen, ausstechen, arbeitgeber, self._ziehe_pause_ab(arbeitszeit, arbeitgeber)]], columns=['Datum', 'Einstechen', 'Ausstechen', 'Arbeitgeber', 'Arbeitszeit'])
        self.content = self.content.append(stechzeit, ignore_index=True)
        print('DATABASE: stechzeit hinzugefügt')

    def edit(self, index, buchungs_datum, einstechen, ausstechen, arbeitgeber):
        '''
        edit an existing stechzeit by tableIndex
        '''
        self.content.loc[self.content.index[[index]], 'Datum'] = buchungs_datum
        self.content.loc[self.content.index[[index]], 'Einstechen'] = einstechen
        self.content.loc[self.content.index[[index]], 'Ausstechen'] = ausstechen
        self.content.loc[self.content.index[[index]], 'Arbeitgeber'] = arbeitgeber


    def _ziehe_datev_ab(self, value):
        print("value", value)
        if value <= timedelta(hours=2):
            return value

        if value <= timedelta(hours=2, minutes=14):
            return timedelta(hours=2)

        if value <= timedelta(hours=4, minutes=45):
            return value - timedelta(minutes=15)

        if value <= timedelta(hours=4, minutes=59):
            return timedelta(hours=4, minutes=30)

        if value <= timedelta(hours=6, minutes=30):
            return value - timedelta(minutes=30)

        if value <= timedelta(hours=6, minutes=44):
            return timedelta(hours=6)

        return value - timedelta(minutes=45)

    def _ziehe_pause_ab(self, value, arbeitgeber):
        if arbeitgeber == "DATEV":
            return self._ziehe_datev_ab(value)
        return value

