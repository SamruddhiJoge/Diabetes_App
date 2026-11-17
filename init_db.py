import sqlite3
from werkzeug.security import generate_password_hash

def init_db():
    # Connect to SQLite (this creates the file if it doesn't exist)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Check if the admin user already exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        # Hash the password securely before storing it
        hashed_password = generate_password_hash('admin123')
        
        # Insert the new user
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", 
            ('admin', hashed_password)
        )
        conn.commit()
        print("Database initialized. User 'admin' created with password 'admin123'.")
    else:
        print("Database already initialized. Admin user exists.")

    conn.close()

if __name__ == '__main__':
    init_db()