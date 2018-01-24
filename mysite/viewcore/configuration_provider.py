from viewcore import configuration_provider
from pathlib import Path
from functools import reduce

LOADED_CONFIG = {}
DEFAULT_CONFIG = {
    'DATABASES': 'Test_User',
    'PARTNERNAME': 'kein_Partnername_gesetzt'
}
def _from_file():
    if not Path("../config").is_file():
        return None

    with open('../config', 'r') as myfile:
        content = myfile.read()
    return content

def _to_file(content):
    with open('../config', 'w') as myfile:
        myfile.write(content)
        myfile.close()


LOADER = _from_file
SAVER = _to_file

def _load_config():
    loaded_content = configuration_provider.LOADER()
    if not loaded_content:
        return configuration_provider.DEFAULT_CONFIG
    lines = loaded_content.split('\n')
    loaded_config = {}
    for line in lines:
        if ':' in line:
            line = line.strip()
            loaded_config[line.split(':')[0]] = line.split(':')[1]
    for key in configuration_provider.DEFAULT_CONFIG:
        if key not in loaded_config:
            loaded_config[key] = configuration_provider.DEFAULT_CONFIG[key]
    print("#####",loaded_config)
    return loaded_config

def _save_config(config):
    content = []
    for key in config:
        content.append('{key}:{value}'.format(key=key, value=config[key]))
    content = reduce(lambda x,y: str(x)+'\n'+str(y), content)
    configuration_provider.SAVER(content)

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


DEBUG_FILE = None
def _from_string():
    return DEBUG_FILE

def _to_string(content):
    configuration_provider.DEBUG_FILE = content


def stub_me(content=None):
    configuration_provider.LOADER = _from_string
    configuration_provider.SAVER = _to_string
    configuration_provider.DEBUG_FILE = content
    configuration_provider.LOADED_CONFIG = None

