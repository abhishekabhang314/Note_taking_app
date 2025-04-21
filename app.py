import streamlit as st
import bcrypt
from db import users, notes
from bson.objectid import ObjectId


st.set_page_config(
    page_title="Notes App",
    page_icon="📝",
)

# --- Session State ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# --- Registration ---
def register():
    st.subheader("Register")
    email = st.text_input("Email", key="reg_email")
    password = st.text_input("Password", type="password", key="reg_password")
    if st.button("Register"):
        if users.find_one({'email': email}):
            st.error("User already exists.")
        else:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'email': email, 'password': hashed})
            st.success("Registered successfully! Please log in.")

# --- Login ---
def login():
    st.subheader("Login")
    email = st.text_input("Email", key="log_email")
    password = st.text_input("Password", type="password", key="log_password")
    if st.button("Login"):
        user = users.find_one({'email': email})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            st.session_state.user_id = str(user['_id'])
            st.success("Logged in!")
        else:
            st.error("Invalid credentials")

# --- Add Note ---
def add_note():
    st.subheader("Add Note")
    title = st.text_input("Title")
    content = st.text_area("Content")
    if st.button("Save Note"):
        notes.insert_one({'title': title, 'content': content, 'user_id': st.session_state.user_id})
        st.success("Note added!")

# --- View Notes ---
def view_notes():
    st.subheader("Your Notes")
    user_notes = notes.find({'user_id': st.session_state.user_id})
    for note in user_notes:
        with st.expander(note['title']):
            st.write(note['content'])
            if st.button("Delete", key=str(note['_id'])):
                notes.delete_one({'_id': ObjectId(note['_id'])})
                st.success("Note deleted.")
                st.experimental_rerun()

# --- Logout ---
def logout():
    st.session_state.user_id = None
    st.success("Logged out!")

# --- Main App ---
st.title("📝 Personal Notes App")

if st.session_state.user_id:
    st.sidebar.success("Logged in")
    if st.sidebar.button("Logout"):
        logout()
    add_note()
    view_notes()
else:
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        login()
    with tab2:
        register()
