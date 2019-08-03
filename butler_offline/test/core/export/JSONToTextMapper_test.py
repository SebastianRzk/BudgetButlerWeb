from butler_offline.core.export.JSONToTextMapper import JSONToTextMapper

def test_dataframe_from_json_string():
    input_json = '''
    [
    {"id":"122","datum":"2019-07-15","name":"Testausgabe1","kategorie":"Kategorie1","wert":"-1.3"},
    {"id":"123","datum":"2019-07-11","name":"Testausgabe2","kategorie":"Kategorie2","wert":"-0.9"}
    ]
    '''

    expected_text_report = '''

#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2019-07-15,Kategorie1,Testausgabe1,-1.3,False
2019-07-11,Kategorie2,Testausgabe2,-0.9,False
#######MaschinenimportEnd
'''

    text_report = JSONToTextMapper().map(input_json)
    assert text_report == expected_text_report
    
