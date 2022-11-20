import unittest

from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest, VersionedPostRequest
from butler_offline.test.database_util import untaint_database
from butler_offline.views.gemeinsame_buchungen import uebersicht_gemeinsam
from butler_offline.core import file_system
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.state.persisted_state import database_instance as db
from butler_offline.viewcore.converter import datum_from_german as datum

class Gemeinsamuebersicht(unittest.TestCase):

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_transaction_id_should_be_in_context(self):
        self.set_up()
        context = uebersicht_gemeinsam.index(GetRequest())
        assert 'ID' in context

    def test_init(self):
        self.set_up()
        uebersicht_gemeinsam.index(GetRequest())

    def test_delete(self):
        self.set_up()

        db().gemeinsamebuchungen.add(datum('01.01.2011'), 'kat1', 'name1', 1, 'pers1')
        db().gemeinsamebuchungen.add(datum('01.01.2012'), 'kat2', 'name2', 1, 'pers2')
        db().gemeinsamebuchungen.add(datum('01.01.2013'), 'kat3', 'name3', 1, 'pers3')
        untaint_database(database=db())

        uebersicht_gemeinsam.index(VersionedPostRequest({
            'action' : 'delete',
            'delete_index' : 1
            }))


        result = uebersicht_gemeinsam.index(GetRequest())

        assert len(result['ausgaben']) == 2
        assert result['ausgaben'][0]['Name'] == 'name1'
        assert result['ausgaben'][1]['Name'] == 'name3'

    def test_list(self):
        self.set_up()

        db().gemeinsamebuchungen.add(datum('01.01.2011'), 'kat1', 'name1', 1, 'pers1')
        untaint_database(database=db())

        result = uebersicht_gemeinsam.index(GetRequest())
        print(result['ausgaben'])
        assert result['ausgaben'] == [{'Datum': '01.01.2011', 'Kategorie': 'kat1', 'Name': 'name1', 'Wert': '1,00', 'Person': 'pers1', 'index': 0}]