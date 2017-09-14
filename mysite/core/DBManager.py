'''
Read panda files
'''

from _io import StringIO
from datetime import datetime
import os

from core import DatabaseModule
import pandas as pd



def read_database(nutzername):
    '''
    read panda tables from disk
    '''
    if not os.path.isfile('../Database_' + nutzername + ".csv"):
        neue_datenbank = DatabaseModule.Database(nutzername)
        write(neue_datenbank)

    file = open('../Database_' + nutzername + ".csv", 'r')
    return read_file(file, nutzername)


def read_file(file, nutzername):
    tables = {}

    tables["einzelbuchungen"] = ""
    tables["dauerauftraege"] = ""
    tables["gemeinsamebuchungen"] = ""
    tables["Stechzeiten"] = ""
    tables["Sollzeiten"] = ""
    tables["Sonderzeiten"] = ""
    mode = "einzelbuchungen"
    for line in file:
        line = line.strip()
        if line == "":
            continue
        if line == 'Dauerauftraege':
            mode = 'dauerauftraege'
            continue

        if line == 'Gemeinsame Buchungen':
            mode = 'gemeinsamebuchungen'
            continue

        if line == 'Stechzeiten':
            mode = 'Stechzeiten'
            continue

        if line == 'Sollzeiten':
            mode = 'Sollzeiten'
            continue

        if line == 'Sonderzeiten':
            mode = 'Sonderzeiten'
            continue

        tables[mode] = tables[mode] + "\n" + line


    database = DatabaseModule.Database(nutzername)

    raw_data = pd.read_csv(StringIO(tables["einzelbuchungen"]))
    database.einzelbuchungen.parse(raw_data)
    print("READER: Einzelbuchungen gelesen")

    database.dauerauftraege.parse(pd.read_csv(StringIO(tables["dauerauftraege"])))
    print("READER: Daueraufträge gelesen")

    database.gemeinsame_buchungen = pd.read_csv(StringIO(tables["gemeinsamebuchungen"]))
    print("READER: Gemmeinsame Buchungen gelesen:")
    print("READER:", database.gemeinsame_buchungen)

    if tables['Stechzeiten'] != "":
        database.stechzeiten = pd.read_csv(StringIO(tables["Stechzeiten"]))
        print("READER: Stech Zeiten gelesen gelesen:")
        print("READER:", database.gemeinsame_buchungen)

    if tables['Sollzeiten'] != "":
        database.soll_zeiten = pd.read_csv(StringIO(tables["Sollzeiten"]))
        print("READER: Soll zeiten gelesen:")
        print("READER:", database.gemeinsame_buchungen)

    if tables['Sonderzeiten'] != "":
        database.sonder_zeiten = pd.read_csv(StringIO(tables["Sonderzeiten"]))
        print("READER: Sonderzeiten gelesen gelesen:")
        print("READER:", database.sonder_zeiten)



    print('READER: Initialisiere Database')
    database.refresh()
    print('READER: Initialisierung abgeschlossen')
    return database

def write(database):
    '''
    writes the DATABASE into a file
    '''
    einzelbuchungen = database.einzelbuchungen.content.copy()[database.einzelbuchungen.content.Dynamisch == False]
    einzelbuchungen_raw_data = einzelbuchungen[['Datum', 'Kategorie', 'Name', 'Wert', 'Tags']]
    content = einzelbuchungen_raw_data.to_csv(index=False)

    content += "\n Dauerauftraege \n"
    content += database.dauerauftraege.content.to_csv(index=False)

    content += "\n Gemeinsame Buchungen \n"
    database.gemeinsame_buchungen = database.gemeinsame_buchungen.sort_values(by='Datum')
    content += database.gemeinsame_buchungen.to_csv(index=False)

    content += "\n Stechzeiten \n"
    content += database.stechzeiten[database.persitent_stechzeiten_columns].to_csv(index=False)

    content += "\n Sollzeiten \n"
    content += database.soll_zeiten.to_csv(index=False)

    content += "\n Sonderzeiten \n"
    content += database.sonder_zeiten.to_csv(index=False)

    file = open('../Database_' + database.name + ".csv", 'w')
    file.write(content)
    file.close()

    print("WRITER: All Saved")

def export(database):
    '''
    writes the DATABASE into a file
    '''
    path = "./" + database.name + "_Export_" + str(datetime.today())
    einzelbuchungen_raw_data = database.einzelbuchungen.content.copy()[['Datum', 'Kategorie', 'Name', 'Wert', 'Tags']]
    einzelbuchungen_raw_data.to_csv(path, index=False)
    print("WRITER: Exportiere in : ", path)
    print("WRITER: Export Data:")
    print(einzelbuchungen_raw_data)
    print("WRITER: Done")
