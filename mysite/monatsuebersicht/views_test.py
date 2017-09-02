import os
import sys
import unittest

from core.DatabaseModule import Database
from monatsuebersicht import views
import viewcore
from viewcore.converter import datum


myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')





# Create your tests here.
class Jahresuebersicht(unittest.TestCase):

    def setUp(self):
        print('create new database')
        self.testdb = Database('test')
        viewcore.viewcore.DATABASE_INSTANCE = self.testdb
        viewcore.viewcore.DATABASES = ['test']
        viewcore.viewcore.TEST = True

    def test_init(self):
        self.setUp()
        views.handle_request(GetRequest())

    def teste_mitMehtAusgabenAlsEinnahmen(self):
        self.setUp()
        self.testdb.einzelbuchungen.add(datum('10/10/2010'), 'some kategorie', 'some name', -100)
        self.testdb.einzelbuchungen.add(datum('10/10/2010'), 'eine einnahme kategorie', 'some name', 10)

        result_context = views.handle_request(PostRequest({'date':'2010_10'}))

        assert result_context['gesamt'] == '-100.00'
        assert result_context['gesamt_einnahmen'] == '10.00'

        assert result_context['einnahmen'] == [('eine einnahme kategorie', '10.00', '3c8dbc')]
        assert result_context['einnahmen_labels'] == ['eine einnahme kategorie']
        assert result_context['einnahmen_data'] == ['10.00']

        assert result_context['ausgaben'] == [('some kategorie', '-100.00', 'f56954')]
        assert result_context['ausgaben_labels'] == ['some kategorie']
        assert result_context['ausgaben_data'] == ['100.00']


class GetRequest():
    method = 'GET'
    POST = {}

class PostRequest:
    def __init__(self, args):
        self.POST = args

    method = 'POST'
