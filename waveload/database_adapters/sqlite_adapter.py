# waveload/database_adapters/sqlite_adapter.py
import sqlite3

class SQLiteAdapter:
    def __init__(self, config):
        self.database_path = config.get("database")
        if not self.database_path:
            raise ValueError("SQLite configuration requires 'database' path.")
        self._connect()
        self._create_table_if_not_exists()

    def _connect(self):
        self.conn = sqlite3.connect(self.database_path)
        self.cursor = self.conn.cursor()

    def _create_table_if_not_exists(self):
        # Define your table schema based on the data you'll extract
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS workrave_data (
                date TEXT PRIMARY KEY,
                usage TEXT,
                breaks TEXT
                -- Add other columns as needed
            )
        """)
        self.conn.commit()

    def insert_data(self, data_list):
        for data in data_list:
            try:
                self.cursor.execute("""
                    INSERT OR REPLACE INTO workrave_data (date, usage, breaks)
                    VALUES (?, ?, ?)
                """, (data.get("date"), data.get("usage"), data.get("breaks")))
            except sqlite3.Error as e:
                print(f"SQLite error during insertion: {e}")
        self.conn.commit()

    def fetch_all(self):
        self.cursor.execute("SELECT * FROM workrave_data")
        return self.cursor.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()
