'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from mysite.test.FileSystemStub import FileSystemStub
from mysite.test.RequestStubs import GetRequest
from mysite.test.RequestStubs import PostRequest
from mysite.test.RequestStubs import VersionedPostRequest
from views import addeinnahme
from mysite.core.DatabaseModule import Database
from mysite.core import FileSystem
from mysite.viewcore import viewcore
from mysite.viewcore.viewcore import database_instance as db
from mysite.viewcore import request_handler
from mysite.viewcore.converter import datum_from_german as datum
from mysite.viewcore.converter import german_to_rfc as rfc

class TestAddEinnahmeView(unittest.TestCase):

    testdb = None
    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        context = addeinnahme.index(GetRequest())
        assert context['approve_title'] == 'Einnahme hinzufügen'

    def test_editCallFromUeberischt_shouldNameButtonEdit(self):
        self.set_up()
        db().einzelbuchungen.add(datum('10.10.2010'), 'kategorie', 'name', 10.00)
        context = addeinnahme.index(PostRequest({'action':'edit', 'edit_index':'0'}))
        assert context['approve_title'] == 'Einnahme aktualisieren'

    def test_add_ausgabe(self):
        self.set_up()
        addeinnahme.index(VersionedPostRequest(
            {'action':'add',
             'date':rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        assert len(db().einzelbuchungen.content) == 1
        assert db().einzelbuchungen.content.Wert[0] == float('2.00')
        assert db().einzelbuchungen.content.Name[0] == 'testname'
        assert db().einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert db().einzelbuchungen.content.Datum[0] == datum('1.1.2017')

    def test_add_ausgabe_should_only_fire_once(self):
        self.set_up()
        next_id = request_handler.current_key()
        addeinnahme.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        addeinnahme.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'date': rfc('1.1.2017'),
             'kategorie':'overwritten',
             'name':'overwritten',
             'wert':'0,00'
             }
         ))

        assert len(db().einzelbuchungen.content) == 1
        assert db().einzelbuchungen.content.Wert[0] == float('2.00')
        assert db().einzelbuchungen.content.Name[0] == 'testname'
        assert db().einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert db().einzelbuchungen.content.Datum[0] == datum('1.1.2017')

    def test_edit_ausgabe(self):
        self.set_up()

        addeinnahme.index(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        addeinnahme.index(VersionedPostRequest(
            {'action':'add',
             'edit_index':'0',
             'date': rfc('5.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,50'
             }
         ))

        assert len(db().einzelbuchungen.content) == 1
        assert db().einzelbuchungen.content.Wert[0] == float('2.50')
        assert db().einzelbuchungen.content.Name[0] == 'testname'
        assert db().einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert db().einzelbuchungen.content.Datum[0] == datum('5.1.2017')


    def test_edit_ausgabe_should_only_fire_once(self):
        self.set_up()

        addeinnahme.index(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        next_id = request_handler.current_key()
        addeinnahme.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'edit_index':'0',
             'date': rfc('5.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,50'
             }
         ))

        addeinnahme.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'edit_index':'0',
             'date': rfc('5.1.2017'),
             'kategorie':'overwritten',
             'name':'overwritten',
             'wert':'0,0'
             }
         ))

        assert len(db().einzelbuchungen.content) == 1
        assert db().einzelbuchungen.content.Wert[0] == float('2.50')
        assert db().einzelbuchungen.content.Name[0] == 'testname'
        assert db().einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert db().einzelbuchungen.content.Datum[0] == datum('5.1.2017')

    def test_edit_einzelbuchung_shouldLoadInputValues(self):
        self.set_up()

        addeinnahme.index(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,34'
             }
         ))

        result = addeinnahme.index(PostRequest(
            {'action':'edit',
             'edit_index':'0'
             }
        ))

        assert result['edit_index'] == 0
        assert result['default_item']['Name'] == 'testname'
        assert result['default_item']['Wert'] == '2,34'
