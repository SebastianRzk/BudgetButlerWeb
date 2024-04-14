from typing import List
from datetime import date
from butler_offline.core.frequency import get_function_for_name


def get_ausfuehrungszeitpunkte(rhythmus: str, start_datum: date, ende_datum: date, today: date) -> List[date]:
    frequenz = get_function_for_name(rhythmus)
    auswahlzeitraum_ende = today + frequenz(5)

    laufdatum = start_datum
    laufindex = 1
    ergebnis = []

    while laufdatum < auswahlzeitraum_ende and laufdatum < ende_datum:
        ergebnis.append(laufdatum)

        laufdatum = start_datum + frequenz(laufindex)
        laufindex += 1

    return ergebnis
