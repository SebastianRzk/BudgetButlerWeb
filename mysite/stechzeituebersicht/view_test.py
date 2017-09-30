'''
Created on 10.05.2017

@author: sebastian
'''

from datetime import date
import datetime
import sys, os
import unittest

from django.test import TestCase
import pandas
from pandas.core.frame import DataFrame

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + "/../")

from test import DBManagerStub
from core.DatabaseModule import Database
from stechzeituebersicht import views
import viewcore
from viewcore.converter import datum, time



class TesteStechzeitenuebersicht(unittest.TestCase):

    def set_up(self):
        DBManagerStub.setup_db_for_test()

    def test_withNoStechzeiten_shouldReturnNothing_andNoError(self):
        self.set_up()
        views.handle_request()


if __name__ == '__main__':
    unittest.main()

class GetRequest():
    method = "GET"

class PostRequest:
    method = "POST"
    def __init__(self, args):
        self.POST = args
