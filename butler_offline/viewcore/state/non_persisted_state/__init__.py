from typing import Callable

from butler_offline.viewcore.state.non_persisted_state.einzelbuchungen import EinzelbuchungsChange
from butler_offline.viewcore.state.non_persisted_state.dauerauftraege import DauerauftraegeChange


class NonPersistedContext:
    def __init__(self):
        self.einzelbuchungen_changed: list[EinzelbuchungsChange] = []
        self.dauerauftraege_changed: list[DauerauftraegeChange] = []
        self.gemeinsamebuchungen_changed: list = []
        self.sparbuchungen_changed: list = []
        self.sparkontos_changed: list = []
        self.depotwerte_changed: list = []
        self.order_changed: list = []
        self.order_dauerauftrag_changed: list = []
        self.depotauszuege_changed: list = []
        self.butler_online_function: Callable = None


CONTEXT: NonPersistedContext = NonPersistedContext()


def get_changed_einzelbuchungen() -> list[EinzelbuchungsChange]:
    return CONTEXT.einzelbuchungen_changed


def add_changed_einzelbuchungen(new_event: EinzelbuchungsChange) -> None:
    CONTEXT.einzelbuchungen_changed.append(new_event)


def get_changed_dauerauftraege() -> list[DauerauftraegeChange]:
    return CONTEXT.dauerauftraege_changed


def add_changed_dauerauftraege(new_event: DauerauftraegeChange) -> None:
    CONTEXT.dauerauftraege_changed.append(new_event)


def add_changed_gemeinsamebuchungen(new_event) -> None:
    CONTEXT.gemeinsamebuchungen_changed.append(new_event)


def get_changed_gemeinsamebuchungen() -> list:
    return CONTEXT.gemeinsamebuchungen_changed


def add_changed_sparbuchungen(new_event) -> None:
    CONTEXT.sparbuchungen_changed.append(new_event)


def get_changed_sparbuchungen() -> list:
    return CONTEXT.sparbuchungen_changed


def add_changed_sparkontos(new_event) -> None:
    CONTEXT.sparkontos_changed.append(new_event)


def get_changed_sparkontos() -> list:
    return CONTEXT.sparkontos_changed


def get_changed_depotwerte() -> list:
    return CONTEXT.depotwerte_changed


def add_changed_depotwerte(new_changed_depotwere_event) -> None:
    CONTEXT.depotwerte_changed.append(new_changed_depotwere_event)


def get_changed_order() -> list:
    return CONTEXT.order_changed


def add_changed_order(new_event) -> None:
    CONTEXT.order_changed.append(new_event)


def get_changed_depotauszuege() -> list:
    return CONTEXT.depotauszuege_changed


def add_changed_depotauszuege(new_changed_order_event) -> None:
    context = get_changed_depotauszuege()
    context.append(new_changed_order_event)


def get_changed_orderdauerauftrag() -> list:
    return CONTEXT.order_dauerauftrag_changed


def add_changed_orderdauerauftrag(new_changed_order_event) -> None:
    return CONTEXT.order_dauerauftrag_changed.append(new_changed_order_event)
