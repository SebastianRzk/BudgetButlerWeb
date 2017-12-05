'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from test import DBManagerStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from addeinnahme import views
from core import DBManager
from core.DatabaseModule import Database
from viewcore import viewcore
from viewcore import request_handler
from viewcore.converter import datum

class TestAddEinnahmeView(unittest.TestCase):

    testdb = None
    def set_up(self):
        self.testdb = DBManagerStub.setup_db_for_test()
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        context = views.index(GetRequest())
        assert context['approve_title'] == 'Einnahme hinzufügen'

    def test_editCallFromUeberischt_shouldNameButtonEdit(self):
        self.set_up()
        self.testdb.einzelbuchungen.add(datum('10/10/2010'), 'kategorie', 'name', 10.00)
        context = views.index(PostRequest({'action':'edit', 'edit_index':'0'}))
        assert context['approve_title'] == 'Einnahme aktualisieren'

    def test_add_ausgabe(self):
        self.set_up()
        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "date":"1/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,00"
             }
         ))

        assert len(self.testdb.einzelbuchungen.content) == 1
        assert self.testdb.einzelbuchungen.content.Wert[0] == float("2.00")
        assert self.testdb.einzelbuchungen.content.Name[0] == "testname"
        assert self.testdb.einzelbuchungen.content.Kategorie[0] == "Essen"
        assert self.testdb.einzelbuchungen.content.Datum[0] == datum("1/1/2017")

    def test_add_ausgabe_should_only_fire_once(self):
        self.set_up()
        next_id = request_handler.current_key()
        views.index(PostRequest(
            {"action":"add",
             "ID":next_id,
             "date":"1/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,00"
             }
         ))

        views.index(PostRequest(
            {"action":"add",
             "ID":next_id,
             "date":"1/1/2017",
             "kategorie":"overwritten",
             "name":"overwritten",
             "wert":"0,00"
             }
         ))

        assert len(self.testdb.einzelbuchungen.content) == 1
        assert self.testdb.einzelbuchungen.content.Wert[0] == float("2.00")
        assert self.testdb.einzelbuchungen.content.Name[0] == "testname"
        assert self.testdb.einzelbuchungen.content.Kategorie[0] == "Essen"
        assert self.testdb.einzelbuchungen.content.Datum[0] == datum("1/1/2017")

    def test_edit_ausgabe(self):
        self.set_up()

        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "date":"1/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,00"
             }
         ))


        print("dbs: " , viewcore.DATABASES)
        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "edit_index":"0",
             "date":"5/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,50"
             }
         ))

        assert len(self.testdb.einzelbuchungen.content) == 1
        assert self.testdb.einzelbuchungen.content.Wert[0] == float("2.50")
        assert self.testdb.einzelbuchungen.content.Name[0] == "testname"
        assert self.testdb.einzelbuchungen.content.Kategorie[0] == "Essen"
        assert self.testdb.einzelbuchungen.content.Datum[0] == datum("5/1/2017")


    def test_edit_ausgabe_should_only_fire_once(self):
        self.set_up()

        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "date":"1/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,00"
             }
         ))

        next_id = request_handler.current_key()
        views.index(PostRequest(
            {"action":"add",
             "ID":next_id,
             "edit_index":"0",
             "date":"5/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,50"
             }
         ))

        views.index(PostRequest(
            {"action":"add",
             "ID":next_id,
             "edit_index":"0",
             "date":"5/1/2017",
             "kategorie":"overwritten",
             "name":"overwritten",
             "wert":"0,0"
             }
         ))

        assert len(self.testdb.einzelbuchungen.content) == 1
        assert self.testdb.einzelbuchungen.content.Wert[0] == float("2.50")
        assert self.testdb.einzelbuchungen.content.Name[0] == "testname"
        assert self.testdb.einzelbuchungen.content.Kategorie[0] == "Essen"
        assert self.testdb.einzelbuchungen.content.Datum[0] == datum("5/1/2017")

    def test_edit_einzelbuchung_shouldLoadInputValues(self):
        self.set_up()

        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "date":"1/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,34"
             }
         ))

        result = views.index(PostRequest(
            {"action":"edit",
             "edit_index":"0"
             }
        ))

        assert result['edit_index'] == 0
        assert result['default_item']['Name'] == "testname"
        assert result['default_item']['Wert'] == "2,34"

if __name__ == '__main__':
    unittest.main()