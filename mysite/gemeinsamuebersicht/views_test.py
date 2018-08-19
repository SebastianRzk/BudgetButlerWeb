import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from test import DBManagerStub
from test.RequestStubs import GetRequest
from test.RequestStubs import VersionedPostRequest
from gemeinsamuebersicht import views
from viewcore import request_handler
from viewcore import viewcore
from viewcore.converter import datum_from_german as datum




# Create your tests here.
class Gemeinsamuebersicht(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        views.index(GetRequest())

    def test_delete(self):
        self.set_up()

        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen
        gemeinsame_buchungen.add(datum('01.01.2011'), 'kat1', 'name1', 1, 'pers1')
        gemeinsame_buchungen.add(datum('01.01.2012'), 'kat2', 'name2', 1, 'pers2')
        gemeinsame_buchungen.add(datum('01.01.2013'), 'kat3', 'name3', 1, 'pers3')

        views.index(VersionedPostRequest({
            'action' : 'delete',
            'delete_index' : 1
            }))


        result = views.index(GetRequest())

        assert len(result['ausgaben']) == 2
        assert result['ausgaben'][0][2] == 'name1'
        assert result['ausgaben'][1][2] == 'name3'
