import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from test.FileSystemStub import FileSystemStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from core import FileSystem
from core.DatabaseModule import Database
from dauerauftraguebersicht import views
from viewcore import viewcore
from viewcore.converter import datum_from_german as datum
from viewcore import request_handler

class Dauerauftragsuebersicht(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        views.index(GetRequest())

    def test_delete(self):
        self.set_up()
        dauerauftraege = viewcore.database_instance().dauerauftraege
        dauerauftraege.add(datum('01.01.2011'), datum('01.01.2011'), '', '11', 'monatlich', 1)
        dauerauftraege.add(datum('01.01.2011'), datum('01.01.2011'), '', '22', 'monatlich', 1)

        views.index(PostRequest({'action':'delete', 'delete_index':'1'}))

        assert len(dauerauftraege.content) == 1
        assert dauerauftraege.content.Name.tolist() == ['11']
