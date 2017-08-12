'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from addgemeinsam import views
from core.DatabaseModule import Database
import viewcore
from viewcore.converter import datum


'''
'''
class TesteAddGemeinsamView(unittest.TestCase):

    def setUp(self):
        print('create new database')
        self.testdb = Database('test')
        viewcore.viewcore.DATABASE_INSTANCE = self.testdb
        viewcore.viewcore.DATABASES = ['test']
        viewcore.viewcore.TEST = True

    def test_init(self):
        self.setUp()
        views.handle_request(GetRequest())

    def test_add_shouldAddGemeinsameBuchung(self):
        self.setUp()
        views.handle_request(PostRequest(
            {'action':'add',
             'ID':viewcore.viewcore.get_next_transaction_id(),
             'date':'1/1/2017',
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson',
             'wert':'2,00'
             }
         ))
        assert self.testdb.gemeinsame_buchungen.Wert[0] == -1 * float('2.00')
        assert self.testdb.gemeinsame_buchungen.Name[0] == 'testname'
        assert self.testdb.gemeinsame_buchungen.Kategorie[0] == 'Essen'
        assert self.testdb.gemeinsame_buchungen.Datum[0] == datum('1/1/2017')
        assert self.testdb.gemeinsame_buchungen.Person[0] == 'testperson'

    def test_add_shouldAddDynamicEinzelbuchung(self):
        self.setUp()
        views.handle_request(PostRequest(
            {'action':'add',
             'ID':viewcore.viewcore.get_next_transaction_id(),
             'date':'1/1/2017',
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson',
             'wert':'2,00'
             }
         ))

        assert self.testdb.einzelbuchungen.content.Wert[0] == -1 * 0.5 * float('2.00')
        assert self.testdb.einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert self.testdb.einzelbuchungen.content.Datum[0] == datum('1/1/2017')
        assert self.testdb.einzelbuchungen.content.Name[0] == 'testname (noch nicht abgerechnet, von testperson)'

    def test_add_should_only_fire_once(self):
        self.setUp()
        next_id = viewcore.viewcore.get_next_transaction_id()
        views.handle_request(PostRequest(
            {'action':'add',
             'ID':next_id,
             'date':'1/1/2017',
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson',
             'wert':'2,00'
             }
         ))
        views.handle_request(PostRequest(
            {'action':'add',
             'ID':next_id,
             'date':'1/1/2017',
             'kategorie':'overwritten',
             'name':'overwritten',
             'person':'overwritten',
             'wert':'0,00'
             }
         ))
        assert self.testdb.gemeinsame_buchungen.Wert[0] == -1 * float('2.00')
        assert self.testdb.gemeinsame_buchungen.Name[0] == 'testname'
        assert self.testdb.gemeinsame_buchungen.Kategorie[0] == 'Essen'
        assert self.testdb.gemeinsame_buchungen.Datum[0] == datum('1/1/2017')
        assert self.testdb.gemeinsame_buchungen.Person[0] == 'testperson'

    def test_edit_ausgabe(self):
        self.setUp()

        views.handle_request(PostRequest(
            {'action':'add',
             'ID':viewcore.viewcore.get_next_transaction_id(),
             'date':'1/1/2017',
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson',
             'wert':'2,00'
             }
         ))

        views.handle_request(PostRequest(
            {'action':'add',
             'ID':viewcore.viewcore.get_next_transaction_id(),
             'edit_index':'0',
             'date':'5/1/2017',
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson2',
             'wert':'2,50'
             }
         ))

        assert self.testdb.gemeinsame_buchungen.Wert[0] == -1 * float('2.50')
        assert self.testdb.gemeinsame_buchungen.Name[0] == 'testname'
        assert self.testdb.gemeinsame_buchungen.Kategorie[0] == 'Essen'
        assert self.testdb.gemeinsame_buchungen.Datum[0] == datum('5/1/2017')
        assert self.testdb.gemeinsame_buchungen.Person[0] == 'testperson2'

    def test_edit_should_only_fire_once(self):
        self.setUp()

        views.handle_request(PostRequest(
            {'action':'add',
             'ID':viewcore.viewcore.get_next_transaction_id(),
             'date':'1/1/2017',
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson',
             'wert':'2,00'
             }
         ))

        next_id = viewcore.viewcore.get_next_transaction_id()
        views.handle_request(PostRequest(
            {'action':'add',
             'ID':next_id,
             'edit_index':'0',
             'date':'5/1/2017',
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson2',
             'wert':'2,50'
             }
         ))
        views.handle_request(PostRequest(
            {'action':'add',
             'ID':next_id,
             'edit_index':'0',
             'date':'5/1/2017',
             'kategorie':'overwritten',
             'name':'overwritten',
             'person':'overwritten',
             'wert':'0,00'
             }
         ))
        assert self.testdb.gemeinsame_buchungen.Wert[0] == -1 * float('2.50')
        assert self.testdb.gemeinsame_buchungen.Name[0] == 'testname'
        assert self.testdb.gemeinsame_buchungen.Kategorie[0] == 'Essen'
        assert self.testdb.gemeinsame_buchungen.Datum[0] == datum('5/1/2017')
        assert self.testdb.gemeinsame_buchungen.Person[0] == 'testperson2'


if __name__ == '__main__':
    unittest.main()

class GetRequest():
    method = 'GET'

class PostRequest:

    def __init__(self, args):
        self.POST = args

    method = 'POST'
