'''
Created on 10.05.2017

@author: sebastian
'''
import datetime

def datum(string):
    return datetime.datetime.strptime(string , '%d/%m/%Y').date()

def dezimal_float(string):
    string = string.replace(",", ".")
    return float(string)

def from_double_to_german(value):
    str = "%.2f" % value
    return str.replace(".", ",")

def laenge(string):
    return datetime.datetime.strptime(string, '%H:%M').time()

def datum_to_string(datum_obj):
    return datum_obj.strftime('%d/%m/%Y')

