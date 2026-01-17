from tkinterdnd2 import TkinterDnD
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk, ImageFilter, ImageEnhance
from utils.path_utils import resource_path
from gui.dashboard import open_dashboard
from database.credentials import init_credentials_table, verify_credentials, update_credentials, reset_to_default

# === Login Screen ===
def start_app():
    # Initialize credentials table
    init_credentials_table()
    
    root = TkinterDnD.Tk()
    root.title("Gym Management Login")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"{screen_width}x{screen_height}")
    root.state('zoomed')  # Maximize window on startup
    root.resizable(True, True)

    # ---- Create Main Container with Modern Gradient ----
    main_frame = tk.Frame(root, bg="#000000")
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)

    # ---- Left Side: Gym Hero Image with Modern Overlay ----
    left_frame = tk.Frame(main_frame, bg="#1a1a1a")
    left_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    try:
        # Try to load the gym hero image first, fallback to photo1.png
        try:
            gym_img = Image.open(resource_path("assets/gym_hero.jpg"))
        except:
            # Fallback to existing photo1.png if gym_hero.jpg doesn't exist
            gym_img = Image.open(resource_path("assets/photo1.png"))
            
        gym_img = gym_img.resize((int(screen_width*0.5), screen_height), Image.Resampling.LANCZOS)
        
        # Enhance the image slightly
        enhancer = ImageEnhance.Brightness(gym_img)
        gym_img = enhancer.enhance(0.85)
        
        gym_photo = ImageTk.PhotoImage(gym_img)
        gym_label = tk.Label(left_frame, image=gym_photo, bg="#000000")
        gym_label.image = gym_photo
        gym_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Add overlay text on image
        overlay_frame = tk.Frame(left_frame, bg="#000000")
        overlay_frame.place(relx=0.5, rely=0.85, anchor="center")
        
        tk.Label(
            overlay_frame,
            text="💪 TRANSFORM YOUR BODY",
            font=("Arial Black", 24, "bold"),
            fg="white",
            bg="#000000"
        ).pack()
        
        tk.Label(
            overlay_frame,
            text="Build Strength • Gain Confidence • Achieve Goals",
            font=("Arial", 14),
            fg="#dddddd",
            bg="#000000"
        ).pack(pady=5)
        
    except Exception as e:
        print(f"Could not load gym image: {e}")
        # Fallback: Create gradient background
        tk.Label(
            left_frame,
            text="💪",
            font=("Arial", 200),
            fg="#333333",
            bg="#000000"
        ).place(relx=0.5, rely=0.5, anchor="center")

    # ---- Right Side: Modern Login Form ----
    right_frame = tk.Frame(main_frame, bg="#000000")
    right_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    # Modern Login Container with Card Effect
    login_container = tk.Frame(right_frame, bg="#000000")
    login_container.place(relx=0.5, rely=0.5, anchor="center")

    # ---- Modern Logo/Title with Gradient Effect ----
    title_frame = tk.Frame(login_container, bg="#000000")
    title_frame.pack(pady=(0, 10))
    
    title_label = tk.Label(
        title_frame,
        text="🏋️FITNESS FUTURE",
        font=("Segoe UI", 42, "bold"),
        fg="#00d4ff",
        bg="#000000",
        compound="left"
    )
    title_label.pack()
    
    # Update to get actual width, then create properly centered underline
    title_frame.update_idletasks()
    title_width = title_label.winfo_reqwidth()
    
    # Animated underline - perfectly centered under the text
    underline_container = tk.Frame(title_frame, bg="#000000")
    underline_container.pack(pady=10)
    tk.Frame(underline_container, bg="#00d4ff", height=4, width=title_width).pack()

    tk.Label(
        login_container,
        text="✨ Admin Login Portal ✨",
        font=("Segoe UI", 15),
        fg="#aaaaaa",
        bg="#000000"
    ).pack(pady=(0, 40))

    # ---- Modern Username Field with Icon ----
    tk.Label(
        login_container,
        text="👤 USERNAME",
        font=("Segoe UI", 11, "bold"),
        fg="#00d4ff",
        bg="#000000",
        anchor="w"
    ).pack(fill="x", padx=40)

    username_entry = tk.Entry(
        login_container,
        font=("Segoe UI", 15),
        bg="#1a1a1a",
        fg="#ffffff",
        insertbackground='#00d4ff',
        relief="flat",
        bd=0,
        highlightthickness=2,
        highlightcolor="#00d4ff",
        highlightbackground="#333333"
    )
    username_entry.pack(fill="x", padx=40, pady=(8, 25), ipady=14)
    username_entry.focus()

    # ---- Modern Password Field with Icon ----
    tk.Label(
        login_container,
        text="🔒 PASSWORD",
        font=("Segoe UI", 11, "bold"),
        fg="#00d4ff",
        bg="#000000",
        anchor="w"
    ).pack(fill="x", padx=40)

    password_entry = tk.Entry(
        login_container,
        font=("Segoe UI", 15),
        bg="#1a1a1a",
        fg="#ffffff",
        insertbackground='#00d4ff',
        show="●",
        relief="flat",
        bd=0,
        highlightthickness=2,
        highlightcolor="#00d4ff",
        highlightbackground="#333333"
    )
    password_entry.pack(fill="x", padx=40, pady=(8, 10), ipady=14)

    def validate_login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Login Failed", "⚠️ Please enter both username and password")
            return
        
        if verify_credentials(username, password):
            root.withdraw()
            open_dashboard(root)
        else:
            messagebox.showerror("Login Failed", "❌ Invalid username or password")
            password_entry.delete(0, tk.END)

    # ---- Modern Login Button with Gradient Effect ----
    login_button = tk.Button(
        login_container,
        text="🚀  LOGIN",
        font=("Segoe UI", 15, "bold"),
        bg="#00d4ff",
        fg="#000000",
        activebackground="#00b8e6",
        activeforeground="#000000",
        relief="flat",
        bd=0,
        cursor="hand2",
        command=validate_login
    )
    login_button.pack(fill="x", padx=40, pady=(30, 10), ipady=16)

    # Modern button hover effects with smooth transition
    def on_enter(e):
        login_button.config(bg="#00b8e6")
    
    def on_leave(e):
        login_button.config(bg="#00d4ff")
    
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

    # ---- Modern Links Section ----
    links_frame = tk.Frame(login_container, bg="#000000")
    links_frame.pack(pady=20)

    def forgot_password():
        forgot_window = tk.Toplevel(root)
        forgot_window.title("Reset Password")
        forgot_window.geometry("450x400")
        forgot_window.configure(bg="#1a1a1a")
        forgot_window.resizable(False, False)
        
        # Center the window
        forgot_window.transient(root)
        forgot_window.grab_set()

        tk.Label(
            forgot_window,
            text="🔑 Reset Password",
            font=("Arial Black", 20, "bold"),
            fg="white",
            bg="#1a1a1a"
        ).pack(pady=30)

        # New Username
        tk.Label(
            forgot_window,
            text="New Username",
            font=("Arial", 10, "bold"),
            fg="#666666",
            bg="#1a1a1a",
            anchor="w"
        ).pack(fill="x", padx=40, pady=(10, 5))
        
        new_user_entry = tk.Entry(
            forgot_window,
            font=("Arial", 12),
            bg="#2a2a2a",
            fg="white",
            insertbackground='white',
            relief="flat"
        )
        new_user_entry.pack(fill="x", padx=40, ipady=8)

        # New Password
        tk.Label(
            forgot_window,
            text="New Password",
            font=("Arial", 10, "bold"),
            fg="#666666",
            bg="#1a1a1a",
            anchor="w"
        ).pack(fill="x", padx=40, pady=(15, 5))
        
        new_pass_entry = tk.Entry(
            forgot_window,
            font=("Arial", 12),
            bg="#2a2a2a",
            fg="white",
            insertbackground='white',
            show="●",
            relief="flat"
        )
        new_pass_entry.pack(fill="x", padx=40, ipady=8)

        # Confirm Password
        tk.Label(
            forgot_window,
            text="Confirm Password",
            font=("Arial", 10, "bold"),
            fg="#666666",
            bg="#1a1a1a",
            anchor="w"
        ).pack(fill="x", padx=40, pady=(15, 5))
        
        confirm_pass_entry = tk.Entry(
            forgot_window,
            font=("Arial", 12),
            bg="#2a2a2a",
            fg="white",
            insertbackground='white',
            show="●",
            relief="flat"
        )
        confirm_pass_entry.pack(fill="x", padx=40, ipady=8)

        def save_new_password():
            new_username = new_user_entry.get().strip()
            new_password = new_pass_entry.get().strip()
            confirm_password = confirm_pass_entry.get().strip()

            if not all([new_username, new_password, confirm_password]):
                messagebox.showerror("Error", "⚠️ All fields are required")
                return

            if len(new_password) < 6:
                messagebox.showerror("Error", "⚠️ Password must be at least 6 characters")
                return

            if new_password != confirm_password:
                messagebox.showerror("Error", "⚠️ Passwords do not match")
                return

            # Reset to the new credentials
            if reset_to_default():
                # Now update to the user's chosen credentials
                success, message = update_credentials("admin", "admin123", new_username, new_password)
                if success:
                    messagebox.showinfo("Success", f"✅ Password reset successfully!\n\nUsername: {new_username}")
                    forgot_window.destroy()
                    username_entry.delete(0, tk.END)
                    password_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", f"❌ {message}")
            else:
                messagebox.showerror("Error", "❌ Failed to reset password")

        tk.Button(
            forgot_window,
            text="RESET PASSWORD",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            relief="flat",
            cursor="hand2",
            command=save_new_password
        ).pack(fill="x", padx=40, pady=(30, 10), ipady=10)

        tk.Button(
            forgot_window,
            text="CANCEL",
            font=("Arial", 12),
            bg="#444444",
            fg="white",
            activebackground="#555555",
            relief="flat",
            cursor="hand2",
            command=forgot_window.destroy
        ).pack(fill="x", padx=40, pady=(0, 10), ipady=10)

    def change_credentials():
        change_window = tk.Toplevel(root)
        change_window.title("Change Credentials")
        change_window.geometry("450x500")
        change_window.configure(bg="#1a1a1a")
        change_window.resizable(False, False)
        
        # Center the window
        change_window.transient(root)
        change_window.grab_set()

        tk.Label(
            change_window,
            text="🔐 Change Credentials",
            font=("Arial Black", 20, "bold"),
            fg="white",
            bg="#1a1a1a"
        ).pack(pady=30)

        # Current Username
        tk.Label(
            change_window,
            text="Current Username",
            font=("Arial", 10, "bold"),
            fg="#666666",
            bg="#1a1a1a",
            anchor="w"
        ).pack(fill="x", padx=40, pady=(10, 5))
        
        current_user = tk.Entry(
            change_window,
            font=("Arial", 12),
            bg="#2a2a2a",
            fg="white",
            insertbackground='white',
            relief="flat"
        )
        current_user.pack(fill="x", padx=40, ipady=8)

        # Current Password
        tk.Label(
            change_window,
            text="Current Password",
            font=("Arial", 10, "bold"),
            fg="#666666",
            bg="#1a1a1a",
            anchor="w"
        ).pack(fill="x", padx=40, pady=(15, 5))
        
        current_pass = tk.Entry(
            change_window,
            font=("Arial", 12),
            bg="#2a2a2a",
            fg="white",
            insertbackground='white',
            show="●",
            relief="flat"
        )
        current_pass.pack(fill="x", padx=40, ipady=8)

        # New Username
        tk.Label(
            change_window,
            text="New Username",
            font=("Arial", 10, "bold"),
            fg="#666666",
            bg="#1a1a1a",
            anchor="w"
        ).pack(fill="x", padx=40, pady=(15, 5))
        
        new_user = tk.Entry(
            change_window,
            font=("Arial", 12),
            bg="#2a2a2a",
            fg="white",
            insertbackground='white',
            relief="flat"
        )
        new_user.pack(fill="x", padx=40, ipady=8)

        # New Password
        tk.Label(
            change_window,
            text="New Password",
            font=("Arial", 10, "bold"),
            fg="#666666",
            bg="#1a1a1a",
            anchor="w"
        ).pack(fill="x", padx=40, pady=(15, 5))
        
        new_pass = tk.Entry(
            change_window,
            font=("Arial", 12),
            bg="#2a2a2a",
            fg="white",
            insertbackground='white',
            show="●",
            relief="flat"
        )
        new_pass.pack(fill="x", padx=40, ipady=8)

        def save_changes():
            old_username = current_user.get().strip()
            old_password = current_pass.get().strip()
            new_username = new_user.get().strip()
            new_password = new_pass.get().strip()

            if not all([old_username, old_password, new_username, new_password]):
                messagebox.showerror("Error", "⚠️ All fields are required")
                return

            if len(new_password) < 6:
                messagebox.showerror("Error", "⚠️ New password must be at least 6 characters")
                return

            success, message = update_credentials(old_username, old_password, new_username, new_password)
            
            if success:
                messagebox.showinfo("Success", f"✅ {message}")
                change_window.destroy()
            else:
                messagebox.showerror("Error", f"❌ {message}")

        tk.Button(
            change_window,
            text="SAVE CHANGES",
            font=("Arial", 12, "bold"),
            bg="#27ae60",
            fg="white",
            activebackground="#229954",
            relief="flat",
            cursor="hand2",
            command=save_changes
        ).pack(fill="x", padx=40, pady=(30, 10), ipady=10)

        tk.Button(
            change_window,
            text="CANCEL",
            font=("Arial", 12),
            bg="#555555",
            fg="white",
            activebackground="#444444",
            relief="flat",
            cursor="hand2",
            command=change_window.destroy
        ).pack(fill="x", padx=40, ipady=10)

    forgot_link = tk.Label(
        links_frame,
        text="🔑 Forgot Password?",
        font=("Segoe UI", 11, "underline"),
        fg="#00d4ff",
        bg="#000000",
        cursor="hand2"
    )
    forgot_link.pack(side="left", padx=10)
    forgot_link.bind("<Button-1>", lambda e: forgot_password())
    forgot_link.bind("<Enter>", lambda e: forgot_link.config(fg="#00b8e6"))
    forgot_link.bind("<Leave>", lambda e: forgot_link.config(fg="#00d4ff"))

    change_link = tk.Label(
        links_frame,
        text="⚙️ Change Credentials",
        font=("Segoe UI", 11, "underline"),
        fg="#00d4ff",
        bg="#000000",
        cursor="hand2"
    )
    change_link.pack(side="left", padx=10)
    change_link.bind("<Button-1>", lambda e: change_credentials())
    change_link.bind("<Enter>", lambda e: change_link.config(fg="#00b8e6"))
    change_link.bind("<Leave>", lambda e: change_link.config(fg="#00d4ff"))

    # Keyboard shortcuts
    root.bind('<Return>', lambda event: validate_login())
    root.bind('<Escape>', lambda event: root.destroy())
    
    root.mainloop()

def close_app(root):
    root.quit()
    root.destroy()
