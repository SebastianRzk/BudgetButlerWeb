'''
Created on 10.05.2017

@author: sebastian
'''

import datetime
import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from addsollzeit import views
from core.DatabaseModule import Database
import viewcore
from viewcore.converter import datum


'''
'''
class TesteSollzeit(unittest.TestCase):

    def setUp(self):
        print("create new database")
        self.testdb = Database("test")
        viewcore.viewcore.DATABASE_INSTANCE = self.testdb
        viewcore.viewcore.DATABASES = ['test']
        viewcore.viewcore.TEST = True

    def test_init(self):
        self.setUp()
        views.handle_request(GetRequest())

    def test_add(self):
        self.setUp()
        views.handle_request(PostRequest(
            {"action":"add",
             "ID":viewcore.viewcore.get_next_transaction_id(),
             "startdatum":"1/1/2017",
             "endedatum":"2/3/2018",
             "laenge":"2:00",
             }
         ))

        assert len(self.testdb.sollzeiten.content) == 1
        assert self.testdb.sollzeiten.content.Startdatum[0] == datum("1/1/2017")
        assert self.testdb.sollzeiten.content.Endedatum[0] == datum("2/3/2018")
        assert self.testdb.sollzeiten.content.Dauer[0] == datetime.datetime.strptime("2:00", '%H:%M').time()


    def test_add_should_only_fire_once(self):
        self.setUp()
        single_id = viewcore.viewcore.get_next_transaction_id()
        views.handle_request(PostRequest(
            {"action":"add",
             "ID":single_id,
             "startdatum":"1/1/2017",
             "endedatum":"2/3/2018",
             "laenge":"2:00",
             }
         ))

        views.handle_request(PostRequest(
            {"action":"add",
             "ID":single_id,
             "startdatum":"2/2/2022",
             "endedatum":"2/2/2022",
             "laenge":"0:00",
             }
         ))

        assert len(self.testdb.sollzeiten.content) == 1
        assert self.testdb.sollzeiten.content.Startdatum[0] == datum("1/1/2017")
        assert self.testdb.sollzeiten.content.Endedatum[0] == datum("2/3/2018")
        assert self.testdb.sollzeiten.content.Dauer[0] == datetime.datetime.strptime("2:00", '%H:%M').time()


    def test_edit(self):
        self.setUp()

        views.handle_request(PostRequest(
            {"action":"add",
             "ID":viewcore.viewcore.get_next_transaction_id(),
             "startdatum":"1/1/2017",
             "endedatum":"2/3/2018",
             "laenge":"2:00",
             }
         ))

        views.handle_request(PostRequest(
            {"action":"edit",
             "ID":viewcore.viewcore.get_next_transaction_id(),
             "edit_index":"0",
             "startdatum":"2/2/2018",
             "endedatum":"3/4/2019",
             "laenge":"3:00",
             }
         ))

        assert len(self.testdb.sollzeiten.content) == 1
        assert self.testdb.sollzeiten.content.Startdatum[0] == datum("2/2/2018")
        assert self.testdb.sollzeiten.content.Endedatum[0] == datum("3/4/2019")
        assert self.testdb.sollzeiten.content.Dauer[0] == datetime.datetime.strptime("3:00", '%H:%M').time()


    def test_edit_ausgabe_should_only_fire_once(self):
        self.setUp()
        views.handle_request(PostRequest(
            {"action":"add",
             "ID":viewcore.viewcore.get_next_transaction_id(),
             "startdatum":"1/1/2017",
             "endedatum":"2/3/2018",
             "laenge":"2:00",
             }
         ))
        same_id = viewcore.viewcore.get_next_transaction_id()
        views.handle_request(PostRequest(
            {"action":"edit",
             "ID":same_id,
             "edit_index":"0",
             "startdatum":"2/2/2018",
             "endedatum":"3/4/2019",
             "laenge":"3:00",
             }
         ))

        views.handle_request(PostRequest(
            {"action":"edit",
             "ID":same_id,
             "edit_index":"0",
             "startdatum":"1/1/2000",
             "endedatum":"1/1/2001",
             "laenge":"0:00",
             }
         ))


        assert len(self.testdb.sollzeiten.content) == 1
        assert self.testdb.sollzeiten.content.Startdatum[0] == datum("2/2/2018")
        assert self.testdb.sollzeiten.content.Endedatum[0] == datum("3/4/2019")
        assert self.testdb.sollzeiten.content.Dauer[0] == datetime.datetime.strptime("3:00", '%H:%M').time()


if __name__ == '__main__':
    unittest.main()

class GetRequest():
    method = "GET"

class PostRequest:

    def __init__(self, args):
        self.POST = args

    method = "POST"
