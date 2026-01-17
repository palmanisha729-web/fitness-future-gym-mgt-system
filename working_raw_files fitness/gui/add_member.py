import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from database.member_ops import add_member, validate_member_exists  # Add the new function for validation
import datetime

class AddMemberPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8fafc")
        self.configure_ui()
        self.create_form()

    def configure_ui(self):
        # Modern header with beautiful gradient effect
        header_frame = tk.Frame(self, bg="#10b981", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Gradient shadow
        tk.Frame(header_frame, bg="#059669", height=3).pack(side="bottom", fill="x")

        heading = tk.Label(
            header_frame,
            text="➕ Add New Member",
            font=("Segoe UI", 24, "bold"),
            bg="#10b981",
            fg="white"
        )
        heading.pack(expand=True, pady=5)

    def create_form(self):
        # Modern card container
        form_outer = tk.Frame(self, bg="#f8fafc")
        form_outer.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Shadow effect
        shadow_frame = tk.Frame(form_outer, bg="#cbd5e1")
        shadow_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        form_container = tk.Frame(shadow_frame, bg="white", bd=0, relief="flat")
        form_container.pack(fill="both", expand=True, padx=20, pady=20)

        label_style = {
            "font": ("Segoe UI", 12, "bold"),
            "bg": "white",
            "fg": "#1e293b",
            "anchor": "w"
        }

        entry_style = {
            "font": ("Segoe UI", 12),
            "width": 30,
            "bd": 0,
            "relief": "flat",
            "bg": "#f8fafc",
            "highlightthickness": 2,
            "highlightcolor": "#10b981",
            "highlightbackground": "#e2e8f0",
            "fg": "#0f172a"
        }

        def add_field(row, text, widget, symbol=None):
            label_text = f"{symbol}  {text}" if symbol else text
            tk.Label(form_container, text=label_text, **label_style).grid(row=row, column=0, sticky="w", pady=10, padx=(0, 15))
            widget.grid(row=row, column=1, pady=10, padx=5, sticky="w", ipady=5, ipadx=8)

        self.name_entry = tk.Entry(form_container, **entry_style)
        add_field(0, "Name*", self.name_entry, symbol="👤")

        self.phone_entry = tk.Entry(form_container, **entry_style)
        add_field(1, "Phone", self.phone_entry, symbol="📞")

        self.address_entry = tk.Entry(form_container, **entry_style)
        add_field(2, "Address", self.address_entry, symbol="🏠")

        self.pincode_entry = tk.Entry(form_container, **entry_style)
        add_field(3, "Pincode", self.pincode_entry, symbol="🔢")

        today = datetime.date.today()
        self.start_date = DateEntry(form_container, font=("Segoe UI", 12), date_pattern='dd-mm-yyyy', width=27)
        self.start_date.set_date(today)
        add_field(4, "Start Date*", self.start_date, symbol="📅")

        self.end_date = DateEntry(form_container, font=("Segoe UI", 12), date_pattern='dd-mm-yyyy', width=27)
        self.end_date.set_date(today)
        add_field(5, "End Date*", self.end_date, symbol="📅")

        fees_frame = tk.Frame(form_container, bg="white")

        rupee_label = tk.Label(fees_frame, text="₹", font=("Segoe UI", 12), bg="white", fg="#2c3e50")
        rupee_label.pack(side="left", padx=(0, 5))

        self.fees_var = tk.StringVar()
        self.fees_entry = tk.Entry(fees_frame, textvariable=self.fees_var, **entry_style)
        self.fees_entry.pack(side="left")

        def format_fees_input(*args):
            value = self.fees_var.get().replace(",", "").strip()
            if value.isdigit():
                formatted = "{:,}".format(int(value))
                self.fees_var.set(formatted)

        self.fees_var.trace_add("write", lambda *args: format_fees_input())

        add_field(6, "Fees", fees_frame, symbol="💰")

        # Modern button container
        btn_container = tk.Frame(self, bg="#f8fafc")
        btn_container.pack(pady=20)
        
        save_btn = tk.Button(
            btn_container,
            text="💾  Save Member",
            font=("Segoe UI", 12, "bold"),
            bg="#10b981",
            fg="white",
            activebackground="#059669",
            activeforeground="white",
            width=20,
            bd=0,
            relief="flat",
            cursor="hand2",
            pady=10,
            command=self.save_member
        )
        save_btn.pack()
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg="#059669"))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg="#10b981"))

        # Bind Enter key to trigger save
        self.name_entry.bind("<Return>", lambda event: self.save_member())

    def save_member(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        address = self.address_entry.get().strip()
        pincode = self.pincode_entry.get().strip()
        fees_input = self.fees_var.get().strip()
        start = self.start_date.get()
        end = self.end_date.get()

        # Validate required fields
        if not name:
            messagebox.showerror("Missing Field", "⚠️ Please enter member name")
            self.name_entry.focus()
            return
            
        if not address:
            messagebox.showerror("Missing Field", "⚠️ Please enter address")
            self.address_entry.focus()
            return
            
        if not pincode:
            messagebox.showerror("Missing Field", "⚠️ Please enter pincode")
            self.pincode_entry.focus()
            return
            
        if not fees_input:
            messagebox.showerror("Missing Field", "⚠️ Please enter fees")
            self.fees_entry.focus()
            return
        
        # Validate phone
        if phone and (not phone.isdigit() or len(phone) != 10):
            messagebox.showerror("Invalid Phone", "📵 Phone number must be exactly 10 digits")
            self.phone_entry.focus()
            return

        # Validate pincode
        if pincode and (not pincode.isdigit() or len(pincode) != 6):
            messagebox.showerror("Invalid Pincode", "📮 Pincode must be 6 digits")
            self.pincode_entry.focus()
            return

        # Check for duplicates
        if phone and validate_member_exists(phone, name):
            messagebox.showerror("Duplicate Member", "⚠️ A member with this phone number already exists")
            self.phone_entry.focus()
            return

        # Add member
        fees = f"₹ {fees_input}"
        if add_member(name, phone, address, pincode, fees, start, end):
            messagebox.showinfo("Success", f"✅ Member '{name}' added successfully!")
            self.clear_fields()
        else:
            messagebox.showerror("Error", "❌ Failed to add member. Please try again.")

    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)
        self.pincode_entry.delete(0, tk.END)
        self.fees_var.set("")
        today = datetime.date.today()
        self.start_date.set_date(today)
        self.end_date.set_date(today)
        self.name_entry.focus()
