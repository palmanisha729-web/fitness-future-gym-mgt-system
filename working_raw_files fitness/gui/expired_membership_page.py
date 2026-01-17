# import tkinter as tk
# from tkinter import ttk, messagebox
# from database.member_ops import fetch_all_members, delete_member_by_id
# from datetime import datetime, timedelta

# class ExpiredMembersPage(tk.Frame):
#     def __init__(self, master):
#         super().__init__(master, bg="#ecf0f3")
#         self.pack(fill="both", expand=True)
#         self.build_ui()
#         self.show_expired_members()

#     def build_ui(self):
#         # Modern title with beautiful styling
#         title_frame = tk.Frame(self, bg="#ecf0f3")
#         title_frame.pack(pady=(25, 10))
        
#         tk.Label(
#             title_frame, text="⏳ Expired Memberships",
#             font=("Segoe UI", 28, "bold"), bg="#ecf0f3", fg="#e74c3c"
#         ).pack()
        
#         tk.Label(
#             title_frame, text="(3+ Months Overdue)",
#             font=("Segoe UI", 14), bg="#ecf0f3", fg="#7f8c8d"
#         ).pack(pady=(5, 0))

#         top_bar = tk.Frame(self, bg="#ecf0f3")
#         top_bar.pack(pady=20)

#         tk.Label(top_bar, text="🔍 Search:", font=("Segoe UI", 12, "bold"), bg="#ecf0f3", fg="#2c3e50").pack(side="left", padx=(0, 10))

#         self.search_entry = tk.Entry(
#             top_bar, font=("Segoe UI", 13),
#             width=40, relief="flat", bg="white", fg="#2c3e50",
#             highlightthickness=2, highlightcolor="#e74c3c", highlightbackground="#bdc3c7"
#         )
        
#         self.search_entry.bind("<Return>", lambda event: self.search_expired_members())
#         self.search_entry.pack(side="left", padx=10, ipady=8)

#         search_btn = tk.Button(
#             top_bar, text="🔍 Search", font=("Segoe UI", 12, "bold"),
#             bg="#3498db", fg="white", activebackground="#2980b9",
#             bd=0, relief="flat", cursor="hand2", padx=15, pady=8,
#             command=self.search_expired_members
#         )
#         search_btn.pack(side="left", padx=10)

#         refresh_btn = tk.Button(
#             top_bar, text="🔁 Refresh", font=("Segoe UI", 12, "bold"),
#             bg="#f39c12", fg="white", activebackground="#e67e22",
#             bd=0, relief="flat", cursor="hand2", padx=15, pady=8,
#             command=self.show_expired_members
#         )
#         refresh_btn.pack(side="left", padx=5)


#         # Treeview
#         tree_outer_frame = tk.Frame(self, bg="#ecf0f3")
#         tree_outer_frame.pack(pady=20, fill="both", expand=True, padx=30)

#         tree_frame = tk.Frame(tree_outer_frame, bg="#ffffff", bd=1, relief="solid")
#         tree_frame.pack(fill="both", expand=True)

#         self.member_tree = ttk.Treeview(
#             tree_frame,
#             columns=("ID", "Name", "Phone", "Start Date", "End Date", "Days Overdue", "Fees", "Address", "Pincode"),
#             show="headings", height=10
#         )

#         for col in self.member_tree["columns"]:
#             self.member_tree.heading(col, text=col)
#             self.member_tree.column(col, anchor="w", width=140)

#         self.member_tree.pack(side="left", expand=True, fill="both", padx=(5, 0), pady=5)

#         scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.member_tree.yview)
#         self.member_tree.configure(yscrollcommand=scrollbar.set)
#         scrollbar.pack(side="right", fill="y")

#         self.no_results_label = tk.Label(
#             self, text="", font=("Segoe UI", 12, "italic"), fg="red", bg="#ecf0f3"
#         )
#         self.no_results_label.pack()

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

#         # Delete Button with modern styling
#         delete_btn = tk.Button(
#             self, text="🗑️ Delete Selected Member",
#             font=("Segoe UI", 13, "bold"), bg="#e74c3c", fg="white",
#             activebackground="#c0392b", activeforeground="white",
#             padx=25, pady=10, relief="flat", cursor="hand2", bd=0,
#             command=self.delete_selected_member
#         )
#         delete_btn.pack(pady=(10, 15))
#         delete_btn.bind("<Enter>", lambda e: delete_btn.config(bg="#c0392b"))
#         delete_btn.bind("<Leave>", lambda e: delete_btn.config(bg="#e74c3c"))

