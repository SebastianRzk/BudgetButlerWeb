
from core.ReportGenerator import ReportGenerator
import unittest


class ReportGenerator_test(unittest.TestCase):

    def test_add_halfline_element(self):
        generator = ReportGenerator()

        data = {
                'Einnahmen': {'Miete': 123.45,
                              'Sonstiges': -34.12}
            }
        generator.add_half_line_elements(data)

        assert generator.get_raw_half_lines() == ['Einnahmen                             ',
                                                  '   Miete                       +123,45',
                                                  '   Sonstiges                    -34,12']

    def test_add_halfline_element_should_shorten_to_long_names(self):
        generator = ReportGenerator()

        data = {
                'Einnahmen': {'MieteMieteMieteMiete1234567890': 123.45}
            }
        generator.add_half_line_elements(data)
        for l in generator.get_raw_half_lines():
            print(l+"|")
        assert generator.get_raw_half_lines() == ['Einnahmen                             ',
                                                  '   MieteMieteMieteMiete12...   +123,45']


    def test_add_halfline_element_max_range(self):
        generator = ReportGenerator()

        data = {
                'Einnahmen': {'MieteMieteMieteMiete1234567890': 12345.45}
            }
        generator.add_half_line_elements(data)
        for l in generator.get_raw_half_lines():
            print(l+"|")
        assert generator.get_raw_half_lines() == ['Einnahmen                             ',
                                                  '   MieteMieteMieteMiete12... +12345,45']

    def test_add_halfline_element_min_range(self):
        generator = ReportGenerator()

        data = {
                'Einnahmen': {'A': 0}
            }
        generator.add_half_line_elements(data)
        for l in generator.get_raw_half_lines():
            print(l+"|")
        assert generator.get_raw_half_lines() == ['Einnahmen                             ',
                                                  '   A                             +0,00']

