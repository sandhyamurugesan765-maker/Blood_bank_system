import sqlite3
import hashlib
from datetime import datetime, timedelta
import random
import os

def hash_password(password):
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def calculate_expiry_date(donation_date_str):
    """Calculate expiry date (42 days after donation)."""
    try:
        donation_date = datetime.strptime(donation_date_str, '%Y-%m-%d')
        expiry_date = donation_date + timedelta(days=42)
        return expiry_date.strftime('%Y-%m-%d')
    except Exception as e:
        # If there's an error, return a date 42 days from now
        return (datetime.now() + timedelta(days=42)).strftime('%Y-%m-%d')

def init_database():
    """Initialize the database with all tables and sample data."""
    
    # Remove existing database to start fresh
    if os.path.exists('bloodbank.db'):
        print("Removing existing database...")
        os.remove('bloodbank.db')
    
    conn = sqlite3.connect('bloodbank.db')
    cursor = conn.cursor()
    
    print("=" * 60)
    print("BLOOD BANK DATABASE SETUP")
    print("=" * 60)
    
    print("\n1. Creating tables...")
    
    # Create users table
    cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT NOT NULL,
        role TEXT DEFAULT 'staff',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create donors table
    cursor.execute('''
    CREATE TABLE donors (
        donor_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        date_of_birth DATE NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        city TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT,
        medical_details TEXT,
        eligible BOOLEAN DEFAULT 1,
        last_donation_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create blood inventory table
    cursor.execute('''
    CREATE TABLE inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        blood_group TEXT NOT NULL UNIQUE,
        units_available INTEGER DEFAULT 0,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'Normal'
    )
    ''')
    
    # Create donation history table
    cursor.execute('''
    CREATE TABLE donation_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        donation_id TEXT NOT NULL UNIQUE,
        donor_id TEXT NOT NULL,
        donor_name TEXT NOT NULL,
        blood_group TEXT NOT NULL,
        units_donated INTEGER NOT NULL,
        donation_date DATE NOT NULL,
        expiry_date DATE NOT NULL,
        received_by TEXT,
        test_result TEXT DEFAULT 'Passed',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    print("✓ Tables created successfully!")
    
    # Insert default users
    print("\n2. Creating default users...")
    users = [
        ('admin@bloodbank.com', hash_password('admin123'), 'System Administrator', 'admin'),
        ('staff@bloodbank.com', hash_password('staff123'), 'John Doe', 'staff'),
    ]
    
    cursor.executemany('''
        INSERT INTO users (email, password, name, role)
        VALUES (?, ?, ?, ?)
    ''', users)
    print("✓ Default users created!")
    print("   Admin: admin@bloodbank.com / admin123")
    print("   Staff: staff@bloodbank.com / staff123")
    
    # Insert default blood groups into inventory
    print("\n3. Initializing blood inventory...")
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    
    for bg in blood_groups:
        units = random.randint(5, 30)
        status = 'Low Stock' if units < 10 else 'Normal' if units < 20 else 'High Stock'
        
        cursor.execute('''
            INSERT INTO inventory (blood_group, units_available, status)
            VALUES (?, ?, ?)
        ''', (bg, units, status))
    
    print("✓ Blood inventory initialized!")
    
    # Insert sample donors
    print("\n4. Creating sample donors...")
    sample_donors = [
        {
            'donor_id': 'DON10001',
            'name': 'Michael Johnson',
            'date_of_birth': '1990-05-15',
            'age': 33,
            'gender': 'Male',
            'blood_group': 'O+',
            'city': 'New York',
            'phone': '555-0101',
            'email': 'michael@email.com',
            'medical_details': 'No medical issues',
            'eligible': 1,
            'last_donation_date': '2023-10-15'
        },
        {
            'donor_id': 'DON10002',
            'name': 'Sarah Williams',
            'date_of_birth': '1985-08-22',
            'age': 38,
            'gender': 'Female',
            'blood_group': 'A-',
            'city': 'Los Angeles',
            'phone': '555-0102',
            'email': 'sarah@email.com',
            'medical_details': 'Allergic to penicillin',
            'eligible': 1,
            'last_donation_date': '2023-09-20'
        },
        {
            'donor_id': 'DON10003',
            'name': 'David Brown',
            'date_of_birth': '1995-02-10',
            'age': 28,
            'gender': 'Male',
            'blood_group': 'B+',
            'city': 'Chicago',
            'phone': '555-0103',
            'email': 'david@email.com',
            'medical_details': 'Asthma controlled',
            'eligible': 1,
            'last_donation_date': '2023-11-05'
        },
        {
            'donor_id': 'DON10004',
            'name': 'Lisa Taylor',
            'date_of_birth': '1988-11-30',
            'age': 35,
            'gender': 'Female',
            'blood_group': 'AB-',
            'city': 'Houston',
            'phone': '555-0104',
            'email': 'lisa@email.com',
            'medical_details': 'No issues',
            'eligible': 1,
            'last_donation_date': '2023-08-10'
        },
        {
            'donor_id': 'DON10005',
            'name': 'James Wilson',
            'date_of_birth': '1992-07-18',
            'age': 31,
            'gender': 'Male',
            'blood_group': 'O-',
            'city': 'Phoenix',
            'phone': '555-0105',
            'email': 'james@email.com',
            'medical_details': 'Universal donor',
            'eligible': 1,
            'last_donation_date': '2023-12-01'
        },
        {
            'donor_id': 'DON10006',
            'name': 'Maria Garcia',
            'date_of_birth': '1998-04-25',
            'age': 25,
            'gender': 'Female',
            'blood_group': 'A+',
            'city': 'Philadelphia',
            'phone': '555-0106',
            'email': 'maria@email.com',
            'medical_details': 'No medical issues',
            'eligible': 1,
            'last_donation_date': None
        },
        {
            'donor_id': 'DON10007',
            'name': 'Robert Miller',
            'date_of_birth': '1975-12-05',
            'age': 48,
            'gender': 'Male',
            'blood_group': 'B-',
            'city': 'San Antonio',
            'phone': '555-0107',
            'email': 'robert@email.com',
            'medical_details': 'High blood pressure controlled',
            'eligible': 1,
            'last_donation_date': '2023-07-22'
        },
        {
            'donor_id': 'DON10008',
            'name': 'Jennifer Davis',
            'date_of_birth': '1982-09-14',
            'age': 41,
            'gender': 'Female',
            'blood_group': 'AB+',
            'city': 'San Diego',
            'phone': '555-0108',
            'email': 'jennifer@email.com',
            'medical_details': 'No issues',
            'eligible': 1,
            'last_donation_date': '2023-11-15'
        }
    ]
    
    # Insert donors into database
    for donor in sample_donors:
        cursor.execute('''
            INSERT INTO donors (donor_id, name, date_of_birth, age, gender, blood_group, city, phone, email, medical_details, eligible, last_donation_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            donor['donor_id'],
            donor['name'],
            donor['date_of_birth'],
            donor['age'],
            donor['gender'],
            donor['blood_group'],
            donor['city'],
            donor['phone'],
            donor['email'],
            donor['medical_details'],
            donor['eligible'],
            donor['last_donation_date']
        ))
    print("✓ Sample donors created!")
    
    # Insert sample donation history
    print("\n5. Creating sample donation history...")
    donations = []
    
    # Create some recent donations for the dashboard (matching your screenshot)
    recent_donations_data = [
        {
            'donor_id': 'DON10007',
            'donor_name': 'Robert Miller',
            'blood_group': 'B-',
            'donation_date': '2026-01-22',
            'units': 1
        },
        {
            'donor_id': 'DON10005',
            'donor_name': 'James Wilson',
            'blood_group': 'O-',
            'donation_date': '2026-01-07',
            'units': 1
        },
        {
            'donor_id': 'DON10001',
            'donor_name': 'Michael Johnson',
            'blood_group': 'O+',
            'donation_date': '2025-12-20',
            'units': 1
        }
    ]
    
    # Add recent donations first
    for i, donation in enumerate(recent_donations_data):
        donation_date = donation['donation_date']
        expiry_date = calculate_expiry_date(donation_date)
        
        donations.append((
            f'DONATION{i+2000}',  # Start from 2000 for recent donations
            donation['donor_id'],
            donation['donor_name'],
            donation['blood_group'],
            donation['units'],
            donation_date,
            expiry_date,
            'System Administrator',
            'Passed',
            'Regular donation'
        ))
    
    # Add more historical donations
    historical_dates = [
        '2025-11-15', '2025-10-28', '2025-09-10', '2025-08-05',
        '2025-07-20', '2025-06-12', '2025-05-08', '2025-04-01',
        '2025-03-15', '2025-02-20', '2025-01-10', '2024-12-05'
    ]
    
    for i in range(12):  # Add 12 more historical donations
        donor = random.choice(sample_donors)
        donation_date = historical_dates[i] if i < len(historical_dates) else (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
        expiry_date = calculate_expiry_date(donation_date)
        
        donations.append((
            f'DONATION{i+1000}',
            donor['donor_id'],
            donor['name'],
            donor['blood_group'],
            random.choice([1, 2]),
            donation_date,
            expiry_date,
            random.choice(['System Administrator', 'John Doe']),
            random.choice(['Passed', 'Passed', 'Passed', 'Failed']),  # Mostly passed
            random.choice(['Regular donation', 'Emergency donation', 'Blood drive'])
        ))
    
    # Insert all donations
    try:
        cursor.executemany('''
            INSERT INTO donation_history (donation_id, donor_id, donor_name, blood_group, units_donated, donation_date, expiry_date, received_by, test_result, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', donations)
        print("✓ Sample donation history created!")
    except Exception as e:
        print(f"❌ Error creating donation history: {e}")
        # Print problematic donations
        for i, donation in enumerate(donations):
            if None in donation:
                print(f"   Problematic donation at index {i}: {donation}")
    
    # Update inventory based on successful donations
    print("\n6. Updating inventory based on donations...")
    
    # First, get all successful donations
    cursor.execute('''
        SELECT blood_group, SUM(units_donated) 
        FROM donation_history 
        WHERE test_result = 'Passed' 
        GROUP BY blood_group
    ''')
    
    donation_totals = cursor.fetchall()
    
    for bg, total_units in donation_totals:
        if total_units:
            status = 'Low Stock' if total_units < 10 else 'Normal' if total_units < 20 else 'High Stock'
            cursor.execute('''
                UPDATE inventory 
                SET units_available = ?,
                    last_updated = CURRENT_TIMESTAMP,
                    status = ?
                WHERE blood_group = ?
            ''', (total_units, status, bg))
    
    conn.commit()
    
    # Verify data insertion
    print("\n" + "=" * 60)
    print("DATABASE SUMMARY")
    print("=" * 60)
    
    tables = ['users', 'donors', 'inventory', 'donation_history']
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        count = cursor.fetchone()[0]
        print(f"📊 {table.upper():20} : {count:3} records")
    
    print("\n📈 BLOOD INVENTORY STATUS:")
    cursor.execute('SELECT blood_group, units_available, status FROM inventory ORDER BY blood_group')
    for row in cursor.fetchall():
        status_icon = "🔴" if row[2] == 'Low Stock' else "🟡" if row[2] == 'Normal' else "🟢"
        print(f"   {row[0]:4} : {row[1]:3} units {status_icon} {row[2]}")
    
    print("\n👥 DONOR DISTRIBUTION:")
    cursor.execute('SELECT blood_group, COUNT(*) FROM donors GROUP BY blood_group ORDER BY blood_group')
    for row in cursor.fetchall():
        print(f"   {row[0]:4} : {row[1]:3} donors")
    
    print("\n🩸 RECENT DONATIONS (for dashboard):")
    cursor.execute('''
        SELECT donor_name, blood_group, units_donated, donation_date 
        FROM donation_history 
        ORDER BY donation_date DESC 
        LIMIT 5
    ''')
    for row in cursor.fetchall():
        print(f"   {row[0]:20} {row[1]:4} {row[2]} unit(s) on {row[3]}")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ DATABASE INITIALIZATION COMPLETED!")
    print("=" * 60)
    print("\n👉 To start the application, run: python app.py")
    print("👉 Access at: http://localhost:5000")
    print("👉 Login with: admin@bloodbank.com / admin123")
    print("\n" + "=" * 60)
    
    return True

def check_database():
    """Check if database exists and is accessible."""
    if not os.path.exists('bloodbank.db'):
        print("❌ Database file not found!")
        return False
    
    try:
        conn = sqlite3.connect('bloodbank.db')
        cursor = conn.cursor()
        
        # Check if tables exist
        tables = ['users', 'donors', 'inventory', 'donation_history']
        for table in tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if not cursor.fetchone():
                print(f"❌ Table '{table}' not found in database!")
                conn.close()
                return False
        
        # Check for NULL expiry dates
        cursor.execute("SELECT COUNT(*) FROM donation_history WHERE expiry_date IS NULL")
        null_expiry_count = cursor.fetchone()[0]
        if null_expiry_count > 0:
            print(f"⚠️  Found {null_expiry_count} donations with NULL expiry dates!")
        
        conn.close()
        print("✅ Database check passed!")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("BLOOD BANK DATABASE SETUP")
    print("=" * 60)
    
    # Create database
    init_database()
    
    # Verify database
    check_database()