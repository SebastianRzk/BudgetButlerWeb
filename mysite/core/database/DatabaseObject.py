'''
Created on 03.05.2018

@author: sebastian
'''


class DatabaseObject:

    def __init__(self):
        self.tainted = 0

    def taint(self):
        self.tainted = self.tainted + 1

    def taint_number(self):
        return self.tainted

    def de_taint(self):
        self.tainted = 0
