from butler_offline.core import database_manager, configuration_provider
from butler_offline.viewcore.state import persisted_state
from butler_offline.core.shares.shares_manager import load_data
import random

DATABASE_INSTANCE = None
DATABASES = []
SHARES_DATA = None


SESSION_RANDOM = str(random.random())
DATABASE_VERSION = 0


def database_instance():
    '''
    returns the actual database instance
    '''
    if not persisted_state.DATABASES:
        persisted_state.DATABASES = configuration_provider.get_configuration('DATABASES').split(',')

    if persisted_state.DATABASE_INSTANCE is None:
        ausgeschlossene_kategorien = set(
            configuration_provider.get_configuration('AUSGESCHLOSSENE_KATEGORIEN').split(','))
        persisted_state.DATABASE_INSTANCE = database_manager.read(persisted_state.DATABASES[0],
                                                                  ausgeschlossene_kategorien=ausgeschlossene_kategorien)
    return persisted_state.DATABASE_INSTANCE


def shares_data():
    if not persisted_state.SHARES_DATA:
        persisted_state.SHARES_DATA = load_data()
    return persisted_state.SHARES_DATA


def switch_database_instance(database_name):
    ausgeschlossene_kategorien = set(configuration_provider.get_configuration('AUSGESCHLOSSENE_KATEGORIEN').split(','))
    persisted_state.DATABASE_INSTANCE = database_manager.read(database_name, ausgeschlossene_kategorien=ausgeschlossene_kategorien)


def _save_database():
    if persisted_state.DATABASE_INSTANCE:
        database_manager.write(persisted_state.DATABASE_INSTANCE)


def _save_refresh():
    _save_database()
    db_name = persisted_state.DATABASE_INSTANCE.name
    persisted_state.DATABASE_INSTANCE = None
    switch_database_instance(db_name)


def save_tainted():
    db = persisted_state.DATABASE_INSTANCE
    if db.is_tainted():
        print('Saving database with', db.taint_number(), 'modifications')
        _save_refresh()
        print('Saved')


def current_database_version():
    return persisted_state.SESSION_RANDOM + ' ' + persisted_state.database_instance().name + '_VERSION_' + str(persisted_state.DATABASE_VERSION)


def increase_database_version():
    persisted_state.DATABASE_VERSION = persisted_state.DATABASE_VERSION + 1
