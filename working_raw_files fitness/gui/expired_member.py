import tkinter as tk
from tkinter import ttk, messagebox
from database.member_ops import fetch_expired_members
from datetime import date
import pandas as pd
from tkinter import filedialog


class ExpiredMembershipPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f8f9fa")
        self.build_ui()
        self.load_expired_members()

    # ================= UI =================
    def build_ui(self):
        tk.Label(
            self,
            text="📛 Expired Memberships",
            font=("Segoe UI", 26, "bold"),
            bg="#f8f9fa",
            fg="#c0392b"
        ).pack(pady=(25, 10))

        top_bar = tk.Frame(self, bg="#f8f9fa")
        top_bar.pack(pady=20)

        tk.Label(
            top_bar,
            text="Search (Name / ID / Phone):",
            font=("Segoe UI", 12),
            bg="#f8f9fa"
        ).pack(side="left", padx=(0, 10))

        self.search_entry = tk.Entry(
            top_bar,
            font=("Segoe UI", 13),
            width=40,
            relief="flat",
            bg="white",
            fg="gray",
            highlightthickness=1,
            highlightcolor="#c0392b"
        )
        self.search_entry.bind("<Return>", lambda event: self.search_members())
        self.search_entry.pack(side="left", padx=5)

        tk.Button(
            top_bar,
            text="🔍 Search",
            font=("Segoe UI", 12, "bold"),
            bg="#2980b9",
            fg="white",
            activebackground="#3498db",
            command=self.search_members
        ).pack(side="left", padx=10)

        tk.Button(
            top_bar,
            text="🔁 Refresh",
            font=("Segoe UI", 12, "bold"),
            bg="#e67e22",
            fg="white",
            activebackground="#f39c12",
            command=self.refresh_members
        ).pack(side="left", padx=5)

        tk.Button(
            top_bar,
            text="📤 Export to Excel",
            font=("Segoe UI", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            command=self.export_to_excel
        ).pack(side="left", padx=5)

        tree_frame = tk.Frame(self, bg="#f8f9fa")
        tree_frame.pack(expand=True, fill="both", pady=20, padx=30)

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Phone", "Start", "End", "Fees", "Address", "Pincode"),
            show="headings",
            height=10
        )

        for col in ("ID", "Name", "Phone", "Start", "End", "Fees", "Address", "Pincode"):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="w", width=130)

        self.tree.pack(side="left", expand=True, fill="both")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.no_results_label = tk.Label(
            self,
            text="",
            font=("Segoe UI", 12, "italic"),
            fg="#c0392b",
            bg="#f8f9fa"
        )
        self.no_results_label.pack()

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            font=("Segoe UI", 11),
            rowheight=36,
            background="white",
            foreground="#2c3e50",
            fieldbackground="white"
        )
        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 13, "bold"),
            background="#e74c3c",
            foreground="white"
        )
        style.map("Treeview", background=[("selected", "#fddede")])

    # ================= SEARCH =================
    def search_members(self):
        query = self.search_entry.get().strip()
        self.load_expired_members(query)

    def refresh_members(self):
        self.search_entry.delete(0, tk.END)
        self.load_expired_members()

    # ================= DATA LOAD =================
    def load_expired_members(self, query=""):
        today = date.today()
        members = fetch_expired_members()

        # ---- Last 3 months filter ----
        try:
            three_months_ago = today.replace(month=today.month - 3) \
                if today.month > 3 else today.replace(year=today.year - 1, month=12 + today.month - 3)
        except ValueError:
            three_months_ago = date(today.year, today.month - 3 if today.month > 3 else 12 + today.month - 3, 1)

        filtered_members = []
        for m in members:
            try:
                date_str = m[4]  # End date
                if date_str and "-" in date_str:
                    parts = date_str.split("-")
                    if len(parts[0]) <= 2:  # dd-mm-yyyy
                        end_date = date(int(parts[2]), int(parts[1]), int(parts[0]))
                    else:  # yyyy-mm-dd
                        end_date = date(int(parts[0]), int(parts[1]), int(parts[2]))

                    if three_months_ago <= end_date < today:
                        filtered_members.append(m)
            except:
                continue

        members = filtered_members

        # ---- SEARCH FILTER (FIXED LOGIC) ----
        query = query.strip()
        if query:
            if query.isdigit():
                query_int = int(query)
                members = [
                    m for m in members
                    if (
                        isinstance(m[0], int) and m[0] == query_int   # EXACT ID
                    ) or (
                        str(m[2]).strip() == query                   # EXACT phone
                    )
                ]
            else:
                members = [
                    m for m in members
                    if query.lower() in str(m[1]).lower()            # NAME partial
                ]

        # ---- UPDATE TABLE ----
        self.tree.delete(*self.tree.get_children())
        self.no_results_label.config(text="")

        if members:
            for member in members:
                self.tree.insert("", "end", values=member)
            if query:
                self.no_results_label.config(text=f"Found {len(members)} expired member(s)")
        else:
            if query:
                self.no_results_label.config(text="No matching expired members found")
            else:
                self.no_results_label.config(text="No expired members in the last 3 months")

    # ================= EXPORT =================
    def export_to_excel(self):
        rows = [self.tree.item(item)["values"] for item in self.tree.get_children()]
        if not rows:
            messagebox.showwarning("No Data", "No data to export.")
            return

        df = pd.DataFrame(
            rows,
            columns=["ID", "Name", "Phone", "Start", "End", "Fees", "Address", "Pincode"]
        )

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )

        if file_path:
            try:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Data exported successfully to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data:\n{e}")



