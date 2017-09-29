'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from configuration import views
from core.DatabaseModule import Database
from mysite.core import DBManager
from mysite.test import DBManagerStub
import viewcore





'''
'''
class TesteSollzeit(unittest.TestCase):

    def setUp(self):
        print('create new database')
        self.testdb = Database('test')
        viewcore.viewcore.DATABASE_INSTANCE = self.testdb
        viewcore.viewcore.DATABASES = ['test']
        DBManager.read_function = DBManagerStub.from_string
        DBManager.write_function = DBManagerStub.to_string

    def test_init(self):
        self.setUp()
        views.handle_request(GetRequest())

    def teste_addKategorie(self):
        self.setUp()
        views.handle_request(PostRequest({'action':'add_kategorie', 'neue_kategorie':'test'}))
        assert self.testdb.einzelbuchungen.get_alle_kategorien() == set(['test'])


if __name__ == '__main__':
    unittest.main()

class GetRequest():
    method = 'GET'

class PostRequest:

    def __init__(self, args):
        self.POST = args

    method = 'POST'
