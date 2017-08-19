'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + "/../")

from adddauerauftrag import views
from core.DatabaseModule import Database
import viewcore
from viewcore.converter import datum


'''
'''
class TesteAddDauerauftragView(unittest.TestCase):

    def setUp(self):
        print("create new database")
        self.testdb = Database("test")
        viewcore.viewcore.DATABASE_INSTANCE = self.testdb
        viewcore.viewcore.DATABASES = ['test']
        viewcore.viewcore.TEST = True

    def test_init(self):
        self.setUp()
        views.handle_request(GetRequest())

    def test_add_dauerauftrag(self):
        self.setUp()
        views.handle_request(PostRequest(
            {"action":"add",
             "ID":"????",
             "startdatum":"1/1/2017",
             "endedatum":"6/1/2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,00"
             }
         ))

        assert len(self.testdb.dauerauftraege.content) == 1
        assert self.testdb.dauerauftraege.content.Wert[0] == -1 * float("2.00")
        assert self.testdb.dauerauftraege.content.Name[0] == "testname"
        assert self.testdb.dauerauftraege.content.Kategorie[0] == "Essen"
        assert self.testdb.dauerauftraege.content.Startdatum[0] == datum("1/1/2017")
        assert self.testdb.dauerauftraege.content.Endedatum[0] == datum("6/1/2017")
        assert self.testdb.dauerauftraege.content.Rhythmus[0] == "monatlich"

    def test_add_dauerauftrag_einnahme(self):
        self.setUp()
        views.handle_request(PostRequest(
            {"action":"add",
             "ID":viewcore.viewcore.get_next_transaction_id(),
             "startdatum":"1/1/2017",
             "endedatum":"6/1/2017",
             "kategorie":"Essen",
             "typ":"Einnahme",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,00"
             }
         ))

        assert len(self.testdb.dauerauftraege.content) == 1
        assert self.testdb.dauerauftraege.content.Wert[0] == float("2.00")
        assert self.testdb.dauerauftraege.content.Name[0] == "testname"
        assert self.testdb.dauerauftraege.content.Kategorie[0] == "Essen"
        assert self.testdb.dauerauftraege.content.Startdatum[0] == datum("1/1/2017")
        assert self.testdb.dauerauftraege.content.Endedatum[0] == datum("6/1/2017")
        assert self.testdb.dauerauftraege.content.Rhythmus[0] == "monatlich"

    def test_edit_dauerauftrag(self):
        self.setUp()

        views.handle_request(PostRequest(
            {"action":"add",
             "ID":"?x???",
             "startdatum":"1/1/2017",
             "endedatum":"6/1/2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,00"
             }
         ))


        print("dbs: " , viewcore.viewcore.DATABASES)
        views.handle_request(PostRequest(
            {"action":"add",
             "ID":"??xxx?",
             "edit_index":"0",
             "startdatum":"2/1/2017",
             "endedatum":"5/1/2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,50"
             }
         ))

        assert len(self.testdb.dauerauftraege.content) == 1
        assert self.testdb.dauerauftraege.content.Wert[0] == -1 * float("2.50")
        assert self.testdb.dauerauftraege.content.Name[0] == "testname"
        assert self.testdb.dauerauftraege.content.Kategorie[0] == "Essen"
        assert self.testdb.dauerauftraege.content.Startdatum[0] == datum("2/1/2017")
        assert self.testdb.dauerauftraege.content.Endedatum[0] == datum("5/1/2017")

    def test_edit_dauerauftrag_ausgabe_to_einnahme(self):
        self.setUp()

        views.handle_request(PostRequest(
            {"action":"add",
             "ID":viewcore.viewcore.get_next_transaction_id(),
             "startdatum":"1/1/2017",
             "endedatum":"6/1/2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,00"
             }
         ))


        print("dbs: " , viewcore.viewcore.DATABASES)
        views.handle_request(PostRequest(
            {"action":"add",
             "ID":viewcore.viewcore.get_next_transaction_id(),
             "edit_index":"0",
             "startdatum":"2/1/2017",
             "endedatum":"5/1/2017",
             "kategorie":"Essen",
             "typ":"Einnahme",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,50"
             }
         ))

        assert len(self.testdb.dauerauftraege.content) == 1
        assert self.testdb.dauerauftraege.content.Wert[0] == float("2.50")
        assert self.testdb.dauerauftraege.content.Name[0] == "testname"
        assert self.testdb.dauerauftraege.content.Kategorie[0] == "Essen"
        assert self.testdb.dauerauftraege.content.Startdatum[0] == datum("2/1/2017")
        assert self.testdb.dauerauftraege.content.Endedatum[0] == datum("5/1/2017")


    def test_edit_dauerauftrag_should_only_fire_once(self):
        self.setUp()

        views.handle_request(PostRequest(
            {"action":"add",
             "ID":viewcore.viewcore.get_next_transaction_id(),
             "startdatum":"1/1/2017",
             "endedatum":"6/1/2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,00"
             }
         ))
        next_id = viewcore.viewcore.get_next_transaction_id()
        views.handle_request(PostRequest(
            {"action":"add",
             "ID":next_id,
             "edit_index":"0",
             "startdatum":"2/1/2017",
             "endedatum":"5/1/2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,50"
             }
         ))

        views.handle_request(PostRequest(
            {"action":"add",
             "ID":next_id,
             "edit_index":"0",
             "startdatum":"2/1/2017",
             "endedatum":"5/1/2017",
             "kategorie":"overwritten",
             "typ":"Ausgabe",
             "rhythmus":"overwritten",
             "name":"overwritten",
             "wert":"0,00"
             }
         ))

        assert len(self.testdb.dauerauftraege.content) == 1
        assert self.testdb.dauerauftraege.content.Wert[0] == -1 * float("2.50")
        assert self.testdb.dauerauftraege.content.Name[0] == "testname"
        assert self.testdb.dauerauftraege.content.Kategorie[0] == "Essen"
        assert self.testdb.dauerauftraege.content.Startdatum[0] == datum("2/1/2017")
        assert self.testdb.dauerauftraege.content.Endedatum[0] == datum("5/1/2017")


    def test_add_dauerauftrag_should_only_fire_once(self):
        self.setUp()

        next_id = viewcore.viewcore.get_next_transaction_id()
        views.handle_request(PostRequest(
            {"action":"add",
             "ID":next_id,
             "startdatum":"2/1/2017",
             "endedatum":"5/1/2017",
             "kategorie":"Essen",
             "typ":"Ausgabe",
             "rhythmus":"monatlich",
             "name":"testname",
             "wert":"2,50"
             }
         ))

        views.handle_request(PostRequest(
            {"action":"add",
             "ID":next_id,
             "startdatum":"2/1/2017",
             "endedatum":"5/1/2017",
             "kategorie":"overwritten",
             "typ":"Ausgabe",
             "rhythmus":"overwritten",
             "name":"overwritten",
             "wert":"0,00"
             }
         ))

        assert len(self.testdb.dauerauftraege.content) == 1
        assert self.testdb.dauerauftraege.content.Wert[0] == -1 * float("2.50")
        assert self.testdb.dauerauftraege.content.Name[0] == "testname"
        assert self.testdb.dauerauftraege.content.Kategorie[0] == "Essen"
        assert self.testdb.dauerauftraege.content.Startdatum[0] == datum("2/1/2017")
        assert self.testdb.dauerauftraege.content.Endedatum[0] == datum("5/1/2017")


if __name__ == '__main__':
    unittest.main()

class GetRequest():
    method = "GET"

class PostRequest:

    def __init__(self, args):
        self.POST = args

    method = "POST"
