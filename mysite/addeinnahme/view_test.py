'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from test.FileSystemStub import FileSystemStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from test.RequestStubs import VersionedPostRequest
from addeinnahme import views
from core.DatabaseModule import Database
from core import FileSystem
from viewcore import viewcore
from viewcore import request_handler
from viewcore.converter import datum_from_german as datum
from viewcore.converter import german_to_rfc as rfc
from viewcore.viewcore import database_instance

class TestAddEinnahmeView(unittest.TestCase):

    testdb = None
    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        context = views.index(GetRequest())
        assert context['approve_title'] == 'Einnahme hinzufügen'

    def test_editCallFromUeberischt_shouldNameButtonEdit(self):
        self.set_up()
        database_instance().einzelbuchungen.add(datum('10.10.2010'), 'kategorie', 'name', 10.00)
        context = views.index(PostRequest({'action':'edit', 'edit_index':'0'}))
        assert context['approve_title'] == 'Einnahme aktualisieren'

    def test_add_ausgabe(self):
        self.set_up()
        views.index(VersionedPostRequest(
            {'action':'add',
             'date':rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        testdb = database_instance()
        assert len(testdb.einzelbuchungen.content) == 1
        assert testdb.einzelbuchungen.content.Wert[0] == float('2.00')
        assert testdb.einzelbuchungen.content.Name[0] == 'testname'
        assert testdb.einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.einzelbuchungen.content.Datum[0] == datum('1.1.2017')

    def test_add_ausgabe_should_only_fire_once(self):
        self.set_up()
        next_id = request_handler.current_key()
        views.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        views.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'date': rfc('1.1.2017'),
             'kategorie':'overwritten',
             'name':'overwritten',
             'wert':'0,00'
             }
         ))

        testdb = database_instance()
        assert len(testdb.einzelbuchungen.content) == 1
        assert testdb.einzelbuchungen.content.Wert[0] == float('2.00')
        assert testdb.einzelbuchungen.content.Name[0] == 'testname'
        assert testdb.einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.einzelbuchungen.content.Datum[0] == datum('1.1.2017')

    def test_edit_ausgabe(self):
        self.set_up()

        views.index(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        views.index(VersionedPostRequest(
            {'action':'add',
             'edit_index':'0',
             'date': rfc('5.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,50'
             }
         ))

        testdb = database_instance()
        assert len(testdb.einzelbuchungen.content) == 1
        assert testdb.einzelbuchungen.content.Wert[0] == float('2.50')
        assert testdb.einzelbuchungen.content.Name[0] == 'testname'
        assert testdb.einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.einzelbuchungen.content.Datum[0] == datum('5.1.2017')


    def test_edit_ausgabe_should_only_fire_once(self):
        self.set_up()

        views.index(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        next_id = request_handler.current_key()
        views.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'edit_index':'0',
             'date': rfc('5.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,50'
             }
         ))

        views.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'edit_index':'0',
             'date': rfc('5.1.2017'),
             'kategorie':'overwritten',
             'name':'overwritten',
             'wert':'0,0'
             }
         ))

        testdb = database_instance()
        assert len(testdb.einzelbuchungen.content) == 1
        assert testdb.einzelbuchungen.content.Wert[0] == float('2.50')
        assert testdb.einzelbuchungen.content.Name[0] == 'testname'
        assert testdb.einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.einzelbuchungen.content.Datum[0] == datum('5.1.2017')

    def test_edit_einzelbuchung_shouldLoadInputValues(self):
        self.set_up()

        views.index(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,34'
             }
         ))

        result = views.index(PostRequest(
            {'action':'edit',
             'edit_index':'0'
             }
        ))

        assert result['edit_index'] == 0
        assert result['default_item']['Name'] == 'testname'
        assert result['default_item']['Wert'] == '2,34'
