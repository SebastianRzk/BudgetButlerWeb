import unittest

from butler_offline.viewcore.state import persisted_state
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import VersionedPostRequest, PostRequest
from butler_offline.core import file_system
from butler_offline.views.sparen import uebersicht_depotwerte
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_from_german as datum

class TestUebersichtDepotwerte(unittest.TestCase):

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_transaction_id_should_be_in_context(self):
        self.set_up()
        context = uebersicht_depotwerte.index(GetRequest())
        assert 'ID' in context

    def add_test_data(self):
        depotwerte = persisted_state.database_instance().depotwerte
        depotwerte.add(name='depotwert1', isin='isin1', typ=depotwerte.TYP_ETF)
        depotwerte.add(name='depotwert2', isin='isin2', typ=depotwerte.TYP_ETF)
        order = persisted_state.database_instance().order
        order.add(datum('12.12.2019'), 'demoname', 'demokonto', 'isin1', 100)

        depotauszuege = persisted_state.database_instance().depotauszuege
        depotauszuege.add(datum('01.01.2020'), 'isin1', 'demokonto', 90)

    def test_should_list_depotwerte(self):
        self.set_up()
        self.add_test_data()

        result = uebersicht_depotwerte.index(GetRequest())

        assert result['depotwerte'] == [
            {
                'index': 0,
                'name': 'depotwert1',
                'isin': 'isin1',
                'typ': 'ETF',
                'buchung': '100,00',
                'difference': '-10,00',
                'difference_is_negativ': True,
                'wert': '90,00'},
            {
                'index': 1,
                'name': 'depotwert2',
                'isin': 'isin2',
                'typ': 'ETF',
                'buchung': '0,00',
                'difference': '0,00',
                'difference_is_negativ': False,
                'wert': '0,00'}
        ]

        assert result['gesamt'] == {
            'buchung': '100,00',
            'difference': '-10,00',
            'difference_is_negativ': True,
            'wert': '90,00'
        }

    def test_init_withEmptyDatabase(self):
        self.set_up()
        uebersicht_depotwerte.index(GetRequest())

    def test_init_filledDatabase(self):
        self.set_up()
        self.add_test_data()
        uebersicht_depotwerte.index(GetRequest())

    def test_delete(self):
        self.set_up()
        self.add_test_data()
        uebersicht_depotwerte.index(VersionedPostRequest({'action': 'delete', 'delete_index': '1'}))
        depotwerte = persisted_state.database_instance().depotwerte
        assert len(depotwerte.content) == 1
        assert depotwerte.get(0) == {'Name': 'depotwert1',
                                     'ISIN': 'isin1',
                                     'Typ': depotwerte.TYP_ETF,
                                     'index': 0}


    def test_delete_should_only_fire_once(self):
        self.set_up()
        self.add_test_data()
        next_id = request_handler.current_key()

        assert len(persisted_state.database_instance().depotwerte.content) == 2
        uebersicht_depotwerte.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
        assert len(persisted_state.database_instance().depotwerte.content) == 1
        uebersicht_depotwerte.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
        assert len(persisted_state.database_instance().depotwerte.content) == 1
