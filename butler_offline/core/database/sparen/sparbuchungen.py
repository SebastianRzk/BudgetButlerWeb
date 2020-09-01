from butler_offline.core.database.database_object import DatabaseObject


class Sparbuchungen(DatabaseObject):
    TABLE_HEADER = ['Datum', 'Name', 'Wert', 'Typ', 'Konto' , 'Dynamisch']

    def __init__(self):
        super().__init__(self.TABLE_HEADER)


    def add(self, datum, name, wert, typ, konto, dynamisch=False):
        neue_sparbuchung = pd.DataFrame([[datum, name, wert, typ, konto, dynamisch]], columns=self.TABLE_HEADER)
        self.content = self.content.append(neue_sparbuchung, ignore_index=True)
        self.taint()
        self._sort()

    def get_all(self):
        return self.content

    def edit(self, index, datum, name, wert, typ, konto,):
        self.edit_element(index, {
            'Datum': datum,
            'Wert': wert,
            'Typ': typ,
            'Konto': konto,
            'Name': name
        })

    def _sort(self):
        self.content = self.content.sort_values(by=['Datum', 'Konto', 'Name'])
        self.content = self.content.reset_index(drop=True)
