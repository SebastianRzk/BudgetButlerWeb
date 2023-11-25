class Betrag:
    def __init__(self, betrag: float):
        self._betrag = betrag

    def js(self):
        return '%.2f' % self._betrag

    def deutsch(self):
        return self.js().replace('.', ',')

    def value(self):
        return self._betrag

    def __eq__(self, other):
        if not isinstance(other, Betrag):
            return False
        return self.js() == other.js()

    def __str__(self):
        return 'Betrag({betrag})'.format(betrag=self.js())

    def __repr__(self):
        return str(self)


class BetragListe:

    def __init__(self, initial: list|None = None):
        if not initial:
            initial = []
        self._liste = initial

    def append(self, betrag: Betrag):
        self._liste.append(betrag)

    def js(self):
        content = ', '.join(map(lambda x: x.js(), self._liste))
        return '[{elemente}]'.format(elemente=content)

    def content(self):
        return self._liste

    def __str__(self):
        return 'BetragListe({elemente})'.format(elemente=self.js())

    def __eq__(self, other):
        if not isinstance(other, BetragListe):
            return False
        return self.js() == other.js()

    def __repr__(self):
        return str(self)