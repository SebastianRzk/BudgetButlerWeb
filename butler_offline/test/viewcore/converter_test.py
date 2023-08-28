from butler_offline.viewcore.converter import (datum_from_german, datum, dezimal_float, datum_to_german,
                                               datum_to_string, from_double_to_german, german_to_rfc)


def test_datum():
    result = datum("2017-03-02")
    assert result.day == 2
    assert result.month == 3
    assert result.year == 2017


def test_dezimal_float():
    result = dezimal_float("2,34")
    assert result == 2.34


def test_datum_to_german():
    result = datum_to_german(datum('2015-12-13'))
    assert result == '13.12.2015'


def test_datum_from_german():
    result = datum_to_german(datum_from_german('13.12.2015'))
    assert result == '13.12.2015'


def test_datum_backwards():
    result = datum_to_string(datum('2015-12-13'))
    assert result == '2015-12-13'


def test_german_to_rfc():
    assert german_to_rfc('13.12.2014') == '2014-12-13'


def test_from_double_to_german():
    result = from_double_to_german(3.444)
    assert result == "3,44"
