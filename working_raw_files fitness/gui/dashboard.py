# main.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import date
from utils.path_utils import resource_path

# === GUI Pages ===
from gui.member_list import MemberListPage
from gui.add_member import AddMemberPage
from gui.update_member import UpdateMemberPage
from gui.delete_member import DeleteMemberPage
from gui.expired_member import ExpiredMembershipPage
from gui.extend_membership import ExtendMembershipPage
from gui.expired_membership_page import ExpiredMembersPage
from gui.drag_drop_import import DragDropImportPage
from gui.report import ReportPage


# === Dashboard ===
def open_dashboard(root):
    dashboard = tk.Toplevel(root)
    dashboard.title("Gym Dashboard - FITNESS FUTURE")
    
    # Maximize the window
    dashboard.state('zoomed')  # Windows maximize
    
    dashboard.resizable(True, True)
    dashboard.configure(bg="#001f3f")
    dashboard.protocol("WM_DELETE_WINDOW", lambda: close_app(root))

    # Sidebar
    sidebar = tk.Frame(dashboard, bg="#001f3f", width=250, relief="solid", bd=1)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    # Main area
    main_area = tk.Frame(dashboard, bg="white")
    main_area.pack(side="right", fill="both", expand=True)

    # Logo section
    logo_container = tk.Frame(sidebar, bg="#001f3f")
    logo_container.pack(pady=10, padx=10)
    
    logo_img = Image.open(resource_path("assets/5.png")).resize((180, 180), Image.Resampling.LANCZOS)
    logo_img = ImageTk.PhotoImage(logo_img)
    logo_label = tk.Label(logo_container, image=logo_img, bg="#001f3f", cursor="hand2")
    logo_label.image = logo_img
    logo_label.pack()

    # Welcome section
    welcome_frame = tk.Frame(sidebar, bg="#001f3f")
    welcome_frame.pack(pady=8)
    
    welcome_label = tk.Label(
        welcome_frame, 
        text="Welcome Admin", 
        font=("Segoe UI", 15, "bold"), 
        fg="white", 
        bg="#001f3f"
    )
    welcome_label.pack()
    
    # Separator line
    tk.Frame(sidebar, bg="#0074D9", height=2).pack(fill="x", padx=20, pady=10)

    cards_visible = True
    card_widgets = []

    def toggle_cards():
        nonlocal cards_visible
        if not card_widgets:
            create_cards()
            cards_visible = True
            return

        if cards_visible:
            hide_cards()
        else:
            show_cards()
        cards_visible = not cards_visible

    logo_label.bind("<Button-1>", lambda e: toggle_cards())

    # Button styling
    button_style = {
        "font": ("Segoe UI", 11),
        "bg": "#002b5c",
        "fg": "white",
        "activebackground": "#0074D9",
        "activeforeground": "white",
        "bd": 0,
        "anchor": "w",
        "padx": 20,
        "pady": 10,
        "cursor": "hand2",
        "relief": "flat"
    }
    
    # Navigation buttons with canvas for scrolling
    nav_container = tk.Frame(sidebar, bg="#001f3f")
    nav_container.pack(fill="both", expand=True, pady=5, padx=10)
    
    canvas = tk.Canvas(nav_container, bg="#001f3f", highlightthickness=0)
    scrollbar = tk.Scrollbar(nav_container, orient="vertical", command=canvas.yview, bg="#001f3f")
    nav_frame = tk.Frame(canvas, bg="#001f3f")
    
    nav_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=nav_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Enable mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def create_nav_button(text, page_cls):
        btn = tk.Button(
            nav_frame, 
            text=text, 
            command=lambda: show_in_main_area(page_cls, main_area), 
            **button_style
        )
        btn.pack(fill="x", pady=3, padx=5)
        btn.bind("<Enter>", lambda e: on_enter(e))
        btn.bind("<Leave>", lambda e: on_leave(e))
        return btn

    create_nav_button("Add Member", AddMemberPage)
    create_nav_button("Update Member", UpdateMemberPage)
    create_nav_button("Delete Member", DeleteMemberPage)
    create_nav_button("Expired 3+ months", ExpiredMembersPage)
    create_nav_button("Extend Membership", ExtendMembershipPage)
    create_nav_button("Expired List", ExpiredMembershipPage)
    create_nav_button("Member List", MemberListPage)
    create_nav_button("Import Excel", DragDropImportPage)
    create_nav_button("Reports", ReportPage)
    
    # Separator line before logout
    tk.Frame(nav_frame, bg="#0074D9", height=2).pack(fill="x", padx=0, pady=10)
    
    # Logout button in navigation
    logout_nav_btn = tk.Button(
        nav_frame, 
        text="⏻ Logout", 
        command=lambda: logout(root),
        font=("Segoe UI", 11, "bold"),
        bg="#d32f2f",
        fg="white",
        activebackground="#f44336",
        activeforeground="white",
        bd=0,
        anchor="w",
        padx=20,
        pady=10,
        cursor="hand2",
        relief="flat"
    )
    logout_nav_btn.pack(fill="x", pady=3, padx=5)
    logout_nav_btn.bind("<Enter>", lambda e: e.widget.configure(bg="#f44336"))
    logout_nav_btn.bind("<Leave>", lambda e: e.widget.configure(bg="#d32f2f"))

    # Header
    header_frame = tk.Frame(main_area, bg="#0074D9", height=70)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    # Add bottom border to header
    tk.Frame(header_frame, bg="#005bb5", height=3).pack(side="bottom", fill="x")
    
    tk.Label(
        header_frame, 
        text="FITNESS FUTURE - Gym Management System", 
        font=("Segoe UI", 20, "bold"), 
        bg="#0074D9", 
        fg="white"
    ).pack(pady=18, padx=30, anchor="w")

    from database.member_ops import (
        fetch_total_members, fetch_expired_members,
        fetch_joining_today, fetch_inactive_members
    )
    today = date.today().isoformat()
    total = fetch_total_members()
    expired = len(fetch_expired_members(today))
    joining_today = len(fetch_joining_today())
    inactive = len(fetch_inactive_members())

    cards = [
        ("Total Members", total, "#3b82f6", "✅"),  # Blue
        ("Expired Members", expired, "#ef4444", "⛔"),  # Red
        ("Joined Today", joining_today, "#10b981", "🕕"),  # Green
        ("Inactive >30 Days", inactive, "#f59e0b", "📞")  # Orange
    ]

    def create_shadow_card(master, title, count, color, emoji):
        # Card with shadow
        card_outer = tk.Frame(master, bg="#e0e0e0")
        card_outer.configure(width=320, height=150)
        card_outer.pack_propagate(False)
        
        # Main card
        card = tk.Frame(card_outer, bg=color, relief="flat", bd=0)
        card.place(x=0, y=0, width=316, height=146)
        
        # Count
        tk.Label(
            card, 
            text=str(count), 
            font=("Segoe UI", 42, "bold"), 
            bg=color, 
            fg="white"
        ).pack(pady=(20, 5))
        
        # Title
        tk.Label(
            card, 
            text=title, 
            font=("Segoe UI", 13, "bold"), 
            bg=color, 
            fg="white"
        ).pack()
        
        return card_outer
    
    # Cards container
    cards_container = tk.Frame(main_area, bg="#f5f5f5")
    cards_container.pack(fill="both", expand=True, padx=20, pady=20)
    
    cards_frame = tk.Frame(cards_container, bg="#f5f5f5")
    cards_frame.pack()

    def create_cards():
        card_widgets.clear()
        for i, (title, count, color, emoji) in enumerate(cards):
            canvas = create_shadow_card(cards_frame, title, count, color, emoji)
            card_widgets.append(canvas)
            canvas.grid(row=i//2, column=i%2, padx=20, pady=20)

    def hide_cards():
        for card in card_widgets:
            try:
                card.grid_forget()
            except:
                pass

    def show_cards():
        for i, card in enumerate(card_widgets):
            try:
                card.grid(row=i//2, column=i%2, padx=20, pady=20)
            except:
                pass

    create_cards()

current_page_name = None

def show_in_main_area(page_cls, main_area):
    global current_page_name
    if current_page_name == page_cls.__name__:
        return
    current_page_name = page_cls.__name__

    for widget in main_area.winfo_children():
        widget.destroy()
    page = page_cls(main_area)
    page.pack(fill="both", expand=True)

def on_enter(e): 
    e.widget['bg'] = '#0088FF'
    
def on_leave(e): 
    e.widget['bg'] = '#002b5c'

def logout(root):
    if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
        root.quit()
        root.destroy()

def close_app(root):
    if messagebox.askokcancel("Quit", "Do you really want to exit?"):
        root.quit()
        root.destroy()
