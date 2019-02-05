'''
Created on 14.09.2017

@author: sebastian
'''
import unittest

from butler_offline.core import DBManager
from butler_offline.core import FileSystem
from butler_offline.test.FileSystemStub import FileSystemStub




class DBManager_readDB(unittest.TestCase):

    def mock_filesystem(self):
        FileSystem.INSTANCE = FileSystemStub()

    def write_db_file_stub(self,name, stub):
        FileSystem.instance().write('../Database_' + name + '.csv', stub)

    def teste_read_with_full_database(self):
        self.mock_filesystem()
        self.write_db_file_stub('testuser', self.full_db)

        database = DBManager.read('testuser', set())

        assert database.name == 'testuser'
        assert len(database.einzelbuchungen.content) == 22
        assert len(database.einzelbuchungen.content[database.einzelbuchungen.content.Dynamisch == False]) == 2
        assert database.einzelbuchungen.select().sum() == -229

        assert len(database.dauerauftraege.content) == 2
        assert database.dauerauftraege.content.Kategorie.tolist() == ['Essen', 'Miete']

    def teste_write_with_full_database(self):
        self.mock_filesystem()
        self.write_db_file_stub('testuser', self.full_db)

        database = DBManager.read('testuser', set())
        DBManager.write(database)

        assert FileSystem.instance().read('../Database_testuser.csv') == self.full_db.split('\n')

    def teste_write_with_old_database_should_migrate(self):
        self.mock_filesystem()
        self.write_db_file_stub('testuser', self.full_db_old)

        database = DBManager.read('testuser', set())
        DBManager.write(database)

        assert FileSystem.instance().read('../Database_testuser.csv') == self.full_db.split('\n')


    full_db_old = '''Datum,Kategorie,Name,Wert,Tags
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
stechzeiten...
'''

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
