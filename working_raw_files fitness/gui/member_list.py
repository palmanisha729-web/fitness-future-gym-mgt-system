# import tkinter as tk
# from tkinter import ttk, messagebox
# from database.member_ops import fetch_all_members
# import openpyxl
# from tkinter import filedialog

# class MemberListPage(tk.Frame):
#     def __init__(self, master):
#         super().__init__(master, bg="#ecf0f3")
#         self.pack(fill="both", expand=True)

#         self.build_ui()
#         self.refresh_data()

#         # Export Button Frame
#         export_frame = tk.Frame(self, bg="#ecf0f3")
#         export_frame.pack(pady=10, fill="x")

#     def build_ui(self):
#         # Title (Centered)
#         title_frame = tk.Frame(self, bg="#ecf0f3")
#         title_frame.pack(fill="x")
#         tk.Label(
#             title_frame, text="🏋️ All Gym Members",
#             font=("Segoe UI", 26, "bold"), bg="#ecf0f3", fg="#2c3e50"
#         ).pack(pady=(25, 10))

#         # Top bar
#         top_bar = tk.Frame(self, bg="#ecf0f3")
#         top_bar.pack(pady=20)

#         tk.Label(top_bar, text="Search (Name/Id/Phone):", font=("Segoe UI", 12), bg="#ecf0f3").pack(side="left", padx=(0, 10))

#         self.search_entry = tk.Entry(top_bar, font=("Segoe UI", 12), width=25, fg="#2c3e50", bg="white", relief="flat", highlightthickness=1, highlightbackground="#27ae60")
#         self.search_entry.pack(side="left", padx=5)

#         search_btn = tk.Button(
#             top_bar, text="🔍 Search", font=("Segoe UI", 12, "bold"),
#             bg="#2980b9", fg="white", activebackground="#3498db",
#             command=self.search_members
#         )
#         search_btn.pack(side="left", padx=10)

#         refresh_btn = tk.Button(
#             top_bar, text="🔁 Refresh", font=("Segoe UI", 12, "bold"),
#             bg="#e67e22", fg="white", activebackground="#f39c12",
#             command=self.refresh_data
#         )
#         refresh_btn.pack(side="left", padx=5)

#         export_btn = tk.Button(
#             top_bar, text="📤 Export to Excel",  # added an icon for better look
#             font=("Segoe UI", 12, "bold"),
#             bg="#27ae60", fg="white", activebackground="#2ecc71",
#             command=lambda: self.export_to_excel(self.get_tree_data())
#         )
#         export_btn.pack(side="left", padx=5)


#         # Treeview Frame
#         tree_outer_frame = tk.Frame(self, bg="#ecf0f3")
#         tree_outer_frame.pack(pady=20, fill="both", expand=True, padx=30)

#         tree_frame = tk.Frame(tree_outer_frame, bg="#ffffff", bd=1, relief="solid")
#         tree_frame.pack(fill="both", expand=True)

#         self.member_tree = ttk.Treeview(
#             tree_frame,
#             columns=("ID", "Name", "Phone", "Start Date", "End Date", "Fees", "Address", "Pincode"),
#             show="headings", height=10
#         )

#         for col in self.member_tree["columns"]:
#             self.member_tree.heading(col, text=col)
#             self.member_tree.column(col, anchor="w", width=140)

#         self.member_tree.pack(side="left", expand=True, fill="both", padx=(5, 0), pady=5)

#         scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.member_tree.yview)
#         self.member_tree.configure(yscrollcommand=scrollbar.set)
#         scrollbar.pack(side="right", fill="y")

#         # No results label
#         self.no_results_label = tk.Label(
#             self, text="", font=("Segoe UI", 12, "italic"),
#             fg="red", bg="#ecf0f3"
#         )
#         self.no_results_label.pack()
#         self.search_entry.bind("<Return>", lambda event: self.search_members()) # ✅ Bind Enter key to Search


#         # Style
#         style = ttk.Style()
#         style.theme_use("clam")
#         style.configure("Treeview",
#             font=("Segoe UI", 11), rowheight=36,
#             background="white", foreground="#2c3e50", fieldbackground="white"
#         )
#         style.configure("Treeview.Heading",
#             font=("Segoe UI", 13, "bold"),
#             background="#3498db", foreground="white"
#         )
#         style.map("Treeview", background=[("selected", "#85c1e9")])

#     def refresh_data(self):
#         self.search_entry.delete(0, tk.END)
#         self.no_results_label.config(text="")
#         self.update_tree(fetch_all_members())

#     def search_members(self):
#         query = self.search_entry.get().strip()
#         if not query:
#             self.refresh_data()
#             return

#         self.no_results_label.config(text="")

#         all_members = fetch_all_members()
#         filtered = []

#         # Check if query is numeric (ID or Phone)
#         if query.isdigit():
#             # Exact match for ID or Phone
#             for member in all_members:
#                 if str(member[0]) == query or str(member[2]) == query:
#                     filtered.append(member)
#         else:
#             # Partial match for Name (case insensitive)
#             query_lower = query.lower()
#             for member in all_members:
#                 name_lower = str(member[1]).lower() if member[1] else ""
#                 if query_lower in name_lower:
#                     filtered.append(member)

