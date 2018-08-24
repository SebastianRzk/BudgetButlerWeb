'''
Created on 10.05.2017

@author: sebastian
'''

import os
import sys
import unittest

from mysite.test.FileSystemStub import FileSystemStub
from mysite.test.RequestStubs import GetRequest
from mysite.test.RequestStubs import PostRequest
from mysite.test.RequestStubs import VersionedPostRequest
from mysite.views import addgemeinsam
from mysite.core import FileSystem
from mysite.viewcore import viewcore
from mysite.viewcore import request_handler
from mysite.viewcore.converter import datum_from_german as datum
from mysite.viewcore.converter import german_to_rfc as rfc


class TesteAddGemeinsamView(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        context = addgemeinsam.index(GetRequest())
        assert context['approve_title'] == 'Gemeinsame Ausgabe hinzufügen'

    def test_editCallFromUeberischt_shouldNameButtonEdit(self):
        self.set_up()
        db = viewcore.database_instance()
        db.gemeinsamebuchungen.add(datum('10.10.2010'), 'kategorie', 'ausgaben_name', -10, 'Sebastian')
        context = addgemeinsam.index(PostRequest({'action':'edit', 'edit_index':'0'}))
        assert context['approve_title'] == 'Gemeinsame Ausgabe aktualisieren'
        preset = context['default_item']
        assert preset['datum'] == rfc('10.10.2010')
        assert preset['edit_index'] == '0'
        assert preset['kategorie'] == 'kategorie'
        assert preset['name'] == 'ausgaben_name'
        assert preset['wert'] == '10,00'
        assert preset['person'] == 'Sebastian'

    def test_add_shouldAddGemeinsameBuchung(self):
        self.set_up()
        addgemeinsam.index(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson',
             'wert':'2,00'
             }
         ))
        testdb = viewcore.database_instance()
        assert testdb.gemeinsamebuchungen.content.Wert[0] == -1 * float('2.00')
        assert testdb.gemeinsamebuchungen.content.Name[0] == 'testname'
        assert testdb.gemeinsamebuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.gemeinsamebuchungen.content.Datum[0] == datum('1.1.2017')
        assert testdb.gemeinsamebuchungen.content.Person[0] == 'testperson'

    def test_add_shouldAddDynamicEinzelbuchung(self):
        self.set_up()
        addgemeinsam.index(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson',
             'wert':'2,00'
             }
         ))
        testdb = viewcore.database_instance()
        assert testdb.einzelbuchungen.content.Wert[0] == -1 * 0.5 * float('2.00')
        assert testdb.einzelbuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.einzelbuchungen.content.Datum[0] == datum('1.1.2017')
        assert testdb.einzelbuchungen.content.Name[0] == 'testname (noch nicht abgerechnet, von testperson)'

    def test_add_should_only_fire_once(self):
        self.set_up()
        next_id = request_handler.current_key()
        addgemeinsam.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson',
             'wert':'2,00'
             }
         ))
        addgemeinsam.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'date': rfc('1.1.2017'),
             'kategorie':'overwritten',
             'name':'overwritten',
             'person':'overwritten',
             'wert':'0,00'
             }
         ))
        testdb = viewcore.database_instance()
        assert testdb.gemeinsamebuchungen.content.Wert[0] == -1 * float('2.00')
        assert testdb.gemeinsamebuchungen.content.Name[0] == 'testname'
        assert testdb.gemeinsamebuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.gemeinsamebuchungen.content.Datum[0] == datum('1.1.2017')
        assert testdb.gemeinsamebuchungen.content.Person[0] == 'testperson'



    def test_edit_ausgabe(self):
        self.set_up()

        addgemeinsam.index(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson',
             'wert':'2,00'
             }
         ))

        addgemeinsam.index(PostRequest(
            {'action':'add',
             'ID':request_handler.current_key(),
             'edit_index':'0',
             'date': rfc('5.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson2',
             'wert':'2,50'
             }
         ))

        testdb = viewcore.database_instance()
        assert testdb.gemeinsamebuchungen.content.Wert[0] == -1 * float('2.50')
        assert testdb.gemeinsamebuchungen.content.Name[0] == 'testname'
        assert testdb.gemeinsamebuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.gemeinsamebuchungen.content.Datum[0] == datum('5.1.2017')
        assert testdb.gemeinsamebuchungen.content.Person[0] == 'testperson2'

    def test_personenOption_shouldContainNames(self):
        self.set_up()
        result = addgemeinsam.index(GetRequest())

        assert viewcore.database_instance().name in result['personen']
        assert viewcore.name_of_partner() in result['personen']
        assert len(result['personen']) == 2

    def test_edit_should_only_fire_once(self):
        self.set_up()

        addgemeinsam.index(VersionedPostRequest(
            {'action':'add',
             'date': rfc('1.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson',
             'wert':'2,00'
             }
         ))

        next_id = request_handler.current_key()
        addgemeinsam.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'edit_index':'0',
             'date': rfc('5.1.2017'),
             'kategorie':'Essen',
             'name':'testname',
             'person':'testperson2',
             'wert':'2,50'
             }
         ))
        addgemeinsam.index(PostRequest(
            {'action':'add',
             'ID':next_id,
             'edit_index':'0',
             'date': rfc('5.1.2017'),
             'kategorie':'overwritten',
             'name':'overwritten',
             'person':'overwritten',
             'wert':'0,00'
             }
         ))
        testdb = viewcore.database_instance()
        assert testdb.gemeinsamebuchungen.content.Wert[0] == -1 * float('2.50')
        assert testdb.gemeinsamebuchungen.content.Name[0] == 'testname'
        assert testdb.gemeinsamebuchungen.content.Kategorie[0] == 'Essen'
        assert testdb.gemeinsamebuchungen.content.Datum[0] == datum('5.1.2017')
        assert testdb.gemeinsamebuchungen.content.Person[0] == 'testperson2'

