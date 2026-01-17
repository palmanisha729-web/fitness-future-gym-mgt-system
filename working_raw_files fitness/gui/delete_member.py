import tkinter as tk
from tkinter import messagebox

class DeleteMemberPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8fafc")
        self.configure_ui()
        self.create_form()

    def configure_ui(self):
        # Modern header with beautiful gradient effect
        header_frame = tk.Frame(self, bg="#f43f5e", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        # Gradient shadow
        tk.Frame(header_frame, bg="#e11d48", height=3).pack(side="bottom", fill="x")

        heading = tk.Label(
            header_frame,
            text="🗑️ Delete Member",
            font=("Segoe UI", 24, "bold"),
            bg="#f43f5e",
            fg="white"
        )
        heading.pack(expand=True, pady=5)

    def create_form(self):
        # Modern card container
        form_outer = tk.Frame(self, bg="#f8fafc")
        form_outer.pack(pady=30, padx=80, fill="both", expand=True)
        
        # Shadow effect
        shadow_frame = tk.Frame(form_outer, bg="#cbd5e1")
        shadow_frame.pack(fill="both", padx=2, pady=2)
        
        form_container = tk.Frame(shadow_frame, bg="white", bd=0, relief="flat")
        form_container.pack(fill="both", padx=30, pady=30)

        label_style = {
            "font": ("Segoe UI", 11, "bold"),
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
            "highlightcolor": "#f43f5e",
            "highlightbackground": "#e2e8f0",
            "fg": "#0f172a"
        }

        # Input field - centered
        field_frame = tk.Frame(form_container, bg="white")
        field_frame.pack(pady=15)
        
        tk.Label(
            field_frame, 
            text="🆔  Member ID or Name*", 
            **label_style
        ).pack(anchor="w", pady=(0, 8))
        
        self.id_entry = tk.Entry(field_frame, **entry_style)
        self.id_entry.pack(ipady=6, ipadx=10)
        self.id_entry.focus()

        # Modern button container
        btn_container = tk.Frame(self, bg="#f8fafc")
        btn_container.pack(pady=30)
        
        delete_btn = tk.Button(
            btn_container,
            text="🗑️ Delete Member",
            font=("Segoe UI", 13, "bold"),
            bg="#f43f5e",
            fg="white",
            activebackground="#e11d48",
            activeforeground="white",
            width=20,
            bd=0,
            relief="flat",
            cursor="hand2",
            pady=12,
            command=self.delete_member_data
        )
        delete_btn.pack()
        delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#e11d48"))
        delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#f43f5e"))

        # Bind Enter key to trigger delete
        self.id_entry.bind("<Return>", lambda event: self.delete_member_data())

    def delete_member_data(self):
        member_id_or_name = self.id_entry.get().strip()

        if not member_id_or_name:
            messagebox.showerror("Missing Input", "⚠️ Please enter Member ID or Name")
            self.id_entry.focus()
            return

        from database.member_ops import get_member_by_id_or_name

        member = get_member_by_id_or_name(member_id_or_name)
        if not member:
            messagebox.showerror("Not Found", f"❌ No member found with: '{member_id_or_name}'")
            self.id_entry.focus()
            return

        member_info = f"ID: {member[0]}\nName: {member[1]}\nPhone: {member[2] if member[2] else 'N/A'}"
        confirm = messagebox.askyesno(
            "⚠️ Confirm Deletion", 
            f"Are you sure you want to permanently delete:\n\n{member_info}\n\nThis action cannot be undone!"
        )
        
        if confirm:
            from database.member_ops import delete_member
            if delete_member(member_id_or_name):
                messagebox.showinfo("Deleted", f"✅ Member '{member[1]}' deleted successfully!")
                self.id_entry.delete(0, tk.END)
                self.id_entry.focus()
            else:
                messagebox.showerror("Error", "❌ Failed to delete member. Please try again.")
