'''
Created on 10.05.2017

@author: sebastian
'''

import sys, os
import unittest

import pandas
from pandas.core.frame import DataFrame



myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")
'''
'''
from viewcore.converter import *




class TesteConverter(unittest.TestCase):

    def test_datum(self):
        result = datum("2.3.2017")
        assert result.day == 2
        assert result.month == 3
        assert result.year == 2017

    def test_dezimal_float(self):
        result = dezimal_float("2,34")
        assert result == 2.34


    def test_datum_backwards(self):
        result = datum_to_string(datum('13.12.2015'))
        assert result == '13.12.2015'

    def test_fromDoubleToGerman(self):
        result = from_double_to_german(3.444)
        assert result == "3,44"

