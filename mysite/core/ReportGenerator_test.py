'''
Created on 10.05.2017

@author: sebastian
'''


class ReportGenerator():

    _half_lines = []
    _full_lines = []


    def __init__(self, page_height):
        self._col_width = 38
        self._page_height = page_height


    def add_half_line_elements(self, summary_data):
        for element in summary_data:
            self._half_lines.append(element.ljust(self._col_width, ' '))

            for data_element in summary_data[element]:
                name = ('   ' + data_element).ljust(26, ' ')

