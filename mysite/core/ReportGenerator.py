
from viewcore.converter import from_double_to_german

class ReportGenerator():



    def __init__(self):
        self._col_width = 38
        self._full_lines = []
        self._half_lines = []

    def add_half_line_elements(self, summary_data):
        for element in summary_data:
            self._half_lines.append(element.ljust(self._col_width, ' '))

            for data_element in summary_data[element]:
                name = ('   ' + self._shorten(data_element, 25)).ljust(28, ' ')
                value = summary_data[element][data_element]

                vorzeichen = '+'
                if value < 0:
                    vorzeichen = ''

                value = (vorzeichen + from_double_to_german(summary_data[element][data_element])).rjust(10, ' ')

                self._half_lines.append(name+value)

    def _shorten(self, name, max_len):
        if len(name) > max_len:
            name = name[:(max_len-3)] + '...'
        return name

    def get_raw_half_lines(self):
        return self._half_lines
    
