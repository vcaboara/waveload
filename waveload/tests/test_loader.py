# waveload/tests/test_loader.py
import unittest
from unittest.mock import patch, mock_open, MagicMock
from waveload.loader import HistorystatsLoader

class TestHistorystatsLoader(unittest.TestCase):

    def test_init_sqlite(self):
        config = {"database": "test.db"}
        loader = HistorystatsLoader("sqlite", config)
        self.assertIsNotNone(loader.adapter)
        self.assertEqual(loader.adapter.database_path, "test.db")

    def test_init_unsupported_db(self):
        config = {}
        with self.assertRaisesRegex(ValueError, "Unsupported database type: postgresql"):
            HistorystatsLoader("postgresql", config)

    @patch('waveload.loader.HistorystatsLoader._parse_historystats')
    @patch('waveload.loader.SQLiteAdapter')
    def test_load_from_content_success(self, MockSQLiteAdapter, MockParseHistorystats):
        mock_adapter_instance = MockSQLiteAdapter.return_value
        mock_parse_historystats_data = [{"date": "2025-04-28", "usage": "some_usage", "breaks": "some_breaks"}]
        MockParseHistorystats.return_value = mock_parse_historystats_data

        config = {"database": "test.db"}
        loader = HistorystatsLoader("sqlite", config)
        content = ["Date: 2025-04-28 Some other data"]  # Example content
        loader.load_from_content(content)

        MockParseHistorystats.assert_called_once_with(content)
        mock_adapter_instance.insert_data.assert_called_once_with(mock_parse_historystats_data)

    @patch('waveload.loader.HistorystatsLoader._parse_historystats')
    @patch('waveload.loader.SQLiteAdapter')
    def test_load_from_content_no_data(self, MockSQLiteAdapter, MockParseHistorystats):
        mock_adapter_instance = MockSQLiteAdapter.return_value
        MockParseHistorystats.return_value = []

        config = {"database": "test.db"}
        loader = HistorystatsLoader("sqlite", config)
        content = ["Some header line"]
        loader.load_from_content(content)

        MockParseHistorystats.assert_called_once_with(content)
        mock_adapter_instance.insert_data.assert_not_called()

    @patch('builtins.open', new_callable=mock_open, read_data="Date: 2025-04-28 Some data\nAnother line")
    @patch('waveload.loader.HistorystatsLoader.load_from_content')
    def test_load_from_file_success(self, MockLoadFromContent, MockOpen):
        config = {"database": "test.db"}
        loader = HistorystatsLoader("sqlite", config)
        file_path = "test_historystats.txt"
        loader.load_from_file(file_path)
        MockOpen.assert_called_once_with(file_path, 'r')
        MockLoadFromContent.assert_called_once_with(["Date: 2025-04-28 Some data\n", "Another line"])

    def test_load_from_file_not_found(self):
        config = {"database": "test.db"}
        loader = HistorystatsLoader("sqlite", config)
        file_path = "nonexistent_file.txt"
        with self.assertRaisesRegex(FileNotFoundError, f"File not found: {file_path}"):
            loader.load_from_file(file_path)

if __name__ == '__main__':
    unittest.main()
