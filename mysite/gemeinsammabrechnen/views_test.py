import os
import sys
import unittest

from core.DatabaseModule import Database
from core.database.Einzelbuchungen import Einzelbuchungen
from gemeinsammabrechnen import views
import viewcore
from viewcore.converter import datum


myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')





# Create your tests here.
class Gemeinsamabrechnen(unittest.TestCase):

    def setUp(self):
        print('create new database')
        self.testdb = Database('test')
        viewcore.viewcore.DATABASE_INSTANCE = self.testdb
        viewcore.viewcore.DATABASE_INSTANCE.TEST = True
        viewcore.viewcore.DATABASES = ['test']
        viewcore.viewcore.TEST = True

    def test_init(self):
        self.setUp()
        result = views.handle_request(GetRequest())


    def test_abrechnen(self):
        self.setUp()
        self.testdb.add_gemeinsame_einnahmeausgabe(datum('01/01/2010'), 'Eine Katgorie', 'Ein Name', 2.60, 'Eine Person')
        self.testdb.einzelbuchungen = Einzelbuchungen()
        views.handle_abrechnen_request(PostRequest({}))

        print(self.testdb.einzelbuchungen.content)

        assert self.testdb.einzelbuchungen.anzahl() == 1
        assert self.testdb.einzelbuchungen.get_all().Wert[0] == '1.30'


class GetRequest():
    method = 'GET'

class PostRequest:

    def __init__(self, args):
        self.POST = args

    method = "POST"
