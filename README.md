# CoinTracker-proto

## Overview
CoinTracker-proto is a Python Flask application and CLI for tracking Bitcoin addresses, balances, and transactions. It uses SQLite for persistence and integrates with Blockchain.com APIs.

## Features
- Add, remove, and list Bitcoin addresses
- Fetch balances and transactions for tracked addresses
- CLI with color output and paging
- SQLite database for local storage
- Unit and integration tests

## Setup
1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd CoinTracker-proto
   ```
2. **Create a virtual environment and install dependencies:**
   ```sh
   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```
3. **Set environment variables (optional):**
   - `COINTRACKER_API_URL`: Override the default API URL for the CLI.
   - `DATABASE_URL`: Set a custom database URI (if needed).


4. **Initialize the database:**
   ```sh
   python init_db.py
   ```

5. **Run the Flask server:**
   ```sh
   flask run
   ```

6. **Run the CLI:**
   ```sh
   python cli.py
   ```

## Testing

### Run all unit tests
```sh
python -m unittest discover tests
```

### Run a specific unit test file
```sh
python -m unittest tests/test_address_api_unit.py
```

### Example: Run all tests and see results
```sh
python -m unittest discover -v
```
