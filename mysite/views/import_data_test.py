from datetime import date
import unittest

from mysite.test.FileSystemStub import FileSystemStub
from mysite.test.RequestStubs import GetRequest
from mysite.test.RequestStubs import PostRequest
from mysite.core import FileSystem
from mysite.views import import_data
from mysite.viewcore import viewcore
from mysite.viewcore.converter import datum_from_german as datum
from mysite.viewcore import request_handler
from mysite.viewcore import configuration_provider
from mysite.viewcore import requester
from mysite.test.RequesterStub import RequesterStub

# Create your tests here.
class Importd(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        viewcore.DATABASES = []
        configuration_provider.set_configuration('PARTNERNAME', 'Maureen')
        configuration_provider.set_configuration('DATABASES', 'Sebastian')
        request_handler.stub_me()

    def test_init_shouldReturnIndexPage(self):
        self.set_up()
        context = import_data.index(GetRequest())
        print(context)
        assert context['element_titel'] == 'Export / Import'

    _IMPORT_DATA = '''
    #######MaschinenimportStart
    Datum,Kategorie,Name,Wert,Dynamisch
    2017-03-06,Essen,Edeka,-10.0,True
    #######MaschinenimportEnd
    '''

    def test_addePassendeKategorie_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

        context = import_data.index(PostRequest({'import':self._IMPORT_DATA}))
        assert context['element_titel'] == 'Export / Import'
        assert einzelbuchungen.select().select_year(2017).sum() == -11.54

    def test_gemeinsam_addePassendeKategorie_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

        html, context = import_data.handle_request(PostRequest({'import':self._IMPORT_DATA_GEMEINSAM}), gemeinsam=True)
        assert context['element_titel'] == 'Export / Import'
        assert len(viewcore.database_instance().gemeinsamebuchungen.content) == 2

    def test_import_shouldWriteIntoAbrechnungen(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)

        context = import_data.index(PostRequest({'import':self._IMPORT_DATA}))

        written_abrechnung = None
        for key in FileSystem.instance()._fs_stub.keys():
            if key.startswith('../Import'):
                written_abrechnung = FileSystem.instance()._fs_stub[key]

        assert written_abrechnung == self._IMPORT_DATA


    def test_addeUnpassendenKategorie_shouldShowImportMappingPage(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'unbekannt', 'some name', -1.54)

        context = import_data.index(PostRequest({'import':self._IMPORT_DATA}))
        assert context['element_titel'] == 'Kategorien zuweisen'

    def test_addeUnpassendenKategorie_mitPassendemMapping_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Unpassend', 'some name', -1.54)

        context = import_data.index(PostRequest({'import':self._IMPORT_DATA, 'Essen_mapping':'als Unpassend importieren'}))
        assert context['element_titel'] == 'Export / Import'
        assert einzelbuchungen.select().select_year(2017).sum() == -11.54

    _IMPORT_DATA_GEMEINSAM = '''#######MaschinenimportStart
Datum,Kategorie,Name,Wert,Dynamisch,Person
2017-03-06,Essen,Edeka,-10.0,True,Sebastian
2017-03-06,Essen,Edeka,-20.0,True,Maureen
#######MaschinenimportEnd
'''

    def test_gemeinsamImport_addePassendeKategorie_shouldImportValue(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)



        requester.INSTANCE = RequesterStub({'https://test.test/getgemeinsam.php': self._IMPORT_DATA_GEMEINSAM,
                                           'https://test.test/deletegemeinsam.php' : '',
                                           'https://test.test/getusername.php': 'Sebastian'})

        context = import_data.index(PostRequest({'action': 'load_online_gemeinsame_transactions',
                                                      'email': '',
                                                      'server': 'test.test',
                                                      'password' : ''}))

        assert context['element_titel'] == 'Export / Import'
        assert len(viewcore.database_instance().gemeinsamebuchungen.content) == 2

        assert requester.instance().call_count_of('https://test.test/deletegemeinsam.php') == 1
        assert requester.instance().complete_call_count() == 3

    _IMPORT_DATA_GEMEINSAM_WRONG_PARTNER = '''
    #######MaschinenimportStart
    Datum,Kategorie,Name,Wert,Dynamisch,Person
    2017-03-06,Essen,Edeka,-10.0,True,Sebastian
    2017-03-06,Essen,Edeka,-20.0,True,Unbekannt
    #######MaschinenimportEnd
    '''

    def test_gemeinsamImport_withUnpassendenPartnername_shouldImportValueAndRepalceName(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)



        requester.INSTANCE = RequesterStub({'https://test.test/getgemeinsam.php': self._IMPORT_DATA_GEMEINSAM_WRONG_PARTNER,
                                           'https://test.test/deletegemeinsam.php': '',
                                           'https://test.test/getusername.php': 'Sebastian'})

        context = import_data.index(PostRequest({'action': 'load_online_gemeinsame_transactions',
                                                      'email': '',
                                                      'server': 'test.test',
                                                      'password' : ''}))

        assert context['element_titel'] == 'Export / Import'
        assert len(viewcore.database_instance().gemeinsamebuchungen.content) == 2
        assert viewcore.database_instance().gemeinsamebuchungen.content.Person[0] == 'Sebastian'
        assert viewcore.database_instance().gemeinsamebuchungen.content.Person[1] == 'Maureen'

        assert requester.instance().call_count_of('https://test.test/deletegemeinsam.php') == 1
        assert requester.instance().complete_call_count() == 3


    def test_gemeinsamImport_withUnpassendenKategorie_shouldImportValueAndRepalceName(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'KeinEssen', 'some name', -1.54)



        requester.INSTANCE = RequesterStub({'https://test.test/getgemeinsam.php': self._IMPORT_DATA_GEMEINSAM,
                                           'https://test.test/deletegemeinsam.php': '',
                                           'https://test.test/getusername.php': 'Sebastian'})

        context = import_data.index(PostRequest({'action': 'load_online_gemeinsame_transactions',
                                                      'email': '',
                                                      'server': 'test.test',
                                                      'password' : ''}))


        print(context)
        assert context['element_titel'] == 'Kategorien zuweisen'
        assert context['import'] == self._IMPORT_DATA_GEMEINSAM
        assert context['unpassende_kategorien'] == ['Essen']


        context = import_data.index(PostRequest({'action': 'map_and_push',
                                                      'Essen_mapping': 'neue Kategorie anlegen',
                                                      'import': self._IMPORT_DATA_GEMEINSAM}))


        assert context['element_titel'] == 'Export / Import'
        assert len(viewcore.database_instance().gemeinsamebuchungen.content) == 2
        assert viewcore.database_instance().gemeinsamebuchungen.content.Person[0] == 'Sebastian'
        assert viewcore.database_instance().gemeinsamebuchungen.content.Person[1] == 'Maureen'

        assert viewcore.database_instance().gemeinsamebuchungen.content.Kategorie[0] == 'Essen'
        assert viewcore.database_instance().gemeinsamebuchungen.content.Kategorie[1] == 'Essen'

        assert requester.instance().call_count_of('https://test.test/deletegemeinsam.php') == 1
        assert requester.instance().complete_call_count() == 3



    _IMPORT_DATA_GEMEINSAM_WRONG_SELF = '''
    #######MaschinenimportStart
    Datum,Kategorie,Name,Wert,Dynamisch,Person
    2017-03-06,Essen,Edeka,-10.0,True,Sebastian_Online
    2017-03-06,Essen,Edeka,-20.0,True,Maureen
    #######MaschinenimportEnd
    '''

    def test_gemeinsamImport_withUnpassendenUsername_shouldImportValueAndRepalceName(self):
        self.set_up()
        einzelbuchungen = viewcore.database_instance().einzelbuchungen
        einzelbuchungen.add(datum('01.01.2017'), 'Essen', 'some name', -1.54)



        requester.INSTANCE = RequesterStub({'https://test.test/getgemeinsam.php': self._IMPORT_DATA_GEMEINSAM_WRONG_SELF,
                                           'https://test.test/deletegemeinsam.php': '',
                                           'https://test.test/getusername.php': 'Sebastian_Online'})

        context = import_data.index(PostRequest({'action': 'load_online_gemeinsame_transactions',
                                                      'email': '',
                                                      'server': 'test.test',
                                                      'password' : ''}))

        assert context['element_titel'] == 'Export / Import'
        assert len(viewcore.database_instance().gemeinsamebuchungen.content) == 2
        assert viewcore.database_instance().gemeinsamebuchungen.content.Person[0] == 'Sebastian'
        assert viewcore.database_instance().gemeinsamebuchungen.content.Person[1] == 'Maureen'

        assert requester.instance().call_count_of('https://test.test/deletegemeinsam.php') == 1
        assert requester.instance().complete_call_count() == 3
