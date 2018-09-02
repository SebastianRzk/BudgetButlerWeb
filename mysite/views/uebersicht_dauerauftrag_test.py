import unittest

from mysite.test.FileSystemStub import FileSystemStub
from mysite.test.RequestStubs import GetRequest
from mysite.test.RequestStubs import PostRequest
from mysite.core import FileSystem
from mysite.core.DatabaseModule import Database
from mysite.views import uebersicht_dauerauftrag
from mysite.viewcore import viewcore
from mysite.viewcore.converter import datum_from_german as datum
from mysite.viewcore import request_handler

class Dauerauftragsuebersicht(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        uebersicht_dauerauftrag.index(GetRequest())

    def test_delete(self):
        self.set_up()
        dauerauftraege = viewcore.database_instance().dauerauftraege
        dauerauftraege.add(datum('01.01.2011'), datum('01.01.2011'), '', '11', 'monatlich', 1)
        dauerauftraege.add(datum('01.01.2011'), datum('01.01.2011'), '', '22', 'monatlich', 1)

        uebersicht_dauerauftrag.index(PostRequest({'action':'delete', 'delete_index':'1'}))

        assert len(dauerauftraege.content) == 1
        assert dauerauftraege.content.Name.tolist() == ['11']

    def test_german_datum(self):
        self.set_up()
        dauerauftraege = viewcore.database_instance().dauerauftraege
        dauerauftraege.add(datum('01.01.2011'), datum('01.01.2011'), '', '11', 'monatlich', 1)

        result = uebersicht_dauerauftrag.index(GetRequest())

        result_dauerauftrag = result['dauerauftraege']['Vergangene  Daueraufträge'][0]
        assert result_dauerauftrag['Startdatum'] == '01.01.2011'
        assert result_dauerauftrag['Endedatum'] == '01.01.2011'
