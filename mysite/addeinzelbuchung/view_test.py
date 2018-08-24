'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest
from django.template.context_processors import request

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from test.FileSystemStub import FileSystemStub
from test.RequestStubs import GetRequest
from test.RequestStubs import PostRequest
from test.RequestStubs import VersionedPostRequest
from addeinzelbuchung import views
from core import FileSystem
from viewcore import viewcore
from core.DatabaseModule import Database
from viewcore.converter import datum_from_german as datum
from viewcore.converter import german_to_rfc as rfc
from viewcore import request_handler
from viewcore.viewcore import database_instance

class TesteAddEinzelbuchungView(unittest.TestCase):

    testdb = None
    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        context = views.handle_request(GetRequest())
        assert context['approve_title'] == 'Ausgabe hinzufügen'

    def test_editCallFromUeberischt_shouldNameButtonEdit(self):
        self.set_up()
        database_instance().einzelbuchungen.add(datum('10.10.2010'), 'kategorie', 'name', 10.00)
        context = views.handle_request(PostRequest({'action':'edit', 'edit_index':'0'}))
        assert context['approve_title'] == 'Ausgabe aktualisieren'

    def test_add_ausgabe(self):
        self.set_up()
        views.handle_request(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))
        testdb = database_instance()
        assert len(testdb.einzelbuchungen.content) == 1
        assert testdb.einzelbuchungen.content.Wert[0] == -1 * float('2.00')
        assert testdb.einzelbuchungen.content.Name[0] == 'testname'
        assert testdb.einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.einzelbuchungen.content.Datum[0] == datum('1.1.2017')

    def test_add_ausgabe_should_only_fire_once(self):
        self.set_up()
        request_key = request_handler.current_key()

        views.index(PostRequest(
            {'action':'add',
             'ID':request_key,
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        views.index(PostRequest(
            {'action':'add',
             'ID':request_key,
             'date': rfc('1.1.2017'),
             'kategorie':'overwritten',
             'name':'overwritten',
             'wert':'0,00'
             }
         ))

        testdb = database_instance()
        assert len(testdb.einzelbuchungen.content) == 1
        assert testdb.einzelbuchungen.content.Wert[0] == -1 * float('2.00')
        assert testdb.einzelbuchungen.content.Name[0] == 'testname'
        assert testdb.einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.einzelbuchungen.content.Datum[0] == datum('1.1.2017')


    def test_edit_ausgabe(self):
        self.set_up()

        views.handle_request(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,00'
             }
         ))

        views.handle_request(VersionedPostRequest(
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
        assert testdb.einzelbuchungen.content.Wert[0] == -1 * float('2.50')
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
             'wert':'0,00'
             }
         ))
        testdb = database_instance()
        assert len(testdb.einzelbuchungen.content) == 1
        assert testdb.einzelbuchungen.content.Wert[0] == -1 * float('2.50')
        assert testdb.einzelbuchungen.content.Name[0] == 'testname'
        assert testdb.einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.einzelbuchungen.content.Datum[0] == datum('5.1.2017')

    def test_edit_einzelbuchung_shouldLoadInputValues_and_invertWert(self):
        self.set_up()

        views.handle_request(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'wert':'2,34'
             }
         ))

        result = views.handle_request(PostRequest(
            {'action':'edit',
             'edit_index':'0'
             }
        ))

        assert result['edit_index'] == 0
        assert result['default_item']['Name'] == 'testname'
        assert result['default_item']['Wert'] == '2,34'

