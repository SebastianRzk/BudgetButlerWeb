import os
import sys
import unittest

from mysite.test.RequestStubs import GetRequest
from mysite.test.FileSystemStub import FileSystemStub
from mysite.core import FileSystem
from mysite.views import dashboard
from mysite.viewcore import viewcore
from mysite.viewcore import request_handler


class TestUebersicht(unittest.TestCase):

    def set_up(self):
        FileSystem.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init_withEmptyDatabase(self):
        self.set_up()
        dashboard.index(GetRequest())
