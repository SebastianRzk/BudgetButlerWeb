import math

from butler_offline.viewcore.converter import from_double_to_german


class ReportGenerator():

    def __init__(self, header, row_count=40, page_space=2):
        self._header = header
        self._col_width = 38
        self._page_space = page_space
        self._row_count = row_count
        self._full_lines = []
        self._half_lines = []

    def add_half_line_elements(self, summary_data):
        if self._half_lines:
            self._half_lines.append(''.ljust(self._col_width, ' '))

        for element in summary_data:
            self._half_lines.append(element.ljust(self._col_width, ' '))

            for data_element in summary_data[element]:
                name = ('   ' + self._shorten(data_element, 25)).ljust(28, ' ')
                value = summary_data[element][data_element]

                vorzeichen = '+'
                if value < 0:
                    vorzeichen = ''

                value = (vorzeichen + from_double_to_german(summary_data[element][data_element])).rjust(10, ' ')

                self._half_lines.append(name + value)

    def _shorten(self, name, max_len):
        if len(name) > max_len:
            name = name[:(max_len - 3)] + '...'
        return name

    def add_halfline(self, halfline):
        self._half_lines.append(halfline.ljust(self._col_width, ' '))

    def get_raw_half_lines(self):
        return self._half_lines

    def _add_header(self):
        self._full_lines.append(self._header.ljust(80, ' '))
        self._full_lines.append(''.ljust(80, '-'))

    def _add_footer(self, page_number, max_pages):
        self._full_lines.append(''.ljust(80, '-'))
        self._full_lines.append('Blatt {page}/{max_page}'.format(page=page_number, max_page=max_pages).rjust(80, ' '))

    def generate_pages(self):
        full_content_rows_per_page = (self._row_count - 2 - 2)
        page = 1
        full_rows = math.ceil(len(self._half_lines) / 2) + len(self._full_lines)
        max_pages = -(-full_rows // full_content_rows_per_page )
        for i in range(0, len(self._half_lines), full_content_rows_per_page * 2):
            self._add_header()
            for element in range(i, i + math.ceil(full_content_rows_per_page)):
                left = self._get_half_line(element)
                right = self._get_half_line(math.ceil(element + full_content_rows_per_page))
                self._full_lines.append(left + '    ' + right)
            self._add_footer(page, max_pages)
            page = page + 1
            for i in range(0, self._page_space):
                self._full_lines.append('')

        for line in self._full_lines:
            print('|' + line + '|')
        return self._full_lines

    def _get_half_line(self, number):
        if number >= len(self._half_lines):
            return ''.ljust(self._col_width, ' ')
        return self._half_lines[number]
