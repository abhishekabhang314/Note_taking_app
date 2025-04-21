import bcrypt
from db import users, notes
from bson.objectid import ObjectId

def register():
    email = input("Enter email: ")
    password = input("Enter password: ").encode('utf-8')
    if users.find_one({'email': email}):
        print("User already exists.")
        return
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    users.insert_one({'email': email, 'password': hashed})
    print("Registration successful!")

def login():
    email = input("Email: ")
    password = input("Password: ").encode('utf-8')
    user = users.find_one({'email': email})
    if user and bcrypt.checkpw(password, user['password']):
        print("Login successful!")
        return str(user['_id'])
    else:
        print("Invalid credentials")
        return None

def add_note(user_id):
    title = input("Note Title: ")
    content = input("Note Content: ")
    notes.insert_one({'title': title, 'content': content, 'user_id': user_id})
    print("Note added!")

def view_notes(user_id):
    print("\nYour Notes:")
    for note in notes.find({'user_id': user_id}):
        print(f"- {note['_id']}: {note['title']}")

def delete_note(user_id):
    view_notes(user_id)
    note_id = input("Enter note ID to delete: ")
    result = notes.delete_one({'_id': ObjectId(note_id), 'user_id': user_id})
    print("Deleted!" if result.deleted_count else "Note not found.")

def main():
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Choose: ")
        if choice == "1":
            register()
        elif choice == "2":
            user_id = login()
            if user_id:
                while True:
                    print("\n1. Add Note\n2. View Notes\n3. Delete Note\n4. Logout")
                    sub = input("Choose: ")
                    if sub == "1":
                        add_note(user_id)
                    elif sub == "2":
                        view_notes(user_id)
                    elif sub == "3":
                        delete_note(user_id)
                    elif sub == "4":
                        break
        elif choice == "3":
            break

if __name__ == "__main__":
    main()
