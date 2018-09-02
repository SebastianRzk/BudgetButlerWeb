import unittest

from mysite.test.FileSystemStub import FileSystemStub
from mysite.test.RequestStubs import GetRequest
from mysite.test.RequestStubs import VersionedPostRequest
from mysite.views import uebersicht_gemeinsam
from mysite.core import FileSystem
from mysite.viewcore import request_handler
from mysite.viewcore import viewcore
from mysite.viewcore.viewcore import database_instance as db
from mysite.viewcore.converter import datum_from_german as datum

class Gemeinsamuebersicht(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        uebersicht_gemeinsam.index(GetRequest())

    def test_delete(self):
        self.set_up()

        db().gemeinsamebuchungen.add(datum('01.01.2011'), 'kat1', 'name1', 1, 'pers1')
        db().gemeinsamebuchungen.add(datum('01.01.2012'), 'kat2', 'name2', 1, 'pers2')
        db().gemeinsamebuchungen.add(datum('01.01.2013'), 'kat3', 'name3', 1, 'pers3')

        uebersicht_gemeinsam.index(VersionedPostRequest({
            'action' : 'delete',
            'delete_index' : 1
            }))


        result = uebersicht_gemeinsam.index(GetRequest())

        assert len(result['ausgaben']) == 2
        assert result['ausgaben'][0][2] == 'name1'
        assert result['ausgaben'][1][2] == 'name3'
