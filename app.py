from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return jsonify([dict(book) for book in books])

@app.route('/books', methods=['POST'])
def add_book():
    new_book = request.get_json()
    title = new_book['title']
    author = new_book['author']
    conn = get_db_connection()
    conn.execute('INSERT INTO books (title, author, issued) VALUES (?, ?, ?)', (title, author, False))
    conn.commit()
    conn.close()
    return {'message': 'Book added successfully'}, 201

@app.route('/books/<int:id>/issue', methods=['POST'])
def issue_book(id):
    conn = get_db_connection()
    conn.execute('UPDATE books SET issued = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return {'message': 'Book issued successfully'}, 200

@app.route('/books/<int:id>/return', methods=['POST'])
def return_book(id):
    conn = get_db_connection()
    conn.execute('UPDATE books SET issued = 0 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return {'message': 'Book returned successfully'}, 200

if __name__ == '__main__':
    app.run(debug=True)