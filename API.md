# CoinTracker-proto API Documentation

## Base URL
`http://127.0.0.1:5000`

## Endpoints

### Health
- `GET /health`
  - Returns: `hello world`

### Address Management
- `POST /addresses`
  - Body: `{ "address": "<bitcoin_address>" }`
  - Response: 201 Created `{ "address": "..." }` or 400/409 error

- `DELETE /addresses/<address>`
  - Response: 200 OK `{ "message": "Address removed" }` or 404 error

- `GET /addresses`
  - Response: 200 OK `[ { "address": "..." }, ... ]`

### Bitcoin Data
- `GET /addresses/<address>/balance`
  - Response: 200 OK `{ "address": "...", "balance": <satoshis> }` or 404/500 error

- `GET /addresses/<address>/transactions?limit=20&offset=0`
  - Query Params:
    - `limit` (default 20, max 50)
    - `offset` (default 0)
  - Response: 200 OK
    ```json
    {
      "address": "...",
      "transactions": [ { ... }, ... ],
      "total": <int>,
      "offset": <int>,
      "limit": <int>
    }
    ```
  - Errors: 404/500

## Error Responses
All errors return JSON: `{ "error": "..." }`
