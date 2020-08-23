import unittest
from butler_offline.core import file_system
from butler_offline.test.core.file_system_stub import FileSystemStub

class MyTestCase(unittest.TestCase):
    def test_alle_abrechnungen(self):
        file_system.INSTANCE = FileSystemStub()
        file_system.instance().write(file_system.ABRECHNUNG_PATH+'*Abrechnung_A', 'content abrechnung a')
        file_system.instance().write(file_system.IMPORT_PATH+'*Import_A', 'content import a')

        abrechnungen = file_system.all_abrechnungen()

        assert abrechnungen == [
            {
                'content': ['content abrechnung a'],
                'name': '../Abrechnungen/*Abrechnung_A'
            },
            {
                'content': ['content import a'],
                'name': '../Import/*Import_A'
            }
       ]




if __name__ == '__main__':
    unittest.main()
