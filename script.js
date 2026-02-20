const bookForm = document.getElementById('bookForm');
const bookList = document.getElementById('bookList');
const feedback = document.getElementById('feedback');
const refreshBtn = document.getElementById('refreshBtn');

function setFeedback(message, type = 'success') {
    feedback.textContent = message;
    feedback.className = type;
}

async function apiRequest(path, options = {}) {
    const response = await fetch(path, {
        headers: { 'Content-Type': 'application/json' },
        ...options,
    });

    const contentType = response.headers.get('content-type') || '';
    const data = contentType.includes('application/json') ? await response.json() : {};

    if (!response.ok) {
        throw new Error(data.error || 'Request failed.');
    }

    return data;
}

function renderBooks(books) {
    if (!books.length) {
        bookList.innerHTML = '<p>No books in the library yet.</p>';
        return;
    }

    bookList.innerHTML = books
        .map(
            (book) => `
            <article class="book-item">
                <div class="book-meta">
                    <strong>${book.title}</strong> by ${book.author}
                    <span class="badge ${book.issued ? 'issued' : 'available'}">
                        ${book.issued ? 'Issued' : 'Available'}
                    </span>
                </div>
                <div class="actions">
                    <button data-action="${book.issued ? 'return' : 'issue'}" data-id="${book.id}">
                        ${book.issued ? 'Return' : 'Issue'}
                    </button>
                    <button class="danger" data-action="delete" data-id="${book.id}">Delete</button>
                </div>
            </article>
        `,
        )
        .join('');
}

async function loadBooks() {
    try {
        const books = await apiRequest('/books');
        renderBooks(books);
    } catch (error) {
        setFeedback(error.message, 'error');
    }
}

bookForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const title = document.getElementById('title').value.trim();
    const author = document.getElementById('author').value.trim();

    if (!title || !author) {
        setFeedback('Title and author are required.', 'error');
        return;
    }

    try {
        await apiRequest('/books', {
            method: 'POST',
            body: JSON.stringify({ title, author }),
        });
        setFeedback('Book added successfully.', 'success');
        bookForm.reset();
        loadBooks();
    } catch (error) {
        setFeedback(error.message, 'error');
    }
});

refreshBtn.addEventListener('click', loadBooks);

bookList.addEventListener('click', async (event) => {
    const button = event.target.closest('button[data-action]');
    if (!button) {
        return;
    }

    const { action, id } = button.dataset;

    try {
        if (action === 'issue') {
            await apiRequest(`/books/${id}/issue`, { method: 'POST' });
            setFeedback('Book issued successfully.', 'success');
        } else if (action === 'return') {
            await apiRequest(`/books/${id}/return`, { method: 'POST' });
            setFeedback('Book returned successfully.', 'success');
        } else if (action === 'delete') {
            await apiRequest(`/books/${id}`, { method: 'DELETE' });
            setFeedback('Book deleted successfully.', 'success');
        }

        loadBooks();
    } catch (error) {
        setFeedback(error.message, 'error');
    }
});

loadBooks();
