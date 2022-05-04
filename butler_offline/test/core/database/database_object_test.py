import unittest
from butler_offline.core.database.database_object import DatabaseObject
import pandas as pd


class DatabaseObjectTest(unittest.TestCase):
    def test_something(self):
        stored_columns = ['col1', 'col2']
        component_under_test = DatabaseObject(stored_columns=stored_columns)
        content = pd.DataFrame([['A', 'B']], columns=stored_columns)
        component_under_test.content = pd.concat([component_under_test.content, content])

        static_content = component_under_test.get_static_content()

        self.assertListEqual(static_content.columns.tolist(), stored_columns)
        assert len(static_content) == 1
        assert static_content.col1[0] == 'A'
        assert static_content.col2[0] == 'B'


if __name__ == '__main__':
    unittest.main()
