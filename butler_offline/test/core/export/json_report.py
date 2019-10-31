from butler_offline.core.export.json_report import JSONReport
from butler_offline.viewcore.converter import datum_from_german
import json

def test_dataframe_from_json():
    input_json = '''
    [
    {"id":"122","datum":"2019-07-15","name":"Testausgabe1","kategorie":"Kategorie1","wert":"-1.3"},
    {"id":"123","datum":"2019-07-11","name":"Testausgabe2","kategorie":"Kategorie2","wert":"-0.9"}
    ]
    '''

    dataframe = JSONReport().dataframe_from_json(json.loads(input_json))

    assert len(dataframe) == 2
    assert dataframe.Datum[0] == datum_from_german('15.07.2019')
    assert dataframe.Datum[1] == datum_from_german('11.07.2019')

    assert dataframe.Name[0] == 'Testausgabe1'
    assert dataframe.Name[1] == 'Testausgabe2'

    assert dataframe.Kategorie[0] == 'Kategorie1'
    assert dataframe.Kategorie[1] == 'Kategorie2'

    assert dataframe.Wert[0] == -1.3
    assert dataframe.Wert[1] == -0.9
    
def test_dataframe_from_json_gemeinsam():
    input_json = '''
    [
    {"id":"122","datum":"2019-07-15","name":"Testausgabe1","kategorie":"Kategorie1","wert":"-1.3", "user": "unknown", "zielperson": "Sebastian"},
    {"id":"123","datum":"2019-07-11","name":"Testausgabe2","kategorie":"Kategorie2","wert":"-0.9", "user": "unknown", "zielperson": "other"}
    ]
    '''

    dataframe = JSONReport().dataframe_from_json_gemeinsam(json.loads(input_json))

    assert len(dataframe) == 2
    assert dataframe.Datum[0] == datum_from_german('15.07.2019')
    assert dataframe.Datum[1] == datum_from_german('11.07.2019')

    assert dataframe.Name[0] == 'Testausgabe1'
    assert dataframe.Name[1] == 'Testausgabe2'

    assert dataframe.Kategorie[0] == 'Kategorie1'
    assert dataframe.Kategorie[1] == 'Kategorie2'

    assert dataframe.Wert[0] == -1.3
    assert dataframe.Wert[1] == -0.9

    assert dataframe.Person[0] == "Sebastian"
    assert dataframe.Person[1] == "other"