#     def show_expired_members(self):
#         all_members = fetch_all_members()
#         expired_list = []
#         today = datetime.today()
#         threshold_date = today - timedelta(days=90)

#         for member in all_members:
#             try:
#                 # Date comes in dd-mm-yyyy format
#                 date_str = member[4]
#                 if date_str and '-' in date_str:
#                     parts = date_str.split('-')
#                     if len(parts) == 3 and len(parts[0]) <= 2:  # dd-mm-yyyy format
#                         end_date = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
#                     else:  # yyyy-mm-dd format (legacy)
#                         end_date = datetime.strptime(date_str, "%Y-%m-%d")
#                 else:
#                     continue
                    
#                 if end_date < threshold_date:
#                     days_overdue = (today - end_date).days - 90
#                     modified_member = member[:5] + (days_overdue,) + member[5:]
#                     expired_list.append(modified_member)
#             except Exception as e:
#                 print(f"Error parsing member {member}: {e}")
#                 continue

#         self.update_tree(expired_list)
#         self.no_results_label.config(text=f"{len(expired_list)} memberships expired (3+ months ago)")

#     def search_expired_members(self):
#         query = self.search_entry.get().strip().lower()
#         if not query or query == "search by id / name / phone":
#             self.no_results_label.config(text="Please enter a search query.")
#             return

#         all_members = fetch_all_members()
#         expired_list = []
#         today = datetime.today()
#         threshold_date = today - timedelta(days=90)

#         for member in all_members:
#             try:
#                 # Date comes in dd-mm-yyyy format
#                 date_str = member[4]
#                 if date_str and '-' in date_str:
#                     parts = date_str.split('-')
#                     if len(parts) == 3 and len(parts[0]) <= 2:  # dd-mm-yyyy format
#                         end_date = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
#                     else:  # yyyy-mm-dd format (legacy)
#                         end_date = datetime.strptime(date_str, "%Y-%m-%d")
#                 else:
#                     continue
                    
#                 if end_date >= threshold_date:
#                     continue
#                 id_str = str(member[0]).lower()
#                 name = member[1].lower() if member[1] else ""
#                 phone = str(member[2]).lower() if member[2] else ""
#                 if query in id_str or query in name or query in phone:
#                     days_overdue = (today - end_date).days - 90
#                     modified_member = member[:5] + (days_overdue,) + member[5:]
#                     expired_list.append(modified_member)
#             except Exception as e:
#                 print(f"Search error for {member}: {e}")
#                 continue

#         if expired_list:
#             self.update_tree(expired_list)
#             self.no_results_label.config(text=f"Found {len(expired_list)} expired members matching your search.")
#         else:
#             self.update_tree([])
#             self.no_results_label.config(text="No matching expired members found.")

#     def update_tree(self, data):
#         self.member_tree.delete(*self.member_tree.get_children())
#         for member in data:
#             self.member_tree.insert('', 'end', values=member)

#     def delete_selected_member(self):
#         selected_item = self.member_tree.selection()
#         if not selected_item:
#             messagebox.showwarning("No Selection", "Please select a member to delete.")
#             return

#         confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected member?")
#         if not confirm:
#             return

#         member_data = self.member_tree.item(selected_item)["values"]
#         member_id = member_data[0]  # Assuming ID is the first column

#         try:
#             delete_member_by_id(member_id)
#             self.member_tree.delete(selected_item)
#             self.no_results_label.config(text=f"Member ID {member_id} deleted.")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to delete member: {e}")


import tkinter as tk
from tkinter import ttk, messagebox
from database.member_ops import fetch_all_members, delete_member_by_id
from datetime import datetime, timedelta


class ExpiredMembersPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#ecf0f3")
        self.pack(fill="both", expand=True)
        self.build_ui()
        self.show_expired_members()

    # ================= UI =================
    def build_ui(self):
        title_frame = tk.Frame(self, bg="#ecf0f3")
        title_frame.pack(pady=(25, 10))

        tk.Label(
            title_frame,
            text="⏳ Expired Memberships",
            font=("Segoe UI", 28, "bold"),
            bg="#ecf0f3",
            fg="#e74c3c"
        ).pack()

        tk.Label(
            title_frame,
            text="(3+ Months Overdue)",
            font=("Segoe UI", 14),
            bg="#ecf0f3",
            fg="#7f8c8d"
        ).pack(pady=(5, 0))

        top_bar = tk.Frame(self, bg="#ecf0f3")
        top_bar.pack(pady=20)

        tk.Label(
            top_bar,
            text="🔍 Search:",
            font=("Segoe UI", 12, "bold"),
            bg="#ecf0f3"
        ).pack(side="left", padx=(0, 10))

        self.search_entry = tk.Entry(
            top_bar,
            font=("Segoe UI", 13),
            width=40,
            relief="flat",
            bg="white",
            fg="#2c3e50",
            highlightthickness=2,
            highlightcolor="#e74c3c",
            highlightbackground="#bdc3c7"
        )
        self.search_entry.bind("<Return>", lambda e: self.search_expired_members())
        self.search_entry.pack(side="left", padx=10, ipady=8)

        tk.Button(
            top_bar,
            text="🔍 Search",
            font=("Segoe UI", 12, "bold"),
            bg="#3498db",
            fg="white",
            activebackground="#2980b9",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.search_expired_members
        ).pack(side="left", padx=10)

        tk.Button(
            top_bar,
            text="🔁 Refresh",
            font=("Segoe UI", 12, "bold"),
            bg="#f39c12",
            fg="white",
            activebackground="#e67e22",
            bd=0,
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.show_expired_members
        ).pack(side="left", padx=5)

        # ================= TABLE =================
        tree_outer = tk.Frame(self, bg="#ecf0f3")
        tree_outer.pack(pady=20, fill="both", expand=True, padx=30)

        tree_frame = tk.Frame(tree_outer, bg="white", bd=1, relief="solid")
        tree_frame.pack(fill="both", expand=True)

        self.member_tree = ttk.Treeview(
            tree_frame,
            columns=("ID", "Name", "Phone", "Start Date", "End Date",
                     "Days Overdue", "Fees", "Address", "Pincode"),
            show="headings",
            height=10
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

        tk.Button(
            self,
            text="🗑️ Delete Selected Member",
            font=("Segoe UI", 13, "bold"),
            bg="#e74c3c",
            fg="white",
            activebackground="#c0392b",
            padx=25,
            pady=10,
            relief="flat",
            cursor="hand2",
            command=self.delete_selected_member
        ).pack(pady=(10, 15))

    # ================= DATA =================
    def get_expired_members(self):
        today = datetime.today()
        threshold = today - timedelta(days=90)
        expired = []

        for m in fetch_all_members():
            try:
                parts = str(m[4]).split("-")
                if len(parts[0]) <= 2:
                    end_date = datetime(int(parts[2]), int(parts[1]), int(parts[0]))
                else:
                    end_date = datetime.strptime(m[4], "%Y-%m-%d")

                if end_date < threshold:
                    days_overdue = (today - end_date).days - 90
                    expired.append(m[:5] + (days_overdue,) + m[5:])
            except:
                continue

        return expired

    # ================= SHOW ALL =================
    def show_expired_members(self):
        data = self.get_expired_members()
        self.update_tree(data)
        self.no_results_label.config(
            text=f"{len(data)} memberships expired (3+ months ago)"
        )

    # ================= SEARCH (FINAL FIXED) =================
    def search_expired_members(self):
        query = self.search_entry.get().strip()
        if not query:
            self.no_results_label.config(text="Please enter a search query.")
            return

        expired_list = self.get_expired_members()
        results = []

        # -------- DIGIT SEARCH --------
        if query.isdigit():
            # SHORT NUMBER → ID ONLY (NO PHONE FALLBACK)
            if len(query) <= 4:
                qid = int(query)
                results = [m for m in expired_list if int(m[0]) == qid]

                if not results:
                    self.update_tree([])
                    self.no_results_label.config(
                        text=f"No expired member found with ID {query}"
                    )
                    return

            # LONG NUMBER → PHONE PARTIAL
            else:
                results = [
                    m for m in expired_list
                    if query in str(m[2]).replace(".0", "")
                ]

        # -------- NAME SEARCH --------
        else:
            q = query.lower()
            results = [
                m for m in expired_list
                if q in str(m[1]).lower()
            ]

        if results:
            self.update_tree(results)
            self.no_results_label.config(
                text=f"Found {len(results)} expired member(s)"
            )
        else:
            self.update_tree([])
            self.no_results_label.config("No matching expired members found.")

    # ================= TABLE =================
    def update_tree(self, data):
        self.member_tree.delete(*self.member_tree.get_children())
        for row in data:
            self.member_tree.insert("", "end", values=row)

    # ================= DELETE =================
    def delete_selected_member(self):
        selected = self.member_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a member to delete.")
            return

        member_id = self.member_tree.item(selected)["values"][0]

        if not messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete member ID {member_id}?"
        ):
            return

        try:
            delete_member_by_id(member_id)
            self.member_tree.delete(selected)
            self.no_results_label.config(text=f"Member ID {member_id} deleted.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete member:\n{e}")
