from flask import Flask, jsonify, request, send_from_directory
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'library.db'

app = Flask(__name__, static_folder='.', static_url_path='')


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            issued INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )
    conn.commit()
    conn.close()


@app.route('/')
def serve_index():
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})


@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT id, title, author, issued, created_at FROM books ORDER BY id DESC').fetchall()
    conn.close()
    return jsonify([dict(book) for book in books])


@app.route('/books', methods=['POST'])
def add_book():
    payload = request.get_json(silent=True) or {}
    title = str(payload.get('title', '')).strip()
    author = str(payload.get('author', '')).strip()

    if not title or not author:
        return jsonify({'error': 'Both title and author are required.'}), 400

    conn = get_db_connection()
    cursor = conn.execute(
        'INSERT INTO books (title, author, issued) VALUES (?, ?, 0)',
        (title, author),
    )
    conn.commit()
    book_id = cursor.lastrowid
    book = conn.execute('SELECT id, title, author, issued, created_at FROM books WHERE id = ?', (book_id,)).fetchone()
    conn.close()
    return jsonify({'message': 'Book added successfully', 'book': dict(book)}), 201


@app.route('/books/<int:book_id>/issue', methods=['POST'])
def issue_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT id, issued FROM books WHERE id = ?', (book_id,)).fetchone()
    if book is None:
        conn.close()
        return jsonify({'error': 'Book not found.'}), 404
    if book['issued'] == 1:
        conn.close()
        return jsonify({'error': 'Book is already issued.'}), 400

    conn.execute('UPDATE books SET issued = 1 WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book issued successfully'}), 200


@app.route('/books/<int:book_id>/return', methods=['POST'])
def return_book(book_id):
    conn = get_db_connection()
    book = conn.execute('SELECT id, issued FROM books WHERE id = ?', (book_id,)).fetchone()
    if book is None:
        conn.close()
        return jsonify({'error': 'Book not found.'}), 404
    if book['issued'] == 0:
        conn.close()
        return jsonify({'error': 'Book is already available.'}), 400

    conn.execute('UPDATE books SET issued = 0 WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Book returned successfully'}), 200


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Book not found.'}), 404

    return jsonify({'message': 'Book deleted successfully'}), 200


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
