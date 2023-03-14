from butler_offline.core.export.text_report import TextReportReader, TextReportWriter
from pandas import DataFrame


def test_read():
    report = '''
#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2017-03-06,Essen,Edeka,-10.0,True
#######MaschinenimportEnd
    '''
    reader = TextReportReader()

    result = reader.read(report)

    assert len(result) == 1
    assert result.Datum[0] == '2017-03-06'
    assert result.Kategorie[0] == 'Essen'
    assert result.Name[0] == 'Edeka'
    assert result.Wert[0] == -10.0
    assert result.Dynamisch[0]


def test_generate_report():
    data = DataFrame([['2017-03-06', 'Essen', 'Edeka', -10.0, True]],
                     columns=['Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'])
    writer = TextReportWriter()

    result = writer.generate_report(data)

    assert result == '''

#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2017-03-06,Essen,Edeka,-10.0,True
#######MaschinenimportEnd
'''

