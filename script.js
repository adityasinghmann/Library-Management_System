document.getElementById('bookForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const title = document.getElementById('title').value;
    const author = document.getElementById('author').value;
    const bookDiv = document.createElement('div');
    bookDiv.textContent = `📘 ${title} by ${author}`;
    document.getElementById('bookList').appendChild(bookDiv);
    this.reset();
});