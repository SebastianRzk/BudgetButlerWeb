# Create your tests here.
'''
'''

import os
import sys
import unittest

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + '/../')

from test import DBManagerStub
from core.DatabaseModule import Database
from dashboard import views
import viewcore






class TestUebersicht(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()

    def test_init_withEmptyDatabase(self):
        self.set_up()
        views.handle_request()

    def test_diagramm_vorbelegung(self):
        self.set_up()
        result = views.handle_request()


if __name__ == '__main__':
    unittest.main()

