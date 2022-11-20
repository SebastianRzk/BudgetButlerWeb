import unittest

from butler_offline.viewcore.state import persisted_state
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import VersionedPostRequest, PostRequest
from butler_offline.test.database_util import untaint_database
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
        sparkontos.add(kontoname='demokonto1', kontotyp=sparkontos.TYP_SPARKONTO)
        sparkontos.add(kontoname='demokonto2', kontotyp=sparkontos.TYP_DEPOT)
        sparbuchungen = persisted_state.database_instance().sparbuchungen
        sparbuchungen.add(datum('01.01.2020'), 'testname', 100, sparbuchungen.TYP_MANUELLER_AUFTRAG, 'demokonto1')
        sparbuchungen.add(datum('01.01.2020'), 'testname', 10, sparbuchungen.TYP_ZINSEN, 'demokonto1')

        depotwerte = persisted_state.database_instance().depotwerte
        depotwerte.add(name='demoname', isin='demoisin', typ=depotwerte.TYP_ETF)
        persisted_state.database_instance().order.add(datum('01.01.2020'), 'testname', 'demokonto2', 'demoisin', 999)
        persisted_state.database_instance().depotauszuege.add(datum('02.01.2020'), 'demoisin', 'demokonto2', 990)
        untaint_database(database=persisted_state.database_instance())

    def test_should_list_kontos(self):
        self.set_up()
        self.add_test_data()

        result = uebersicht_sparkontos.index(GetRequest())

        assert result['sparkontos'] == [
            {
                'index': 0,
                'kontoname': 'demokonto2',
                'kontotyp': 'Depot',
                'wert': '990,00',
                'aufbuchungen': '999,00',
                'difference': '-9,00',
                'difference_is_negativ': True
            },
            {
                'index': 1,
                'kontoname': 'demokonto1',
                'kontotyp': 'Sparkonto',
                'wert': '110,00',
                'aufbuchungen': '100,00',
                'difference': '10,00',
                'difference_is_negativ': False
            }
        ]

        assert result['gesamt'] == {
            'wert': '1100,00',
            'aufbuchungen': '1099,00',
            'difference': '1,00',
            'difference_is_negativ': False
        }

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
        assert sparkontos.get(0) == {'Kontoname': 'demokonto2',
                                     'Kontotyp': 'Depot',
                                     'index': 0}


    def test_delete_should_only_fire_once(self):
        self.set_up()
        self.add_test_data()
        next_id = persisted_state.current_database_version()

        assert len(persisted_state.database_instance().sparkontos.content) == 2
        uebersicht_sparkontos.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
        assert len(persisted_state.database_instance().sparkontos.content) == 1
        uebersicht_sparkontos.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
        assert len(persisted_state.database_instance().sparkontos.content) == 1
