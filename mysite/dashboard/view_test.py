import os
import sys
import unittest

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + '/../')

from test.RequestStubs import GetRequest
from test import DBManagerStub
from core.DatabaseModule import Database
from dashboard import views
import viewcore
from viewcore import request_handler


class TestUebersicht(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()
        request_handler.stub_me()

    def test_init_withEmptyDatabase(self):
        self.set_up()
        views.index(GetRequest())


if __name__ == '__main__':
    unittest.main()

