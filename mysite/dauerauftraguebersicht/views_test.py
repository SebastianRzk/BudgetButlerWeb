import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from adddauerauftrag.view_test import PostRequest, GetRequest
from core.DatabaseModule import Database
from dauerauftraguebersicht import views
from mysite.core import DBManager
from mysite.test import DBManagerStub
import viewcore
from viewcore.converter import datum


class Dauerauftragsuebersicht(unittest.TestCase):

    testdb = None
    def set_up(self):
        self.testdb = DBManagerStub.setup_db_for_test()

    def test_init(self):
        self.set_up()
        result = views.handle_request(GetRequest())

    def test_delete(self):
        self.set_up()
        dauerauftraege = viewcore.viewcore.database_instance().dauerauftraege
        dauerauftraege.add(datum('01/01/2011'), datum('01/01/2011'), '', '11', 'monatlich', 1)
        dauerauftraege.add(datum('01/01/2011'), datum('01/01/2011'), '', '22', 'monatlich', 1)

        result = views.handle_request(PostRequest({'action':'delete', 'delete_index':'1'}))

        assert len(dauerauftraege.content) == 1
        assert dauerauftraege.content.Name.tolist() == ['11']
