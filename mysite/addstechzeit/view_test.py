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
from addstechzeit import views
from core import DBManager
from core.DatabaseModule import Database
import viewcore
from viewcore.converter import datum, time


class TesteSollzeit(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()

    def test_page_init(self):
        self.set_up()
        views.handle_request(GetRequest())

    def test_add(self):
        self.set_up()
        views.handle_request(PostRequest(
            {'action':'add',
             'ID':viewcore.viewcore.get_next_transaction_id(),
             'date':'1/1/2017',
             'start':'9:00',
             'ende':'10:00',
             'arbeitgeber':'DATEV',
             }
         ))

        stechzeiten_tabelle = viewcore.viewcore.database_instance().stechzeiten.content
        assert len(stechzeiten_tabelle) == 1
        assert stechzeiten_tabelle.Datum[0] == datum('1/1/2017')
        assert stechzeiten_tabelle.Einstechen[0] == time('9:00')
        assert stechzeiten_tabelle.Ausstechen[0] == time('10:00')
        assert stechzeiten_tabelle.Arbeitgeber[0] == 'DATEV'


    def test_add_should_only_fire_once(self):
        self.set_up()
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
        stechzeiten_tabelle = viewcore.viewcore.database_instance().stechzeiten.content
        assert len(stechzeiten_tabelle) == 1
        assert stechzeiten_tabelle.Datum[0] == datum('1/1/2017')
        assert stechzeiten_tabelle.Einstechen[0] == time('9:00')
        assert stechzeiten_tabelle.Ausstechen[0] == time('10:00')
        assert stechzeiten_tabelle.Arbeitgeber[0] == 'DATEV'

    def test_edit(self):
        self.set_up()

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
        stechzeiten_tabelle = viewcore.viewcore.database_instance().stechzeiten.content
        assert len(stechzeiten_tabelle) == 1
        assert stechzeiten_tabelle.Datum[0] == datum('1/1/2017')
        assert stechzeiten_tabelle.Einstechen[0] == time('9:00')
        assert stechzeiten_tabelle.Ausstechen[0] == time('10:00')
        assert stechzeiten_tabelle.Arbeitgeber[0] == 'DATEV'

    def test_edit_stechzeit_should_only_fire_once(self):
        self.set_up()

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

        stechzeiten_tabelle = viewcore.viewcore.database_instance().stechzeiten.content
        print(stechzeiten_tabelle)
        assert len(stechzeiten_tabelle) == 1
        assert stechzeiten_tabelle.Datum[0] == datum('1/1/2017')
        assert stechzeiten_tabelle.Einstechen[0] == time('9:00')
        assert stechzeiten_tabelle.Ausstechen[0] == time('10:00')
        assert stechzeiten_tabelle.Arbeitgeber[0] == 'DATEV'



    def test_add_sonderzeit(self):
        self.set_up()

        views.handle_request(PostRequest(
            {'action':'add_sonderzeit',
             'ID':viewcore.viewcore.get_next_transaction_id(),
             'date':'2/2/2017',
             'length':'11:00',
             'typ':'Urlaub',
             'arbeitgeber':'asDATEV',
             }
         ))

        sonderzeiten_tabelle = viewcore.viewcore.database_instance().sonderzeiten.content
        assert len(sonderzeiten_tabelle) == 1
        assert sonderzeiten_tabelle.Datum[0] == datum('2/2/2017')
        assert sonderzeiten_tabelle.Dauer[0] == time('11:00')
        assert sonderzeiten_tabelle.Typ[0] == 'Urlaub'
        assert sonderzeiten_tabelle.Arbeitgeber[0] == 'asDATEV'

    def test_add_sonderzeit_should_only_fire_once(self):
        self.set_up()

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

        sonderzeiten_tabelle = viewcore.viewcore.database_instance().sonderzeiten.content
        assert len(sonderzeiten_tabelle) == 1
        assert sonderzeiten_tabelle.Datum[0] == datum('2/2/2017')
        assert sonderzeiten_tabelle.Dauer[0] == time('11:00')
        assert sonderzeiten_tabelle.Typ[0] == 'Urlaub'
        assert sonderzeiten_tabelle.Arbeitgeber[0] == 'asDATEV'

if __name__ == '__main__':
    unittest.main()

class GetRequest():
    method = 'GET'

class PostRequest:
    def __init__(self, args):
        self.POST = args
    method = 'POST'
