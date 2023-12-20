from typing import Callable, Any

from butler_offline.viewcore.context.builder import PageContext, VorgeschlageneProblembehebung
from butler_offline.viewcore.http import Request
from butler_offline.viewcore.routes import (EINZELBUCHUNGEN_AUSGABE_ADD, EINZELBUCHUNGEN_EINNAHME_ADD,
                                            EINZELBUCHUNGEN_DAUERAUFTRAG_ADD, GEMEINSAME_BUCHUNGEN_ADD,
                                            SPAREN_SPARKONTO_ADD, SPAREN_DEPOTWERT_ADD, SPAREN_DEPOTAUSZUG_ADD,
                                            SPAREN_ORDER_ADD, SPAREN_ORDERDAUERAUFTRAG_ADD, SPAREN_SPARBUCHUNG_ADD)

KEINE_BUCHUNGEN_ERFASST_MESSAGE = 'Aktuell sind keine Buchungen erfasst'
KEINE_GEMEINSAME_BUCHUNGEN_ERFASST_MESSAGE = 'Aktuell sind keine gemeinsame Buchungen erfasst'
KEINE_DAUERAUFTRAEGE_ERFASST_MESSAGE = 'Aktuell sind keine Dauerauftraege erfasst'
KEINE_DEPOTS_ERFASST_MESSAGE = 'Aktuell ist noch kein Sparkonto vom Typ "Depot" erfasst'
KEINE_DEPOTWERTE_ERFASST_MESSAGE = 'Aktuell sind keine Depotwerte erfasst'
KEINE_SPARFAEHIGEN_KONTOS_ERFASST_MESSAGE = 'Aktuell ist noch kein Sparkonto vom Typ "Sparkonto" erfasst'
KEINE_DEPOTAUSZUEGE_ERFASST_MESSAGE = 'Aktuell ist noch kein Depotauszug erfasst'
KEINE_ETFS_ERFASST_MESSAGE = 'Aktuell ist kein Depotwert mit Typ "ETF" und einer gültigen ISIN erfasst'
KEINE_ORDER_ERFASST_MESSAGE = 'Aktuell ist keine Order erfasst'
KEINE_ORDER_DAUERAUFTRAEGE_ERFASST_MESSAGE = 'Aktuell sind keine Order-Dauerauftraege erfasst'
KEINE_SPARBUCHUNGEN_ERFASST_MESSAGE = 'Aktuell sind keine Sparbuchungen erfasst'
DATENBANK_LEER_MESSAGE = 'Aktuell sind weder Einnahmen, Ausgaben, Order oder Sparbuchungen erfasst'


def einzelbuchung_needed_decorator():
    return needed_something_decorator(
        something_matcher=lambda database: database.einzelbuchungen().select().count() > 0,
        message=KEINE_BUCHUNGEN_ERFASST_MESSAGE,
        vorgeschlagene_problemloesung=[
            ausgabe_erfassen_vorschlag(),
            einnahme_erfassen_vorschlag(),
            dauerauftrag_erfassen_vorschlag()]
    )


def einnahme_erfassen_vorschlag() -> VorgeschlageneProblembehebung:
    return VorgeschlageneProblembehebung(
        link=EINZELBUCHUNGEN_EINNAHME_ADD,
        link_beschreibung='Jetzt eine Einnahme erfassen'
    )


def ausgabe_erfassen_vorschlag() -> VorgeschlageneProblembehebung:
    return VorgeschlageneProblembehebung(
        link=EINZELBUCHUNGEN_AUSGABE_ADD,
        link_beschreibung='Jetzt eine Ausgabe erfassen'
    )


def dauerauftrag_needed_decorator():
    return needed_something_decorator(
        something_matcher=lambda database: database.dauerauftraege().select().count() > 0,
        message=KEINE_DAUERAUFTRAEGE_ERFASST_MESSAGE,
        vorgeschlagene_problemloesung=[
            dauerauftrag_erfassen_vorschlag()
        ]
    )


def dauerauftrag_erfassen_vorschlag() -> VorgeschlageneProblembehebung:
    return VorgeschlageneProblembehebung(
        link=EINZELBUCHUNGEN_DAUERAUFTRAG_ADD,
        link_beschreibung='Jetzt einen Dauerauftrag erfassen'
    )


def gemeinsame_buchung_needed_decorator():
    return needed_something_decorator(
        something_matcher=lambda database: database.gemeinsamebuchungen().select().count() > 0,
        message=KEINE_GEMEINSAME_BUCHUNGEN_ERFASST_MESSAGE,
        vorgeschlagene_problemloesung=[
            VorgeschlageneProblembehebung(
                link=GEMEINSAME_BUCHUNGEN_ADD,
                link_beschreibung='Jetzt eine gemeinsame Buchung erfassen'
            )
        ]
    )


