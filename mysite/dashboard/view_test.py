# Create your tests here.
'''
'''

import unittest

from core.DatabaseModule import Database
from dashboard import views
import viewcore


class TestUebersicht(unittest.TestCase):

    def set_up(self):
        print("create new database")
        viewcore.viewcore.DATABASE_INSTANCE = Database("test")
        viewcore.viewcore.DATABASES = ['test']
        viewcore.viewcore.TEST = True

    def test_init_withEmptyDatabase(self):
        self.set_up()
        views.handle_request(GetRequest())


if __name__ == '__main__':
    unittest.main()

class GetRequest():
    method = "GET"
