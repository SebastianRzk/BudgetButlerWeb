import pandas as pd
from datetime import datetime


class JSONReport:
    def dataframe_from_json(self, json_data):
        dataframe = self._map_basic_values(json_data)
        return dataframe[['Datum','Kategorie','Name','Wert','Dynamisch']]

    def _map_basic_values(self, json_data):
        dataframe = pd.DataFrame(json_data)
        dataframe['Datum'] = dataframe.datum.map(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
        dataframe['Kategorie'] = dataframe.kategorie
        dataframe['Name'] = dataframe.name
        dataframe['Wert'] = pd.to_numeric(dataframe.wert)
        dataframe['Dynamisch'] = False
        return dataframe

    def dataframe_from_json_gemeinsam(self, json_data):
        dataframe = self._map_basic_values(json_data)
        dataframe['Person'] = dataframe['zielperson']
        return dataframe[['Datum','Kategorie','Name','Wert', 'Person','Dynamisch']]

