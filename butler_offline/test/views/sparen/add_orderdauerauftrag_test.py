import unittest

from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import PostRequest
from butler_offline.test.RequestStubs import VersionedPostRequest
from butler_offline.views.sparen import add_orderdauerauftrag
from butler_offline.core import file_system
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.viewcore.converter import german_to_rfc as rfc


class AddOrderDauerauftragTest(unittest.TestCase):
    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        depotwerte = persisted_state.database_instance().depotwerte
        persisted_state.database_instance().sparkontos.add('demokonto', Kontos.TYP_DEPOT)
        depotwerte.add(name='demowert', isin='demoisin', typ=depotwerte.TYP_ETF)
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        context = add_orderdauerauftrag.index(GetRequest())
        assert context['approve_title'] == 'Order-Dauerauftrag hinzufügen'
        assert context['kontos'] == ['demokonto']
        assert context['depotwerte'] == [{'description': 'demowert (demoisin)', 'isin': 'demoisin'}]
        assert context['typen'] == [add_orderdauerauftrag.TYP_KAUF, add_orderdauerauftrag.TYP_VERKAUF]

    def test_init_empty_should_return_error(self):
        self.set_up()
        persisted_state.DATABASE_INSTANCE = None

        context = add_orderdauerauftrag.index(GetRequest())

        assert '%Errortext' in context
        assert context['%Errortext'] == 'Bitte erfassen Sie zuerst ein Sparkonto vom Typ "Depot".'

    def test_init_without_depotwert_should_return_error(self):
        self.set_up()
        persisted_state.DATABASE_INSTANCE = None
        sparkontos = persisted_state.database_instance().sparkontos
        sparkontos.add('1name', sparkontos.TYP_DEPOT)

        context = add_orderdauerauftrag.index(GetRequest())

        assert '%Errortext' in context
        assert context['%Errortext'] == 'Bitte erfassen Sie zuerst ein Depotwert.'


    def test_transaction_id_should_be_in_context(self):
        self.set_up()
        context = add_orderdauerauftrag.index(GetRequest())
        assert 'ID' in context

    def test_add(self):
        self.set_up()
        add_orderdauerauftrag.index(VersionedPostRequest(
            {'action': 'add',
             'startdatum': rfc('1.1.2017'),
             'endedatum': rfc('1.1.2018'),
             'rhythmus': 'monatlich',
             'name': 'testname',
             'wert': '2,00',
             'typ': add_orderdauerauftrag.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
         ))

        db = persisted_state.database_instance()
        assert len(db.orderdauerauftrag.content) == 1
        assert db.orderdauerauftrag.content.Startdatum[0] == datum('1.1.2017')
        assert db.orderdauerauftrag.content.Endedatum[0] == datum('1.1.2018')
        assert db.orderdauerauftrag.content.Rhythmus[0] == 'monatlich'
        assert db.orderdauerauftrag.content.Wert[0] == float('2.00')
        assert db.orderdauerauftrag.content.Name[0] == 'testname'
        assert db.orderdauerauftrag.content.Depotwert[0] == 'demoisin'
        assert db.orderdauerauftrag.content.Konto[0] == 'demokonto'

    def test_add_order_should_show_in_recently_added(self):
        self.set_up()
        result = add_orderdauerauftrag.index(VersionedPostRequest(
            {'action': 'add',
             'startdatum': rfc('1.1.2017'),
             'endedatum': rfc('1.1.2018'),
             'rhythmus': 'monatlich',
             'name': 'testname',
             'wert': '2,00',
             'typ': add_orderdauerauftrag.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
         ))
        result_element = list(result['letzte_erfassung'])[0]

        assert result_element['fa'] == 'plus'
        assert result_element['startdatum'] == '01.01.2017'
        assert result_element['endedatum'] == '01.01.2018'
        assert result_element['rhythmus'] == 'monatlich'
        assert result_element['konto'] == 'demokonto'
        assert result_element['name'] == 'testname'
        assert result_element['wert'] == '2,00'
        assert result_element['typ'] == add_orderdauerauftrag.TYP_KAUF
        assert result_element['depotwert'] == 'demoisin'


    def test_add_should_only_fire_once(self):
        self.set_up()
        next_id = request_handler.current_key()
        add_orderdauerauftrag.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'startdatum': rfc('1.1.2017'),
             'endedatum': rfc('1.1.2018'),
             'rhythmus': 'monatlich',
             'name':'testname',
             'wert':'2,00',
             'typ': add_orderdauerauftrag.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
         ))
        add_orderdauerauftrag.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'startdatum': rfc('2.2.2012'),
             'endedatum': rfc('2.2.2012'),
             'rhythmus': 'monatlich',
             'name': 'overwritten',
             'wert': '0,00',
             'typ': add_orderdauerauftrag.TYP_KAUF,
             'depotwert': 'overwritten',
             'konto': 'overwritten'
             }
         ))
        db = persisted_state.database_instance()
        assert len(db.orderdauerauftrag.content) == 1
        assert db.orderdauerauftrag.content.Startdatum[0] == datum('1.1.2017')
        assert db.orderdauerauftrag.content.Endedatum[0] == datum('1.1.2018')
        assert db.orderdauerauftrag.content.Rhythmus[0] == 'monatlich'
        assert db.orderdauerauftrag.content.Wert[0] == float('2.00')
        assert db.orderdauerauftrag.content.Name[0] == 'testname'
        assert db.orderdauerauftrag.content.Depotwert[0] == 'demoisin'
        assert db.orderdauerauftrag.content.Konto[0] == 'demokonto'

    def test_edit(self):
        self.set_up()
        add_orderdauerauftrag.index(VersionedPostRequest(
            {'action': 'add',
             'startdatum': rfc('1.1.2017'),
             'endedatum': rfc('1.1.2018'),
             'rhythmus': 'monatlich',
             'name': 'testname',
             'wert': '2,00',
             'typ': add_orderdauerauftrag.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
         ))

        result = add_orderdauerauftrag.index(VersionedPostRequest(
            {'action': 'add',
             'edit_index': 0,
             'startdatum': rfc('2.1.2017'),
             'endedatum': rfc('2.1.2018'),
             'rhythmus': 'monatlich',
             'name': '2testname',
             'wert': '3,00',
             'typ': add_orderdauerauftrag.TYP_VERKAUF,
             'depotwert': '2demoisin',
             'konto': '2demokonto'
             }
         ))

        db = persisted_state.database_instance()
        assert len(db.orderdauerauftrag.content) == 1
        assert db.orderdauerauftrag.content.Startdatum[0] == datum('2.1.2017')
        assert db.orderdauerauftrag.content.Endedatum[0] == datum('2.1.2018')
        assert db.orderdauerauftrag.content.Rhythmus[0] == 'monatlich'
        assert db.orderdauerauftrag.content.Wert[0] == float('-3.00')
        assert db.orderdauerauftrag.content.Name[0] == '2testname'
        assert db.orderdauerauftrag.content.Depotwert[0] == '2demoisin'
        assert db.orderdauerauftrag.content.Konto[0] == '2demokonto'

        result_element = list(result['letzte_erfassung'])[0]

        assert result_element['fa'] == 'pencil'
        assert result_element['startdatum'] == '02.01.2017'
        assert result_element['endedatum'] == '02.01.2018'
        assert result_element['rhythmus'] == 'monatlich'
        assert result_element['konto'] == '2demokonto'
        assert result_element['name'] == '2testname'
        assert result_element['depotwert'] == '2demoisin'
        assert result_element['wert'] == '3,00'
        assert result_element['typ'] == add_orderdauerauftrag.TYP_VERKAUF


    def test_edit_should_only_fire_once(self):
        self.set_up()
        add_orderdauerauftrag.index(VersionedPostRequest(
            {'action': 'add',
             'startdatum': rfc('1.1.2017'),
             'endedatum': rfc('1.1.2018'),
             'rhythmus': 'monatlich',
             'name': 'testname',
             'wert': '2,00',
             'typ': add_orderdauerauftrag.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
        ))

        next_id = request_handler.current_key()
        add_orderdauerauftrag.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'edit_index': 0,
             'startdatum': rfc('2.1.2017'),
             'endedatum': rfc('2.1.2018'),
             'rhythmus': 'monatlich',
             'name': '2testname',
             'wert': '3,00',
             'typ': add_orderdauerauftrag.TYP_VERKAUF,
             'depotwert': '2demoisin',
             'konto': '2demokonto'
             }
        ))

        add_orderdauerauftrag.index(PostRequest(
            {'action': 'add',
             'ID': next_id,
             'edit_index': 0,
             'endedatum': rfc('1.1.2010'),
             'startdatum': rfc('1.1.2010'),
             'rhythmus': 'monatlich',
             'name': 'overwritten',
             'wert': '0,00',
             'typ': add_orderdauerauftrag.TYP_KAUF,
             'depotwert': 'overwritten',
             'konto': 'overwritten'
             }
        ))

        db = persisted_state.database_instance()
        assert len(db.orderdauerauftrag.content) == 1
        assert db.orderdauerauftrag.content.Startdatum[0] == datum('2.1.2017')
        assert db.orderdauerauftrag.content.Endedatum[0] == datum('2.1.2018')
        assert db.orderdauerauftrag.content.Rhythmus[0] == 'monatlich'
        assert db.orderdauerauftrag.content.Wert[0] == float('-3.00')
        assert db.orderdauerauftrag.content.Name[0] == '2testname'
        assert db.orderdauerauftrag.content.Depotwert[0] == '2demoisin'
        assert db.orderdauerauftrag.content.Konto[0] == '2demokonto'

    def test_edit_call_from_ueberischt_should_preset_values_and_rename_button(self):
        self.set_up()
        add_orderdauerauftrag.index(VersionedPostRequest(
            {'action': 'add',
             'startdatum': rfc('1.1.2017'),
             'endedatum': rfc('1.1.2018'),
             'rhythmus': 'monatlich',
             'name': 'testname',
             'wert': '2,00',
             'typ': add_orderdauerauftrag.TYP_KAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
        ))

        context = add_orderdauerauftrag.index(PostRequest({'action': 'edit', 'edit_index': '0'}))
        assert context['approve_title'] == 'Order-Dauerauftrag aktualisieren'
        preset = context['default_item']

        assert preset['edit_index'] == '0'
        assert preset['startdatum'] == '2017-01-01'
        assert preset['endedatum'] == '2018-01-01'
        assert preset['rhythmus'] == 'monatlich'
        assert preset['konto'] == 'demokonto'
        assert preset['name'] == 'testname'
        assert preset['wert'] == '2,00'
        assert preset['typ'] == add_orderdauerauftrag.TYP_KAUF
        assert preset['depotwert'] == 'demoisin'

    def test_edit_call_from_ueberischt_should_preset_values_verkauf(self):
        self.set_up()
        add_orderdauerauftrag.index(VersionedPostRequest(
            {'action': 'add',
             'endedatum': rfc('1.1.2017'),
             'startdatum': rfc('1.1.2018'),
             'rhythmus': 'monatlich',
             'name': 'testname',
             'wert': '2,00',
             'typ': add_orderdauerauftrag.TYP_VERKAUF,
             'depotwert': 'demoisin',
             'konto': 'demokonto'
             }
        ))

        context = add_orderdauerauftrag.index(PostRequest({'action': 'edit', 'edit_index': '0'}))
        assert context['approve_title'] == 'Order-Dauerauftrag aktualisieren'
        preset = context['default_item']

        assert preset['wert'] == '2,00'
        assert preset['typ'] == add_orderdauerauftrag.TYP_VERKAUF


if __name__ == '__main__':
    unittest.main()
