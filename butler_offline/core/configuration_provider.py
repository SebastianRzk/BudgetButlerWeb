from functools import reduce
import logging
from butler_offline.core import file_system
from butler_offline.core import configuration_provider
from os import getenv
from typing import Callable


BUDGETBUTLERWEB_DATABASE_PATH = getenv('BUDGETBUTLERWEB_DATABASE_PATH', '.')
BUDGETBUTLERWEB_DATABASE_BACKUP_PATH = getenv('BUDGETBUTLERWEB_DATABASE_BACKUP_PATH', './Backups')
BUDGETBUTLERWEB_CONFIG_PATH = getenv('BUDGETBUTLERWEB_CONFIG_PATH', '.')
LOADED_CONFIG = {}
DEFAULT_CONFIG = {
    'DATABASES': 'Test_User',
    'PARTNERNAME': 'kein_Partnername_gesetzt',
    'DESIGN_COLORS': '3c8dbc,f56954,00a65a,00c0ef,f39c12,d2d6de,001F3F,39CCCC,3D9970,01FF70,FF851B,F012BE,8E24AA,D81B60,222222,d2d6de',
    'THEME_COLOR' : '#00acd6',
    'ONLINE_DEFAULT_SERVER': '',
    'ONLINE_DEFAULT_USER': '',
    'AUSGESCHLOSSENE_KATEGORIEN': ''
}


def get_database_path() -> str:
    return BUDGETBUTLERWEB_DATABASE_PATH


def get_database_backup_path() -> str:
    return BUDGETBUTLERWEB_DATABASE_BACKUP_PATH


def get_config_path() -> str:
    return BUDGETBUTLERWEB_CONFIG_PATH


def _load_config():
    lines = file_system.instance().read(get_config_path() + '/config')
    if not lines:
        return dict(configuration_provider.DEFAULT_CONFIG)
    loaded_config = {}
    for line in lines:
        if ':' in line:
            line = line.strip()
            loaded_config[line.split(':', 1)[0]] = line.split(':', 1)[1]
    for key in dict(configuration_provider.DEFAULT_CONFIG):
        if key not in loaded_config:
            loaded_config[key] = configuration_provider.DEFAULT_CONFIG[key]
    logging.debug('loaded info %s', loaded_config)
    return loaded_config


def _save_config(config):
    content = []
    for key in config:
        content.append('{key}:{value}'.format(key=key, value=config[key]))
    content = reduce(lambda x, y: str(x) + '\n' + str(y), content)
    file_system.instance().write(get_config_path() + '/config', content)


def get_configuration(key):
    if not configuration_provider.LOADED_CONFIG:
        configuration_provider.LOADED_CONFIG = _load_config()
    return configuration_provider.LOADED_CONFIG[key]


def set_configuration(key, value):
    if not configuration_provider.LOADED_CONFIG:
        configuration_provider.LOADED_CONFIG = _load_config()
    configuration_provider.LOADED_CONFIG[key] = value
    _save_config(configuration_provider.LOADED_CONFIG)
    configuration_provider.LOADED_CONFIG = _load_config()


class ConfigurationProvider:
    def __init__(self, set_configuration_fun: Callable[[str, str], None], get_configuration_fun: Callable[[str], str]):
        self._set_configuration = set_configuration_fun
        self._get_configuration = get_configuration_fun

    def set_configuration(self, key: str, value: str):
        self._set_configuration(key=key, value=value)

    def get_configuration(self, key: str) -> str:
        return self._get_configuration(key=key)


CONFIGURATION_PROVIDER = ConfigurationProvider(
    set_configuration_fun=set_configuration,
    get_configuration_fun=get_configuration,
)


class DictConfiguration(ConfigurationProvider):
    def __init__(self, initial_conf: dict):
        super().__init__(set_configuration_fun=self.set_to_dict, get_configuration_fun=self.get_from_dict)
        self._conf = initial_conf

    def get_from_dict(self, key: str):
        return self._conf[key]

    def set_to_dict(self, key: str, value: str):
        self._conf[key] = value