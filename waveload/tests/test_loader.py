import unittest
from unittest.mock import patch, mock_open
from waveload.loader import HistorystatsLoader
from waveload.database_adapters.sqlite_adapter import SQLiteAdapter  # Assuming SQLite for now

class TestHistorystatsLoader(unittest.TestCase):

    @patch("waveload.loader.open", new_callable=mock_open, read_data="""2025-04-28
  Usage: 00:10:00
  Idle: 00:05:00
  Breaks: 00:01:00
  Productive: 00:09:00
  Mouse clicks: 100
  Keystrokes: 50
2025-04-29
  Usage: 00:20:00
  Idle: 00:08:00
  Breaks: 00:02:00
  Productive: 00:18:00
  Mouse clicks: 200
  Keystrokes: 100
""")
    @patch.object(SQLiteAdapter, 'insert_data')
    def test_load_from_file_success(self, mock_insert, mock_file):
        loader = HistorystatsLoader("sqlite", {"database": ":memory:"})
        loader.load_from_file("dummy_path.txt")
        mock_insert.assert_called_once_with([
            {'date': '2025-04-28', 'usage': '00:10:00', 'idle': '00:05:00', 'breaks': '00:01:00', 'productive': '00:09:00', 'mouse_clicks': 100, 'keystrokes': 50},
            {'date': '2025-04-29', 'usage': '00:20:00', 'idle': '00:08:00', 'breaks': '00:02:00', 'productive': '00:18:00', 'mouse_clicks': 200, 'keystrokes': 100}
        ])

    @patch("waveload.loader.open", side_effect=FileNotFoundError)
    def test_load_from_file_not_found(self, mock_file):
        loader = HistorystatsLoader("sqlite", {"database": ":memory:"})
        with self.assertRaises(FileNotFoundError):
            loader.load_from_file("nonexistent_path.txt")

    def test_unsupported_db_type(self):
        with self.assertRaises(ValueError) as context:
            HistorystatsLoader("invalid_db", {})
        self.assertEqual(str(context.exception), "Unsupported database type: invalid_db")

if __name__ == '__main__':
    unittest.main()

