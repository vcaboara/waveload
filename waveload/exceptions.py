# waveload/exceptions.py

class ParsingError(Exception):
    """Custom exception for errors during data parsing."""
    pass

class DatabaseConnectionError(Exception):
    """Custom exception for errors during database connection."""
    pass

class DatabaseOperationError(Exception):
    """Custom exception for errors during database operations."""
    pass

