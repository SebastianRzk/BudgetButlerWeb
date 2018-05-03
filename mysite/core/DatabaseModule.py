'''
Created on 17.09.2016

@author: sebastian
'''

from datetime import datetime, date, timedelta

from core.Frequency import FrequencsFunctions
from core.database.Dauerauftraege import Dauerauftraege
from core.database.Einzelbuchungen import Einzelbuchungen
from core.database.Gemeinsamebuchungen import Gemeinsamebuchungen
from pandas import DataFrame
from viewcore import viewcore
from viewcore.converter import datum, datum_to_string
from viewcore.viewcore import name_of_partner
from viewcore.viewcore import today


class StringWriter():
    '''
    Shadowes file
    '''

    def __init__(self):
        self.value = ""

    def write(self, new_line):
        '''write line into virtual file'''
        self.value = self.value + new_line

    def to_string(self):
        ''' get filecontent'''
        return self.value


class Database:
    '''
    Database
    '''

    def __init__(self, name):
        self.name = name
        self.dauerauftraege = Dauerauftraege()
        self.gemeinsamebuchungen = Gemeinsamebuchungen()
        self.einzelbuchungen = Einzelbuchungen()
        self.tainted = 0

    def taint(self):
        self.tainted = self.tainted + 1

    def is_tainted(self):
        return self.taint_number() != 0

    def taint_number(self):
        return self.tainted + self.dauerauftraege.taint_number() + self.einzelbuchungen.taint_number()

    def de_taint(self):
        self.tainted = 0
        self.dauerauftraege.de_taint()
        self.einzelbuchungen.de_taint()

    def refresh(self):
        print('DATABASE: Erneuere Datenbestand')
        alle_dauerauftragsbuchungen = self.dauerauftraege.get_all_einzelbuchungen_until_today()
        self.einzelbuchungen.append_row(alle_dauerauftragsbuchungen)

        anteil_gemeinsamer_buchungen = self.gemeinsamebuchungen.anteil_gemeinsamer_buchungen()
        self.einzelbuchungen.append_row(anteil_gemeinsamer_buchungen)

        self.einzelbuchungen.sort()
        print('DATABASE: Datenbestand erneuert')

    def _write_trenner(self, abrechnunsdatei):
        return abrechnunsdatei.write("".rjust(40, "#") + "\n ")

    def abrechnen(self):
        '''
        rechnet gemeinsame ausgaben aus der Datenbank ab
        '''
        name_self = viewcore.database_instance().name
        name_partner = viewcore.name_of_partner()

        ausgaben_maureen = self.gemeinsamebuchungen.content[self.gemeinsamebuchungen.content.Person == name_partner]
        ausgaben_sebastian = self.gemeinsamebuchungen.content[self.gemeinsamebuchungen.content.Person == name_self]
        summe_maureen = self._sum(ausgaben_maureen['Wert'])
        summe_sebastian = self._sum(ausgaben_sebastian['Wert'])

        ausgaben_gesamt = summe_maureen + summe_sebastian

        dif_maureen = (ausgaben_gesamt / 2) - summe_maureen

        abrechnunsdatei = StringWriter()
        abrechnunsdatei.write("Abrechnung vom " + datum_to_string(today()) + "\n")
        self._write_trenner(abrechnunsdatei)
        abrechnunsdatei.write("Ergebnis:\n")

        if dif_maureen > 0:
            abrechnunsdatei.write(name_self + ' muss an ' + name_partner + ' noch ' + str('%.2f' % dif_maureen) + "€ überweisen.\n")
        else:
            abrechnunsdatei.write(name_partner + ' muss an ' + name_self + ' noch ' + str("%.2f" % (dif_maureen * -1)) + "€ überweisen.\n")

        abrechnunsdatei.write("\n")
        abrechnunsdatei.write(('Ausgaben von ' + name_partner).ljust(30, " ") + str("%.2f" % summe_maureen).rjust(7, " ") + "\n")
        abrechnunsdatei.write(('Ausgaben von ' + name_self).ljust(30, " ") + str("%.2f" % summe_sebastian).rjust(7, " ") + "\n")
        abrechnunsdatei.write("".ljust(38, "-") + "\n")
        abrechnunsdatei.write("Gesamt".ljust(30, " ") + str("%.2f" % ausgaben_gesamt).rjust(7, " ") + "\n \n \n")

        self._write_trenner(abrechnunsdatei)
        abrechnunsdatei.write("Gesamtausgaben pro Person \n")
        self._write_trenner(abrechnunsdatei)

        abrechnunsdatei.write("Datum".ljust(10, " ") + " Kategorie    " + "Name".ljust(20, " ") + " " + "Wert".rjust(7, " ") + "\n")
        for _, row in self.gemeinsamebuchungen.content.iterrows():
            abrechnunsdatei.write(datum_to_string(row['Datum']) + "  " + row['Kategorie'].ljust(len("Kategorie   "), " ") + " " + row['Name'].ljust(20, " ") + " " + str("%.2f" % (row['Wert'] / 2)).rjust(7, " ") + "\n")

        abrechnunsdatei.write("\n")
        abrechnunsdatei.write("\n")

        self._write_trenner(abrechnunsdatei)
        abrechnunsdatei.write('Ausgaben von ' + name_partner + '\n')
        self._write_trenner(abrechnunsdatei)

        abrechnunsdatei.write("Datum".ljust(10, " ") + " Kategorie    " + "Name".ljust(20, " ") + " " + "Wert".rjust(7, " ") + "\n")
        for _ , row in ausgaben_maureen.iterrows():
            abrechnunsdatei.write(datum_to_string(row['Datum']) + "  " + row['Kategorie'].ljust(len("Kategorie   "), " ") + " " + row['Name'].ljust(20, " ") + " " + str("%.2f" % (row['Wert'])).rjust(7, " ") + "\n")

        abrechnunsdatei.write("\n")
        abrechnunsdatei.write("\n")
        self._write_trenner(abrechnunsdatei)
        abrechnunsdatei.write('Ausgaben von ' + name_self + '\n')
        self._write_trenner(abrechnunsdatei)

        abrechnunsdatei.write("Datum".ljust(10, " ") + " Kategorie    " + "Name".ljust(20, " ") + " " + "Wert".rjust(7, " ") + "\n")
        for _ , row in ausgaben_sebastian.iterrows():
            abrechnunsdatei.write(datum_to_string(row['Datum']) + "  " + row['Kategorie'].ljust(len("Kategorie   "), " ") + " " + row['Name'].ljust(20, " ") + " " + str("%.2f" % (row['Wert'])).rjust(7, " ") + "\n")

        ausgaben = DataFrame()
        for _ , row in self.gemeinsamebuchungen.content.iterrows():
            buchung = self._berechne_abbuchung(row['Datum'], row['Kategorie'], row['Name'], ("%.2f" % (row['Wert'] / 2)))
            buchung.Dynamisch = False
            ausgaben = ausgaben.append(buchung)

        abrechnunsdatei.write("\n\n")
        abrechnunsdatei.write("#######MaschinenimportStart\n")
        abrechnunsdatei.write(ausgaben.to_csv(index=False))
        abrechnunsdatei.write("#######MaschinenimportEnd\n")

        self.einzelbuchungen.append_row(ausgaben)
        self.gemeinsamebuchungen.empty()
        viewcore.save_refresh()
        self.abrechnungs_write_function("../Abrechnung_" + str(datetime.now()), abrechnunsdatei.to_string())
        return abrechnunsdatei.to_string()

    def _sum(self, data):
        if data.empty:
            return 0
        return data.sum()

    def _write_to_file(self, filename, content):
        f = open(filename, "w")
        f.write(content)

    abrechnungs_write_function = _write_to_file

    def _berechne_abbuchung(self, laufdatum, kategorie, name, wert):
        return DataFrame([[laufdatum, kategorie, name, wert, True]], columns=('Datum', 'Kategorie', 'Name', 'Wert', 'Dynamisch'))

    def func_woechentlich(self, buchungs_datum):
        return buchungs_datum.isocalendar()[1]

    def func_monatlich(self, buchungs_datum):
        return buchungs_datum.month

    def _row_to_dict(self, columns, index, row_data):
        row = {}
        row['index'] = index
        for key in columns:
            row[key] = row_data[key]
        return row

    def frame_to_list_of_dicts(self, dataframe):
        result_list = []
        for index, row_data in dataframe.iterrows():
            row = self._row_to_dict(dataframe.columns, index, row_data)
            result_list.append(row)

        return result_list
