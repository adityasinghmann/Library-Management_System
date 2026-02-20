# Library Management System

A complete, runnable Library Management System with:

- **Flask + SQLite backend API**
- **HTML/CSS/JavaScript frontend** served by Flask
- **C++ CLI program** for basic in-memory library operations

## Features

### Web app
- Add books
- View all books
- Issue / return books
- Delete books
- Simple status feedback for every operation

### Backend API
- `GET /health`
- `GET /books`
- `POST /books`
- `POST /books/<id>/issue`
- `POST /books/<id>/return`
- `DELETE /books/<id>`

### CLI app (C++)
- Add, issue, return, and view books in terminal mode

---

## Quick Start (Web App)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python init_db.py
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

---

## Run C++ CLI version

```bash
g++ main.cpp -o library
./library
```

---

## Optional SQL schema

`schema.sql` is included for MySQL users who want to create a similar table structure.
