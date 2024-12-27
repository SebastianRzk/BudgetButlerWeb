import logging
from os import getenv
from typing import Callable
import file_system


DEFAULT_CONFIG = {
    'DATABASES': 'Test_User',
    'PARTNERNAME': 'kein_Partnername_gesetzt',
    'DESIGN_COLORS': '3c8dbc,f56954,00a65a,00c0ef,f39c12,d2d6de,001F3F,39CCCC,3D9970,01FF70,FF851B,F012BE,8E24AA,D81B60,222222,d2d6de',
    'THEME_COLOR' : '#00acd6',
    'ONLINE_DEFAULT_SERVER': '',
    'ONLINE_DEFAULT_USER': '',
    'AUSGESCHLOSSENE_KATEGORIEN': ''
}


def _load_config():
    lines = file_system.FileSystemImpl().read('./config')
    if not lines:
        return dict(DEFAULT_CONFIG)
    loaded_config = {}
    for line in lines:
        if ':' in line:
            line = line.strip()
            loaded_config[line.split(':', 1)[0]] = line.split(':', 1)[1]
    for key in dict(DEFAULT_CONFIG):
        if key not in loaded_config:
            loaded_config[key] = DEFAULT_CONFIG[key]
    logging.debug('loaded info %s', loaded_config)
    return loaded_config



def get_configuration(key):
    return _load_config()[key]



class ConfigurationProvider:
    def __init__(self, set_configuration_fun: Callable[[str, str], None], get_configuration_fun: Callable[[str], str]):
        self._set_configuration = set_configuration_fun
        self._get_configuration = get_configuration_fun

    def set_configuration(self, key: str, value: str):
        self._set_configuration(key=key, value=value)

    def get_configuration(self, key: str) -> str:
        return self._get_configuration(key=key)



class DictConfiguration(ConfigurationProvider):
    def __init__(self, initial_conf: dict):
        super().__init__(set_configuration_fun=self.set_to_dict, get_configuration_fun=self.get_from_dict)
        self._conf = initial_conf

    def get_from_dict(self, key: str):
        return self._conf[key]

    def set_to_dict(self, key: str, value: str):
        self._conf[key] = value