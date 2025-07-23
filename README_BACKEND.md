# Python Backend for Library Management System

This is a basic Flask backend API for the Library Management System.

## 🔧 Endpoints

- `GET /books` - List all books
- `POST /books` - Add a new book (JSON: `{ "title": "...", "author": "..." }`)
- `POST /books/<id>/issue` - Mark a book as issued
- `POST /books/<id>/return` - Mark a book as returned

## 🚀 How to Run

```bash
pip install -r requirements.txt
python init_db.py
python app.py
```

The backend will run on `http://127.0.0.1:5000/`.

You can use Postman or connect the frontend via `fetch()` in JS.