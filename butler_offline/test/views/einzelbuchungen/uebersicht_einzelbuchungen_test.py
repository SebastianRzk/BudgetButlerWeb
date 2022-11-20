import unittest

from butler_offline.viewcore.state import persisted_state
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest,  VersionedPostRequest, PostRequest
from butler_offline.test.database_util import untaint_database
from butler_offline.core import file_system
from butler_offline.views.einzelbuchungen import uebersicht_einzelbuchungen
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore import request_handler


class TestUebersichtEinzelbuchungen(unittest.TestCase):

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_transaction_id_should_be_in_context(self):
        self.set_up()
        context = uebersicht_einzelbuchungen.index(GetRequest())
        assert 'ID' in context

    def add_test_data(self):
        einzelbuchungen = persisted_state.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('12.12.2012'), 'Test einnahme kategorie', 'test einnahme name', 100)
        einzelbuchungen.add(datum('13.12.2012'), 'Test ausgabe kategorie', 'test azsgabe name', -100)
        untaint_database(database=persisted_state.database_instance())

    def test_init_withEmptyDatabase(self):
        self.set_up()
        uebersicht_einzelbuchungen.index(GetRequest())

    def test_withEntry_shouldReturnGermanDateFormat(self):
        self.set_up()
        self.add_test_data()
        result = uebersicht_einzelbuchungen.index(GetRequest())
        assert result['alles']['2012.12'][0]['datum'] == '12.12.2012'

    def test_init_filledDatabase(self):
        self.set_up()
        self.add_test_data()
        uebersicht_einzelbuchungen.index(GetRequest())

    def test_getRequest_withEinnahme_shouldReturnEditLinkOfEinnahme(self):
        self.set_up()
        self.add_test_data()
        result = uebersicht_einzelbuchungen.index(GetRequest())
        item = result['alles']['2012.12'][0]
        assert item['wert'] == '100,00'
        assert item['link'] == 'addeinnahme'
        item = result['alles']['2012.12'][1]
        assert item['wert'] == '-100,00'
        assert item['link'] == 'addausgabe'

    def test_delete(self):
        self.set_up()
        self.add_test_data()
        uebersicht_einzelbuchungen.index(VersionedPostRequest({'action': 'delete', 'delete_index': '1'}))
        einzelbuchungen = persisted_state.database_instance().einzelbuchungen
        assert einzelbuchungen.select().sum() == 100

    def test_delete_should_only_trigger_one(self):
        self.set_up()
        self.add_test_data()
        next_id = request_handler.persisted_state.current_database_version()

        assert len(persisted_state.database_instance().einzelbuchungen.content) == 2
        uebersicht_einzelbuchungen.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
        assert len(persisted_state.database_instance().einzelbuchungen.content) == 1
        uebersicht_einzelbuchungen.index(PostRequest({'action': 'delete', 'delete_index': '1', 'ID': next_id}))
        assert len(persisted_state.database_instance().einzelbuchungen.content) == 1
