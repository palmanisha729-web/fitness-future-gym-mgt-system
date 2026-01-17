import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from tkinter import Tk, messagebox
from database.db_connect import connect_db
from datetime import datetime, timedelta



class DragDropImportPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")

        tk.Label(self, text="📥 Import Excel File", font=("Arial Black", 18), bg="white", fg="#001f3f").pack(pady=20)

        import_btn = tk.Button(
            self,
            text="Browse Excel File (.xlsx)",
            command=self.import_file,
            font=("Arial", 13),
            bg="#0074D9",
            fg="white",
            padx=20,
            pady=10
        )
        import_btn.pack(pady=30)

    def import_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel Files", "*.xlsx")]
        )

        if not file_path:
            return  # User cancelled

        if not file_path.endswith(".xlsx"):
            messagebox.showerror("Invalid File", "Only .xlsx files are allowed.")
            return

        try:
            import_fresh_excel_data(file_path)
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import Excel file:\n{str(e)}")

def import_fresh_excel_data(excel_file=None):
    from tkinter import filedialog

    if not excel_file:
        # File dialog for user to select Excel file
        root = Tk()
        root.withdraw()
        excel_file = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )
        root.destroy()

    if not excel_file:
        print("❌ No file selected.")
        return

    print(f"📂 Selected file: {excel_file}")
    print("Reading Excel data...")

    try:
        df = pd.read_excel(excel_file)
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
    except Exception as e:
        messagebox.showerror("Error Reading File", f"Failed to read Excel file:\n{e}")
        return

    conn = connect_db()
    cursor = conn.cursor()

    # 🔥 Step 1: Delete all existing data
    confirm = messagebox.askyesno("Confirm Deletion", "⚠️ This will DELETE all current members.\nDo you want to continue?")
    if not confirm:
        print("Aborted.")
        return
    
    try:
        cursor.execute("DELETE FROM members")
        conn.commit()
        print("✅ Old data deleted.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to clear database:\n{e}")
        return

    inserted_count = 0
    skipped_count = 0
    errors = []
    
    # Print column names for debugging
    print(f"\n{'='*60}")
    print(f"Excel columns found: {list(df.columns)}")
    print(f"Total rows in Excel: {len(df)}")
    print(f"{'='*60}\n")

    for index, row in df.iterrows():
        try:
            # Get FF ID first
            ff_id = None
            for col in ['FF ID', 'ff_id', 'FF_ID', 'id', 'ID', 'member_id', 'Member ID']:
                if col in df.columns:
                    val = row.get(col)
                    if pd.notna(val) and str(val).strip():
                        ff_id = str(val).strip()
                        break
            
            # Get name - try combining FIRST NAME and LAST NAME, or single name field
            name = None
            
            # Try to get first and last name separately
            first_name = ''
            last_name = ''
            
            if 'FIRST NAME' in df.columns:
                val = row.get('FIRST NAME')
                if pd.notna(val) and str(val).strip():
                    first_name = str(val).strip()
            
            if 'LAST NAME' in df.columns:
                val = row.get('LAST NAME')
                if pd.notna(val) and str(val).strip():
                    last_name = str(val).strip()
            
            # Combine first and last name
            if first_name:
                name = f"{first_name} {last_name}".strip() if last_name else first_name
            
            # If no name found, try other column variations
            if not name:
                for col in ['name', 'Name', 'NAME', 'member_name', 'Member Name', 'first_name', 'First Name']:
                    if col in df.columns:
                        val = row.get(col)
                        if pd.notna(val) and str(val).strip():
                            name = str(val).strip()
                            break
            
            # If still no name but we have FF ID, use FF ID as name
            if (not name or name.lower() in ['nan', 'none', '']) and ff_id:
                name = f"Member-{ff_id}"
                print(f"[PROCESSING] Row {index+2} - Using FF ID {ff_id} (no name provided)")
            elif not name or name.lower() in ['nan', 'none', '']:
                print(f"[SKIPPED] Row {index+2} - Missing both name and FF ID")
                skipped_count += 1
                continue
            else:
                print(f"[PROCESSING] Row {index+2} - Name: {name}")

            # Get phone - try different column name variations
            phone = ''
            for col in ['phone', 'Phone', 'PHONE', 'mobile', 'Mobile', 'contact', 'Contact', 'CONTACT NO.', 'contact_no', 'Contact No.']:
                if col in df.columns and pd.notna(row.get(col)):
                    phone = str(row.get(col)).strip()
                    break

            # Handle fees - try different column name variations
            fees_formatted = "₹ 0"
            for col in ['fees', 'Fees', 'FEES', 'fee', 'Fee', 'amount', 'Amount']:
                if col in df.columns:
                    try:
                        fees_value = row.get(col)
                        if pd.notna(fees_value):
                            fees = float(str(fees_value).replace(',', '').replace('₹', '').replace('Rs.', '').strip())
                            fees_formatted = f"₹ {fees:,.0f}"
                            break
                    except:
                        pass

            # Handle dates with multiple format support
            from datetime import datetime as dt_module
            def parse_date(date_val):
                if pd.isna(date_val):
                    # Return today's date as default
                    return dt_module.now().strftime('%Y-%m-%d')
                try:
                    # Try pandas datetime parsing first
                    parsed = pd.to_datetime(date_val, errors='coerce', dayfirst=True)
                    if pd.notna(parsed):
                        return parsed.strftime('%Y-%m-%d')
                    
                    # Try manual string parsing for dd-mm-yyyy or dd/mm/yyyy
                    date_str = str(date_val).strip()
                    for sep in ['-', '/', '.']:
                        if sep in date_str:
                            parts = date_str.split(sep)
                            if len(parts) == 3:
                                # Try different formats
                                try:
                                    if len(parts[2]) == 4:  # dd-mm-yyyy or dd/mm/yyyy
                                        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
                                        return f"{year:04d}-{month:02d}-{day:02d}"
                                    elif len(parts[0]) == 4:  # yyyy-mm-dd or yyyy/mm/dd
                                        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
                                        return f"{year:04d}-{month:02d}-{day:02d}"
                                except:
                                    pass
                    
                    # If all else fails, return today's date
                    return dt_module.now().strftime('%Y-%m-%d')
                except:
                    return dt_module.now().strftime('%Y-%m-%d')

            # Try different column name variations for dates
            start_date = None
            for col in ['start_date', 'Start Date', 'START_DATE', 'start', 'Start', 'joining_date', 'Joining Date', 'DATE FROM', 'date_from', 'Date From']:
                if col in df.columns:
                    start_date = parse_date(row.get(col))
                    break
            
            if not start_date:
                from datetime import datetime as dt_fallback
                start_date = dt_fallback.now().strftime('%Y-%m-%d')

            end_date = None
            for col in ['end_date', 'End Date', 'END_DATE', 'end', 'End', 'expiry_date', 'Expiry Date', 'DATE TO', 'date_to', 'Date To']:
                if col in df.columns:
                    end_date = parse_date(row.get(col))
                    break
            
            if not end_date:
                # Default: 30 days from start
                from datetime import datetime as dt_calc
                end_date = (dt_calc.strptime(start_date, '%Y-%m-%d') + timedelta(days=30)).strftime('%Y-%m-%d')

            # Get address and pincode - try different column name variations
            address = ''
            for col in ['address', 'Address', 'ADDRESS', 'addr']:
                if col in df.columns and pd.notna(row.get(col)):
                    address = str(row.get(col)).strip()
                    break

            pincode = ''
            for col in ['pincode', 'Pincode', 'PINCODE', 'pin', 'Pin', 'PIN']:
                if col in df.columns and pd.notna(row.get(col)):
                    pincode = str(row.get(col)).strip()
                    break

            # Insert into database (let database auto-generate ID)
            print(f"[INSERT] Name={name}, Phone={phone}, Start={start_date}, End={end_date}, Fees={fees_formatted}")
            cursor.execute("""
                INSERT INTO members (name, phone, start_date, end_date, fees, address, pincode)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, phone, start_date, end_date, fees_formatted, address, pincode))

            inserted_count += 1
            print(f"[SUCCESS] Row {index+2} inserted successfully")

        except Exception as e:
            error_msg = f"Row {index+2}: {str(e)}"
            print(f"[ERROR] {error_msg}")
            errors.append(error_msg)
            skipped_count += 1

    try:
        conn.commit()
        result_msg = f"✅ Inserted: {inserted_count}\n⚠️ Skipped: {skipped_count}"
        if errors and len(errors) <= 5:
            result_msg += f"\n\nErrors:\n" + "\n".join(errors[:5])
        elif errors:
            result_msg += f"\n\n{len(errors)} errors occurred (showing first 5)"
        messagebox.showinfo("Import Completed", result_msg)
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Error", f"Failed to commit data:\n{e}")
