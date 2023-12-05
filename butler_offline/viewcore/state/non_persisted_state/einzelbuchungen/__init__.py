from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.viewcore.template.fa import fa_plus, fa_pencil


class EinzelbuchungsChange:
    def __init__(self, fa: str, datum: str, name: str, kategorie: str, wert: Betrag):
        self.fa = fa
        self.datum = datum
        self.name = name
        self.kategorie = kategorie
        self.wert = wert

    def __eq__(self, other):
        if not type(self) is type(other):
            return False
        return (self.fa == other.fa
                and self.datum == other.datum
                and self.name == other.name
                and self.kategorie == other.kategorie
                and self.wert == other.wert)

    def __str__(self):
        return (f'EinzelbuchungsChange(fa={self.fa}, datum={self.datum}, name={self.name}, kategorie={self.kategorie},'
                f' wert={self.wert})')

    def __repr__(self):
        return str(self)


class EinzelbuchungAddedChange(EinzelbuchungsChange):
    def __init__(self, datum: str, name: str, kategorie: str, wert: Betrag):
        super().__init__(fa=fa_plus, datum=datum, name=name, kategorie=kategorie, wert=wert)


class EinzelbuchungEditiertChange(EinzelbuchungsChange):
    def __init__(self, datum: str, name: str, kategorie: str, wert: Betrag):
        super().__init__(fa=fa_pencil, datum=datum, name=name, kategorie=kategorie, wert=wert)
