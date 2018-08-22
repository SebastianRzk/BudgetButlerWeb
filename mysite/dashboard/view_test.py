import os
import sys
import unittest

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + '/../')

from test.RequestStubs import GetRequest
from test.FileSystemStub import FileSystemStub
from core import FileSystem
from dashboard import views
from viewcore import viewcore
from viewcore import request_handler


class TestUebersicht(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init_withEmptyDatabase(self):
        self.set_up()
        views.index(GetRequest())
