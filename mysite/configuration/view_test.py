'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from test import DBManagerStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from configuration import views
from core import DBManager
from core.DatabaseModule import Database
from viewcore import viewcore
from viewcore import request_handler
from viewcore.converter import datum
from viewcore import configuration_provider


class TestKonfiguration(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()
        request_handler.stub_me()
        configuration_provider.stub_me()

    def test_init(self):
        self.set_up()
        views.index(GetRequest())

    def test_addKategorie(self):
        self.set_up()
        views.index(PostRequest({'action':'add_kategorie', 'neue_kategorie':'test'}))
        assert viewcore.database_instance().einzelbuchungen.get_alle_kategorien() == set(['test'])

    def test_change_db_should_trigger_db_reload(self):
        self.set_up()
        views.index(PostRequest({'action':'edit_databases', 'dbs':'test'}))
        assert viewcore.database_instance().name == 'test'

        views.index(PostRequest({'action':'edit_databases', 'dbs':'test2'}))
        assert viewcore.database_instance().name == 'test2'

    def test_change_partnername_should_change_partnername(self):
        self.set_up()
        assert viewcore.name_of_partner() == 'kein_Partnername_gesetzt'
        views.index(PostRequest({'action':'set_partnername', 'partnername':'testpartner'}))
        assert viewcore.name_of_partner() == 'testpartner'

    def test_change_themecolor_should_change_partnername(self):
        self.set_up()
        assert configuration_provider.get_configuration('THEME_COLOR') == '#00acd6'
        views.index(PostRequest({'action':'change_themecolor', 'themecolor':'#000000'}))
        assert configuration_provider.get_configuration('THEME_COLOR') == '#000000'

    def test_change_partnername_should_mirgrate_old_partnernames(self):
        self.set_up()
        name_of_partner = viewcore.name_of_partner()
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen
        gemeinsame_buchungen.add(datum('01.01.2017'), 'kat', 'name', 1, name_of_partner)

        views.index(PostRequest({'action':'set_partnername', 'partnername':'testpartner_renamed'}))
        gemeinsame_buchungen = viewcore.database_instance().gemeinsamebuchungen
        database_partners = gemeinsame_buchungen.content.Person

        assert set(database_partners) == set(['testpartner_renamed'])

