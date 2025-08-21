# CoinTracker-proto
#
# Assumptions
- Only valid Bitcoin addresses (legacy, segwit, bech32) are accepted and validated using regex.
- The application is intended for local or small team use, not for production-scale deployment.
- SQLite is used for simplicity; for production, a more robust DB is recommended.
- Blockchain.com public APIs are used for BTC data; API rate limits and availability are assumed sufficient for demo/testing.
- No authentication is implemented; all API endpoints are open by default.

# Architecture Decisions
- **Separation of Concerns:** Flask app is modularized with blueprints for address and BTC data routes, and a CLI for user interaction.
- **Persistence:** SQLAlchemy ORM abstracts the database layer, making it easy to swap SQLite for another DB.
- **API Integration:** All external Bitcoin data is fetched via a dedicated integration module, making it easy to swap providers.
- **Testing:** Unit tests mock all DB and network actions for fast, reliable test runs. Integration tests are separated.
- **Configuration:** Sensitive settings (API URLs, DB URIs) are managed via environment variables for security and flexibility.
- **CLI/UX:** The CLI is colorized, supports paging, and is robust to network/API errors, providing a user-friendly experience.

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

## Further Improvements
- Implement rate limiting and logging for better security and monitoring.
- Improve input validation and error handling throughout the stack.
- Add Docker support for easier deployment and environment consistency.
- Integrate with a production-ready database (e.g., PostgreSQL) for scalability.
- Add a web-based dashboard for visualization and management.
- Expand test coverage, including more edge cases and integration tests.
- Use async requests for better performance on high-latency operations.