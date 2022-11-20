from butler_offline.core.database.dauerauftraege import Dauerauftraege
from butler_offline.core.database.einzelbuchungen import Einzelbuchungen
from butler_offline.core.database.gemeinsamebuchungen import Gemeinsamebuchungen
from butler_offline.core.database.sparen.sparbuchungen import Sparbuchungen
from butler_offline.core.database.sparen.kontos import Kontos
from butler_offline.core.database.sparen.depotwerte import Depotwerte
from butler_offline.core.database.sparen.order import Order
from butler_offline.core.database.sparen.depotauszuege import Depotauszuege
from butler_offline.core.database.sparen.orderdauerauftrag import OrderDauerauftrag
from butler_offline.core.database.gemeinsamebuchungen.abrechnen import abrechnen



class Database:
    def __init__(self, name, ausgeschlossene_kategorien=set()):
        self.name = name
        self.dauerauftraege = Dauerauftraege()
        self.gemeinsamebuchungen = Gemeinsamebuchungen()
        self.einzelbuchungen = Einzelbuchungen()
        self.sparbuchungen = Sparbuchungen()
        self.sparkontos = Kontos()
        self.depotwerte = Depotwerte()
        self.order = Order()
        self.orderdauerauftrag = OrderDauerauftrag()
        self.depotauszuege = Depotauszuege()
        self.einzelbuchungen.ausgeschlossene_kategorien = ausgeschlossene_kategorien
        self.tainted = 0

    def taint(self):
        self.tainted = self.tainted + 1

    def is_tainted(self):
        return self.taint_number() != 0

    def taint_number(self):
        return self.tainted + \
               self.dauerauftraege.taint_number() + \
               self.einzelbuchungen.taint_number() + \
               self.gemeinsamebuchungen.taint_number() + \
               self.sparbuchungen.taint_number() + \
               self.sparkontos.taint_number() + \
               self.depotwerte.taint_number() + \
               self.order.taint_number() +\
               self.depotauszuege.taint_number() +\
               self.orderdauerauftrag.taint_number()

    def refresh(self):
        print('DATABASE: Erneuere Datenbestand')
        alle_dauerauftragsbuchungen = self.dauerauftraege.get_all_einzelbuchungen_until_today()
        self.einzelbuchungen.append_row(alle_dauerauftragsbuchungen)

        anteil_gemeinsamer_buchungen = self.gemeinsamebuchungen.anteil_gemeinsamer_buchungen()
        self.einzelbuchungen.append_row(anteil_gemeinsamer_buchungen)

        anteil_sparbuchungen = self.sparbuchungen.get_dynamische_einzelbuchungen()
        self.einzelbuchungen.append_row(anteil_sparbuchungen)

        anteil_orderdauerauftrag = self.orderdauerauftrag.get_all_order_until_today()
        self.order.append_row(anteil_orderdauerauftrag)

        anteil_order = self.order.get_dynamische_einzelbuchungen()
        self.einzelbuchungen.append_row(anteil_order)

        print('DATABASE: Datenbestand erneuert')

    def _row_to_dict(self, columns, index, row_data):
        row = {'index': index}
        for key in columns:
            row[key] = row_data[key]
        return row

    def frame_to_list_of_dicts(self, dataframe):
        result_list = []
        for index, row_data in dataframe.iterrows():
            row = self._row_to_dict(dataframe.columns, index, row_data)
            result_list.append(row)

        return result_list

    def abrechnen(self,
              mindate,
              maxdate,
              set_ergebnis=None,
              verhaeltnis=50,
              set_self_kategorie=None,
              set_other_kategorie=None):
        return abrechnen(
            database=self,
            mindate=mindate,
            maxdate=maxdate,
            set_ergebnis=set_ergebnis,
            verhaeltnis=verhaeltnis,
            set_self_kategorie=set_self_kategorie,
            set_other_kategorie=set_other_kategorie
        )