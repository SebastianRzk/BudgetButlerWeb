from datetime import date
import os
import sys
import unittest

from core.DatabaseModule import Database
from importd import views
import viewcore
from viewcore.converter import datum


myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")




# Create your tests here.
class Jahresuebersicht(unittest.TestCase):

    def setUp(self):
        print("create new database")
        self.testdb = Database("test")
        viewcore.viewcore.DATABASE_INSTANCE = self.testdb
        viewcore.viewcore.DATABASES = ['test']
        viewcore.viewcore.TEST = True

    def test_init_shouldReturnIndexPage(self):
        self.setUp()
        page, context = views.handle_request(GetRequest())
        assert page == 'import.html'

    _IMPORT_DATA = '''
    #######MaschinenimportStart
    Datum,Kategorie,Name,Wert,Dynamisch
    2017-03-06,Essen,Edeka,-10.0,True
    #######MaschinenimportEnd
    '''
    def test_addePassendeKategorie_shouldImportValue(self):
        self.setUp()
        viewcore.viewcore.database_instance().add_einzelbuchung(datum('01/01/2017'), 'Essen', 'some name', -1.54)

        page, context = views.handle_request(PostRequest({'import':self._IMPORT_DATA}))
        assert page == 'import.html'
        assert viewcore.viewcore.database_instance().get_jahresausgaben(2017) == -11.54


    def test_addeUnpassendenKategorie_shouldShowImportMappingPage(self):
        self.setUp()
        viewcore.viewcore.database_instance().add_einzelbuchung(datum('01/01/2017'), 'unbekannt', 'some name', -1.54)

        page, context = views.handle_request(PostRequest({'import':self._IMPORT_DATA}))
        assert page == 'import_mapping.html'

    def test_addeUnpassendenKategorie_mitPassendemMapping_shouldImportValue(self):
        self.setUp()
        viewcore.viewcore.database_instance().add_einzelbuchung(datum('01/01/2017'), 'Unpassend', 'some name', -1.54)

        page, context = views.handle_request(PostRequest({'import':self._IMPORT_DATA, 'Essen_mapping':'als Unpassend importieren'}))
        assert page == 'import.html'
        assert viewcore.viewcore.database_instance().get_jahresausgaben(2017) == -11.54



class GetRequest():
    method = "GET"
    POST = {}


class PostRequest:

    def __init__(self, args):
        self.POST = args

    method = "POST"
