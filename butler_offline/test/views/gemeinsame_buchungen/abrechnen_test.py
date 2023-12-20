from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.request_stubs import PostRequest
from butler_offline.core import file_system
from butler_offline.views.gemeinsame_buchungen import abrechnen
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.core.database import Database
from butler_offline.core.configuration_provider import configuration_provider
from datetime import time, datetime


def test_abrechnen():
    testdb = Database()
    testdb.gemeinsamebuchungen.add(datum('01.01.2010'), 'Eine Katgorie', 'Ein Name', 2.60, 'Eine Person')

    abrechnen.handle_request(
        request=PostRequest({
            'set_mindate': '01.01.2010',
            'set_maxdate': '01.01.2010',
            'set_ergebnis': '',
            'set_verhaeltnis': '50'}),
        context=abrechnen.AbrechnenContext(
            database=testdb,
            filesystem=FileSystemStub(),
            now=datetime.combine(datum('01.01.2019'), time.min)
        )
    )

    assert testdb.einzelbuchungen.select().count() == 1
    assert testdb.einzelbuchungen.get_all().Wert[0] == '1.30'


def test_abrechnen_should_create_abrechnung_online():
    configuration_provider.set_configuration('PARTNERNAME', 'Partner')
    file_system.INSTANCE = FileSystemStub()
    testdb = Database(name='Test_User')
    testdb.gemeinsamebuchungen.add(datum('01.01.2010'), 'Eine Katgorie', 'Ein Name', 2.60, 'Eine Person')

    context = abrechnen.handle_request(
        request=PostRequest({
            'set_mindate': '01.01.2010',
            'set_maxdate': '01.01.2010',
            'set_ergebnis': '%Ergebnis%',
            'set_verhaeltnis': 50
        }),
        context=abrechnen.AbrechnenContext(
            database=testdb,
            filesystem=FileSystemStub(),
            now=datetime.combine(datum('01.01.2019'), time.min)
        )
    )

    assert context.get('abrechnungstext') == '''Abrechnung vom 01.01.2019 
(01.01.2010-01.01.2010)<br>########################################<br> 
Ergebnis:<br>%Ergebnis%<br><br>Ausgaben von 
Partner             0.00<br>Ausgaben von 
Test_User           
0.00<br>--------------------------------------<br>Gesamt                           
2.60<br><br><br>########################################<br> 
Gesamtausgaben pro Person 
<br>########################################<br> 
Datum      Kategorie    
Name                    Wert<br>01.01.2010  
Eine Katgorie Ein Name                
1.30<br><br><br>########################################<br> 
Ausgaben von 
Partner<br>########################################<br> 
Datum      Kategorie    
Name                    
Wert<br><br><br>########################################<br> 
Ausgaben von 
Test_User<br>########################################<br> 
Datum      Kategorie    
Name                    
Wert<br><br><br>#######MaschinenimportStart<br>Datum,Kategorie,Name,Wert,Dynamisch<br>2010-01-01,Eine 
Katgorie,Ein 
Name,1.30,False<br>#######MaschinenimportEnd<br>'''.replace('\n', '')


def test_abrechnen_should_create_abrechnung_on_disk():
    configuration_provider.set_configuration('PARTNERNAME', 'Partner')
    testdb = Database(name='Test_User')
    filesystem = FileSystemStub()
    testdb.gemeinsamebuchungen.add(datum('01.01.2010'), 'Eine Katgorie', 'Ein Name', 2.60, 'Eine Person')

    abrechnen.handle_request(
        request=PostRequest({
            'set_mindate': '01.01.2010',
            'set_maxdate': '01.01.2010',
            'set_ergebnis': '%Ergebnis%',
            'set_verhaeltnis': 50
        }),
        context=abrechnen.AbrechnenContext(
            database=testdb,
            filesystem=filesystem,
            now=datetime.combine(datum('01.01.2019'), time.min)
        ))

    abrechnung = filesystem.read('./Abrechnungen/Abrechnung_2019-01-01 00:00:00')
    assert abrechnung == ['Abrechnung vom 01.01.2019 (01.01.2010-01.01.2010)\n',
                          '########################################\n',
                          ' Ergebnis:\n',
                          '%Ergebnis%\n',
                          '\n',
                          'Ausgaben von Partner             0.00\n',
                          'Ausgaben von Test_User           0.00\n',
                          '--------------------------------------\n',
                          'Gesamt                           2.60\n',
                          '\n',
                          '\n',
                          '########################################\n',
                          ' Gesamtausgaben pro Person \n',
                          '########################################\n',
                          ' Datum      Kategorie    Name                    Wert\n',
                          '01.01.2010  Eine Katgorie Ein Name                1.30\n',
                          '\n',
                          '\n',
                          '########################################\n',
                          ' Ausgaben von Partner\n',
                          '########################################\n',
                          ' Datum      Kategorie    Name                    Wert\n',
                          '\n',
                          '\n',
                          '########################################\n',
                          ' Ausgaben von Test_User\n',
                          '########################################\n',
                          ' Datum      Kategorie    Name                    Wert\n',
                          '\n',
                          '\n',
                          '#######MaschinenimportStart\n',
                          'Datum,Kategorie,Name,Wert,Dynamisch\n',
                          '2010-01-01,Eine Katgorie,Ein Name,1.30,False\n',
                          '#######MaschinenimportEnd\n',
                          '']


def test_index_should_be_secured_by_request_handler():
    def index():
        abrechnen.index(PostRequest({
            'set_mindate': '01.01.2010',
            'set_maxdate': '01.01.2010',
            'set_ergebnis': '%Ergebnis%',
            'set_verhaeltnis': 50
        }))

    result = run_in_mocked_handler(index_handle=index)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['shared/present_abrechnung.html']
