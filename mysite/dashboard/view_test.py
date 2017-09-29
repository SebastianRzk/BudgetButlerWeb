# Create your tests here.
'''
'''

import os
import sys
import unittest

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + '/../')

from core.DatabaseModule import Database
from dashboard import views
from mysite.test import DBManagerStub
import viewcore







class TestUebersicht(unittest.TestCase):

    testdb = None
    def set_up(self):
        self.testdb = DBManagerStub.setup_db_for_test()

    def test_init_withEmptyDatabase(self):
        self.set_up()
        views.handle_request()


if __name__ == '__main__':
    unittest.main()

