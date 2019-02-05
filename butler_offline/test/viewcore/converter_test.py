'''
Created on 10.05.2017

@author: sebastian
'''

import unittest
from butler_offline.viewcore.converter import *

class TesteConverter(unittest.TestCase):

    def test_datum(self):
        result = datum("2017-03-02")
        assert result.day == 2
        assert result.month == 3
        assert result.year == 2017

    def test_dezimal_float(self):
        result = dezimal_float("2,34")
        assert result == 2.34


    def test_datum_to_german(self):
        result = datum_to_german(datum('2015-12-13'))
        assert result == '13.12.2015'

    def test_datum_from_german(self):
        result = datum_to_german(datum_from_german('13.12.2015'))
        assert result == '13.12.2015'

    def test_datum_backwards(self):
        result = datum_to_string(datum('2015-12-13'))
        assert result == '2015-12-13'

    def test_german_to_rfc(self):
        assert german_to_rfc('13.12.2014') == '2014-12-13'

    def test_fromDoubleToGerman(self):
        result = from_double_to_german(3.444)
        assert result == "3,44"



