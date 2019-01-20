import os
import sys
import unittest

from mysite.viewcore import request_handler
from mysite.test.FileSystemStub import FileSystemStub
from mysite.test.RequestStubs import GetRequest
from mysite.test.RequestStubs import PostRequest
from mysite.core import FileSystem
from mysite.core.database.Einzelbuchungen import Einzelbuchungen
from mysite.views import gemeinsam_abrechnen
from mysite.viewcore import viewcore
from mysite.viewcore.converter import datum_from_german as datum
from mysite.viewcore import configuration_provider

class Gemeinsamabrechnen(unittest.TestCase):
    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        configuration_provider.LOADED_CONFIG = None
        viewcore.DATABASE_INSTANCE = None
        viewcore.DATABASES = []
        print(viewcore.database_instance().name)
        configuration_provider.set_configuration('PARTNERNAME','Maureen')
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        result = gemeinsam_abrechnen.index(GetRequest())


    def test_abrechnen(self):
        self.set_up()
        testdb = viewcore.database_instance()
        testdb.gemeinsamebuchungen.add(datum('01.01.2010'), 'Eine Katgorie', 'Ein Name', 2.60, 'Eine Person')
        gemeinsam_abrechnen.abrechnen(PostRequest({}))

        assert testdb.einzelbuchungen.anzahl() == 1
        assert testdb.einzelbuchungen.get_all().Wert[0] == '1.30'

    def test_shortResult_withEqualValue_shouldReturnEqualSentence(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = viewcore.database_instance().name
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(datum('01.01.2010'), self.some_name(), self.some_kategorie(), -11, self_name)
        gemeinsame_buchungen.add(datum('01.01.2010'), self.some_name(), self.some_kategorie(), -11, name_partner)

        result = gemeinsam_abrechnen.index(GetRequest())
        assert result['ergebnis'] == 'Die gemeinsamen Ausgaben sind ausgeglichen.'

    def test_shortResult_withSelectedDate_shouldFilterEntries(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = viewcore.database_instance().name
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -1000, self_name)
        gemeinsame_buchungen.add(datum('15.01.2011'), self.some_name(), self.some_kategorie(), -20, name_partner)
        gemeinsame_buchungen.add(datum('15.01.2012'), self.some_name(), self.some_kategorie(), -1000, name_partner)

        result = gemeinsam_abrechnen.index(PostRequest({'set_mindate': '2011-01-01', 'set_maxdate': '2011-02-01'}))

        assert result['ergebnis'] == 'Maureen bekommt von Test_User noch 10.00€.'
        assert result['count'] == 3
        assert result['set_count'] == 1


    def test_result_withSelektiertemVerhaeltnis(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = viewcore.database_instance().name
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, self_name)
        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, name_partner)

        result = gemeinsam_abrechnen.index(PostRequest({'set_verhaeltnis': 60}))

        assert result['ergebnis'] == 'Maureen bekommt von Test_User noch 10.00€.'
        assert result['sebastian_soll'] == '60.00'
        assert result['maureen_soll'] == '40.00'
        assert result['sebastian_diff'] == '-10.00'
        assert result['maureen_diff'] == '10.00'


    def test_result_withLimitPartnerAndValueUnderLimit_shouldReturnDefaultVerhaeltnis(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = viewcore.database_instance().name
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, self_name)
        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, name_partner)

        result = gemeinsam_abrechnen.index(PostRequest({'set_verhaeltnis': 50,
                                                        'set_limit': 'on',
                                                        'set_limit_fuer': name_partner,
                                                        'set_limit_value': 100}))

        assert result['ergebnis'] == 'Die gemeinsamen Ausgaben sind ausgeglichen.'
        assert result['sebastian_soll'] == '50.00'
        assert result['maureen_soll'] == '50.00'
        assert result['sebastian_diff'] == '0.00'
        assert result['maureen_diff'] == '0.00'

    def test_result_withLimitPartnerAndValueOverLimit_shouldModifyVerhaeltnis(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = viewcore.database_instance().name
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, self_name)
        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, name_partner)

        result = gemeinsam_abrechnen.index(PostRequest({'set_verhaeltnis': 50,
                                                        'set_limit': 'on',
                                                        'set_limit_fuer': name_partner,
                                                        'set_limit_value': 40}))

        assert result['ergebnis'] == 'Durch das Limit bei Maureen von 40 EUR wurde das Verhältnis von 50 auf 60.0 aktualisiert<br>Maureen bekommt von Test_User noch 10.00€.'
        assert result['sebastian_soll'] == '60.00'
        assert result['maureen_soll'] == '40.00'
        assert result['sebastian_diff'] == '-10.00'
        assert result['maureen_diff'] == '10.00'

    def test_result_withLimitSelfAndValueUnderLimit_shouldReturnDefaultVerhaeltnis(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = viewcore.database_instance().name
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, self_name)
        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, name_partner)

        result = gemeinsam_abrechnen.index(PostRequest({'set_verhaeltnis': 50,
                                                        'set_limit': 'on',
                                                        'set_limit_fuer': self_name,
                                                        'set_limit_value': 100}))

        assert result['ergebnis'] == 'Die gemeinsamen Ausgaben sind ausgeglichen.'
        assert result['sebastian_soll'] == '50.00'
        assert result['maureen_soll'] == '50.00'
        assert result['sebastian_diff'] == '0.00'
        assert result['maureen_diff'] == '0.00'

    def test_result_withLimitSelfAndValueOverLimit_shouldModifyVerhaeltnis(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = viewcore.database_instance().name
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, self_name)
        gemeinsame_buchungen.add(self.some_datum(), self.some_name(), self.some_kategorie(), -50, name_partner)

        result = gemeinsam_abrechnen.index(PostRequest({'set_verhaeltnis': 50,
                                                        'set_limit': 'on',
                                                        'set_limit_fuer': self_name,
                                                        'set_limit_value': 40}))

        assert result[
                   'ergebnis'] == 'Durch das Limit bei Test_User von 40 EUR wurde das Verhältnis von 50 auf 40.0 aktualisiert<br>Test_User bekommt von Maureen noch 10.00€.'
        assert result['sebastian_soll'] == '40.00'
        assert result['maureen_soll'] == '60.00'
        assert result['sebastian_diff'] == '10.00'
        assert result['maureen_diff'] == '-10.00'


    def some_name(self):
        return 'Some Cat.'

    def some_datum(self):
        return datum('15.01.2010')

    def test_withEmptyDatabse_shouldReturnError(self):
        self.set_up()

        result = gemeinsam_abrechnen.index(GetRequest())
        assert '%Errortext' in result

    def test_shortResult_withPartnerMoreSpendings_shouldReturnEqualSentence(self):
        self.set_up()
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen
        name_partner = viewcore.name_of_partner()
        gemeinsame_buchungen.add(datum('01.01.2010'), self.some_name(), self.some_kategorie(), -11, name_partner)
        result = gemeinsam_abrechnen.index(GetRequest())
        assert result['ergebnis'] == 'Maureen bekommt von Test_User noch 5.50€.'

    def some_kategorie(self):
        return ''

    def test_shortResult_withSelfMoreSpendings_shouldReturnEqualSentence(self):
        self.set_up()
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen
        name_self = viewcore.database_instance().name
        gemeinsame_buchungen.add(datum('01.01.2010'), self.some_name(), self.some_kategorie(), -11, name_self)

        result = gemeinsam_abrechnen.index(GetRequest())

        assert result['ergebnis'] == 'Test_User bekommt von Maureen noch 5.50€.'
