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
from viewcore import configuration_provider

class TesteSollzeit(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()
        request_handler.stub_me()
        configuration_provider.stub_me()

    def test_init(self):
        self.set_up()
        views.index(GetRequest())

    def teste_addKategorie(self):
        self.set_up()
        views.index(PostRequest({'action':'add_kategorie', 'neue_kategorie':'test'}))
        assert viewcore.database_instance().einzelbuchungen.get_alle_kategorien() == set(['test'])

    def teste_change_partnername(self):
        self.set_up()
        assert viewcore.name_of_partner() == 'kein_Partnername_gesetzt'
        views.index(PostRequest({'action':'set_partnername', 'partnername':'testpartner'}))
        assert viewcore.name_of_partner() == 'testpartner'


if __name__ == '__main__':
    unittest.main()
