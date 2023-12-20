from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen
from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.test.test import assert_info_message_keine_gemeinsame_buchungen_erfasst_in_context, \
    assert_keine_message_set
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.views.gemeinsame_buchungen import uebersicht_gemeinsam


def test_context_should_be_transactional():
    context = uebersicht_gemeinsam.handle_request(
        request=GetRequest(),
        context=uebersicht_gemeinsam.UebersichtGemeinsamContext(
            gemeinsamebuchungen=Gemeinsamebuchungen()
        )
    )
    assert context.is_transactional()


def test_init():
    context = uebersicht_gemeinsam.handle_request(
        request=GetRequest(),
        context=empty_context()
    )
    assert context.is_ok()


def empty_context():
    return uebersicht_gemeinsam.UebersichtGemeinsamContext(
        gemeinsamebuchungen=Gemeinsamebuchungen()
    )


def test_init_with_empty_database_should_show_info_message():
    context = uebersicht_gemeinsam.handle_request(
        GetRequest(),
        context=empty_context()
    )
    assert_info_message_keine_gemeinsame_buchungen_erfasst_in_context(result=context)


def test_init_with_buchungen_should_not_show_any_message():
    gemeinsamebuchungen = Gemeinsamebuchungen()
    gemeinsamebuchungen.add(datum('01.01.2011'), 'kat1', 'name1', 1, 'pers1')
    context = uebersicht_gemeinsam.UebersichtGemeinsamContext(gemeinsamebuchungen=gemeinsamebuchungen)
    context = uebersicht_gemeinsam.handle_request(
        GetRequest(),
        context=context
    )
    assert_keine_message_set(result=context)


def test_delete():
    gemeinsamebuchungen = Gemeinsamebuchungen()

    gemeinsamebuchungen.add(datum('01.01.2011'), 'kat1', 'name1', 1, 'pers1')
    gemeinsamebuchungen.add(datum('01.01.2012'), 'kat2', 'name2', 1, 'pers2')
    gemeinsamebuchungen.add(datum('01.01.2013'), 'kat3', 'name3', 1, 'pers3')

    assert uebersicht_gemeinsam.handle_request(
        request=PostRequest({
            'action': 'delete',
            'delete_index': 1
        }),
        context=uebersicht_gemeinsam.UebersichtGemeinsamContext(
            gemeinsamebuchungen=gemeinsamebuchungen
        )
    ).is_ok()

    result = uebersicht_gemeinsam.handle_request(
        request=GetRequest(),
        context=uebersicht_gemeinsam.UebersichtGemeinsamContext(
            gemeinsamebuchungen=gemeinsamebuchungen
        )
    )

    assert result.is_ok()
    assert len(result.get('ausgaben')) == 2
    assert result.get('ausgaben')[0]['Name'] == 'name1'
    assert result.get('ausgaben')[1]['Name'] == 'name3'


def test_list():
    gemeinsamebuchungen = Gemeinsamebuchungen()
    gemeinsamebuchungen.add(datum('01.01.2011'), 'kat1', 'name1', 1, 'pers1')

    result = uebersicht_gemeinsam.handle_request(
        request=GetRequest(),
        context=uebersicht_gemeinsam.UebersichtGemeinsamContext(
            gemeinsamebuchungen=gemeinsamebuchungen
        )
    )
    assert result.get('ausgaben') == [
        {'Datum': '01.01.2011', 'Kategorie': 'kat1', 'Name': 'name1', 'Wert': '1,00', 'Person': 'pers1', 'index': 0}]


def test_index_should_be_secured_by_requesthandler():
    def handle():
        uebersicht_gemeinsam.index(request=GetRequest())

    result = run_in_mocked_handler(handle)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['gemeinsame_buchungen/uebersicht_gemeinsam.html']
