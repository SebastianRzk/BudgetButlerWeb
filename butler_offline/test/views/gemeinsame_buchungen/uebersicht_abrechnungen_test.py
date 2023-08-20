from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.core import file_system
from butler_offline.views.gemeinsame_buchungen import uebersicht_abrechnungen


ABRECHNUNG_A_CONTENT = '''
#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2017-03-06,Abrechung,Abrechung,-10.0,True
#######MaschinenimportEnd'''
IMPORT_A_CONTENT = '''
#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch
2017-04-06,Import,Import,-10.0,True
2017-04-06,Import,Import,-10.0,True
#######MaschinenimportEnd'''


def test_init():
    filesystem = FileSystemStub()
    filesystem.write(file_system.ABRECHNUNG_PATH+'*Abrechnung_A', ABRECHNUNG_A_CONTENT)
    filesystem.write(file_system.IMPORT_PATH+'*Import_A', IMPORT_A_CONTENT)

    context = uebersicht_abrechnungen.handle_request(
        request=GetRequest(),
        context=uebersicht_abrechnungen.UbersichtAbrechnungenContext(
            filesystem=filesystem
        )
    )

    assert context.is_ok()
    assert context.get('zusammenfassungen') == [{
        'jahr': 2017,
        'monate': [0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0]
    }]
    assert context.get('abrechnungen') == [
        {
            'content': ABRECHNUNG_A_CONTENT,
            'name': '../Abrechnungen/*Abrechnung_A'
        },
        {
            'content': IMPORT_A_CONTENT,
            'name': '../Import/*Import_A'
        }
    ]
