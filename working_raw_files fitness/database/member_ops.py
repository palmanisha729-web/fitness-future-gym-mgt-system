from datetime import datetime, timedelta
from database.db_connect import connect_db
import re

def convert_date_to_iso(date_str):
    """Convert dd-mm-yyyy to yyyy-mm-dd for database storage."""
    try:
        if '-' in date_str:
            parts = date_str.split('-')
            if len(parts[0]) == 4:  # Already yyyy-mm-dd
                return date_str
            # Convert dd-mm-yyyy to yyyy-mm-dd
            return f"{parts[2]}-{parts[1]}-{parts[0]}"
        return date_str
    except:
        return date_str

def convert_date_to_display(date_str):
    """Convert yyyy-mm-dd to dd-mm-yyyy for display."""
    try:
        if date_str and '-' in date_str:
            parts = date_str.split('-')
            if len(parts[0]) == 4:  # yyyy-mm-dd format
                return f"{parts[2]}-{parts[1]}-{parts[0]}"
        return date_str
    except:
        return date_str

def add_member(name, phone, address, pincode, fees, start_date, end_date):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Sanitize inputs
        name = name.strip()[:100]  # Limit name length
        phone = phone.strip()[:15]
        address = address.strip()[:200]
        pincode = pincode.strip()[:10]
        
        cleaned_fees = re.sub(r'[^\d.]', '', str(fees))
        formatted_fees = f"₹ {float(cleaned_fees):,.0f}"
        
        # Convert dates to ISO format for storage
        start_iso = convert_date_to_iso(start_date)
        end_iso = convert_date_to_iso(end_date)

        cursor.execute("""
            INSERT INTO members (name, phone, address, pincode, fees, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, phone, address, pincode, formatted_fees, start_iso, end_iso))

        conn.commit()
        return True
    except Exception as e:
        print(f"Error adding member: {e}")
        conn.rollback()
        return False


def update_member(member_id, name, phone, start_date, end_date, fees, address, pincode):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Sanitize inputs
        name = name.strip()[:100]
        phone = phone.strip()[:15]
        address = address.strip()[:200]
        pincode = pincode.strip()[:10]
        
        # Format the fees with ₹ symbol
        cleaned_fees = re.sub(r'[^\d.]', '', str(fees))
        formatted_fees = f"₹ {float(cleaned_fees):,.0f}"
        
        # Convert dates to ISO format for storage
        start_iso = convert_date_to_iso(start_date)
        end_iso = convert_date_to_iso(end_date)

        cursor.execute('''
            UPDATE members
            SET name = ?, phone = ?, start_date = ?, end_date = ?, fees = ?, address = ?, pincode = ?
            WHERE id = ?
        ''', (name, phone, start_iso, end_iso, formatted_fees, address, pincode, member_id))

        conn.commit()
        return cursor.rowcount > 0  # Return True only if a row was actually updated
    except Exception as e:
        print(f"Error updating member: {e}")
        conn.rollback()
        return False


def fetch_all_members():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM members WHERE name != "" AND name IS NOT NULL')
        rows = cursor.fetchall()
        # Convert dates to display format
        formatted_rows = []
        for row in rows:
            row_list = list(row)
            if row_list[3]:  # start_date
                row_list[3] = convert_date_to_display(row_list[3])
            if row_list[4]:  # end_date
                row_list[4] = convert_date_to_display(row_list[4])
            formatted_rows.append(tuple(row_list))
        return formatted_rows
    except Exception as e:
        print(f"Error fetching members: {e}")
        return []

def fetch_expired_members(today=None):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        if today:
            # Convert display format to ISO for comparison
            today_iso = convert_date_to_iso(today) if today else datetime.now().date().isoformat()
            cursor.execute("SELECT * FROM members WHERE end_date < ? AND name != ''", (today_iso,))
        else:
            cursor.execute("SELECT * FROM members WHERE name != ''")

        results = cursor.fetchall()
        # Convert dates to display format
        formatted_results = []
        for row in results:
            row_list = list(row)
            if row_list[3]:  # start_date
                row_list[3] = convert_date_to_display(row_list[3])
            if row_list[4]:  # end_date
                row_list[4] = convert_date_to_display(row_list[4])
            formatted_results.append(tuple(row_list))
        return formatted_results
    except Exception as e:
        print(f"Error fetching expired members: {e}")
        return []

def fetch_total_members():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM members WHERE name != '' AND name IS NOT NULL")
        count = cursor.fetchone()[0]
        return count
    except Exception as e:
        print(f"Error fetching total members: {e}")
        return 0

def fetch_joining_today():
    try:
        today = datetime.now().date().isoformat()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE start_date = ? AND name != ''", (today,))
        rows = cursor.fetchall()
        # Convert dates to display format
        formatted_rows = []
        for row in rows:
            row_list = list(row)
            if row_list[3]:  # start_date
                row_list[3] = convert_date_to_display(row_list[3])
            if row_list[4]:  # end_date
                row_list[4] = convert_date_to_display(row_list[4])
            formatted_rows.append(tuple(row_list))
        return formatted_rows
    except Exception as e:
        print(f"Error fetching today's joinings: {e}")
        return []

def fetch_inactive_members():
    try:
        thirty_days_ago = (datetime.now() - timedelta(days=30)).date().isoformat()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE end_date <= ? AND name != ''", (thirty_days_ago,))
        rows = cursor.fetchall()
        # Convert dates to display format
        formatted_rows = []
        for row in rows:
            row_list = list(row)
            if row_list[3]:  # start_date
                row_list[3] = convert_date_to_display(row_list[3])
            if row_list[4]:  # end_date
                row_list[4] = convert_date_to_display(row_list[4])
            formatted_rows.append(tuple(row_list))
        return formatted_rows
    except Exception as e:
        print(f"Error fetching inactive members: {e}")
        return []

def extend_membership(member_id, new_start_date, new_end_date, new_fee):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Convert dates to ISO format
        start_iso = convert_date_to_iso(new_start_date)
        end_iso = convert_date_to_iso(new_end_date)
        
        cursor.execute(
            "UPDATE members SET start_date = ?, end_date = ?, fees = ? WHERE id = ?",
            (start_iso, end_iso, new_fee, member_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error extending membership: {e}")
        conn.rollback()
        return False

def get_member_by_id(member_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM members WHERE id = ?', (member_id,))
        row = cursor.fetchone()

        if row:
            # Assuming column order: id, name, phone, start_date, end_date, fees, address, pincode
            return {
                'id': row[0],
                'name': row[1],
                'phone': row[2],
                'start_date': convert_date_to_display(row[3]) if row[3] else '',
                'end_date': convert_date_to_display(row[4]) if row[4] else '',
                'fees': row[5],
                'address': row[6],
                'pincode': row[7]
            }
        return None
    except Exception as e:
        print(f"Error fetching member by ID: {e}")
        return None

def delete_member(member_id_or_name):
    try:
        member = get_member_by_id_or_name(member_id_or_name)
        if member:
            conn = connect_db()
            cursor = conn.cursor()
            # Actually delete the member from database
            cursor.execute("DELETE FROM members WHERE id = ?", (member[0],))
            conn.commit()
            return True
        else:
            return False
    except Exception as e:
        print(f"Error deleting member: {e}")
        return False

def get_member_by_id_or_name(member_id_or_name):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Try ID search (numeric)
            cursor.execute("SELECT * FROM members WHERE id = ?", (int(member_id_or_name),))
        except ValueError:
            # Name-based search (case-insensitive)
            cursor.execute(
                "SELECT * FROM members WHERE LOWER(name) = LOWER(?)",
                (member_id_or_name,)
            )

        member = cursor.fetchone()
        return member
    except Exception as e:
        print(f"Error fetching member by ID or name: {e}")
        return None

def validate_member_exists(phone, name):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Query to check if a member exists with the same phone (phone is more unique)
        if phone and phone.strip():
            cursor.execute("SELECT * FROM members WHERE phone = ? AND name != ''", (phone,))
            result = cursor.fetchone()
            return result is not None
        
        return False
    except Exception as e:
        print(f"Error validating member: {e}")
        return False

# ... your existing functions like validate_member_exists()

def fetch_members_expired_3_months_ago():
    try:
        three_months_ago = (datetime.now() - timedelta(days=90)).date().isoformat()
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM members WHERE end_date < ? AND name != ''", (three_months_ago,))
        rows = cursor.fetchall()
        # Convert dates to display format
        formatted_rows = []
        for row in rows:
            row_list = list(row)
            if row_list[3]:  # start_date
                row_list[3] = convert_date_to_display(row_list[3])
            if row_list[4]:  # end_date
                row_list[4] = convert_date_to_display(row_list[4])
            formatted_rows.append(tuple(row_list))
        return formatted_rows
    except Exception as e:
        print(f"Error fetching expired members (3 months): {e}")
        return []

def delete_member_by_id(member_id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Actually delete the member
        cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Error deleting member by ID: {e}")
        conn.rollback()
        return False


