import json
import os
import streamlit as st

data_file = 'library.txt'

def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file, indent=4)

# 🎀 Streamlit UI Settings
st.set_page_config(page_title="📚 My Cute Library", page_icon="💖", layout="centered")

# 💫 Custom Header
st.markdown("""
    <h1 style='text-align: center; color: #FF69B4;'>💖 My Personal Library Manager 💖</h1>
    <p style='text-align: center; font-size: 18px; color: #8B008B;'>Organize your books with love & style 📚✨</p>
""", unsafe_allow_html=True)

library = load_library()

# 📌 Navigation
menu = st.sidebar.radio("🌸 Menu", [
    "Add a Book", "Remove a Book", "Search Books", "Display All", "Statistics"
])

# ➕ Add Book
if menu == "Add a Book":
    st.header("➕ Add a New Book")
    with st.form("book_form"):
        title = st.text_input("📖 Title")
        author = st.text_input("🖋️ Author")
        year = st.text_input("📅 Year")
        genre = st.text_input("🎀 Genre")
        read = st.checkbox("✅ I have read it")
        submitted = st.form_submit_button("💾 Add Book")

        if submitted and title and author:
            library.append({
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read
            })
            save_library(library)
            st.success(f'🌟 Book **"{title}"** added successfully!')

# ❌ Remove Book
elif menu == "Remove a Book":
    st.header("❌ Remove a Book")
    titles = [book['title'] for book in library]
    selected = st.selectbox("Choose a book to remove:", titles)

    if st.button("🗑️ Delete"):
        library = [book for book in library if book['title'] != selected]
        save_library(library)
        st.success(f'🚫 Book **"{selected}"** removed.')

# 🔍 Search
elif menu == "Search Books":
    st.header("🔍 Search Books")
    search_by = st.radio("Search by", ["title", "author"])
    query = st.text_input(f"Enter {search_by.title()}")

    if query:
        results = [book for book in library if query.lower() in book[search_by].lower()]
        if results:
            for book in results:
                st.markdown(f"""
                💗 **{book['title']}**  
                *by* **{book['author']}** ({book['year']})  
                _Genre:_ {book['genre']}  
                _Status:_ {"✅ Read" if book['read'] else "📖 Unread"}
                ---
                """)
        else:
            st.warning("No matching books found.")

# 📚 Display All
elif menu == "Display All":
    st.header("📚 All Books in Your Library")
    if library:
        for book in library:
            st.markdown(f"""
            💕 **{book['title']}** by *{book['author']}*  
            🗓️ {book['year']} | 🎀 {book['genre']} | {'✅ Read' if book['read'] else '📖 Unread'}
            ---
            """)
    else:
        st.info("No books yet! Add your first one 💗")

# 📊 Stats
elif menu == "Statistics":
    st.header("📊 Your Reading Stats")
    total = len(library)
    read_books = len([b for b in library if b['read']])
    percent = (read_books / total) * 100 if total > 0 else 0

    st.metric("📚 Total Books", total)
    st.metric("✅ Books Read", read_books)
    st.metric("📈 Read Percentage", f"{percent:.2f}%")
