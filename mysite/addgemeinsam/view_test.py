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
from mysite.test import DBManagerStub
import viewcore
from viewcore.converter import datum




'''
'''
class TesteAddGemeinsamView(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()


    def test_init(self):
        self.set_up()
        context = views.handle_request(GetRequest())
        assert context['approve_title'] == 'Gemeinsame Ausgabe hinzufügen'

    def test_editCallFromUeberischt_shouldNameButtonEdit(self):
        self.set_up()
        testdb = viewcore.viewcore.database_instance()
        testdb.gemeinsamebuchungen.add(datum('10/10/2010'), 'kategorie', 'ausgaben_name', 10, 'Sebastian')
        context = views.handle_request(PostRequest({'action':'edit', 'edit_index':'0'}))
        assert context['approve_title'] == 'Gemeinsame Ausgabe aktualisieren'

    def test_add_shouldAddGemeinsameBuchung(self):
        self.set_up()
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
        testdb = viewcore.viewcore.database_instance()
        assert testdb.gemeinsamebuchungen.content.Wert[0] == -1 * float('2.00')
        assert testdb.gemeinsamebuchungen.content.Name[0] == 'testname'
        assert testdb.gemeinsamebuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.gemeinsamebuchungen.content.Datum[0] == datum('1/1/2017')
        assert testdb.gemeinsamebuchungen.content.Person[0] == 'testperson'

    def test_add_shouldAddDynamicEinzelbuchung(self):
        self.set_up()
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
        testdb = viewcore.viewcore.database_instance()
        assert testdb.einzelbuchungen.content.Wert[0] == -1 * 0.5 * float('2.00')
        assert testdb.einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.einzelbuchungen.content.Datum[0] == datum('1/1/2017')
        assert testdb.einzelbuchungen.content.Name[0] == 'testname (noch nicht abgerechnet, von testperson)'

    def test_add_should_only_fire_once(self):
        self.set_up()
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
        testdb = viewcore.viewcore.database_instance()
        assert testdb.gemeinsamebuchungen.content.Wert[0] == -1 * float('2.00')
        assert testdb.gemeinsamebuchungen.content.Name[0] == 'testname'
        assert testdb.gemeinsamebuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.gemeinsamebuchungen.content.Datum[0] == datum('1/1/2017')
        assert testdb.gemeinsamebuchungen.content.Person[0] == 'testperson'

    def test_edit_ausgabe(self):
        self.set_up()

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

        testdb = viewcore.viewcore.database_instance()
        assert testdb.gemeinsamebuchungen.content.Wert[0] == -1 * float('2.50')
        assert testdb.gemeinsamebuchungen.content.Name[0] == 'testname'
        assert testdb.gemeinsamebuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.gemeinsamebuchungen.content.Datum[0] == datum('5/1/2017')
        assert testdb.gemeinsamebuchungen.content.Person[0] == 'testperson2'

    def test_edit_should_only_fire_once(self):
        self.set_up()

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
        testdb = viewcore.viewcore.database_instance()
        assert testdb.gemeinsamebuchungen.content.Wert[0] == -1 * float('2.50')
        assert testdb.gemeinsamebuchungen.content.Name[0] == 'testname'
        assert testdb.gemeinsamebuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.gemeinsamebuchungen.content.Datum[0] == datum('5/1/2017')
        assert testdb.gemeinsamebuchungen.content.Person[0] == 'testperson2'


if __name__ == '__main__':
    unittest.main()

class GetRequest():
    method = 'GET'

class PostRequest:

    def __init__(self, args):
        self.POST = args

    method = 'POST'
