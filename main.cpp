#include <iostream>
#include <vector>
#include <string>
using namespace std;

struct Book {
    int id;
    string title;
    string author;
    bool issued = false;
};

vector<Book> library;

void addBook() {
    Book book;
    cout << "Enter Book ID: "; cin >> book.id;
    cin.ignore();
    cout << "Enter Title: "; getline(cin, book.title);
    cout << "Enter Author: "; getline(cin, book.author);
    library.push_back(book);
    cout << "Book added successfully!\n";
}

void issueBook() {
    int id;
    cout << "Enter Book ID to issue: "; cin >> id;
    for (auto& book : library) {
        if (book.id == id && !book.issued) {
            book.issued = true;
            cout << "Book issued!\n";
            return;
        }
    }
    cout << "Book not found or already issued.\n";
}

void returnBook() {
    int id;
    cout << "Enter Book ID to return: "; cin >> id;
    for (auto& book : library) {
        if (book.id == id && book.issued) {
            book.issued = false;
            cout << "Book returned!\n";
            return;
        }
    }
    cout << "Invalid ID or book wasn't issued.\n";
}

void showBooks() {
    for (const auto& book : library) {
        cout << "ID: " << book.id << ", Title: " << book.title
             << ", Author: " << book.author << ", Issued: "
             << (book.issued ? "Yes" : "No") << endl;
    }
}

int main() {
    int choice;
    do {
        cout << "\n--- Library Menu ---\n";
        cout << "1. Add Book\n2. Issue Book\n3. Return Book\n4. Show All Books\n5. Exit\nChoice: ";
        cin >> choice;
        switch (choice) {
            case 1: addBook(); break;
            case 2: issueBook(); break;
            case 3: returnBook(); break;
            case 4: showBooks(); break;
            case 5: cout << "Exiting...\n"; break;
            default: cout << "Invalid option.\n";
        }
    } while (choice != 5);
    return 0;
}