from butler_offline.viewcore.state.non_persisted_state.einzelbuchungen import EinzelbuchungAddedChange, \
    EinzelbuchungEditiertChange
from butler_offline.viewcore.renderhelper import Betrag


EINE_KATEGORIE = 'eine kategorie'
EIN_DATUM = '01.01.2023'
EIN_NAME = 'ein name'
EIN_WERT = Betrag(123)

EINZELBUCHUNG_ADDED_CHANGE_STR = 'EinzelbuchungsChange(fa=fa fa-plus, datum=01.01.2023, name=ein name,' \
                                 ' kategorie=eine kategorie, wert=Betrag(123.00))'

EINZELBUCHUNG_EDITIERT_CHANGE_STR = 'EinzelbuchungsChange(fa=fa fa-pencil, datum=01.01.2023, name=ein name,' \
                                    ' kategorie=eine kategorie, wert=Betrag(123.00))'

EINZELBUCHUNG_EDITIERT_CHANGE = EinzelbuchungEditiertChange(datum=EIN_DATUM, kategorie=EINE_KATEGORIE,
                                                            name=EIN_NAME, wert=EIN_WERT)

EINZELBUCHUNG_ADDED_CHANGE = EinzelbuchungAddedChange(datum=EIN_DATUM, kategorie=EINE_KATEGORIE,
                                                      name=EIN_NAME, wert=EIN_WERT)
