from butler_offline.views.core.configuration import rename_kategorie
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.core.database.dauerauftraege import Dauerauftraege
from butler_offline.test.request_stubs import GetRequest, PostRequest
from butler_offline.test.viewcore.request_handler import run_in_mocked_handler
from butler_offline.viewcore.converter import datum_from_german
from butler_offline.core.frequency import FREQUENCY_MONATLICH_NAME


def test_rename_should_rename():
    einzelbuchungen = Einzelbuchungen()
    einzelbuchungen.add(
        kategorie='Kategorie A',
        name='',
        datum=datum_from_german('01.01.2022'),
        wert=1
    )
    einzelbuchungen.add(
        kategorie='Kategorie A',
        name='not to rename',
        datum=datum_from_german('01.01.2022'),
        wert=1,
        dynamisch=True
    )

    dauerauftraege = Dauerauftraege()
    dauerauftraege.add(
        kategorie='Kategorie A',
        wert=0,
        name='',
        rhythmus=FREQUENCY_MONATLICH_NAME,
        startdatum=datum_from_german('01.01.2022'),
        endedatum=datum_from_german('01.01.2023')
    )

    result = rename_kategorie.handle_request(
        request=PostRequest(
            {
                'kategorie_alt': 'Kategorie A',
                'kategorie_neu': 'Kategorie B'
            }
        ),
        context=rename_kategorie.RenameContext(
            einzelbuchungen=einzelbuchungen,
            dauerauftraege=dauerauftraege
        )
    )

    assert result.is_redirect()
    assert result.redirect_target_url() == ('/configuration/?success_message=Kategorie Kategorie A erfolgreich in '
                                            'Kategorie B umbenannt. <br> 1 Einzelbuchungen wurden aktualisiert <br> 1 '
                                            'Daueraufträge wurden aktualisiert')
    assert einzelbuchungen.get(0)['Kategorie'] == 'Kategorie B'
    assert dauerauftraege.get(0)['Kategorie'] == 'Kategorie B'


def test_index_should_be_secured_by_request_handler():
    def handle():
        rename_kategorie.index(request=GetRequest())

    result = run_in_mocked_handler(handle)

    assert result.number_of_calls() == 1
    assert result.html_pages_requested_to_render() == ['core/configuration.html']
