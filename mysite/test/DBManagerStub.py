'''
Created on 28.09.2017

@author: sebastian
'''
from _io import StringIO

from core import DatabaseModule, DBManager
from core.DatabaseModule import Database
from viewcore import viewcore
from datetime import datetime
from viewcore.converter import datum


__DATABASES = {}


def from_string(nutzername):
    print('Reading database from RAM')
    if not __DATABASES[nutzername]:
        print('No database in RAM found! creating empty one!')
        neue_datenbank = DatabaseModule.Database(nutzername)
        to_string(neue_datenbank)
    print('Trigger original database parser')
    return DBManager.read_file(StringIO(__DATABASES[nutzername]), nutzername)

def to_string(database):
    print('Writing database to RAM')
    file = StringIO()
    DBManager.write_file(database, file)
    __DATABASES[database.name] = file.getvalue()
    print('CACHED DATABASES:', __DATABASES)

def setup_db_for_test():
    print('Instrumentating database')
    print('Creating testdatabase')
    database = Database('test')
    viewcore.DATABASE_INSTANCE = database
    viewcore.DATABASES = ['test']

    print('Overwrite database read and write')
    DBManager.read_function = from_string
    DBManager.write_function = to_string
    database.func_today = _fixed_date

    return database

def _fixed_date():
    return datum('01/01/2010')

def stub_abrechnungs_write():
    viewcore.database_instance().abrechnungs_write_function = write_to_console

def write_to_console(filename, content):
    print('Consolewriter:::::')
    print('Filename:', filename)
    print('Content:')
    print(content)

