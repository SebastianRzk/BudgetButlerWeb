'''
Created on 14.09.2017

@author: sebastian
'''
from _io import StringIO
import os
import sys
import unittest

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + '/../')

from core import DBManager
from viewcore import viewcore





class DBManager_readDB(unittest.TestCase):

    def teste_read_with_full_database(self):
        database = DBManager.read_file(StringIO(self.full_db) , 'testuser')

        assert database.name == 'testuser'
        assert len(database.einzelbuchungen.content) == 22
        assert len(database.einzelbuchungen.content[database.einzelbuchungen.content.Dynamisch == False]) == 2
        assert database.einzelbuchungen.select().sum() == -229

        assert len(database.dauerauftraege.content) == 2
        assert database.dauerauftraege.content.Kategorie.tolist() == ['Essen', 'Miete']

    def teste_write_with_full_database(self):
        database = DBManager.read_file(StringIO(self.full_db) , 'testuser')
        string_writer = StringIO()
        DBManager.write_file(database, string_writer)

        assert string_writer.getvalue() == self.full_db





    full_db = '''Datum,Kategorie,Name,Wert,Tags
2017-10-10,Essen,Essen gehen,-10.0,[]
2017-11-11,Essen,Nochwas,-1.0,[]

 Dauerauftraege 
Endedatum,Kategorie,Name,Rhythmus,Startdatum,Wert
2017-09-18,Essen,Other Something,monatlich,2017-01-12,-1.0
2017-09-30,Miete,Miete,monatlich,2017-01-13,-1.0

 Gemeinsame Buchungen 
Datum,Kategorie,Name,Wert,Person
2017-12-30,Miete,monatlich,-200.0,Sebastian
2017-12-31,Miete,monatlich,-200.0,Maureen
'''
