from butler_offline.viewcore.renderhelper import Betrag
from butler_offline.viewcore.template.fa import fa_plus, fa_pencil


class DauerauftraegeChange:
    def __init__(self, fa: str, start_datum: str, ende_datum: str, name: str, kategorie: str, rhythmus: str,
                 wert: Betrag):
        self.fa = fa
        self.start_datum = start_datum
        self.ende_datum = ende_datum
        self.name = name
        self.kategorie = kategorie
        self.wert = wert
        self.rhythmus = rhythmus

    def __eq__(self, other):
        if not type(self) is type(other):
            return False
        return (self.fa == other.fa
                and self.start_datum == other.start_datum
                and self.ende_datum == other.ende_datum
                and self.name == other.name
                and self.kategorie == other.kategorie
                and self.rhythmus == other.rhythmus
                and self.wert == other.wert)

    def __str__(self):
        return (f'DauerauftragChange(fa={self.fa}, start_datum={self.start_datum}, ende_datum={self.ende_datum},'
                f' name={self.name}, kategorie={self.kategorie}, rhythmus={self.rhythmus}, wert={self.wert})')

    def __repr__(self):
        return str(self)


class DauerauftragAddedChange(DauerauftraegeChange):
    def __init__(self, start_datum: str, ende_datum: str, name: str, kategorie: str, rhythmus: str, wert: Betrag):
        super().__init__(fa=fa_plus, start_datum=start_datum, ende_datum=ende_datum,
                         name=name, kategorie=kategorie, rhythmus=rhythmus, wert=wert)


class DauerauftragEditiertChange(DauerauftraegeChange):
    def __init__(self, start_datum: str, ende_datum: str, name: str, kategorie: str, rhythmus: str, wert: Betrag):
        super().__init__(fa=fa_pencil, start_datum=start_datum, ende_datum=ende_datum,
                         name=name, kategorie=kategorie, rhythmus=rhythmus, wert=wert)
