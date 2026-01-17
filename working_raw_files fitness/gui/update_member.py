import tkinter as tk
import re
from tkinter import messagebox
from tkcalendar import DateEntry
from database.member_ops import update_member, get_member_by_id
import datetime

class UpdateMemberPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#f8fafc")
        self.configure_ui()

    def configure_ui(self):
        # Modern header with beautiful gradient effect
        header_frame = tk.Frame(self, bg="#6366f1", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Gradient shadow
        tk.Frame(header_frame, bg="#4f46e5", height=3).pack(side="bottom", fill="x")

        heading = tk.Label(
            header_frame,
            text="✏️ Update Member Details",
            font=("Segoe UI", 24, "bold"),
            bg="#6366f1",
            fg="white"
        )
        heading.pack(expand=True, pady=5)

        # Modern card container
        form_outer = tk.Frame(self, bg="#f8fafc")
        form_outer.pack(pady=20, padx=40, fill="both", expand=True)
        
        # Shadow effect
        shadow_frame = tk.Frame(form_outer, bg="#cbd5e1")
        shadow_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        container = tk.Frame(shadow_frame, bg="white", bd=0, relief="flat")
        container.pack(fill="both", expand=True, padx=20, pady=20)

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
            "highlightcolor": "#6366f1",
            "highlightbackground": "#e2e8f0",
            "fg": "#0f172a"
        }

        def add_field(row, text, widget, symbol=None):
            label_text = f"{symbol}  {text}" if symbol else text
            tk.Label(container, text=label_text, **label_style).grid(row=row, column=0, sticky="w", pady=10, padx=(0, 15))
            widget.grid(row=row, column=1, pady=10, padx=5, sticky="w", ipady=5, ipadx=8)

        # Input Fields
        self.id_entry = tk.Entry(container, **entry_style)
        add_field(0, "Member ID*", self.id_entry, symbol="🆔")

        load_btn = tk.Button(
            container, 
            text="🔍 Load",
            font=("Segoe UI", 11, "bold"),
            bg="#8b5cf6", 
            fg="white",
            activebackground="#7c3aed",
            command=self.load_member,
            width=10,
            bd=0,
            relief="flat",
            cursor="hand2",
            pady=6
        )
        load_btn.grid(row=0, column=2, padx=5)
        load_btn.bind("<Enter>", lambda e: load_btn.config(bg="#7c3aed"))
        load_btn.bind("<Leave>", lambda e: load_btn.config(bg="#8b5cf6"))

        self.name_entry = tk.Entry(container, **entry_style)
        add_field(1, "Name", self.name_entry, symbol="👤")

        self.phone_entry = tk.Entry(container, **entry_style)
        add_field(2, "Phone", self.phone_entry, symbol="📞")

        self.start_date = DateEntry(container, font=("Segoe UI", 12), date_pattern='dd-mm-yyyy', width=27)
        add_field(3, "Start Date", self.start_date, symbol="📅")

        self.end_date = DateEntry(container, font=("Segoe UI", 12), date_pattern='dd-mm-yyyy', width=27)
        add_field(4, "End Date", self.end_date, symbol="📅")

        self.fees_entry = tk.Entry(container, **entry_style)
        add_field(5, "Fees", self.fees_entry, symbol="💰")

        self.address_entry = tk.Entry(container, **entry_style)
        add_field(6, "Address", self.address_entry, symbol="🏠")

        self.pincode_entry = tk.Entry(container, **entry_style)
        add_field(7, "Pincode", self.pincode_entry, symbol="🔢")

        # Modern button container
        btn_container = tk.Frame(self, bg="#f8fafc")
        btn_container.pack(pady=20)
        
        self.update_btn = tk.Button(
            btn_container,
            text="✨ Update Member",
            font=("Segoe UI", 13, "bold"),
            bg="#6366f1",
            fg="white",
            activebackground="#4f46e5",
            activeforeground="white",
            width=22,
            bd=0,
            relief="flat",
            cursor="hand2",
            pady=12,
            command=self.update_member_data
        )
        self.update_btn.pack()
        self.update_btn.bind("<Enter>", lambda e: self.update_btn.config(bg="#4f46e5"))
        self.update_btn.bind("<Leave>", lambda e: self.update_btn.config(bg="#6366f1"))

        # Bind Enter key to update
        self.bind("<Return>", lambda event: self.update_member_data())

    def load_member(self):
        member_id = self.id_entry.get().strip()
        if not member_id:
            messagebox.showerror("Missing ID", "⚠️ Please enter a Member ID")
            self.id_entry.focus()
            return

        data = get_member_by_id(member_id)
        if not data:
            messagebox.showerror("Not Found", f"❌ No member found with ID: {member_id}")
            self.id_entry.focus()
            return

        # Populate form with existing data
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, data['name'])

        self.phone_entry.delete(0, tk.END)
        self.phone_entry.insert(0, data['phone'])

        # Parse dates - they come in dd-mm-yyyy format from database
        try:
            if data['start_date']:
                self.start_date.set_date(data['start_date'])
        except:
            pass
            
        try:
            if data['end_date']:
                self.end_date.set_date(data['end_date'])
        except:
            pass
        
        cleaned_fees = data['fees'].replace('₹', '').replace('Rs.', '').replace(',', '').strip()
        self.fees_entry.delete(0, tk.END)
        self.fees_entry.insert(0, cleaned_fees)

        self.address_entry.delete(0, tk.END)
        self.address_entry.insert(0, data['address'])

        self.pincode_entry.delete(0, tk.END)
        self.pincode_entry.insert(0, data['pincode'])

        # Check if fees are pending (today is after end_date)
        today = datetime.date.today()
        try:
            # end_date is in dd-mm-yyyy format
            if data['end_date']:
                parts = data['end_date'].split('-')
                if len(parts) == 3:
                    end_date = datetime.date(int(parts[2]), int(parts[1]), int(parts[0]))
                    if today > end_date:
                        self.update_btn.config(bg="red", activebackground="darkred")
                    else:
                        self.update_btn.config(bg="#3498db", activebackground="#2980b9")
        except Exception as e:
            print("Error parsing end date:", e)
            self.update_btn.config(bg="#3498db", activebackground="#2980b9")

    def update_member_data(self):
        member_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        start = self.start_date.get()
        end = self.end_date.get()
        fees = self.fees_entry.get().strip()
        address = self.address_entry.get().strip()
        pincode = self.pincode_entry.get().strip()

        if not member_id:
            messagebox.showerror("Missing Field", "⚠️ Please load a member first")
            self.id_entry.focus()
            return
            
        if not name:
            messagebox.showerror("Missing Field", "⚠️ Name cannot be empty")
            self.name_entry.focus()
            return

        # Validate phone
        if phone and (not phone.isdigit() or len(phone) != 10):
            messagebox.showerror("Invalid Phone", "📵 Phone must be 10 digits")
            self.phone_entry.focus()
            return

        # Validate pincode
        if pincode and (not pincode.isdigit() or len(pincode) != 6):
            messagebox.showerror("Invalid Pincode", "📮 Pincode must be 6 digits")
            self.pincode_entry.focus()
            return

        if update_member(member_id, name, phone, start, end, fees, address, pincode):
            messagebox.showinfo("Success", "✅ Member updated successfully!")
        else:
            messagebox.showerror("Error", "❌ Failed to update member")
