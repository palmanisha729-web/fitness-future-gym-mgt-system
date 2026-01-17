import tkinter as tk
from tkinter import ttk, messagebox
from database.member_ops import fetch_expired_members, extend_membership
from datetime import date, timedelta, datetime
from tkcalendar import DateEntry

class ExtendMembershipPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8f9fa")
        self.dialog_open = False  # Flag to prevent multiple dialogs
        self.fees_by_months = {
            1: 600,
            2: 1200,
            3: 1500,
            6: 2800
        }
        self.build_ui()
        self.load_members()

    def build_ui(self):
        # Modern title with beautiful styling
        title_frame = tk.Frame(self, bg="#f8f9fa")
        title_frame.pack(pady=(25, 10))
        
        tk.Label(
            title_frame, text="🔄 Extend Memberships",
            font=("Segoe UI", 28, "bold"),
            bg="#f8f9fa", fg="#27ae60"
        ).pack()
        
        tk.Label(
            title_frame, text="Renew expired or expiring memberships",
            font=("Segoe UI", 13),
            bg="#f8f9fa", fg="#7f8c8d"
        ).pack(pady=(5, 0))

        # 🔍 Search + 📅 Month Dropdown + 🔁 Buttons in One Line
        top_bar = tk.Frame(self, bg="#f8f9fa")
        top_bar.pack(pady=20)

        tk.Label(top_bar, text="🔍 Search:", font=("Segoe UI", 12, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(side="left", padx=(0, 10))

        self.search_entry = tk.Entry(top_bar, font=("Segoe UI", 13), width=28, fg="#2c3e50", bg="white", relief="flat", highlightthickness=2, highlightcolor="#27ae60", highlightbackground="#bdc3c7")
        self.search_entry.pack(side="left", padx=5, ipady=6)
        self.search_entry.bind("<Return>", lambda event: self.search_members())

        tk.Label(top_bar, text="📅 Extend:", font=("Segoe UI", 12, "bold"), bg="#f8f9fa", fg="#2c3e50").pack(side="left", padx=(20, 10))

        self.month_combo = ttk.Combobox(top_bar, values=list(self.fees_by_months.keys()), font=("Segoe UI", 12), state="readonly", width=6)
        self.month_combo.pack(side="left", padx=5)

        search_btn = tk.Button(
            top_bar, text="🔍 Search", font=("Segoe UI", 12, "bold"),
            bg="#3498db", fg="white", activebackground="#2980b9",
            bd=0, relief="flat", cursor="hand2", padx=15, pady=8,
            command=self.search_members
        )
        search_btn.pack(side="left", padx=10)

        refresh_btn = tk.Button(
            top_bar, text="🔁 Refresh", font=("Segoe UI", 12, "bold"),
            bg="#f39c12", fg="white", activebackground="#e67e22",
            bd=0, relief="flat", cursor="hand2", padx=15, pady=8,
            command=self.load_members
        )
        refresh_btn.pack(side="left", padx=5)

        # Treeview
        tree_frame = tk.Frame(self, bg="#f8f9fa")
        tree_frame.pack(expand=True, fill="both", pady=10, padx=30)

        self.tree = ttk.Treeview(
            tree_frame, columns=("ID", "Name", "Phone", "Start", "End", "fees", "address", "pincode"),
            show="headings", height=10, selectmode="browse"
        )

        for col in ("ID", "Name", "Phone", "Start", "End", "fees", "address", "pincode"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="w", width=130)
        self.tree.pack(side="left", expand=True, fill="both")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
            font=("Segoe UI", 11), rowheight=36,
            background="white", foreground="#2c3e50", fieldbackground="white"
        )
        style.configure("Treeview.Heading",
            font=("Segoe UI", 13, "bold"),
            background="#27ae60", foreground="white"
        )
        style.map("Treeview", 
            background=[("selected", "#3498db")],
            foreground=[("selected", "white")])

        self.extend_button = tk.Button(
            self, text="✨ Extend Selected Membership",
            font=("Segoe UI", 14, "bold"),
            bg="#27ae60", fg="white", activebackground="#2ecc71",
            activeforeground="white", bd=0, relief="flat",
            cursor="hand2", padx=30, pady=15,
            command=self.on_extend_button_click
        )
        self.extend_button.pack(pady=20)
        self.extend_button.bind("<Enter>", lambda e: self.extend_button.config(bg="#2ecc71"))
        self.extend_button.bind("<Leave>", lambda e: self.extend_button.config(bg="#27ae60"))

    def load_members(self):
        # Get today's date in ISO format for database query
        today_iso = date.today().isoformat()
        expired_members = fetch_expired_members(today_iso)
        self.tree.delete(*self.tree.get_children())

        if expired_members:
            for member in expired_members:
                self.tree.insert("", "end", values=member)
        else:
            messagebox.showinfo("No Expired Members", "No expired members found.")

    def search_members(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showinfo("Empty Search", "Please enter a name, ID, or phone to search.")
            return

        # Get today's date in ISO format for database query
        today_iso = date.today().isoformat()
        all_members = fetch_expired_members(today_iso)
        matched_members = []

        query_lower = query.lower()

        for member in all_members:
            member_id = str(member[0]).strip()
            member_name = str(member[1]).strip().lower()
            member_phone = str(member[2]).strip()

            # Check if query is a number (ID search) - exact match
            # Otherwise do partial matching for name and phone
            if query.isdigit():
                # Exact ID match only
                if query == member_id:
                    matched_members.append(member)
            else:
                # Partial match for name or phone (case-insensitive)
                if (query_lower in member_name or query in member_phone):
                    matched_members.append(member)

        self.tree.delete(*self.tree.get_children())

        if matched_members:
            for member in matched_members:
                self.tree.insert("", "end", values=member)
        else:
            messagebox.showinfo("No Match", f"No expired members found matching: '{query}'")

    def on_extend_button_click(self):
        # Prevent multiple dialogs from opening
        if self.dialog_open:
            return
            
        item = self.tree.focus()
        if not item:
            messagebox.showwarning("No Selection", "Please select a member to extend their membership.")
            return

        values = self.tree.item(item)["values"]
        member_id = values[0]
        member_name = values[1]
        phone = values[2]
        current_end_date_str = values[4]  # Format: dd-mm-yyyy
        
        # Disable button while dialog is open
        self.extend_button.config(state="disabled")
        
        # Show dialog to select extension options
        self.show_extend_dialog(member_id, member_name, phone, current_end_date_str)
    
    def show_extend_dialog(self, member_id, member_name, phone, current_end_date_str):
        """Show dialog with extension options and date picker"""
        self.dialog_open = True  # Set flag
        
        dialog = tk.Toplevel(self)
        dialog.title("Extend Membership")
        dialog.geometry("500x600")
        dialog.configure(bg="white")
        dialog.grab_set()  # Make dialog modal
        dialog.resizable(False, False)
        
        # Clear flag when dialog closes
        def on_close():
            self.dialog_open = False
            self.extend_button.config(state="normal")  # Re-enable button
            dialog.destroy()
        
        dialog.protocol("WM_DELETE_WINDOW", on_close)
        
        # Header
        tk.Label(
            dialog, text="🔄 Extend Membership",
            font=("Segoe UI", 18, "bold"), bg="white", fg="#27ae60"
        ).pack(pady=20)
        
        # Member info
        info_frame = tk.Frame(dialog, bg="white")
        info_frame.pack(pady=10, padx=30, fill="x")
        
        tk.Label(info_frame, text=f"Member: {member_name}", font=("Segoe UI", 12), bg="white", fg="#2c3e50").pack(anchor="w")
        tk.Label(info_frame, text=f"Phone: {phone}", font=("Segoe UI", 12), bg="white", fg="#2c3e50").pack(anchor="w")
        tk.Label(info_frame, text=f"Current End Date: {current_end_date_str}", font=("Segoe UI", 12, "bold"), bg="white", fg="#e74c3c").pack(anchor="w", pady=(5, 0))
        
        # Extension options frame
        extend_frame = tk.Frame(dialog, bg="white")
        extend_frame.pack(pady=20, padx=30, fill="x")
        
        tk.Label(extend_frame, text="Extension Duration:", font=("Segoe UI", 12, "bold"), bg="white", fg="#2c3e50").pack(anchor="w", pady=(0, 10))
        
        # Radio buttons for months
        selected_months = tk.IntVar(value=1)
        for months, fee in self.fees_by_months.items():
            rb = tk.Radiobutton(
                extend_frame,
                text=f"{months} Month{'s' if months > 1 else ''} - ₹{fee:,}",
                variable=selected_months,
                value=months,
                font=("Segoe UI", 11),
                bg="white",
                activebackground="white",
                selectcolor="#27ae60"
            )
            rb.pack(anchor="w", pady=2)
        
        # Date selection frame
        date_frame = tk.Frame(dialog, bg="white")
        date_frame.pack(pady=20, padx=30, fill="x")
        
        tk.Label(date_frame, text="Or Select Custom Start Date:", font=("Segoe UI", 12, "bold"), bg="white", fg="#2c3e50").pack(anchor="w", pady=(0, 10))
        
        # Parse current end date
        try:
            current_end = datetime.strptime(current_end_date_str, '%d-%m-%Y').date()
        except:
            current_end = date.today()
        
        # DateEntry for start date (default to current end date + 1 day)
        default_start = current_end + timedelta(days=1)
        
        date_entry_frame = tk.Frame(date_frame, bg="white")
        date_entry_frame.pack(anchor="w")
        
        tk.Label(date_entry_frame, text="Start from:", font=("Segoe UI", 11), bg="white").pack(side="left", padx=(0, 10))
        
        start_date_picker = DateEntry(
            date_entry_frame,
            width=15,
            background='#27ae60',
            foreground='white',
            borderwidth=2,
            date_pattern='dd-mm-yyyy',
            year=default_start.year,
            month=default_start.month,
            day=default_start.day
        )
        start_date_picker.pack(side="left")
        
        # Buttons
        button_frame = tk.Frame(dialog, bg="white")
        button_frame.pack(pady=20)
        
        def on_confirm():
            months = selected_months.get()
            start_date = start_date_picker.get_date()
            
            # Calculate new end date
            # Approximate: 30 days per month
            new_end_date = start_date + timedelta(days=30 * months)
            
            fee = self.fees_by_months[months]
            
            self.dialog_open = False  # Clear flag
            self.extend_button.config(state="normal")  # Re-enable button
            dialog.destroy()
            self.extend_membership(member_id, member_name, phone, start_date, new_end_date, fee)
        
        tk.Button(
            button_frame, text="✅ Confirm Extension",
            font=("Segoe UI", 12, "bold"),
            bg="#27ae60", fg="white",
            activebackground="#2ecc71",
            command=on_confirm,
            width=18
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame, text="❌ Cancel",
            font=("Segoe UI", 12, "bold"),
            bg="#e74c3c", fg="white",
            activebackground="#c0392b",
            command=on_close,
            width=12
        ).pack(side="left", padx=5)

    def extend_membership(self, member_id, member_name, phone, start_date, end_date, fee):
        try:
            # Format dates as dd-mm-yyyy for the extend_membership function
            start_str = start_date.strftime('%d-%m-%Y')
            end_str = end_date.strftime('%d-%m-%Y')
            fee_formatted = f"₹ {fee:,.0f}"

            extend_membership(member_id, start_str, end_str, fee_formatted)
            self.load_members()

            self.show_receipt_popup(member_name, phone, fee, start_date, end_date)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to extend membership for {member_name}: {str(e)}")

    def generate_fee_receipt(self, name, phone, amount, start_date, end_date):
        self.show_receipt_popup(name, phone, amount, start_date, end_date)
        self.save_receipt_to_file(name, phone, amount, start_date, end_date)

    def show_receipt_popup(self, name, phone, amount, start_date, end_date):
        receipt_win = tk.Toplevel(self)
        receipt_win.title("Membership Fee Receipt")
        receipt_win.geometry("400x400")
        receipt_win.configure(bg="white")

        tk.Label(receipt_win, text="🏋 Gym Membership Receipt", font=("Segoe UI", 16, "bold"), fg="#27ae60", bg="white").pack(pady=20)

        details = [
            f"Name: {name}",
            f"Phone: {phone}",
            f"Amount Paid: ₹{amount}",
            f"Start Date: {start_date.strftime('%d-%m-%Y')}",
            f"End Date: {end_date.strftime('%d-%m-%Y')}",
        ]

        for line in details:
            tk.Label(receipt_win, text=line, font=("Segoe UI", 12), bg="white", fg="#2c3e50").pack(anchor="w", padx=40, pady=5)

        tk.Button(
            receipt_win, text="OK", command=receipt_win.destroy,
            font=("Segoe UI", 12), bg="#27ae60", fg="white",
            activebackground="#2ecc71", activeforeground="white", width=10
        ).pack(pady=30)

