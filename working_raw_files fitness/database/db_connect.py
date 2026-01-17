import sqlite3
from utils.path_utils import get_db_path
import threading

# Thread-local storage for database connections
_thread_local = threading.local()

def connect_db():
    """Create or reuse a thread-local database connection."""
    if not hasattr(_thread_local, 'conn') or _thread_local.conn is None:
        db_path = get_db_path()
        conn = sqlite3.connect(db_path, check_same_thread=False, timeout=30.0)
        conn.execute('PRAGMA journal_mode=WAL')  # Better concurrency
        conn.execute('PRAGMA synchronous=NORMAL')  # Faster writes
        conn.execute('PRAGMA cache_size=10000')  # Better cache
        conn.execute('PRAGMA temp_store=MEMORY')  # Use memory for temp tables
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                start_date TEXT,
                end_date TEXT,
                fees TEXT NOT NULL,
                address TEXT,
                pincode TEXT
            )
        ''')
        
        # Create indexes for better query performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON members(name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_phone ON members(phone)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_end_date ON members(end_date)')
        
        conn.commit()
        _thread_local.conn = conn
    
    return _thread_local.conn

def close_db():
    """Close the thread-local database connection."""
    if hasattr(_thread_local, 'conn') and _thread_local.conn is not None:
        _thread_local.conn.close()
        _thread_local.conn = None
