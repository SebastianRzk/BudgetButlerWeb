import unittest

from butler_offline.core import time, configuration_provider
from butler_offline.viewcore import request_handler
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest, PostRequest, VersionedPostRequest
from butler_offline.test.database_util import untaint_database
from butler_offline.core import file_system
from butler_offline.views.gemeinsame_buchungen import gemeinsam_abrechnen
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.context import get_error_message


class Gemeinsamabrechnen(unittest.TestCase):
    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        configuration_provider.LOADED_CONFIG = None
        persisted_state.DATABASE_INSTANCE = None
        persisted_state.DATABASES = []
        time.stub_today_with(datum('01.01.2019'))
        configuration_provider.set_configuration('PARTNERNAME', 'Partner')
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        gemeinsam_abrechnen.index(GetRequest())

    def test_abrechnen(self):
        self.set_up()
        testdb = persisted_state.database_instance()
        testdb.gemeinsamebuchungen.add(datum('01.01.2010'), 'Eine Katgorie', 'Ein Name', 2.60, 'Eine Person')
        untaint_database(database=testdb)

        gemeinsam_abrechnen.abrechnen(VersionedPostRequest({
            'set_mindate': '01.01.2010',
            'set_maxdate': '01.01.2010',
            'set_ergebnis': '',
            'set_verhaeltnis': '50'}))

        assert testdb.einzelbuchungen.anzahl() == 1
        assert testdb.einzelbuchungen.get_all().Wert[0] == '1.30'

    def test_abrechnen_should_create_abrechnung_online(self):
        self.set_up()
        testdb = persisted_state.database_instance()
        testdb.gemeinsamebuchungen.add(datum('01.01.2010'), 'Eine Katgorie', 'Ein Name', 2.60, 'Eine Person')
        untaint_database(database=testdb)

        context = gemeinsam_abrechnen.abrechnen(VersionedPostRequest({
            'set_mindate': '01.01.2010',
            'set_maxdate': '01.01.2010',
            'set_ergebnis': '%Ergebnis%',
            'set_verhaeltnis': 50
        }))

        assert context['content']['abrechnungstext'] == '''Abrechnung vom 01.01.2019 
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

    def test_abrechnen_should_create_abrechnung_on_disk(self):
        self.set_up()
        testdb = persisted_state.database_instance()
        testdb.gemeinsamebuchungen.add(datum('01.01.2010'), 'Eine Katgorie', 'Ein Name', 2.60, 'Eine Person')
        untaint_database(database=testdb)

        gemeinsam_abrechnen.abrechnen(VersionedPostRequest({
            'set_mindate': '01.01.2010',
            'set_maxdate': '01.01.2010',
            'set_ergebnis': '%Ergebnis%',
            'set_verhaeltnis': 50
        }))

        abrechnung = file_system.instance().read('../Abrechnungen/Abrechnung_2019-01-01 00:00:00')
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

    def test_shortResult_withEqualValue_shouldReturnEqualSentence(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = persisted_state.database_instance().name
        gemeinsame_buchungen = persisted_state.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(datum('01.01.2010'), self.some_name(), self.some_kategorie(), -11, self_name)
        gemeinsame_buchungen.add(datum('01.01.2010'), self.some_name(), self.some_kategorie(), -11, name_partner)
        untaint_database(database=persisted_state.database_instance())

        result = gemeinsam_abrechnen.index(GetRequest())
        assert result['ergebnis'] == 'Die gemeinsamen Ausgaben sind ausgeglichen.'

    def test_shortResult_withSelectedDate_shouldFilterEntries(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = persisted_state.database_instance().name
        gemeinsame_buchungen = persisted_state.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -1000, self_name)
        gemeinsame_buchungen.add(datum('15.01.2011'), self.some_name(), self.some_kategorie(), -20, name_partner)
        gemeinsame_buchungen.add(datum('15.01.2012'), self.some_name(), self.some_kategorie(), -1000, name_partner)
        untaint_database(database=persisted_state.database_instance())

        result = gemeinsam_abrechnen.index(PostRequest({'set_mindate': '2011-01-01', 'set_maxdate': '2011-02-01'}))

        assert result['ergebnis'] == 'Partner bekommt von Test_User noch 10.00€.'
        assert result['count'] == 3
        assert result['set_count'] == 1

    def test_result_withSelektiertemVerhaeltnis(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = persisted_state.database_instance().name
        gemeinsame_buchungen = persisted_state.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, self_name)
        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, name_partner)

        untaint_database(database=persisted_state.database_instance())

        result = gemeinsam_abrechnen.index(PostRequest({'set_verhaeltnis': 60}))

        assert result[
                   'ergebnis'] == 'Test_User übernimmt einen Anteil von 60% der Ausgaben.<br>Partner bekommt von Test_User noch 10.00€.'
        assert result['self_soll'] == '60.00'
        assert result['partner_soll'] == '40.00'
        assert result['self_diff'] == '-10.00'
        assert result['partner_diff'] == '10.00'


    def test_result_withLimitPartnerAndValueUnderLimit_shouldReturnDefaultVerhaeltnis(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = persisted_state.database_instance().name
        gemeinsame_buchungen = persisted_state.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, self_name)
        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, name_partner)

        untaint_database(database=persisted_state.database_instance())

        result = gemeinsam_abrechnen.index(PostRequest({'set_verhaeltnis': 50,
                                                        'set_limit': 'on',
                                                        'set_limit_fuer': name_partner,
                                                        'set_limit_value': 100}))

        assert result['ergebnis'] == 'Die gemeinsamen Ausgaben sind ausgeglichen.'
        assert result['self_soll'] == '50.00'
        assert result['partner_soll'] == '50.00'
        assert result['self_diff'] == '0.00'
        assert result['partner_diff'] == '0.00'

    def test_result_withLimitPartnerAndValueOverLimit_shouldModifyVerhaeltnis(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = persisted_state.database_instance().name
        gemeinsame_buchungen = persisted_state.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, self_name)
        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, name_partner)

        untaint_database(database=persisted_state.database_instance())

        result = gemeinsam_abrechnen.index(PostRequest({'set_verhaeltnis': 50,
                                                        'set_limit': 'on',
                                                        'set_limit_fuer': name_partner,
                                                        'set_limit_value': 40}))

        assert result[
                   'ergebnis'] == 'Durch das Limit bei Partner von 40 EUR wurde das Verhältnis von 50 auf 60.0 aktualisiert<br>Partner bekommt von Test_User noch 10.00€.'
        assert result['self_soll'] == '60.00'
        assert result['partner_soll'] == '40.00'
        assert result['self_diff'] == '-10.00'
        assert result['partner_diff'] == '10.00'
        assert result['set_verhaeltnis'] == 50
        assert result['set_verhaeltnis_real'] == 60

    def test_result_withLimitSelfAndValueUnderLimit_shouldReturnDefaultVerhaeltnis(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = persisted_state.database_instance().name
        gemeinsame_buchungen = persisted_state.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, self_name)
        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, name_partner)

        untaint_database(database=persisted_state.database_instance())

        result = gemeinsam_abrechnen.index(PostRequest({'set_verhaeltnis': 50,
                                                        'set_limit': 'on',
                                                        'set_limit_fuer': self_name,
                                                        'set_limit_value': 100}))

        assert result['ergebnis'] == 'Die gemeinsamen Ausgaben sind ausgeglichen.'
        assert result['self_soll'] == '50.00'
        assert result['partner_soll'] == '50.00'
        assert result['self_diff'] == '0.00'
        assert result['partner_diff'] == '0.00'

    def test_result_withLimitSelfAndValueOverLimit_shouldModifyVerhaeltnis(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = persisted_state.database_instance().name
        gemeinsame_buchungen = persisted_state.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, self_name)
        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, name_partner)

        untaint_database(database=persisted_state.database_instance())

        result = gemeinsam_abrechnen.index(PostRequest({'set_verhaeltnis': 50,
                                                        'set_limit': 'on',
                                                        'set_limit_fuer': self_name,
                                                        'set_limit_value': 40}))

        assert result[
                   'ergebnis'] == 'Durch das Limit bei Test_User von 40 EUR wurde das Verhältnis von 50 auf 40.0 aktualisiert<br>Test_User bekommt von Partner noch 10.00€.'
        assert result['self_soll'] == '40.00'
        assert result['partner_soll'] == '60.00'
        assert result['self_diff'] == '10.00'
        assert result['partner_diff'] == '-10.00'

    def some_name(self):
        return 'Some Cat.'

    def some_datum(self):
        return datum('15.01.2010')

    def test_withEmptyDatabse_shouldReturnError(self):
        self.set_up()

        result = gemeinsam_abrechnen.index(GetRequest())
        assert get_error_message(result)

    def test_shortResult_withPartnerMoreSpendings_shouldReturnEqualSentence(self):
        self.set_up()
        gemeinsame_buchungen = persisted_state.database_instance().gemeinsamebuchungen
        name_partner = viewcore.name_of_partner()
        gemeinsame_buchungen.add(datum('01.01.2010'), self.some_name(), self.some_kategorie(), -11, name_partner)
        untaint_database(database=persisted_state.database_instance())
        result = gemeinsam_abrechnen.index(GetRequest())
        assert result['ergebnis'] == 'Partner bekommt von Test_User noch 5.50€.'

    def some_kategorie(self):
        return ''

    def test_shortResult_withSelfMoreSpendings_shouldReturnEqualSentence(self):
        self.set_up()
        gemeinsame_buchungen = persisted_state.database_instance().gemeinsamebuchungen
        name_self = persisted_state.database_instance().name
        gemeinsame_buchungen.add(datum('01.01.2010'), self.some_name(), self.some_kategorie(), -11, name_self)
        untaint_database(database=persisted_state.database_instance())

        result = gemeinsam_abrechnen.index(GetRequest())

        assert result['ergebnis'] == 'Test_User bekommt von Partner noch 5.50€.'
