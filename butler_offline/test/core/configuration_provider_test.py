from butler_offline.core import file_system, configuration_provider
from butler_offline.test.core.file_system_stub import FileSystemStub

def set_up():
    file_system.INSTANCE = FileSystemStub()
    configuration_provider.LOADED_CONFIG = None


def test_configuration_provider__shoud_load_default__if_no_file_provided():
    set_up()
    assert configuration_provider.get_configuration('DATABASES') == configuration_provider.DEFAULT_CONFIG['DATABASES']
    assert configuration_provider.LOADED_CONFIG == configuration_provider.DEFAULT_CONFIG


def test_configuration_provider__should_extend_loaded_config__if_key_missing():
    set_up()
    configuration_provider.set_configuration('test', 'bla')
    assert configuration_provider.get_configuration('DATABASES') == configuration_provider.DEFAULT_CONFIG['DATABASES']


def test_configuration_provider_should_store_values():
    set_up()
    configuration_provider.set_configuration('test', 'bla')
    assert configuration_provider.get_configuration('test') == 'bla'


def test_configuration_provider_should_update_values():
    set_up()
    configuration_provider.set_configuration('test', 'bla')
    assert configuration_provider.get_configuration('test') == 'bla'
    configuration_provider.set_configuration('test', 'not bla')
    assert configuration_provider.get_configuration('test') == 'not bla'

    
