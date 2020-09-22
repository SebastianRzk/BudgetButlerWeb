from butler_offline.core.database.database_object import DatabaseObject
import pandas as pd


class Order(DatabaseObject):
    TABLE_HEADER = ['Datum', 'Name', 'Konto', 'Depotwert', 'Wert']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)

    def add(self, datum, name, konto, depotwert, wert):
        neue_order = pd.DataFrame([[datum, name, konto, depotwert, wert]], columns=self.TABLE_HEADER)
        self.content = self.content.append(neue_order, ignore_index=True)
        self.taint()
        self._sort()

    def get_all(self):
        return self.content

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

