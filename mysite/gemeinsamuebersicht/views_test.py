import os
import sys
import unittest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from test import DBManagerStub
from gemeinsamuebersicht import views




# Create your tests here.
class Gemeinsamuebersicht(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()

    def test_init(self):
        self.set_up()
        views.handle_request(GetRequest())


class GetRequest():
    method = "GET"
