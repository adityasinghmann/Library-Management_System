# Python Backend for Library Management System

This backend uses **Flask + SQLite** and serves both API endpoints and the frontend UI.

## Setup

```bash
pip install -r requirements.txt
python init_db.py
python app.py
```

Server runs at `http://127.0.0.1:5000`.

## Endpoints

- `GET /health` - health check
- `GET /books` - list books
- `POST /books` - add a book (`{ "title": "...", "author": "..." }`)
- `POST /books/<id>/issue` - issue a book
- `POST /books/<id>/return` - return a book
- `DELETE /books/<id>` - delete a book

## Notes

- Database file: `library.db`
- Table initialization is automatic on app startup; `init_db.py` is included for manual initialization.
