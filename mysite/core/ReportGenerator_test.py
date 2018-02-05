
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

            
