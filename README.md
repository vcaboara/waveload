# waveload

A Python library to load Workrave historystats text data into various databases.

## Installation

To install waveload, first ensure you have Python 3.12 or higher installed. Then, you can install it using pip:

```
pip install waveload
```

## Usage

```
from waveload.loader import HistorystatsLoader

# Configuration for SQLite (example)
db_config = {"database": "workrave.db"}
loader = HistorystatsLoader("sqlite", db_config)

try:
    loader.load_from_file("path/to/your/historystats.txt")
    print("Workrave data loaded successfully into SQLite.")
except FileNotFoundError as e:
    print(f"Error: {e}")
except ValueError as e:
    print(f"Error: {e}")
finally:
    if hasattr(loader, 'adapter') and hasattr(loader.adapter, 'close'):
        loader.adapter.close()
```

## Supported Databases

  - SQLite (initially)
  - (More to come...)

## Contributing

Contributions are welcome! 

Generated with Gemini 2.0 Flash

