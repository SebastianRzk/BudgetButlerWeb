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
import viewcore.viewcore




class TesteViewcore(unittest.TestCase):

    def teste_getIcon_withExactKategoryName_shouldReturnIcon(self):
        icon = viewcore.viewcore.get_icon_for_categorie('Essen');
        assert icon == 'fa fa-cutlery'

    def teste_getIcon_withNameContainsAcategoryName_shouldReturnIcon(self):
        icon = viewcore.viewcore.get_icon_for_categorie('Essen (gemeinsam)');
        assert icon == 'fa fa-cutlery'


if __name__ == '__main__':
    unittest.main()
