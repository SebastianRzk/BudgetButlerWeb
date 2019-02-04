
from mysite.core.ReportGenerator import ReportGenerator
import unittest


class ReportGenerator_test(unittest.TestCase):

    def test_add_halfline_element(self):
        generator = ReportGenerator('header')

        data = {
                'Einnahmen': {'Miete': 123.45,
                              'Sonstiges':-34.12}
            }
        generator.add_half_line_elements(data)

        assert generator.get_raw_half_lines() == ['Einnahmen                             ',
                                                  '   Miete                       +123,45',
                                                  '   Sonstiges                    -34,12']

    def test_add_halfline_element_should_shorten_to_long_names(self):
        generator = ReportGenerator('header')

        data = {
                'Einnahmen': {'MieteMieteMieteMiete1234567890': 123.45}
            }
        generator.add_half_line_elements(data)
        assert generator.get_raw_half_lines() == ['Einnahmen                             ',
                                                  '   MieteMieteMieteMiete12...   +123,45']


    def test_add_halfline_element_max_range(self):
        generator = ReportGenerator('header')

        data = {
                'Einnahmen': {'MieteMieteMieteMiete1234567890': 12345.45}
            }
        generator.add_half_line_elements(data)
        assert generator.get_raw_half_lines() == ['Einnahmen                             ',
                                                  '   MieteMieteMieteMiete12... +12345,45']

    def test_add_halfline_element_min_range(self):
        generator = ReportGenerator('header')

        data = {
                'Einnahmen': {'A': 0}
            }
        generator.add_half_line_elements(data)
        for l in generator.get_raw_half_lines():
            print(l + "|")
        assert generator.get_raw_half_lines() == ['Einnahmen                             ',
                                                  '   A                             +0,00']

    def test_generate_page(self):
        generator = ReportGenerator('SamplePage', 10)

        data = {
                'Einnahmen': {'Firma1': 123.45,
                              'Firma2': 34.12,
                              'Firma3': 222.22},
                'Ausgaben': {'Essen':-300.40,
                             'Miete':-450.00,
                             'Versicherung':-200.00,
                             'Sport':-50.00}
            }
        generator.add_half_line_elements(data)

        assert generator.generate_pages() == [
            'SamplePage                                                                      ',
            '--------------------------------------------------------------------------------',
            'Einnahmen                                    Miete                       -450,00',
            '   Firma1                      +123,45       Versicherung                -200,00',
            '   Firma2                       +34,12       Sport                        -50,00',
            '   Firma3                      +222,22                                          ',
            'Ausgaben                                                                        ',
            '   Essen                       -300,40                                          ',
            '--------------------------------------------------------------------------------',
            '                                                                       Blatt 1/1',
            '', '']

    def test_generate_page_with_no_data_should_generate_empty_page(self):
        generator = ReportGenerator('SamplePage', 10)

        data = {'Einnahmen': {},
                'Ausgaben': {}
                }
        generator.add_half_line_elements(data)
        result = generator.generate_pages()
        print(result)

        assert result == [
            'SamplePage                                                                      ',
            '--------------------------------------------------------------------------------',
            'Einnahmen                                                                       ',
            'Ausgaben                                                                        ',
            '                                                                                ',
            '                                                                                ',
            '                                                                                ',
            '                                                                                ',
            '--------------------------------------------------------------------------------',
            '                                                                       Blatt 1/1',
            '', '']

    def test_generate_page_should_empty_line_between_elements(self):
        generator = ReportGenerator('SamplePage', 10)

        generator.add_half_line_elements({'Einnahmen': {}})
        generator.add_half_line_elements({'Ausgaben': {}})
        result = generator.generate_pages()
        print(result)

        assert result == [
            'SamplePage                                                                      ',
            '--------------------------------------------------------------------------------',
            'Einnahmen                                                                       ',
            '                                                                                ',
            'Ausgaben                                                                        ',
            '                                                                                ',
            '                                                                                ',
            '                                                                                ',
            '--------------------------------------------------------------------------------',
            '                                                                       Blatt 1/1',
            '', '']

    def test_add_halfline(self):
        generator = ReportGenerator('SamplePage', 10)

        generator.add_halfline('----Ausgaben----')
        result = generator.generate_pages()
        print(result)

        assert result == [
            'SamplePage                                                                      ',
            '--------------------------------------------------------------------------------',
            '----Ausgaben----                                                                ',
            '                                                                                ',
            '                                                                                ',
            '                                                                                ',
            '                                                                                ',
            '                                                                                ',
            '--------------------------------------------------------------------------------',
            '                                                                       Blatt 1/1',
            '', '']
