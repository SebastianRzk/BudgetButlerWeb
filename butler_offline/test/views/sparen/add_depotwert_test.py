import unittest

from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import PostRequest
from butler_offline.test.RequestStubs import VersionedPostRequest
from butler_offline.views.sparen import add_depotwert
from butler_offline.core import file_system
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler


class AddDepotwertTest(unittest.TestCase):
    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        context = add_depotwert.index(GetRequest())
        assert context['approve_title'] == 'Depotwert hinzufügen'

    def test_transaction_id_should_be_in_context(self):
        self.set_up()
        context = add_depotwert.index(GetRequest())
        assert 'ID' in context

    def test_add_shouldAddSparkonto(self):
        self.set_up()
        add_depotwert.index(VersionedPostRequest(
            {'action': 'add',
             'name': '1name',
             'isin': '1isin'
             }
         ))

        db = persisted_state.database_instance()
        assert len(db.depotwerte.content) == 1
        assert db.depotwerte.content.Name[0] == '1name'
        assert db.depotwerte.content.ISIN[0] == '1isin'

    def test_add_sparkonto_should_show_in_recently_added(self):
        self.set_up()
        result = add_depotwert.index(VersionedPostRequest(
            {'action': 'add',
             'name': '1name',
             'isin': '1isin'
             }
         ))
        result_element = list(result['letzte_erfassung'])[0]

        assert result_element['fa'] == 'plus'
        assert result_element['Name'] == '1name'
        assert result_element['Isin'] == '1isin'


    def test_add_should_only_fire_once(self):
        self.set_up()
        next_id = request_handler.current_key()
        add_depotwert.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'name': '1name',
             'isin': '1isin'
             }
         ))
        add_depotwert.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'name': 'overwritten',
             'isin': 'overwritten'
             }
         ))
        db = persisted_state.database_instance()
        assert len(db.depotwerte.content) == 1
        assert db.depotwerte.content.Name[0] == '1name'
        assert db.depotwerte.content.ISIN[0] == '1isin'

    def test_edit_sparkonto(self):
        self.set_up()
        add_depotwert.index(VersionedPostRequest(
            {'action': 'add',
             'name': '1name',
             'isin': '1isin'
             }
        ))

        result = add_depotwert.index(VersionedPostRequest(
            {'action': 'add',
             'edit_index': 0,
             'name': '2name',
             'isin': '2isin'
             }
        ))

        db = persisted_state.database_instance()
        assert len(db.depotwerte.content) == 1
        assert db.depotwerte.content.Name[0] == '2name'
        assert db.depotwerte.content.ISIN[0] == '2isin'

        result_element = list(result['letzte_erfassung'])[0]

        assert result_element['fa'] == 'pencil'
        assert result_element['Name'] == '2name'
        assert result_element['Isin'] == '2isin'


    def test_edit_sparkonto_should_only_fire_once(self):
        self.set_up()
        add_depotwert.index(VersionedPostRequest(
            {'action': 'add',
             'name': '1name',
             'isin': '1isin'
             }
        ))

        next_id = request_handler.current_key()
        add_depotwert.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'edit_index': 0,
             'name': '2name',
             'isin': '2isin'
             }
        ))
        add_depotwert.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'edit_index': 0,
             'name': 'overwritten',
             'isin': 'overwritten'
             }
        ))

        db = persisted_state.database_instance()
        assert len(db.depotwerte.content) == 1
        assert db.depotwerte.content.Name[0] == '2name'
        assert db.depotwerte.content.ISIN[0] == '2isin'

    def test_editCallFromUeberischt_shouldPresetValues_andRenameButton(self):
        self.set_up()
        add_depotwert.index(VersionedPostRequest(
            {'action': 'add',
             'name': '1name',
             'isin': '1isin'
             }
        ))

        context = add_depotwert.index(PostRequest({'action': 'edit', 'edit_index': '0'}))
        assert context['approve_title'] == 'Depotwert aktualisieren'
        preset = context['default_item']

        assert preset['edit_index'] == '0'
        assert preset['name'] == '1name'
        assert preset['isin'] == '1isin'


if __name__ == '__main__':
    unittest.main()
