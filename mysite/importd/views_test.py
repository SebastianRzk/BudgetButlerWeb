from datetime import date
import os
import sys
import unittest

from test import DBManagerStub
from core.DatabaseModule import Database
from importd import views
import viewcore
from viewcore.converter import datum


myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")




# Create your tests here.
class Importd(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()

    def test_init_shouldReturnIndexPage(self):
        self.set_up()
        page, context = views.handle_request(GetRequest())
        assert page == 'import.html'

    _IMPORT_DATA = '''
    #######MaschinenimportStart
    Datum,Kategorie,Name,Wert,Dynamisch
    2017-03-06,Essen,Edeka,-10.0,True
    #######MaschinenimportEnd
    '''
    def test_addePassendeKategorie_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01/01/2017'), 'Essen', 'some name', -1.54)

        page, context = views.handle_request(PostRequest({'import':self._IMPORT_DATA}))
        assert page == 'import.html'
        assert einzelbuchungen.select().select_year(2017).sum() == -11.54


    def test_addeUnpassendenKategorie_shouldShowImportMappingPage(self):
        self.set_up()
        einzelbuchungen = viewcore.viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01/01/2017'), 'unbekannt', 'some name', -1.54)

        page, context = views.handle_request(PostRequest({'import':self._IMPORT_DATA}))
        assert page == 'import_mapping.html'

    def test_addeUnpassendenKategorie_mitPassendemMapping_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01/01/2017'), 'Unpassend', 'some name', -1.54)

        page, context = views.handle_request(PostRequest({'import':self._IMPORT_DATA, 'Essen_mapping':'als Unpassend importieren'}))
        assert page == 'import.html'
        assert einzelbuchungen.select().select_year(2017).sum() == -11.54



class GetRequest():
    method = "GET"
    POST = {}


class PostRequest:

    def __init__(self, args):
        self.POST = args

    method = "POST"
