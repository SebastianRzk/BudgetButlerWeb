import json
import pandas as pd
from datetime import datetime

class JSONReport:
    def dataframe_from_json_string(self, data):
        json_data = json.loads(data)
        dataframe = pd.DataFrame(json_data)
        dataframe['Datum'] = dataframe.datum.map(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
        dataframe['Kategorie'] = dataframe.kategorie
        dataframe['Name'] = dataframe.name
        dataframe['Wert'] = pd.to_numeric(dataframe.wert)
        dataframe['Dynamisch'] = False
        return dataframe[['Datum','Kategorie','Name','Wert','Dynamisch']]
        
