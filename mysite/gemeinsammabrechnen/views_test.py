import os
import sys
import unittest
from viewcore.viewcore import name_of_partner
from viewcore import request_handler

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from test import DBManagerStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from core.DatabaseModule import Database
from core.database.Einzelbuchungen import Einzelbuchungen
from gemeinsammabrechnen import views
from viewcore import viewcore
from viewcore.converter import datum
from viewcore import configuration_provider

class Gemeinsamabrechnen(unittest.TestCase):
    def set_up(self):
        DBManagerStub.setup_db_for_test()
        request_handler.stub_me()
        configuration_provider.stub_me('''
        PARTNERNAME:Maureen
        ''')

    def test_init(self):
        self.set_up()
        result = views.index(GetRequest())


    def test_abrechnen(self):
        self.set_up()
        testdb = viewcore.database_instance()
        testdb.gemeinsamebuchungen.add(datum('01.01.2010'), 'Eine Katgorie', 'Ein Name', 2.60, 'Eine Person')
        DBManagerStub.stub_abrechnungs_write()
        views.abrechnen(PostRequest({}))

        assert testdb.einzelbuchungen.anzahl() == 1
        assert testdb.einzelbuchungen.get_all().Wert[0] == '1.30'

    def test_shortResult_withEqualValue_shouldReturnEqualSentence(self):
        self.set_up()
        result = views.index(GetRequest())
        assert result['ergebnis'] == 'Die gemeinsamen Ausgaben sind ausgeglichen.'

    def test_shortResult_withPartnerMoreSpendings_shouldReturnEqualSentence(self):
        self.set_up()
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen
        name_partner = viewcore.name_of_partner()
        gemeinsame_buchungen.add(datum('01.01.2010'), 'Some Cat.', '', -11, name_partner)
        result = views.index(GetRequest())
        assert result['ergebnis'] == 'Maureen bekommt von test noch 5.50€.'

    def test_shortResult_withSelfMoreSpendings_shouldReturnEqualSentence(self):
        self.set_up()
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen
        name_self = viewcore.database_instance().name
        gemeinsame_buchungen.add(datum('01.01.2010'), 'Some Cat.', 'Some Name', -11, name_self)
        result = views.index(GetRequest())
        assert result['ergebnis'] == 'test bekommt von Maureen noch 5.50€.'
