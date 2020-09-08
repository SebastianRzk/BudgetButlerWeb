import unittest

from butler_offline.viewcore.state import persisted_state
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import VersionedPostRequest, PostRequest
from butler_offline.core import file_system
from butler_offline.views.sparen import uebersicht_sparkontos
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_from_german as datum


class TestUebersichtSparkontos(unittest.TestCase):

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_transaction_id_should_be_in_context(self):
        self.set_up()
        context = uebersicht_sparkontos.index(GetRequest())
        assert 'ID' in context

    def add_test_data(self):
        sparkontos = persisted_state.database_instance().sparkontos
        sparkontos.add(kontoname='demokonto1', kontotyp='demotyp1')
        sparkontos.add(kontoname='demokonto2', kontotyp='demotyp2')
        sparbuchungen = persisted_state.database_instance().sparbuchungen
        sparbuchungen.add(datum('01.01.2020'), 'testname', 100, sparbuchungen.TYP_MANUELLER_AUFTRAG, 'demokonto1')

    def test_should_list_kontos(self):
        self.set_up()
        self.add_test_data()

        result = uebersicht_sparkontos.index(GetRequest())

        assert result['sparkontos'] == [
            {
                'index': 0,
                'kontoname': 'demokonto1',
                'kontotyp': 'demotyp1',
                'wert': '100.00'},
            {
                'index': 1,
                'kontoname': 'demokonto2',
                'kontotyp': 'demotyp2',
                'wert': '0.00'}
        ]

    def test_init_withEmptyDatabase(self):
        self.set_up()
        uebersicht_sparkontos.index(GetRequest())

    def test_init_filledDatabase(self):
        self.set_up()
        self.add_test_data()
        uebersicht_sparkontos.index(GetRequest())

    def test_delete(self):
        self.set_up()
        self.add_test_data()
        uebersicht_sparkontos.index(VersionedPostRequest({'action': 'delete', 'delete_index': '1'}))
        sparkontos = persisted_state.database_instance().sparkontos
        assert len(sparkontos.content) == 1
        assert sparkontos.get(0) == {'Kontoname': 'demokonto1',
                                     'Kontotyp': 'demotyp1',
                                     'index': 0}


    def test_delete_should_only_fire_once(self):
        self.set_up()
        self.add_test_data()
        next_id = request_handler.current_key()

        assert len(persisted_state.database_instance().sparkontos.content) == 2
        uebersicht_sparkontos.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
        assert len(persisted_state.database_instance().sparkontos.content) == 1
        uebersicht_sparkontos.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
        assert len(persisted_state.database_instance().sparkontos.content) == 1
