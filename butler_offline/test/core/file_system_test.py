from butler_offline.core import file_system
from butler_offline.test.core.file_system_stub import FileSystemStub


def test_alle_abrechnungen():
    filesystem = FileSystemStub()
    filesystem.write(file_system.ABRECHNUNG_PATH+'*Abrechnung_A', 'content abrechnung a')
    filesystem.write(file_system.IMPORT_PATH+'*Import_A', 'content import a')

    abrechnungen = file_system.all_abrechnungen(filesystem=filesystem)

    assert abrechnungen == [
                             {
                                 'content': ['content abrechnung a'],
                                 'name': './Abrechnungen/*Abrechnung_A'
                             },
                             {
                                 'content': ['content import a'],
                                 'name': './Import/*Import_A'
                             }
                          ]
