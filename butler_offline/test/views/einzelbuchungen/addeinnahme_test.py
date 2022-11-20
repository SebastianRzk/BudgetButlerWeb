import unittest

from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest, PostRequest, VersionedPostRequest
from butler_offline.test.database_util import untaint_database
from butler_offline.views.einzelbuchungen import addeinnahme
from butler_offline.core import file_system
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore.state.persisted_state import database_instance as db
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc

class TestAddEinnahmeView(unittest.TestCase):

    testdb = None
    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        request_handler.stub_me()


    def test_transaction_id_should_be_in_context(self):
        self.set_up()
        context = addeinnahme.index(GetRequest())
        assert 'ID' in context

    def test_init(self):
        self.set_up()
        context = addeinnahme.index(GetRequest())
        assert context['approve_title'] == 'Einnahme hinzufügen'

    def test_editCallFromUeberischt_shouldNameButtonEdit(self):
        self.set_up()
        db().einzelbuchungen.add(datum('10.10.2010'), 'kategorie', 'name', 10.00)
        untaint_database(database=db())

        context = addeinnahme.index(PostRequest({'action': 'edit', 'edit_index': '0'}))

        assert context['approve_title'] == 'Einnahme aktualisieren'

    def test_add_ausgabe(self):
        self.set_up()
        addeinnahme.index(VersionedPostRequest(
            {'action':'add',
             'date':rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        assert len(db().einzelbuchungen.content) == 1
        assert db().einzelbuchungen.content.Wert[0] == float('2.00')
        assert db().einzelbuchungen.content.Name[0] == 'testname'
        assert db().einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert db().einzelbuchungen.content.Datum[0] == datum('1.1.2017')

    def test_add_ausgabe_should_only_fire_once(self):
        self.set_up()
        next_id = persisted_state.current_database_version()
        addeinnahme.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        addeinnahme.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'date': rfc('1.1.2017'),
             'kategorie':'overwritten',
             'name':'overwritten',
             'wert':'0,00'
             }
         ))

        assert len(db().einzelbuchungen.content) == 1
        assert db().einzelbuchungen.content.Wert[0] == float('2.00')
        assert db().einzelbuchungen.content.Name[0] == 'testname'
        assert db().einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert db().einzelbuchungen.content.Datum[0] == datum('1.1.2017')

    def test_add_einnahme_should_show_in_recently_added(self):
        self.set_up()
        result = addeinnahme.handle_request(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        result_element = list(result['letzte_erfassung'])[0]

        assert result_element['fa'] == 'plus'
        assert result_element['datum'] == '01.01.2017'
        assert result_element['kategorie'] == 'Essen'
        assert result_element['name'] == 'testname'
        assert result_element['wert'] == '2,00'

    def test_edit_ausgabe(self):
        self.set_up()

        addeinnahme.index(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        addeinnahme.index(VersionedPostRequest(
            {'action':'add',
             'edit_index':'0',
             'date': rfc('5.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,50'
             }
         ))

        assert len(db().einzelbuchungen.content) == 1
        assert db().einzelbuchungen.content.Wert[0] == float('2.50')
        assert db().einzelbuchungen.content.Name[0] == 'testname'
        assert db().einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert db().einzelbuchungen.content.Datum[0] == datum('5.1.2017')


    def test_edit_ausgabe_should_only_fire_once(self):
        self.set_up()

        addeinnahme.index(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        next_id = persisted_state.current_database_version()
        addeinnahme.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'edit_index':'0',
             'date': rfc('5.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,50'
             }
         ))

        addeinnahme.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'edit_index':'0',
             'date': rfc('5.1.2017'),
             'kategorie':'overwritten',
             'name':'overwritten',
             'wert':'0,0'
             }
         ))

        assert len(db().einzelbuchungen.content) == 1
        assert db().einzelbuchungen.content.Wert[0] == float('2.50')
        assert db().einzelbuchungen.content.Name[0] == 'testname'
        assert db().einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert db().einzelbuchungen.content.Datum[0] == datum('5.1.2017')

    def test_edit_einzelbuchung_shouldLoadInputValues(self):
        self.set_up()

        addeinnahme.index(VersionedPostRequest(
            {
                'action': 'add',
                'date': rfc('1.1.2017'),
                'kategorie': 'Essen',
                'name': 'testname',
                'wert': '2,34'
             }
         ))

        result = addeinnahme.index(PostRequest(
            {'action':'edit',
             'edit_index':'0'
             }
        ))

        assert result['edit_index'] == 0
        assert result['default_item']['Name'] == 'testname'
        assert result['default_item']['Wert'] == '2,34'
