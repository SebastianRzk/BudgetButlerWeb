from butler_offline.viewcore.state.persisted_state import database_instance

CONTEXT = {}

KEY_CHANGED_EINZELBUCHUNGEN = 'einzelbuchungen_changed'
KEY_CHANGED_DAUERAUFTRAEGE = 'dauerauftraege_changed'
KEY_CHANGED_GEMEINSAME_BUCHUNGEN = 'gemeinsamebuchungen_changed'
KEY_CHANGED_SPARBUCHUNGEN = 'sparbuchungen_changed'
KEY_CHANGED_SPARKONTOS = 'sparkontos_changed'
KEY_CHANGED_DEPOTWERTE = 'depotwerte_changed'
KEY_CHANGED_ORDER = 'order_changed'
KEY_CHANGED_DEPOTAUSZUEGE = 'depotauszue_changed'

def _get_context():
    database_name = database_instance().name
    if database_name not in CONTEXT.keys():
        CONTEXT[database_name] = {}
    return CONTEXT[database_name]


def _get_context_for_key(key):
    context = _get_context()
    if key not in context.keys():
        context[key] = []
    return context[key]


def get_changed_einzelbuchungen():
   return _get_context_for_key(KEY_CHANGED_EINZELBUCHUNGEN)


def add_changed_einzelbuchungen(new_changed_einzelbuchung_event):
    context = get_changed_einzelbuchungen()
    context.append(new_changed_einzelbuchung_event)


def get_changed_dauerauftraege():
    return _get_context_for_key(KEY_CHANGED_DAUERAUFTRAEGE)


def add_changed_dauerauftraege(new_changed_dauerauftraege_event):
    context = get_changed_dauerauftraege()
    context.append(new_changed_dauerauftraege_event)


def add_changed_gemeinsamebuchungen(new_changed_gemeinsamebuchungen_event):
    context = get_changed_gemeinsamebuchungen()
    context.append(new_changed_gemeinsamebuchungen_event)


def get_changed_gemeinsamebuchungen():
    return _get_context_for_key(KEY_CHANGED_GEMEINSAME_BUCHUNGEN)


def add_changed_sparbuchungen(new_changed_sparbuchungen_event):
    context = get_changed_sparbuchungen()
    context.append(new_changed_sparbuchungen_event)


def get_changed_sparbuchungen():
    return _get_context_for_key(KEY_CHANGED_SPARBUCHUNGEN)


def add_changed_sparkontos(new_changed_sparkontos_event):
    context = get_changed_sparkontos()
    context.append(new_changed_sparkontos_event)


def get_changed_sparkontos():
    return _get_context_for_key(KEY_CHANGED_SPARKONTOS)


def get_changed_depotwerte():
    return _get_context_for_key(KEY_CHANGED_DEPOTWERTE)


def add_changed_depotwerte(new_changed_depotwere_event):
    context = get_changed_depotwerte()
    context.append(new_changed_depotwere_event)


def get_changed_order():
    return _get_context_for_key(KEY_CHANGED_ORDER)


def add_changed_order(new_changed_order_event):
    context = get_changed_order()
    context.append(new_changed_order_event)


def get_changed_depotauszuege():
    return _get_context_for_key(KEY_CHANGED_DEPOTAUSZUEGE)


def add_changed_depotauszuege(new_changed_order_event):
    context = get_changed_depotauszuege()
    context.append(new_changed_order_event)


