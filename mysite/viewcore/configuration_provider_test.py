import sys, os
import unittest
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")
'''
'''
from viewcore import configuration_provider




class TesteConverter(unittest.TestCase):
    def test_configuration_provider_shouldLoadDefault_ifNoFileProvided(self):
        configuration_provider.stub_me(None)
        assert configuration_provider.get_configuration('DATABASES') == configuration_provider.DEFAULT_CONFIG['DATABASES']

    def test_configuration_provider_shouldExtendLoadedConfig_ifKeyMissing(self):
        configuration_provider.stub_me('''
        test:bla
        ''')
        assert configuration_provider.get_configuration('DATABASES') == configuration_provider.DEFAULT_CONFIG['DATABASES']

    def test_configuration_provider_should_load_values(self):
        configuration_provider.stub_me('''
        test:bla
        ''')
        assert configuration_provider.get_configuration('test') == 'bla'
