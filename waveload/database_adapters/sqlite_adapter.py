# waveload/database_adapters/sqlite_adapter.py
"""Provides an adapter for interacting with SQLite databases."""
import sqlite3
from typing import Dict, Any, List, Tuple
from waveload.exceptions import DatabaseConnectionError, DatabaseOperationError

class SQLiteAdapter:
    """
    A database adapter for SQLite databases.
    Provides methods for connecting, creating tables, inserting data,
    fetching data, and closing the connection.
    """
    def __init__(self, config: Dict[str, str]):
        """
        Initializes the SQLiteAdapter with the database configuration.

        Args:
            config (Dict[str, str]): A dictionary containing the database path.
                                     Expected key: 'database'.

        Raises:
            ValueError: If the 'database' path is not provided in the config.
        """
        self.database_path = config.get("database")
        if not self.database_path:
            raise ValueError("SQLite configuration requires 'database' path.")
        self.conn: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None
        self._connect()
        self._create_table_if_not_exists()

    def _connect(self):
        """Establishes a connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.database_path)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            raise DatabaseConnectionError(f"Error connecting to SQLite database: {e}") from e

    def _create_table_if_not_exists(self):
        """Creates the workrave data table if it doesn't already exist."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS workrave_data (
                    date TEXT PRIMARY KEY,
                    usage TEXT,
                    breaks TEXT
                    -- Add other columns as needed
                )
            """)
            self.conn.commit()
        except sqlite3.Error as e:
            raise DatabaseOperationError(f"Error creating table: {e}") from e

    def insert_data(self, data_list: List[Dict[str, Any]]):
        """
        Inserts a list of data dictionaries into the workrave_data table.

        Args:
            data_list (List[Dict[str, Any]]): A list of dictionaries, where each
                                              dictionary represents a row to insert.
                                              Expected keys: 'date', 'usage', 'breaks'.
        """
        for data in data_list:
            try:
                self.cursor.execute("""
                    INSERT OR REPLACE INTO workrave_data (date, usage, breaks)
                    VALUES (?, ?, ?)
                """, (data.get("date"), data.get("usage"), data.get("breaks")))
            except sqlite3.Error as e:
                print(f"SQLite error during insertion: {e}")
        self.conn.commit()

    def fetch_all(self) -> List[Tuple[Any, ...]]:
        """
        Fetches all rows from the workrave_data table.

        Returns:
            List[Tuple[Any, ...]]: A list of tuples, where each tuple represents a row.
        """
        try:
            self.cursor.execute("SELECT * FROM workrave_data")
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            raise DatabaseOperationError(f"Error fetching data: {e}") from e

    def close(self):
        """Closes the connection to the SQLite database."""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
