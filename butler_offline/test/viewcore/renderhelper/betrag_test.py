from butler_offline.viewcore.renderhelper import Betrag


def test_should_be_equal():
    assert Betrag(2.00) == Betrag(2.00)
    assert Betrag(2) == Betrag(2.000)
    assert not Betrag(2.00) == Betrag(3.00)
    assert not Betrag(12) == ''


def test_to_str():
    assert str(Betrag(2.00)) == 'Betrag(2.00)'


def test_to_repr():
    assert repr(Betrag(2.00)) == 'Betrag(2.00)'


def test_js():
    assert Betrag(2.34).js() == '2.34'


def test_deutsch():
    assert Betrag(2.34).deutsch() == '2,34'
