# waveload/exceptions.py
"""Custom exceptions for the waveload application."""

class ParsingError(Exception):
    """Custom exception for errors during data parsing."""

class DatabaseConnectionError(Exception):
    """Custom exception for errors during database connection."""

class DatabaseOperationError(Exception):
    """Custom exception for errors during database operations."""
