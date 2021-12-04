'''
Created on 10.05.2017

@author: sebastian
'''

import unittest

from butler_offline.viewcore.state.persisted_state import database_instance
from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.test.RequestStubs import PostRequest
from butler_offline.views.core import configuration
from butler_offline.core import file_system, configuration_provider
from butler_offline.viewcore import viewcore
from butler_offline.viewcore.state import persisted_state
from butler_offline.viewcore import request_handler
from butler_offline.viewcore.converter import datum_from_german as datum

class TestKonfiguration(unittest.TestCase):

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        persisted_state.DATABASE_INSTANCE = None
        configuration_provider.LOADED_CONFIG = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        configuration.index(GetRequest())

    def test_transaction_id_should_be_in_context(self):
        self.set_up()
        context = configuration.index(GetRequest())
        assert 'ID' in context

    def test_addKategorie(self):
        self.set_up()
        configuration.index(PostRequest({'action': 'add_kategorie', 'neue_kategorie': 'test'}))
        assert database_instance().einzelbuchungen.get_alle_kategorien() == set(['test'])

    def test_change_db_should_trigger_db_reload(self):
        self.set_up()
        configuration.index(PostRequest({'action': 'edit_databases', 'dbs': 'test'}))
        assert database_instance().name == 'test'

        configuration.index(PostRequest({'action': 'edit_databases', 'dbs': 'test2'}))
        assert database_instance().name == 'test2'

    def test_change_partnername_should_change_partnername(self):
        self.set_up()
        assert viewcore.name_of_partner() == 'kein_Partnername_gesetzt'
        configuration.index(PostRequest({'action': 'set_partnername', 'partnername': 'testpartner'}))
        assert viewcore.name_of_partner() == 'testpartner'

    def test_change_themecolor_should_change_themecolor(self):
        self.set_up()
        assert configuration_provider.get_configuration('THEME_COLOR') == '#00acd6'
        configuration.index(PostRequest({'action': 'change_themecolor', 'themecolor': '#000000'}))
        assert configuration_provider.get_configuration('THEME_COLOR') == '#000000'

    def test_change_schliesse_kateorien_aus_should_change_add_ausgeschlossene_kategorien(self):
        self.set_up()
        assert configuration_provider.get_configuration('AUSGESCHLOSSENE_KATEGORIEN') == ''
        configuration.index(PostRequest({'action': 'set_ausgeschlossene_kategorien', 'ausgeschlossene_kategorien': 'Alkohol'}))
        assert configuration_provider.get_configuration('AUSGESCHLOSSENE_KATEGORIEN') == 'Alkohol'

    def test_change_partnername_should_mirgrate_old_partnernames(self):
        self.set_up()
        name_of_partner = viewcore.name_of_partner()
        gemeinsame_buchungen = database_instance().gemeinsamebuchungen
        gemeinsame_buchungen.add(datum('01.01.2017'), 'kat', 'name', 1, name_of_partner)

        configuration.index(PostRequest({'action': 'set_partnername', 'partnername': 'testpartner_renamed'}))
        gemeinsame_buchungen = database_instance().gemeinsamebuchungen
        database_partners = gemeinsame_buchungen.content.Person

        assert set(database_partners) == set(['testpartner_renamed'])

    def test_change_colors(self):
        self.set_up()
        assert viewcore.design_colors() == '3c8dbc,f56954,00a65a,00c0ef,f39c12,d2d6de,001F3F,39CCCC,3D9970,01FF70,FF851B,F012BE,8E24AA,D81B60,222222,d2d6de'.split(',')
        configuration.index(PostRequest({'action': 'change_colorpalette',
                                 '0_checked': 'on',
                                 '0_farbe' : '#000000',
                                 '1_checked': 'on',
                                 '1_farbe': '#FFFFFF',
                                 '2_farbe': '#555555'}))
        assert viewcore.design_colors() == ['000000', 'FFFFFF']
        self.set_up()
