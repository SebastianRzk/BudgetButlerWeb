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
from test import DBManagerStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from core.DatabaseModule import Database
from viewcore import viewcore
from viewcore import request_handler
from viewcore.converter import datum


'''
'''
class TesteSollzeit(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        views.index(GetRequest())

    def test_add(self):
        self.set_up()
        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "startdatum":"1/1/2017",
             "endedatum":"2/3/2018",
             "laenge":"2:00",
             }
         ))
        db = viewcore.database_instance()
        assert len(db.sollzeiten.content) == 1
        assert db.sollzeiten.content.Startdatum[0] == datum("1/1/2017")
        assert db.sollzeiten.content.Endedatum[0] == datum("2/3/2018")
        assert db.sollzeiten.content.Dauer[0] == datetime.datetime.strptime("2:00", '%H:%M').time()


    def test_add_should_only_fire_once(self):
        self.set_up()
        single_id = request_handler.current_key()
        views.index(PostRequest(
            {"action":"add",
             "ID":single_id,
             "startdatum":"1/1/2017",
             "endedatum":"2/3/2018",
             "laenge":"2:00",
             }
         ))

        views.index(PostRequest(
            {"action":"add",
             "ID":single_id,
             "startdatum":"2/2/2022",
             "endedatum":"2/2/2022",
             "laenge":"0:00",
             }
         ))
        db = viewcore.database_instance()
        assert len(db.sollzeiten.content) == 1
        assert db.sollzeiten.content.Startdatum[0] == datum("1/1/2017")
        assert db.sollzeiten.content.Endedatum[0] == datum("2/3/2018")
        assert db.sollzeiten.content.Dauer[0] == datetime.datetime.strptime("2:00", '%H:%M').time()


    def test_edit(self):
        self.set_up()

        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "startdatum":"1/1/2017",
             "endedatum":"2/3/2018",
             "laenge":"2:00",
             }
         ))

        views.index(PostRequest(
            {"action":"edit",
             "ID":request_handler.current_key(),
             "edit_index":"0",
             "startdatum":"2/2/2018",
             "endedatum":"3/4/2019",
             "laenge":"3:00",
             }
         ))
        db = viewcore.database_instance()
        assert len(db.sollzeiten.content) == 1
        assert db.sollzeiten.content.Startdatum[0] == datum("2/2/2018")
        assert db.sollzeiten.content.Endedatum[0] == datum("3/4/2019")
        assert db.sollzeiten.content.Dauer[0] == datetime.datetime.strptime("3:00", '%H:%M').time()


    def test_edit_ausgabe_should_only_fire_once(self):
        self.set_up()
        views.index(PostRequest(
            {"action":"add",
             "ID":request_handler.current_key(),
             "startdatum":"1/1/2017",
             "endedatum":"2/3/2018",
             "laenge":"2:00",
             }
         ))
        same_id = request_handler.current_key()
        views.index(PostRequest(
            {"action":"edit",
             "ID":same_id,
             "edit_index":"0",
             "startdatum":"2/2/2018",
             "endedatum":"3/4/2019",
             "laenge":"3:00",
             }
         ))

        views.index(PostRequest(
            {"action":"edit",
             "ID":same_id,
             "edit_index":"0",
             "startdatum":"1/1/2000",
             "endedatum":"1/1/2001",
             "laenge":"0:00",
             }
         ))

        db = viewcore.database_instance()
        assert len(db.sollzeiten.content) == 1
        assert db.sollzeiten.content.Startdatum[0] == datum("2/2/2018")
        assert db.sollzeiten.content.Endedatum[0] == datum("3/4/2019")
        assert db.sollzeiten.content.Dauer[0] == datetime.datetime.strptime("3:00", '%H:%M').time()


if __name__ == '__main__':
    unittest.main()
