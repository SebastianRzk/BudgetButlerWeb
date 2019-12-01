import unittest

from butler_offline.test.core.file_system_stub import FileSystemStub
from butler_offline.test.RequestStubs import GetRequest
from butler_offline.core import file_system
from butler_offline.views import uebersicht_abrechnungen
from butler_offline.viewcore import viewcore
from butler_offline.viewcore import request_handler


class TestUebersichtAbrechnungen(unittest.TestCase):

    def set_up(self):
        file_system.INSTANCE = FileSystemStub()
        viewcore.DATABASE_INSTANCE = None
        request_handler.stub_me()

    def test_init(self):
        self.set_up()
        context = uebersicht_abrechnungen.index(GetRequest())
        #assert context['zusammenfassungen'] == []
        #assert context['abrechnungen'] == []
