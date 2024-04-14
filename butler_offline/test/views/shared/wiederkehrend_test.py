from butler_offline.views.shared.wiederkehrend  import get_ausfuehrungszeitpunkte
from butler_offline.viewcore.converter import datum_from_german as datum
from butler_offline.core.frequency import FREQUENCY_MONATLICH_NAME


def test_berechne_moegliche_ausfuehrungszeitpunkte_should_cap_on_5_in_der_zukunft():
    result = get_ausfuehrungszeitpunkte(
        today=datum('02.01.2022'),
        start_datum=datum('01.01.2022'),
        ende_datum=datum('31.12.2099'),
        rhythmus=FREQUENCY_MONATLICH_NAME,
    )

    assert result == [
        datum('01.01.2022'),
        datum('01.02.2022'),
        datum('01.03.2022'),
        datum('01.04.2022'),
        datum('01.05.2022'),
        datum('01.06.2022'),
    ]


def test_berechne_moegliche_ausfuehrungszeitpunkte_should_cap_at_endedatum():
    result = get_ausfuehrungszeitpunkte(
        today=datum('02.01.2022'),
        start_datum=datum('01.01.2022'),
        ende_datum=datum('02.03.2022'),
        rhythmus=FREQUENCY_MONATLICH_NAME,
    )

    assert result == [
        datum('01.01.2022'),
        datum('01.02.2022'),
        datum('01.03.2022'),
    ]
