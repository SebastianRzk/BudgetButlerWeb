import unittest

from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest, PostRequest, VersionedPostRequest
from butler_offline.test.database_util import untaint_database
from butler_offline.views.sparen import add_sparbuchung
from butler_offline.core import file_system
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc
from butler_offline.core.database.sparen.sparbuchungen import Sparbuchungen
from butler_offline.viewcore.context import get_error_message

class AddSparbuchungTest(unittest.TestCase):
    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        persisted_state.database_instance().sparkontos.add('demokonto', Kontos.TYP_SPARKONTO)
        untaint_database(database=persisted_state.database_instance())
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        context = add_sparbuchung.index(GetRequest())
        assert context['approve_title'] == 'Sparbuchung hinzufügen'
        assert context['kontos'] == ['demokonto']

    def test_init_empty_should_return_error(self):
        self.set_up()
        persisted_state.DATABASE_INSTANCE = None

        context = add_sparbuchung.index(GetRequest())

        assert get_error_message(context) == 'Bitte erfassen Sie zuerst ein Sparkonto.'

    def test_transaction_id_should_be_in_context(self):
        self.set_up()
        context = add_sparbuchung.index(GetRequest())
        assert 'ID' in context

    def test_add_shouldAddSparbuchung(self):
        self.set_up()
        add_sparbuchung.index(VersionedPostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'demokonto'
             }
         ))

        db = persisted_state.database_instance()
        assert len(db.sparbuchungen.content) == 1
        assert db.sparbuchungen.content.Datum[0] == datum('1.1.2017')
        assert db.sparbuchungen.content.Wert[0] == float('2.00')
        assert db.sparbuchungen.content.Name[0] == 'testname'
        assert db.sparbuchungen.content.Typ[0] == Sparbuchungen.TYP_MANUELLER_AUFTRAG
        assert db.sparbuchungen.content.Konto[0] == 'demokonto'

    def test_add_sparbuchung_should_show_in_recently_added(self):
        self.set_up()
        result = add_sparbuchung.index(VersionedPostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'demokonto'
             }
         ))
        result_element = list(result['letzte_erfassung'])[0]

        assert result_element['fa'] == 'plus'
        assert result_element['datum'] == '01.01.2017'
        assert result_element['konto'] == 'demokonto'
        assert result_element['name'] == 'testname'
        assert result_element['wert'] == '2,00'
        assert result_element['typ'] == Sparbuchungen.TYP_MANUELLER_AUFTRAG


    def test_add_should_only_fire_once(self):
        self.set_up()
        next_id = persisted_state.current_database_version()
        add_sparbuchung.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'demokonto'
             }
         ))
        add_sparbuchung.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'datum': rfc('2.2.2012'),
             'name': 'overwritten',
             'wert': '0,00',
             'typ': 'overwritten',
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'overwritten'
             }
         ))
        db = persisted_state.database_instance()
        assert len(db.sparbuchungen.content) == 1
        assert db.sparbuchungen.content.Datum[0] == datum('1.1.2017')
        assert db.sparbuchungen.content.Wert[0] == float('2.00')
        assert db.sparbuchungen.content.Name[0] == 'testname'
        assert db.sparbuchungen.content.Typ[0] == Sparbuchungen.TYP_MANUELLER_AUFTRAG
        assert db.sparbuchungen.content.Konto[0] == 'demokonto'

    def test_edit_sparbuchung(self):
        self.set_up()
        add_sparbuchung.index(VersionedPostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'demokonto'
             }
        ))

        result = add_sparbuchung.index(VersionedPostRequest(
            {'action': 'add',
             'edit_index': 0,
             'datum': rfc('2.2.2012'),
             'name': 'testname2',
             'wert': '3,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'demokonto2'
             }
        ))

        db = persisted_state.database_instance()
        assert len(db.sparbuchungen.content) == 1
        assert db.sparbuchungen.content.Datum[0] == datum('2.2.2012')
        assert db.sparbuchungen.content.Wert[0] == float('3.00')
        assert db.sparbuchungen.content.Name[0] == 'testname2'
        assert db.sparbuchungen.content.Typ[0] == Sparbuchungen.TYP_MANUELLER_AUFTRAG
        assert db.sparbuchungen.content.Konto[0] == 'demokonto2'

        result_element = list(result['letzte_erfassung'])[0]

        assert result_element['fa'] == 'pencil'
        assert result_element['datum'] == '02.02.2012'
        assert result_element['konto'] == 'demokonto2'
        assert result_element['name'] == 'testname2'
        assert result_element['wert'] == '3,00'
        assert result_element['typ'] == Sparbuchungen.TYP_MANUELLER_AUFTRAG


    def test_edit_sparbuchung_should_only_fire_once(self):
        self.set_up()
        add_sparbuchung.index(VersionedPostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'demokonto'
             }
        ))

        next_id = persisted_state.current_database_version()
        add_sparbuchung.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'edit_index': 0,
             'datum': rfc('2.2.2012'),
             'name': 'testname2',
             'wert': '3,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'demokonto2'
             }
        ))
        add_sparbuchung.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'edit_index': 0,
             'datum': rfc('1.1.2010'),
             'name': 'overwritten',
             'wert': '0,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'overwritten'
             }
        ))

        db = persisted_state.database_instance()
        assert len(db.sparbuchungen.content) == 1
        assert db.sparbuchungen.content.Datum[0] == datum('2.2.2012')
        assert db.sparbuchungen.content.Wert[0] == float('3.00')
        assert db.sparbuchungen.content.Name[0] == 'testname2'
        assert db.sparbuchungen.content.Typ[0] == Sparbuchungen.TYP_MANUELLER_AUFTRAG
        assert db.sparbuchungen.content.Konto[0] == 'demokonto2'

    def test_editCallFromUeberischt_shouldPresetValues_andRenameButton(self):
        self.set_up()
        add_sparbuchung.index(VersionedPostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_EINZAHLUNG,
             'konto': 'demokonto'
             }
        ))

        context = add_sparbuchung.index(PostRequest({'action': 'edit', 'edit_index': '0'}))
        assert context['approve_title'] == 'Sparbuchung aktualisieren'
        preset = context['default_item']

        assert preset['edit_index'] == '0'
        assert preset['datum'] == '2017-01-01'
        assert preset['konto'] == 'demokonto'
        assert preset['name'] == 'testname'
        assert preset['wert'] == '2,00'
        assert preset['eigenschaft'] == 'Einzahlung'
        assert preset['typ'] == Sparbuchungen.TYP_MANUELLER_AUFTRAG

    def test_editCallFromUeberischt_shouldPresetValues_auszahlung(self):
        self.set_up()
        add_sparbuchung.index(VersionedPostRequest(
            {'action': 'add',
             'datum': rfc('1.1.2017'),
             'name': 'testname',
             'wert': '2,00',
             'typ': Sparbuchungen.TYP_MANUELLER_AUFTRAG,
             'eigenschaft': add_sparbuchung.EIGENSCHAFT_AUSZAHLUNG,
             'konto': 'demokonto'
             }
        ))

        context = add_sparbuchung.index(PostRequest({'action': 'edit', 'edit_index': '0'}))
        assert context['approve_title'] == 'Sparbuchung aktualisieren'
        preset = context['default_item']

        assert preset['wert'] == '2,00'
        assert preset['eigenschaft'] == 'Auszahlung'


if __name__ == '__main__':
    unittest.main()
