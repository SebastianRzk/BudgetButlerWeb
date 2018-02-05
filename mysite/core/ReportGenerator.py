
from viewcore.converter import from_double_to_german

class ReportGenerator():

    _half_lines = []
    _full_lines = []


    def __init__(self):
        self._col_width = 38

    def add_half_line_elements(self, summary_data):
        for element in summary_data:
            self._half_lines.append(element.ljust(self._col_width, ' '))

            for data_element in summary_data[element]:
                name = ('   ' + data_element).ljust(27, ' ')
                value = summary_data[element][data_element]

                vorzeichen = '+'
                if value < 0:
                    vorzeichen = ''

                value = (vorzeichen + from_double_to_german(summary_data[element][data_element])).rjust(11, ' ')

                self._half_lines.append(name+value)

    def get_raw_half_lines(self):
        return self._half_lines
    
