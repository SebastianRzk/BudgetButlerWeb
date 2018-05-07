'''
Created on 11.08.2017

@author: sebastian
'''
from datetime import date
import os
import sys
import unittest

_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _PATH + '/../../')

from viewcore.converter import datum
import core.DatabaseModule as db
from core.database.Einzelbuchungen import Einzelbuchungen


class gemeinsame_buchungen(unittest.TestCase):
    pass