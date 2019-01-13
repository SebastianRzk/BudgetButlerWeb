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

        gemeinsame_buchungen.add(datum('01.01.2010'), 'Some Cat.', '', -11, self_name)
        gemeinsame_buchungen.add(datum('01.01.2010'), 'Some Cat.', '', -11, name_partner)

        result = gemeinsam_abrechnen.index(GetRequest())
        assert result['ergebnis'] == 'Die gemeinsamen Ausgaben sind ausgeglichen.'

    def test_shortResult_withSelectedDate_shouldFilterEntries(self):
        self.set_up()
        name_partner = viewcore.name_of_partner()
        self_name = viewcore.database_instance().name
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen

        gemeinsame_buchungen.add(datum('15.01.2010'), 'Some Cat.', '', -1000, self_name)
        gemeinsame_buchungen.add(datum('15.01.2011'), 'Some Cat.', '', -20, name_partner)
        gemeinsame_buchungen.add(datum('15.01.2012'), 'Some Cat.', '', -1000, name_partner)

        result = gemeinsam_abrechnen.index(PostRequest({'set_mindate': '2011-01-01', 'set_maxdate': '2011-02-01'}))

        assert result['ergebnis'] == 'Maureen bekommt von Test_User noch 10.00€.'
        assert result['count'] == 3
        assert result['set_count'] == 1

    def test_withEmptyDatabse_shouldReturnError(self):
        self.set_up()

        result = gemeinsam_abrechnen.index(GetRequest())
        assert '%Errortext' in result

    def test_shortResult_withPartnerMoreSpendings_shouldReturnEqualSentence(self):
        self.set_up()
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen
        name_partner = viewcore.name_of_partner()
        gemeinsame_buchungen.add(datum('01.01.2010'), 'Some Cat.', '', -11, name_partner)
        result = gemeinsam_abrechnen.index(GetRequest())
        assert result['ergebnis'] == 'Maureen bekommt von Test_User noch 5.50€.'

    def test_shortResult_withSelfMoreSpendings_shouldReturnEqualSentence(self):
        self.set_up()
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen
        name_self = viewcore.database_instance().name
        gemeinsame_buchungen.add(datum('01.01.2010'), 'Some Cat.', 'Some Name', -11, name_self)
        result = gemeinsam_abrechnen.index(GetRequest())
        assert result['ergebnis'] == 'Test_User bekommt von Maureen noch 5.50€.'