#         if filtered:
#             self.update_tree(filtered)
#             if len(filtered) != len(all_members):
#                 self.no_results_label.config(text=f"Found {len(filtered)} member(s)")
#         else:
#             self.update_tree([]) 
#             self.no_results_label.config(text="No matching members found")

#     def update_tree(self, data):
#         self.member_tree.delete(*self.member_tree.get_children())
#         for member in data:
#             self.member_tree.insert('', 'end', values=member)

#     def get_tree_data(self):
#         items = self.member_tree.get_children()
#         return [self.member_tree.item(item)['values'] for item in items]

#     def export_to_excel(self, data):
#         file_path = filedialog.asksaveasfilename(
#             defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")]
#         )
#         if not file_path:
#             return
#         wb = openpyxl.Workbook()
#         ws = wb.active
#         headers = ["ID", "Name", "Phone", "Start Date", "End Date", "Fees", "Address", "Pincode"]
#         ws.append(headers)
#         for row in data:
#             ws.append(row)
#         wb.save(file_path)
#         messagebox.showinfo("Success", "✅ Exported to Excel successfully!")



import tkinter as tk
from tkinter import ttk, messagebox
from database.member_ops import fetch_all_members
import openpyxl
from tkinter import filedialog


class MemberListPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#ecf0f3")
        self.pack(fill="both", expand=True)

        self.build_ui()
        self.refresh_data()

    # ================= UI =================
    def build_ui(self):
        title_frame = tk.Frame(self, bg="#ecf0f3")
        title_frame.pack(fill="x")
        tk.Label(
            title_frame,
            text="🏋️ All Gym Members",
            font=("Segoe UI", 26, "bold"),
            bg="#ecf0f3",
            fg="#2c3e50"
        ).pack(pady=(25, 10))

        top_bar = tk.Frame(self, bg="#ecf0f3")
        top_bar.pack(pady=20)

        tk.Label(
            top_bar,
            text="Search (Name / ID / Phone):",
            font=("Segoe UI", 12),
            bg="#ecf0f3"
        ).pack(side="left", padx=(0, 10))

        self.search_entry = tk.Entry(
            top_bar,
            font=("Segoe UI", 12),
            width=25,
            fg="#2c3e50",
            bg="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#27ae60"
        )
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda e: self.search_members())

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
            command=self.refresh_data
        ).pack(side="left", padx=5)

        tk.Button(
            top_bar,
            text="📤 Export to Excel",
            font=("Segoe UI", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#2ecc71",
            command=lambda: self.export_to_excel(self.get_tree_data())
        ).pack(side="left", padx=5)

        tree_outer_frame = tk.Frame(self, bg="#ecf0f3")
        tree_outer_frame.pack(pady=20, fill="both", expand=True, padx=30)

        tree_frame = tk.Frame(tree_outer_frame, bg="#ffffff", bd=1, relief="solid")
        tree_frame.pack(fill="both", expand=True)

        self.member_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Phone", "Start Date", "End Date", "Fees", "Address", "Pincode"),
            show="headings", height=10
        )

        for col in self.member_tree["columns"]:
            self.member_tree.heading(col, text=col)
            self.member_tree.column(col, anchor="w", width=140)

        self.member_tree.pack(side="left", expand=True, fill="both", padx=(5, 0), pady=5)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.member_tree.yview)
        self.member_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.no_results_label = tk.Label(
            self,
            text="",
            font=("Segoe UI", 12, "italic"),
            fg="red",
            bg="#ecf0f3"
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
            background="#3498db",
            foreground="white"
        )
        style.map("Treeview", background=[("selected", "#85c1e9")])

    # ================= DATA =================
    def refresh_data(self):
        self.search_entry.delete(0, tk.END)
        self.no_results_label.config(text="")
        self.update_tree(fetch_all_members())

    # ================= SEARCH (FIXED) =================
    def search_members(self):
        query = self.search_entry.get().strip()
        if not query:
            self.refresh_data()
            return

        all_members = fetch_all_members()
        results = []

        if query.isdigit():
            query_int = int(query)

            # 1️⃣ Exact ID match
            id_matches = [m for m in all_members if int(m[0]) == query_int]

            if id_matches:
                results = id_matches
            else:
                # 2️⃣ Partial phone match
                results = [
                    m for m in all_members
                    if query in str(m[2]).replace(".0", "")
                ]
        else:
            # 3️⃣ Partial name match
            q = query.lower()
            results = [
                m for m in all_members
                if q in str(m[1]).lower()
            ]

        if results:
            self.update_tree(results)
            self.no_results_label.config(text=f"Found {len(results)} member(s)")
        else:
            self.update_tree([])
            self.no_results_label.config(text="No matching members found")

    # ================= TABLE =================
    def update_tree(self, data):
        self.member_tree.delete(*self.member_tree.get_children())
        for member in data:
            self.member_tree.insert("", "end", values=member)

    def get_tree_data(self):
        return [self.member_tree.item(i)["values"] for i in self.member_tree.get_children()]

    # ================= EXPORT =================
    def export_to_excel(self, data):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if not file_path:
            return

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["ID", "Name", "Phone", "Start Date", "End Date", "Fees", "Address", "Pincode"])

        for row in data:
            ws.append(row)

        wb.save(file_path)
        messagebox.showinfo("Success", "✅ Exported to Excel successfully!")


