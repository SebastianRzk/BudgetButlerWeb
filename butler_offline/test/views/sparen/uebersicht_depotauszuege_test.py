import unittest

from butler_offline.viewcore.state import persisted_state
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import VersionedPostRequest, PostRequest
from butler_offline.core import file_system
from butler_offline.views.sparen import uebersicht_depotauszuege
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore import request_handler


class TestUebersichtDepotauszuege(unittest.TestCase):

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_transaction_id_should_be_in_context(self):
        self.set_up()
        context = uebersicht_depotauszuege.index(GetRequest())
        assert 'ID' in context

    def add_test_data(self):
        depotauszuege = persisted_state.database_instance().depotauszuege
        depotauszuege.add(datum('01.01.2020'), '1isin', '1demokonto', 1)
        depotauszuege.add(datum('03.01.2020'), '2isin', '2demokonto', 2)
        depotauszuege.add(datum('03.01.2020'), '3isin', '2demokonto', 3)
        depotauszuege.add(datum('03.01.2020'), '4isin', '3demokonto', 4)

        depotwerte = persisted_state.database_instance().depotwerte
        depotwerte.add(name='1name', isin='1isin', typ=depotwerte.TYP_ETF)
        depotwerte.add(name='2name', isin='2isin', typ=depotwerte.TYP_ETF)
        depotwerte.add(name='3name', isin='3isin', typ=depotwerte.TYP_ETF)
        depotwerte.add(name='4name', isin='4isin', typ=depotwerte.TYP_ETF)


    def test_init_withEmptyDatabase(self):
        self.set_up()
        content = uebersicht_depotauszuege.index(GetRequest())
        assert content['gesamt'] == []


    def test_init_filledDatabase(self):
        self.set_up()
        self.add_test_data()

        content = uebersicht_depotauszuege._handle_request(GetRequest())

        assert content['gesamt'] == [
            {'buchungen': [
                {'depotwert': '1name (1isin)', 'wert': 1}],
                'index': 0,
                'name': '1demokonto vom 01.01.2020'},
            {'buchungen': [{'depotwert': '2name (2isin)', 'wert': 2},
                           {'depotwert': '3name (3isin)', 'wert': 3}],
             'index': 1,
             'name': '2demokonto vom 03.01.2020'},
            {'buchungen': [{'depotwert': '4name (4isin)', 'wert': 4}],
             'index': 3,
             'name': '3demokonto vom 03.01.2020'},
        ]

    def test_delete(self):
        self.set_up()
        self.add_test_data()

        uebersicht_depotauszuege.index(VersionedPostRequest({'action': 'delete', 'delete_index': '1'}))
        depotauszuege = persisted_state.database_instance().depotauszuege

        assert len(depotauszuege.content) == 2

        page_conent = uebersicht_depotauszuege._handle_request(GetRequest())
        assert page_conent['gesamt'] == [
            {'buchungen': [
                {'depotwert': '1name (1isin)', 'wert': 1}],
                'index': 0,
                'name': '1demokonto vom 01.01.2020'},
            {'buchungen': [{'depotwert': '4name (4isin)', 'wert': 4}],
             'index': 1,
             'name': '3demokonto vom 03.01.2020'},
        ]

    def test_delete_should_only_fire_once(self):
        self.set_up()
        self.add_test_data()
        next_id = request_handler.current_key()

        assert len(persisted_state.database_instance().depotauszuege.content) == 4
        uebersicht_depotauszuege.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
        assert len(persisted_state.database_instance().depotauszuege.content) == 2
        uebersicht_depotauszuege.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
        assert len(persisted_state.database_instance().depotauszuege.content) == 2
