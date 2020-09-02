
from butler_offline.viewcore.viewcore import database_instance



CONTEXT = {}

KEY_CHANGED_EINZELBUCHUNGEN = 'einzelbuchungen_changed'
KEY_CHANGED_DAUERAUFTRAEGE = 'dauerauftraege_changed'
KEY_CHANGED_GEMEINSAME_BUCHUNGEN = 'gemeinsamebuchungen_changed'

def _get_context():
    database_name = database_instance()
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
