from butler_offline.viewcore.state.non_persisted_state.dauerauftraege import (DauerauftragAddedChange,
                                                                              DauerauftragEditiertChange)
from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.core.frequency import FREQUENCY_JAEHRLICH_NAME

EINE_KATEGORIE = 'eine kategorie'
EIN_START_DATUM = '01.01.2023'
EIN_ENDE_DATUM = '01.01.2024'
EIN_NAME = 'ein name'
EIN_RHYTHMUS = FREQUENCY_JAEHRLICH_NAME
EIN_WERT = Betrag(123)

DAUERAUFTRAG_ADDED_CHANGE_STR = ('DauerauftragChange(fa=fa fa-plus, start_datum=01.01.2023, ende_datum=01.01.2024,'
                                 ' name=ein name, kategorie=eine kategorie, rhythmus=jaehrlich, wert=Betrag(123.00))')

DAUERAUFTRAG_EDITIERT_CHANGE_STR = ('DauerauftragChange(fa=fa fa-pencil, start_datum=01.01.2023, ende_datum=01.01.2024,'
                                    ' name=ein name, kategorie=eine kategorie, rhythmus=jaehrlich,'
                                    ' wert=Betrag(123.00))')

DAUERAUFTRAG_EDITIERT_CHANGE = DauerauftragEditiertChange(start_datum=EIN_START_DATUM, ende_datum=EIN_ENDE_DATUM,
                                                          kategorie=EINE_KATEGORIE, name=EIN_NAME,
                                                          rhythmus=EIN_RHYTHMUS, wert=EIN_WERT)

DAUERAUFTRAG_ADDED_CHANGE = DauerauftragAddedChange(start_datum=EIN_START_DATUM, ende_datum=EIN_ENDE_DATUM,
                                                    kategorie=EINE_KATEGORIE, name=EIN_NAME,
                                                    rhythmus=EIN_RHYTHMUS, wert=EIN_WERT)
