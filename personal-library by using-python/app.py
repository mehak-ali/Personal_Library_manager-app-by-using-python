import streamlit as st
import json
import os

# ----- File Setup -----
DATA_FILE = 'library.json'
DELETED_FILE = 'deleted_books.json'

def load_data(file):
    if os.path.exists(file):
        with open(file, 'r') as f:
            return json.load(f)
    return []

def save_data(data, file):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

# Load library data
library = load_data(DATA_FILE)
deleted_books = load_data(DELETED_FILE)

# ----- Sidebar -----
st.sidebar.title("📚 Personal Library Manager")
option = st.sidebar.radio("Choose an action:", ("Add Book", "View Library", "Search Book", "Delete Book", "View Deleted Books"))

# ----- Add Book -----
if option == "Add Book":
    st.header("📖 Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    status = st.selectbox("Status", ["To Read", "Reading", "Completed"])

    if st.button("Add Book"):
        if title and author:
            new_book = {"title": title, "author": author, "genre": genre, "status": status}
            library.append(new_book)
            save_data(library, DATA_FILE)
            st.success("Book added successfully!")
        else:
            st.error("Title and Author are required!")

# ----- View Library -----
elif option == "View Library":
    st.header("📚 Your Library")
    if library:
        st.dataframe(library)
    else:
        st.info("No books in your library yet.")

# ----- Search Book -----
elif option == "Search Book":
    st.header("🔍 Search Your Library")
    search_term = st.text_input("Enter title or author to search:")
    if search_term:
        results = [book for book in library if search_term.lower() in book['title'].lower() or search_term.lower() in book['author'].lower()]
        st.write(f"Found {len(results)} result(s):")
        st.dataframe(results)

# ----- Delete Book -----
elif option == "Delete Book":
    st.header("🗑️ Delete a Book")
    titles = [book['title'] for book in library]
    if titles:
        to_delete = st.selectbox("Select book to delete:", titles)
        if st.button("Delete"):
            book_to_remove = [book for book in library if book['title'] == to_delete]
            if book_to_remove:
                deleted_books.extend(book_to_remove)
                library = [book for book in library if book['title'] != to_delete]
                save_data(library, DATA_FILE)
                save_data(deleted_books, DELETED_FILE)
                st.success(f"Deleted '{to_delete}' from your library and recorded it in deleted books.")
    else:
        st.info("No books to delete.")

# ----- View Deleted Books -----
elif option == "View Deleted Books":
    st.header("🗃️ Deleted Books Record")
    if deleted_books:
        st.dataframe(deleted_books)
    else:
        st.info("No books have been deleted yet.")
