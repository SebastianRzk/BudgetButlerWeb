from butler_offline.viewcore.converter import datum_from_german


def order_dict(
        datum: str,
        wert: float,
        name: str,
        depotwert: str,
        konto: str,
        index: int = 0,
        dynamisch: bool = False
) -> dict:
    return {
        'Datum': datum_from_german(datum),
        'Wert': wert,
        'Name': name,
        'Depotwert': depotwert,
        'Konto': konto,
        'index': index,
        'Dynamisch': dynamisch
    }
