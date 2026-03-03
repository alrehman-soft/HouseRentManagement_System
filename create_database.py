
import sqlite3
import os, shutil
import sys
import string
from datetime import datetime
from tkinter import messagebox

def get_available_drives():
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives

def get_best_drive_for_data():
    available_drives = get_available_drives()
    
    # First try to find a non-system drive
    for drive in available_drives:
        if drive.upper() != "C:\\":
            return drive
    return None

def get_database_path():
    data_folder = os.path.join(os.path.abspath("."), "HouseRentData")
    os.makedirs(data_folder, exist_ok=True)
    return os.path.join(data_folder, "house_rent_management.db")

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

DATABASE_NAME = get_database_path()

def ensure_db_directory():
    """Ensure that the database directory exists, create if not"""
    db_dir = os.path.dirname(DATABASE_NAME)
    if not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir)
            print(f"Created directory: {db_dir}")
        except Exception as e:
            print(f"❌ Could not create directory: {e}")

def get_connection():
    # ensure_db_directory()
    conn = sqlite3.connect(DATABASE_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def get_login_connection():
    """Get database connection for login operations"""
    # ensure_db_directory()
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def initialize_database():
    backup_database()
    """Create all necessary tables if they don't exist"""
    conn = get_connection()
    c = conn.cursor()

    try:
        # Tenants Table
        c.execute('''CREATE TABLE IF NOT EXISTS tenants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            father_name TEXT,
            cnic TEXT UNIQUE,
            phone TEXT NOT NULL,
            emergency_contact TEXT,
            profession TEXT,
            building_name TEXT,
            floor INTEGER NOT NULL,
            flat_no INTEGER NOT NULL,
            entry_date TEXT,
            exit_date TEXT,
            status TEXT DEFAULT 'Active' CHECK (status IN ('Active', 'Vacated')),
            owner_name TEXT,
            owner_phone TEXT,
            rent_amount REAL NOT NULL DEFAULT 0,
            security_deposit REAL DEFAULT 0,
            advance_amount REAL DEFAULT 0,
            photo_path TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        try:
            c.execute("ALTER TABLE tenants ADD COLUMN notes TEXT DEFAULT ''")
        except:
            pass

        # Witness Table
        c.execute('''CREATE TABLE IF NOT EXISTS witnesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id INTEGER NOT NULL,
            w1_name TEXT NOT NULL,
            w1_cnic TEXT,
            w1_phone TEXT,
            w2_name TEXT NOT NULL,
            w2_cnic TEXT,
            w2_phone TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE,
            UNIQUE(tenant_id)
        )''')

        # Payments Table
        c.execute('''CREATE TABLE IF NOT EXISTS payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id INTEGER NOT NULL,
            month_year TEXT NOT NULL,
            rent_amount REAL DEFAULT 0,
            gas_bill REAL DEFAULT 0,
            water_bill REAL DEFAULT 0,
            electricity_bill REAL DEFAULT 0,
            total_amount REAL DEFAULT 0,
            paid_amount REAL DEFAULT 0,
            balance_amount REAL DEFAULT 0,
            payment_date TEXT,
            status TEXT DEFAULT 'Pending',
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE
        )''')
        try:
            c.execute("ALTER TABLE payments ADD COLUMN collection_id INTEGER")
        except:
            pass

        # Rent Collectors Table
        c.execute('''CREATE TABLE IF NOT EXISTS rent_collectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            building_name TEXT NOT NULL,
            rent_collector_name TEXT NOT NULL,
            father_name TEXT NOT NULL,
            cnic TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            reporting_to TEXT,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')

        # Users Table
        c.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            phone TEXT,
            role TEXT DEFAULT 'user',
            created_date TEXT,
            last_login TEXT,
            reset_token TEXT,
            reset_token_expiry TEXT
        )''')

        # Building Payment Collection Table
        c.execute("""
        CREATE TABLE IF NOT EXISTS building_collections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            building_name TEXT NOT NULL,
            collector_name TEXT,
            collection_date TEXT,
            total_collected REAL NOT NULL,
            remaining_amount REAL NOT NULL,
            invest_to TEXT,
            status TEXT DEFAULT 'Open'
        )
        """)

        conn.commit()
        print(f"Database initialized at: {DATABASE_NAME}")

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        conn.rollback()
    finally:
        conn.close()

def add_default_users():
    """Add default users"""
    conn = get_login_connection()
    c = conn.cursor()
    
    # Check if any user exists
    c.execute("SELECT COUNT(*) FROM users")
    count = c.fetchone()[0]
    
    if count == 0:
        # Default admin user
        c.execute('''INSERT INTO users 
                    (username, email, password, full_name, phone, role, created_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    ('admin', 'admin@example.com', 'admin123', 'Administrator', 
                     '03001234567', 'admin', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        # Default normal user
        c.execute('''INSERT INTO users 
                    (username, email, password, full_name, phone, role, created_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                    ('user', 'user@example.com', 'user123', 'Normal User', 
                     '03007654321', 'user', datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        conn.commit()    
    conn.close()

def get_tenant_by_cnic(cnic):
    #Get tenant details by CNIC number
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM tenants WHERE cnic=?", (cnic,))
    result = c.fetchone()
    conn.close()
    return result

def get_counts():
    conn = get_connection()
    c = conn.cursor()

    # Active tenants count
    c.execute("SELECT COUNT(*) FROM tenants WHERE status='Active'")
    active_tenants = c.fetchone()[0] or 0
    
    # Vacated tenants count
    c.execute("SELECT COUNT(*) FROM tenants WHERE status='Vacated'")
    vacated = c.fetchone()[0] or 0
    
    # Total unique flats from tenants table
    c.execute("SELECT COUNT(DISTINCT flat_no) FROM tenants")
    total_flats = c.fetchone()[0] or 0
    
    # Occupied units
    occupied = active_tenants
    
    # Vacant units
    vacant = max(0, total_flats - occupied)
    
    conn.close()
    return total_flats, occupied, vacant, active_tenants

def display_database_info():
    """Display complete database information"""
    conn = get_connection()
    c = conn.cursor()
    
    # Get list of all tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    
    print("\n" + "="*60)
    print("DATABASE INFORMATION")
    print("="*60)
    print(f"Location: {DATABASE_NAME}")
    print(f"Total Tables: {len(tables)}")
    print("-"*60)
    
    # Display each table
    for table in tables:
        table_name = table[0]
        c.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = c.fetchone()[0]
        print(f"  {table_name}: {count} records")
    
    # Show drive information
    print("-"*60)
    db_drive = os.path.splitdrive(DATABASE_NAME)[0]
    if db_drive:
        free_space = get_free_space(db_drive)
        if free_space:
            print(f"Drive: {db_drive} (Free: {free_space:.2f} GB)")
    
    print("="*60)
    conn.close()

def get_free_space(drive):
    # Get free space
    try:
        if os.name == 'nt':
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(drive), None, None, ctypes.pointer(free_bytes))
            return free_bytes.value / (1024**3)
    except:
        pass
    return None

def backup_database():
    backup_dir = os.path.join(os.path.dirname(DATABASE_NAME), "backups")
    os.makedirs(backup_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"backup_{timestamp}.db")

    if os.path.exists(DATABASE_NAME):
        shutil.copy2(DATABASE_NAME, backup_file)

if __name__ == "__main__":
    # Initialize database
    initialize_database()
    add_default_users()
    backup_database()
    
    # Inform user
    if os.path.exists(DATABASE_NAME):
        messagebox.showinfo(
            "House Rent Management",
            f"Database is ready and located at:\n{DATABASE_NAME}\n\nOld data is safe. Automatic backup created."
        )
