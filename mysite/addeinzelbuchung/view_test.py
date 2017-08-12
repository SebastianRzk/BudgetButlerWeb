'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from addeinzelbuchung import views
from core.DatabaseModule import Database
import viewcore
from viewcore.converter import datum


'''
'''
class TesteAddEinzelbuchungView(unittest.TestCase):

    def setUp(self):
        print("create new database")
        self.testdb = Database("test")
        viewcore.viewcore.DATABASE_INSTANCE = self.testdb
        viewcore.viewcore.DATABASES = ['test']
        viewcore.viewcore.TEST = True

    def test_init(self):
        self.setUp()
        views.handle_request(GetRequest())

    def test_add_ausgabe(self):
        self.setUp()
        views.handle_request(PostRequest(
            {"action":"add",
             "ID":viewcore.viewcore.get_next_transaction_id(),
             "date":"1/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,00"
             }
         ))

        assert len(self.testdb.einzelbuchungen.content) == 1
        assert self.testdb.einzelbuchungen.content.Wert[0] == -1 * float("2.00")
        assert self.testdb.einzelbuchungen.content.Name[0] == "testname"
        assert self.testdb.einzelbuchungen.content.Kategorie[0] == "Essen"
        assert self.testdb.einzelbuchungen.content.Datum[0] == datum("1/1/2017")

    def test_add_ausgabe_should_only_fire_once(self):
        self.setUp()
        next_id = viewcore.viewcore.get_next_transaction_id()
        views.handle_request(PostRequest(
            {"action":"add",
             "ID":next_id,
             "date":"1/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,00"
             }
         ))

        views.handle_request(PostRequest(
            {"action":"add",
             "ID":next_id,
             "date":"1/1/2017",
             "kategorie":"overwritten",
             "name":"overwritten",
             "wert":"0,00"
             }
         ))

        assert len(self.testdb.einzelbuchungen.content) == 1
        assert self.testdb.einzelbuchungen.content.Wert[0] == -1 * float("2.00")
        assert self.testdb.einzelbuchungen.content.Name[0] == "testname"
        assert self.testdb.einzelbuchungen.content.Kategorie[0] == "Essen"
        assert self.testdb.einzelbuchungen.content.Datum[0] == datum("1/1/2017")


    def test_edit_ausgabe(self):
        self.setUp()

        views.handle_request(PostRequest(
            {"action":"add",
             "ID":viewcore.viewcore.get_next_transaction_id(),
             "date":"1/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,00"
             }
         ))


        print("dbs: " , viewcore.viewcore.DATABASES)
        views.handle_request(PostRequest(
            {"action":"add",
             "ID":viewcore.viewcore.get_next_transaction_id(),
             "edit_index":"0",
             "date":"5/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,50"
             }
         ))

        assert len(self.testdb.einzelbuchungen.content) == 1
        assert self.testdb.einzelbuchungen.content.Wert[0] == -1 * float("2.50")
        assert self.testdb.einzelbuchungen.content.Name[0] == "testname"
        assert self.testdb.einzelbuchungen.content.Kategorie[0] == "Essen"
        assert self.testdb.einzelbuchungen.content.Datum[0] == datum("5/1/2017")

    def test_edit_ausgabe_should_only_fire_once(self):
        self.setUp()

        views.handle_request(PostRequest(
            {"action":"add",
             "ID":viewcore.viewcore.get_next_transaction_id(),
             "date":"1/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,00"
             }
         ))

        next_id = viewcore.viewcore.get_next_transaction_id()
        views.handle_request(PostRequest(
            {"action":"add",
             "ID":next_id,
             "edit_index":"0",
             "date":"5/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,50"
             }
         ))

        views.handle_request(PostRequest(
            {"action":"add",
             "ID":next_id,
             "edit_index":"0",
             "date":"5/1/2017",
             "kategorie":"overwritten",
             "name":"overwritten",
             "wert":"0,00"
             }
         ))

        assert len(self.testdb.einzelbuchungen.content) == 1
        assert self.testdb.einzelbuchungen.content.Wert[0] == -1 * float("2.50")
        assert self.testdb.einzelbuchungen.content.Name[0] == "testname"
        assert self.testdb.einzelbuchungen.content.Kategorie[0] == "Essen"
        assert self.testdb.einzelbuchungen.content.Datum[0] == datum("5/1/2017")

    def test_edit_einzelbuchung_shouldLoadInputValues_and_invertWert(self):
        self.setUp()

        views.handle_request(PostRequest(
            {"action":"add",
             "ID":viewcore.viewcore.get_next_transaction_id(),
             "date":"1/1/2017",
             "kategorie":"Essen",
             "name":"testname",
             "wert":"2,34"
             }
         ))

        result = views.handle_request(PostRequest(
            {"action":"edit",
             "edit_index":"0"
             }
        ))

        assert result['edit_index'] == 0
        assert result['default_item']['Name'] == "testname"
        assert result['default_item']['Wert'] == "2,34"


if __name__ == '__main__':
    unittest.main()

class GetRequest():
    method = "GET"

class PostRequest:

    def __init__(self, args):
        self.POST = args

    method = "POST"