def depotauszug_needed_decorator():
    return needed_something_decorator(
        something_matcher=lambda database: database.depotauszuege().select().count() > 0,
        message=KEINE_DEPOTAUSZUEGE_ERFASST_MESSAGE,
        vorgeschlagene_problemloesung=[
            VorgeschlageneProblembehebung(
                link=SPAREN_DEPOTAUSZUG_ADD,
                link_beschreibung='Jetzt einen Depotauszug erfassen'
            )
        ]
    )


def depots_needed_decorator():
    return needed_something_decorator(
        something_matcher=lambda database: len(database.kontos().get_depots()) > 0,
        message=KEINE_DEPOTS_ERFASST_MESSAGE,
        vorgeschlagene_problemloesung=[
            VorgeschlageneProblembehebung(
                link=SPAREN_SPARKONTO_ADD,
                link_beschreibung='Jetzt ein Sparkonto vom Typ "Depot" erfassen'
            )
        ]
    )


def sparkontos_needed_decorator():
    return needed_something_decorator(
        something_matcher=lambda database: len(database.kontos().get_sparfaehige_kontos()) > 0,
        message=KEINE_SPARFAEHIGEN_KONTOS_ERFASST_MESSAGE,
        vorgeschlagene_problemloesung=[
            VorgeschlageneProblembehebung(
                link=SPAREN_SPARKONTO_ADD,
                link_beschreibung='Jetzt ein Sparkonto vom Typ "Sparkonto" erfassen'
            )
        ]
    )


def etfs_needed_decorator():
    return needed_something_decorator(
        something_matcher=lambda database: len(database.depotwerte().get_valid_isins()) > 0,
        message=KEINE_ETFS_ERFASST_MESSAGE,
        vorgeschlagene_problemloesung=[
            VorgeschlageneProblembehebung(
                link=SPAREN_DEPOTWERT_ADD,
                link_beschreibung='Jetzt ein Depotwertvom Typ ETF mit einer gültigen ISIN erfassen'
            )
        ]
    )


def depotwerte_needed_decorator():
    return needed_something_decorator(
        something_matcher=lambda database: len(database.depotwerte().get_depotwerte()) > 0,
        message=KEINE_DEPOTWERTE_ERFASST_MESSAGE,
        vorgeschlagene_problemloesung=[
            VorgeschlageneProblembehebung(
                link=SPAREN_DEPOTWERT_ADD,
                link_beschreibung='Jetzt ein Depotwert erfassen'
            )
        ]
    )


def order_needed_decorator():
    return needed_something_decorator(
        something_matcher=lambda database: database.order().select().count() > 0,
        message=KEINE_ORDER_ERFASST_MESSAGE,
        vorgeschlagene_problemloesung=[
            order_erfassen_vorschlag()
        ]
    )


def order_erfassen_vorschlag():
    return VorgeschlageneProblembehebung(
        link=SPAREN_ORDER_ADD,
        link_beschreibung='Jetzt eine Order erfassen'
    )


def order_dauerauftrag_needed_decorator():
    return needed_something_decorator(
        something_matcher=lambda database: database.orderdauerauftrag().select().count() > 0,
        message=KEINE_ORDER_DAUERAUFTRAEGE_ERFASST_MESSAGE,
        vorgeschlagene_problemloesung=[
            VorgeschlageneProblembehebung(
                link=SPAREN_ORDERDAUERAUFTRAG_ADD,
                link_beschreibung='Jetzt einen Order-Dauerauftrag erfassen'
            )
        ]
    )


def sparbuchungen_needed_decorator():
    return needed_something_decorator(
        something_matcher=lambda database: database.sparbuchungen().select().count() > 0,
        message=KEINE_SPARBUCHUNGEN_ERFASST_MESSAGE,
        vorgeschlagene_problemloesung=[
            sparbuchungen_erfassen_vorschlag()
        ]
    )


def sparbuchungen_erfassen_vorschlag():
    return VorgeschlageneProblembehebung(
        link=SPAREN_SPARBUCHUNG_ADD,
        link_beschreibung='Jetzt eine Sparbuchung erfassen'
    )


def irgendwas_needed_decorator():
    return needed_something_decorator(
        something_matcher=lambda
            database: database.order().select().count() > 0 or database.einzelbuchungen().select().count() > 0,
        message=DATENBANK_LEER_MESSAGE,
        vorgeschlagene_problemloesung=[
            einnahme_erfassen_vorschlag(),
            ausgabe_erfassen_vorschlag(),
            sparbuchungen_erfassen_vorschlag(),
            order_erfassen_vorschlag()
        ]
    )


def needed_something_decorator(
        something_matcher: Callable[[Any], bool],
        message: str,
        vorgeschlagene_problemloesung: list[VorgeschlageneProblembehebung]
):
    def decorator(fun: Callable[[Request, Any], PageContext]):
        def wrapper(*args, **kwargs):
            result: PageContext = fun(*args, **kwargs)
            if 'context' in kwargs.keys():
                database = kwargs['context']
            else:
                database = args[1]
            if something_matcher(database):
                return result

            result.add_info_message(
                message=message,
                vorgeschlagene_problembehebungen=vorgeschlagene_problemloesung)
            return result
        return wrapper
    return decorator
