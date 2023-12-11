from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.core import file_system
from butler_offline.views.einzelbuchungen import uebersicht_dauerauftrag
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.database.dauerauftraege import Dauerauftraege
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.renderhelper import Betrag


file_system.INSTANCE = FileSystemStub()


def test_init():
    uebersicht_dauerauftrag.handle_request(GetRequest(), uebersicht_dauerauftrag.UbersichtDauerauftragContext(
        dauerauftraege=Dauerauftraege()
    ))


def test_transaction_id_should_be_in_context():
    context = uebersicht_dauerauftrag.handle_request(GetRequest(),
                                                     context=uebersicht_dauerauftrag.UbersichtDauerauftragContext(
                                                          dauerauftraege=Dauerauftraege()
                                                      ))
    assert context.is_transactional()


def test_delete():
    dauerauftraege = Dauerauftraege()
    dauerauftraege.add(datum('01.01.2011'), datum('01.01.2011'), '', '11', 'monatlich', 1)
    dauerauftraege.add(datum('01.01.2011'), datum('01.01.2011'), '', '22', 'monatlich', 1)

    uebersicht_dauerauftrag.handle_request(
        request=PostRequest({'action': 'delete', 'delete_index': '1'}),
        context=uebersicht_dauerauftrag.UbersichtDauerauftragContext(dauerauftraege=dauerauftraege)
    )

    assert dauerauftraege.select().count() == 1
    assert dauerauftraege.content.Name.tolist() == ['11']


def test_render():
    dauerauftraege = Dauerauftraege()
    dauerauftraege.add(datum('01.01.2011'), datum('01.01.2011'), '', '11', 'monatlich', 1)

    result = uebersicht_dauerauftrag.handle_request(request=GetRequest(),
                                                    context=uebersicht_dauerauftrag.UbersichtDauerauftragContext(
                                                         dauerauftraege=dauerauftraege
                                                     ))

    result_dauerauftrag = result.get('dauerauftraege')['Vergangene  Daueraufträge'][0]
    assert result_dauerauftrag['Startdatum'] == '01.01.2011'
    assert result_dauerauftrag['Endedatum'] == '01.01.2011'
    assert result_dauerauftrag['Wert'] == Betrag(1)


def test_index_should_be_secured_by_requesthandler():
    def handle():
        uebersicht_dauerauftrag.index(request=GetRequest())

    result = run_in_mocked_handler(handle)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['einzelbuchungen/uebersicht_dauerauftrag.html']
