import sqlite3
from database.db_connect import connect_db
import hashlib

def init_credentials_table():
    """Initialize the credentials table if it doesn't exist."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS admin_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Check if default admin exists
        cursor.execute("SELECT COUNT(*) FROM admin_credentials WHERE username = ?", ("admin",))
        if cursor.fetchone()[0] == 0:
            # Create default admin with hashed password
            default_password = "admin123"
            password_hash = hashlib.sha256(default_password.encode()).hexdigest()
            cursor.execute(
                "INSERT INTO admin_credentials (username, password_hash) VALUES (?, ?)",
                ("admin", password_hash)
            )
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error initializing credentials: {e}")
        return False

def hash_password(password):
    """Hash a password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_credentials(username, password):
    """Verify username and password."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        cursor.execute(
            "SELECT id FROM admin_credentials WHERE username = ? AND password_hash = ?",
            (username, password_hash)
        )
        
        result = cursor.fetchone()
        return result is not None
    except Exception as e:
        print(f"Error verifying credentials: {e}")
        return False

def update_credentials(old_username, old_password, new_username, new_password):
    """Update username and/or password."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Verify old credentials first
        old_password_hash = hash_password(old_password)
        cursor.execute(
            "SELECT id FROM admin_credentials WHERE username = ? AND password_hash = ?",
            (old_username, old_password_hash)
        )
        
        if cursor.fetchone() is None:
            return False, "Invalid current credentials"
        
        # Update credentials
        new_password_hash = hash_password(new_password)
        cursor.execute(
            "UPDATE admin_credentials SET username = ?, password_hash = ?, updated_at = CURRENT_TIMESTAMP WHERE username = ?",
            (new_username, new_password_hash, old_username)
        )
        
        conn.commit()
        return True, "Credentials updated successfully"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
    except Exception as e:
        print(f"Error updating credentials: {e}")
        return False, f"Error: {str(e)}"

def reset_to_default():
    """Reset credentials to default (for recovery)."""
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Set to default: username=admin, password=admin123
        default_password_hash = hash_password("admin123")
        cursor.execute("DELETE FROM admin_credentials")
        cursor.execute(
            "INSERT INTO admin_credentials (username, password_hash) VALUES (?, ?)",
            ("admin", default_password_hash)
        )
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error resetting credentials: {e}")
        return False
