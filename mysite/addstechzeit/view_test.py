'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from addstechzeit import views
from core.DatabaseModule import Database
from mysite.core import DBManager
from mysite.test import DBManagerStub
import viewcore
from viewcore.converter import datum, time





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

    def test_page_init(self):
        self.setUp()
        views.handle_request(GetRequest())

    def test_add(self):
        self.setUp()
        views.handle_request(PostRequest(
            {'action':'add',
             'ID':viewcore.viewcore.get_next_transaction_id(),
             'date':'1/1/2017',
             'start':'9:00',
             'ende':'10:00',
             'arbeitgeber':'DATEV',
             }
         ))

        assert len(self.testdb.stechzeiten.content) == 1
        assert self.testdb.stechzeiten.content.Datum[0] == datum('1/1/2017')
        assert self.testdb.stechzeiten.content.Einstechen[0] == time('9:00')
        assert self.testdb.stechzeiten.content.Ausstechen[0] == time('10:00')
        assert self.testdb.stechzeiten.content.Arbeitgeber[0] == 'DATEV'


    def test_add_should_only_fire_once(self):
        self.setUp()
        same_id = viewcore.viewcore.get_next_transaction_id()
        views.handle_request(PostRequest(
            {'action':'add',
             'ID':same_id,
             'date':'1/1/2017',
             'start':'9:00',
             'ende':'10:00',
             'arbeitgeber':'DATEV',
             }
         ))

        views.handle_request(PostRequest(
            {'action':'add',
             'ID':same_id,
             'date':'2/2/2017',
             'start':'11:00',
             'ende':'12:00',
             'arbeitgeber':'asDATEV',
             }
         ))

        assert len(self.testdb.stechzeiten.content) == 1
        assert self.testdb.stechzeiten.content.Datum[0] == datum('1/1/2017')
        assert self.testdb.stechzeiten.content.Einstechen[0] == time('9:00')
        assert self.testdb.stechzeiten.content.Ausstechen[0] == time('10:00')
        assert self.testdb.stechzeiten.content.Arbeitgeber[0] == 'DATEV'


    def test_edit(self):
        self.setUp()

        views.handle_request(PostRequest(
            {'action':'add',
             'ID':viewcore.viewcore.get_next_transaction_id(),
             'date':'2/2/2017',
             'start':'11:00',
             'ende':'12:00',
             'arbeitgeber':'asDATEV',
             }
         ))

        views.handle_request(PostRequest(
            {'action':'edit',
             'ID':viewcore.viewcore.get_next_transaction_id(),
             'edit_index':'0',
             'date':'1/1/2017',
             'start':'9:00',
             'ende':'10:00',
             'arbeitgeber':'DATEV',
             }
         ))

        assert len(self.testdb.stechzeiten.content) == 1
        assert self.testdb.stechzeiten.content.Datum[0] == datum('1/1/2017')
        assert self.testdb.stechzeiten.content.Einstechen[0] == time('9:00')
        assert self.testdb.stechzeiten.content.Ausstechen[0] == time('10:00')
        assert self.testdb.stechzeiten.content.Arbeitgeber[0] == 'DATEV'

    def test_edit_ausgabe_should_only_fire_once(self):
        self.setUp()

        views.handle_request(PostRequest(
            {'action':'add',
             'ID':viewcore.viewcore.get_next_transaction_id(),
             'date':'2/2/2017',
             'start':'11:00',
             'ende':'12:00',
             'arbeitgeber':'asDATEV',
             }
         ))

        same_index = viewcore.viewcore.get_next_transaction_id()
        views.handle_request(PostRequest(
            {'action':'edit',
             'ID':same_index,
             'edit_index':'0',
             'date':'1/1/2017',
             'start':'9:00',
             'ende':'10:00',
             'arbeitgeber':'DATEV',
             }
         ))

        views.handle_request(PostRequest(
            {'action':'edit',
             'ID':same_index,
             'edit_index':'0',
             'date':'3/2/2020',
             'start':'0:00',
             'ende':'13:22',
             'arbeitgeber':'BlaBla',
             }
         ))

        assert len(self.testdb.stechzeiten.content) == 1
        assert self.testdb.stechzeiten.content.Datum[0] == datum('1/1/2017')
        assert self.testdb.stechzeiten.content.Einstechen[0] == time('9:00')
        assert self.testdb.stechzeiten.content.Ausstechen[0] == time('10:00')
        assert self.testdb.stechzeiten.content.Arbeitgeber[0] == 'DATEV'



    def test_add_sonderzeit(self):
        self.setUp()

        views.handle_request(PostRequest(
            {'action':'add_sonderzeit',
             'ID':viewcore.viewcore.get_next_transaction_id(),
             'date':'2/2/2017',
             'length':'11:00',
             'typ':'Urlaub',
             'arbeitgeber':'asDATEV',
             }
         ))
        assert len(self.testdb.sonderzeiten.content) == 1
        assert self.testdb.sonderzeiten.content.Datum[0] == datum('2/2/2017')
        assert self.testdb.sonderzeiten.content.Dauer[0] == time('11:00')
        assert self.testdb.sonderzeiten.content.Typ[0] == 'Urlaub'
        assert self.testdb.sonderzeiten.content.Arbeitgeber[0] == 'asDATEV'

    def test_add_sonderzeit_should_only_fire_once(self):
        self.setUp()

        same_id = viewcore.viewcore.get_next_transaction_id()
        views.handle_request(PostRequest(
            {'action':'add_sonderzeit',
             'ID':same_id,
             'date':'2/2/2017',
             'length':'11:00',
             'typ':'Urlaub',
             'arbeitgeber':'asDATEV',
             }
         ))
        views.handle_request(PostRequest(
            {'action':'add_sonderzeit',
             'ID':same_id,
             'date':'2/2/2017',
             'length':'11:00',
             'typ':'Urlaub',
             'arbeitgeber':'asDATEV',
             }
         ))
        assert len(self.testdb.sonderzeiten.content) == 1
        assert self.testdb.sonderzeiten.content.Datum[0] == datum('2/2/2017')
        assert self.testdb.sonderzeiten.content.Dauer[0] == time('11:00')
        assert self.testdb.sonderzeiten.content.Typ[0] == 'Urlaub'
        assert self.testdb.sonderzeiten.content.Arbeitgeber[0] == 'asDATEV'

if __name__ == '__main__':
    unittest.main()

class GetRequest():
    method = 'GET'

class PostRequest:

    def __init__(self, args):
        self.POST = args

    method = 'POST'
