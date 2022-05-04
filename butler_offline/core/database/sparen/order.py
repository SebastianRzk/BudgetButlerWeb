from butler_offline.core.database.database_object import DatabaseObject
import pandas as pd


class Order(DatabaseObject):
    STATIC_TABLE_HEADER = ['Datum', 'Name', 'Konto', 'Depotwert', 'Wert']
    TABLE_HEADER = STATIC_TABLE_HEADER + ['Dynamisch']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)

    def add(self, datum, name, konto, depotwert, wert, dynamisch=False):
        neue_order = pd.DataFrame([[datum, name, konto, depotwert, wert, dynamisch]], columns=self.TABLE_HEADER)
        self.content = pd.concat([self.content, neue_order], ignore_index=True)
        self.taint()
        self._sort()

    def get_all(self):
        return self.content

    def append_row(self, row):
        self.content = pd.concat([self.content, row], ignore_index=True)
        self._sort()

    def edit(self, index, datum, name, konto, depotwert, wert):
        self.edit_element(index, {
            'Datum': datum,
            'Name': name,
            'Konto': konto,
            'Depotwert': depotwert,
            'Wert': wert
        })

    def _sort(self):
        self.content = self.content.sort_values(by=['Datum', 'Konto', 'Name'])
        self.content = self.content.reset_index(drop=True)

    def get_order_fuer(self, konto):
        konto_buchungen = self.content[self.content.Konto == konto].copy()
        return konto_buchungen.Wert.sum()

    def get_order_fuer_depotwert(self, depotwert):
        konto_buchungen = self.content[self.content.Depotwert == depotwert].copy()
        return konto_buchungen.Wert.sum()

    def get_dynamische_einzelbuchungen(self):
        order = self.content.copy()
        order['Kategorie'] = 'Sparen'
        order.Wert = order.Wert * -1

        order['Dynamisch'] = True
        order['Tags'] = None

        del order['Konto']
        del order['Depotwert']

        return order

    def select_year(self, year):
        include = self.content.copy()
        include['datum_filter'] = include.Datum.map(lambda x: x.year)
        include = include[include.datum_filter == year].copy()
        del include['datum_filter']
        selected = Order()
        selected.content = include
        return selected

    def get_static_content(self):
        static_content = self.content.copy()[self.content.Dynamisch == False]
        return static_content[self.STATIC_TABLE_HEADER]
