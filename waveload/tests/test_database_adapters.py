import unittest
import sqlite3
from waveload.database_adapters.sqlite_adapter import SQLiteAdapter

class TestSQLiteAdapter(unittest.TestCase):

    def setUp(self):
        self.db_config = {"database": ":memory:"}  # In-memory database for testing
        self.adapter = SQLiteAdapter(self.db_config)

    def tearDown(self):
        self.adapter.close()

    def test_create_table(self):
        # Table creation is handled on initialization, so just check if connection is active
        self.assertIsNotNone(self.adapter.conn)

    def test_insert_and_fetch_data(self):
        data_to_insert = [
            {'date': '2025-04-28', 'usage': '01:00:00', 'idle': '00:10:00', 'breaks': '00:05:00', 'productive': '00:55:00', 'mouse_clicks': 500, 'keystrokes': 250},
            {'date': '2025-04-29', 'usage': '02:00:00', 'idle': '00:20:00', 'breaks': '00:10:00', 'productive': '01:50:00', 'mouse_clicks': 1000, 'keystrokes': 500},
        ]
        self.adapter.insert_data(data_to_insert)
        fetched_data = self.adapter.fetch_all()
        self.assertEqual(len(fetched_data), 2)
        self.assertEqual(fetched_data[0][0], '2025-04-28')
        self.assertEqual(fetched_data[1][1], '02:00:00')

    def test_insert_or_replace(self):
        initial_data = [{'date': '2025-04-30', 'usage': '00:30:00', 'idle': '00:03:00', 'breaks': '00:01:00', 'productive': '00:29:00', 'mouse_clicks': 150, 'keystrokes': 75}]
        self.adapter.insert_data(initial_data)
        updated_data = [{'date': '2025-04-30', 'usage': '00:40:00', 'idle': '00:05:00', 'breaks': '00:02:00', 'productive': '00:38:00', 'mouse_clicks': 200, 'keystrokes': 100}]
        self.adapter.insert_data(updated_data)
        fetched_data = self.adapter.fetch_all()
        self.assertEqual(len(fetched_data), 1)
        self.assertEqual(fetched_data[0][1], '00:40:00')

    def test_invalid_config(self):
        with self.assertRaises(ValueError) as context:
            SQLiteAdapter({})
        self.assertEqual(str(context.exception), "SQLite configuration requires 'database' path.")

if __name__ == '__main__':
    unittest.main()


