import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

from core.DatabaseModule import Database
from core.database.Einzelbuchungen import Einzelbuchungen
from gemeinsammabrechnen import views
from mysite.test import DBManagerStub
import viewcore
from viewcore.converter import datum






# Create your tests here.
class Gemeinsamabrechnen(unittest.TestCase):
    def set_up(self):
        DBManagerStub.setup_db_for_test()


    def test_init(self):
        self.set_up()
        result = views.handle_request(GetRequest())


    def test_abrechnen(self):
        self.set_up()
        testdb = viewcore.viewcore.database_instance()
        testdb.gemeinsamebuchungen.add(datum('01/01/2010'), 'Eine Katgorie', 'Ein Name', 2.60, 'Eine Person')
        DBManagerStub.stub_abrechnungs_write()
        views.handle_abrechnen_request(PostRequest({}))

        print(testdb.einzelbuchungen.content)

        assert testdb.einzelbuchungen.anzahl() == 1
        assert testdb.einzelbuchungen.get_all().Wert[0] == '1.30'


class GetRequest():
    method = 'GET'

class PostRequest:

    def __init__(self, args):
        self.POST = args

    method = "POST"
