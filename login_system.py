import tkinter as tk
from tkinter import ttk, messagebox
from create_database import get_login_connection
from datetime import datetime
import re
import random
import string


class LoginSystem:
    def __init__(self, parent, on_login_success):
        # Initialize Login System
        self.parent = parent
        self.on_login_success = on_login_success
        self.current_frame = None
        
        # String variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        # Registration
        self.reg_username_var = tk.StringVar()
        self.reg_email_var = tk.StringVar()
        self.reg_password_var = tk.StringVar()
        self.reg_confirm_var = tk.StringVar()
        self.reg_fullname_var = tk.StringVar()
        self.reg_phone_var = tk.StringVar()
        
        # Forgot password variables
        self.forgot_email_var = tk.StringVar()
        
        # Show login screen
        self.show_login_frame()
    
    def clear_frame(self):
        """Clear the current frame to load new content"""
        if self.current_frame:
            self.current_frame.destroy()
    
    def show_login_frame(self):
        """Display the login form"""
        self.clear_frame()
        
        # Create main frame
        self.current_frame = tk.Frame(self.parent, bg="#ffffff")
        self.current_frame.pack(expand=True, fill="both", padx=30, pady=20)
        
        # Welcome heading
        tk.Label(self.current_frame, text="Login to Your Account", 
                font=("Bookman Old Style", 16, "bold italic"), bg="#ffffff", 
                fg="#000000").pack(pady=(0, 20))
        
        # Form frame
        form_frame = tk.Frame(self.current_frame, bg="#ffffff")
        form_frame.pack(pady=10)
        
        # Username label and entry
        tk.Label(form_frame, text="Username", font=("Segoe UI", 10, "bold"),
                bg="#ffffff", anchor="w").grid(row=0, column=0, sticky="w", pady=(10,5))
        
        # Username entry with border
        username_frame = tk.Frame(form_frame, bg="#f8fafc", relief="solid", bd=1)
        username_frame.grid(row=0, column=1, pady=(10,5), padx=10)
        
        username_entry = tk.Entry(username_frame, textvariable=self.username_var,
                                font=("Segoe UI", 11), bg="#f8fafc", 
                                width=24, bd=0)
        username_entry.pack(side="left", fill="both", expand=True, ipady=5, padx=5)
        username_entry.focus()
        
        # Password label and entry
        tk.Label(form_frame, text="Password", font=("Segoe UI", 10, "bold"),
                bg="#ffffff", anchor="w").grid(row=1, column=0, sticky="w", pady=(10,5))
        
        # Password frame
        password_frame = tk.Frame(form_frame, bg="#f8fafc", relief="solid", bd=1)
        password_frame.grid(row=1, column=1, pady=(10,5), padx=10)
        
        self.password_entry = tk.Entry(password_frame, textvariable=self.password_var,
                                    font=("Segoe UI", 11), bg="#f8fafc", 
                                    width=20, bd=0, show="•")
        self.password_entry.pack(side="left", fill="both", expand=True, ipady=5, padx=(5,0))
        
        self.show_password = False
        toggle_btn = tk.Button(password_frame, text="👁", font=("Segoe UI", 11),
                            bg="#f8fafc", fg="#666666", bd=0, cursor="hand2",
                            command=self.toggle_password)
        toggle_btn.pack(side="right", padx=(0,5))
        
        # Buttons frame
        btn_frame = tk.Frame(self.current_frame, bg="#ffffff")
        btn_frame.pack(pady=20)
        
        # Login button
        login_btn = tk.Button(btn_frame, text="LOGIN", font=("Segoe UI", 11, "bold"),
                            bg="#31726C", fg="white", width=15, height=1,
                            cursor="hand2", bd=0, command=self.login)
        login_btn.pack(side="left", padx=5, ipady=5)
        
        # Login button hover effects
        # login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#29BFB0"))
        # login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#29BFB0"))
        
        # Clear button
        clear_btn = tk.Button(btn_frame, text="CLEAR", font=("Segoe UI", 11, "bold"),
                            bg="#1A1919", fg="white", width=15, height=1,
                            cursor="hand2", bd=0, command=self.clear_login)
        clear_btn.pack(side="left", padx=5, ipady=5)
        
        # Clear button hover effects
        # clear_btn.bind("<Enter>", lambda e: clear_btn.config(bg="#271E1E"))
        # clear_btn.bind("<Leave>", lambda e: clear_btn.config(bg="#271E1E"))
        
        # Links frame
        links_frame = tk.Frame(self.current_frame, bg="#ffffff")
        links_frame.pack(pady=10)
        
        # Register link
        tk.Label(links_frame, text="Don't have an account? ", 
                font=("Segoe UI", 9), bg="#ffffff").pack(side="left")
        reg_link = tk.Label(links_frame, text="Register", font=("Segoe UI", 9, "bold"),
                        bg="#ffffff", fg="#1e3a8a", cursor="hand2")
        reg_link.pack(side="left")
        reg_link.bind("<Button-1>", lambda e: self.show_register_frame())
        
        # Forgot password link
        forgot_link = tk.Label(self.current_frame, text="Forgot Password?", 
                            font=("Segoe UI", 9, "bold"), bg="#ffffff", 
                            fg="#dc2626", cursor="hand2")
        forgot_link.pack(pady=5)
        forgot_link.bind("<Button-1>", lambda e: self.show_forgot_password())
        
        # Bind Enter key
        self.parent.bind('<Return>', lambda e: self.login())
            
    def toggle_password(self):
        """Toggle password visibility (show/hide)"""
        if self.show_password:
            self.password_entry.config(show="•")
        else:
            self.password_entry.config(show="")
        self.show_password = not self.show_password
    
    def clear_login(self):
        """Clear login form fields"""
        self.username_var.set("")
        self.password_var.set("")
    
    def login(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()
        
        # Validation
        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password!")
            return
        
        # Connect to database
        conn = get_login_connection()
        c = conn.cursor()
        
        # Check user credentials
        c.execute("SELECT id, username, full_name, role FROM users WHERE username=? AND password=?", 
                 (username, password))
        
        user = c.fetchone()
        
        if user:
            # Update last login time
            c.execute("UPDATE users SET last_login=? WHERE id=?", 
                     (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), user[0]))
            conn.commit()
            
            messagebox.showinfo("Success", f"Welcome {user[2]}!")
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Invalid username or password!")
        
        conn.close()
    
    def show_register_frame(self):
        """Display registration form for new users"""
        self.clear_frame()
        
        # Registration scrollable frame
        self.current_frame = tk.Frame(self.parent, bg="#ffffff")
        self.current_frame.pack(expand=True, fill="both", padx=30, pady=10)
        
        # Canvas and scrollbar
        canvas = tk.Canvas(self.current_frame, bg="#ffffff", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.current_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#ffffff")
        
        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Title
        tk.Label(scrollable_frame, text="Create New Account", 
                font=("Segoe UI", 16, "bold"), bg="#ffffff", 
                fg="#1e3a8a").pack(pady=(0, 15))
        
        # Form frame
        form_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        form_frame.pack(pady=5)
        
        # Full Name field
        tk.Label(form_frame, text="Full Name *", font=("Segoe UI", 10, "bold"),
                bg="#ffffff", anchor="w").grid(row=0, column=0, sticky="w", pady=8)
        tk.Entry(form_frame, textvariable=self.reg_fullname_var,
                font=("Segoe UI", 11), bg="#f8fafc", width=25,
                relief="solid", bd=1).grid(row=0, column=1, pady=8, padx=10, ipady=5)
        
        # Username field
        tk.Label(form_frame, text="Username *", font=("Segoe UI", 10, "bold"),
                bg="#ffffff", anchor="w").grid(row=1, column=0, sticky="w", pady=8)
        tk.Entry(form_frame, textvariable=self.reg_username_var,
                font=("Segoe UI", 11), bg="#f8fafc", width=25,
                relief="solid", bd=1).grid(row=1, column=1, pady=8, padx=10, ipady=5)
        
        # Email field
        tk.Label(form_frame, text="Email *", font=("Segoe UI", 10, "bold"),
                bg="#ffffff", anchor="w").grid(row=2, column=0, sticky="w", pady=8)
        tk.Entry(form_frame, textvariable=self.reg_email_var,
                font=("Segoe UI", 11), bg="#f8fafc", width=25,
                relief="solid", bd=1).grid(row=2, column=1, pady=8, padx=10, ipady=5)
        
        # Phone number field
        tk.Label(form_frame, text="Phone Number", font=("Segoe UI", 10),
                bg="#ffffff", anchor="w").grid(row=3, column=0, sticky="w", pady=8)
        tk.Entry(form_frame, textvariable=self.reg_phone_var,
                font=("Segoe UI", 11), bg="#f8fafc", width=25,
                relief="solid", bd=1).grid(row=3, column=1, pady=8, padx=10, ipady=5)
        
        # Password field
        tk.Label(form_frame, text="Password *", font=("Segoe UI", 10, "bold"),
                bg="#ffffff", anchor="w").grid(row=4, column=0, sticky="w", pady=8)
        tk.Entry(form_frame, textvariable=self.reg_password_var,
                font=("Segoe UI", 11), bg="#f8fafc", width=25,
                relief="solid", bd=1, show="•").grid(row=4, column=1, pady=8, padx=10, ipady=5)
        
        # Confirm Password field
        tk.Label(form_frame, text="Confirm Password *", font=("Segoe UI", 10, "bold"),
                bg="#ffffff", anchor="w").grid(row=5, column=0, sticky="w", pady=8)
        tk.Entry(form_frame, textvariable=self.reg_confirm_var,
                font=("Segoe UI", 11), bg="#f8fafc", width=25,
                relief="solid", bd=1, show="•").grid(row=5, column=1, pady=8, padx=10, ipady=5)
        
        # Buttons frame
        btn_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        btn_frame.pack(pady=20)
        
        # Register button
        reg_btn = tk.Button(btn_frame, text="REGISTER", font=("Segoe UI", 11, "bold"),
                           bg="#1e3a8a", fg="white", width=15, height=1,
                           cursor="hand2", bd=0, command=self.register)
        reg_btn.pack(side="left", padx=5, ipady=5)
        
        # Register button hover effect
        reg_btn.bind("<Enter>", lambda e: reg_btn.config(bg="#2a4a9a"))
        reg_btn.bind("<Leave>", lambda e: reg_btn.config(bg="#1e3a8a"))
        
        # Back button
        back_btn = tk.Button(btn_frame, text="BACK", font=("Segoe UI", 11, "bold"),
                            bg="#f97316", fg="white", width=15, height=1,
                            cursor="hand2", bd=0, command=self.show_login_frame)
        back_btn.pack(side="left", padx=5, ipady=5)
        
        # Back button hover effect
        back_btn.bind("<Enter>", lambda e: back_btn.config(bg="#fb923c"))
        back_btn.bind("<Leave>", lambda e: back_btn.config(bg="#f97316"))
        
        # Login link
        link_frame = tk.Frame(scrollable_frame, bg="#ffffff")
        link_frame.pack(pady=10)
        
        tk.Label(link_frame, text="Already have an account? ", 
                font=("Segoe UI", 9), bg="#ffffff").pack(side="left")
        login_link = tk.Label(link_frame, text="Login", font=("Segoe UI", 9, "bold"),
                             bg="#ffffff", fg="#1e3a8a", cursor="hand2")
        login_link.pack(side="left")
        login_link.bind("<Button-1>", lambda e: self.show_login_frame())
    
    def validate_email(self, email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None
    
    def register(self):
        # Get form values
        fullname = self.reg_fullname_var.get().strip()
        username = self.reg_username_var.get().strip()
        email = self.reg_email_var.get().strip()
        phone = self.reg_phone_var.get().strip()
        password = self.reg_password_var.get().strip()
        confirm = self.reg_confirm_var.get().strip()
        
        # Validation checks
        if not all([fullname, username, email, password, confirm]):
            messagebox.showerror("Error", "Please fill all required fields (*)")
            return
        
        if not self.validate_email(email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return
        
        if password != confirm:
            messagebox.showerror("Error", "Passwords do not match")
            return
        
        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters")
            return
        
        # Connect to database
        conn = get_login_connection()
        c = conn.cursor()
        
        try:
            # Check if username already exists
            c.execute("SELECT id FROM users WHERE username=?", (username,))
            if c.fetchone():
                messagebox.showerror("Error", "Username already exists")
                conn.close()
                return
            
            # Check if email already exists
            c.execute("SELECT id FROM users WHERE email=?", (email,))
            if c.fetchone():
                messagebox.showerror("Error", "Email already registered")
                conn.close()
                return
            
            # Insert new user
            c.execute('''INSERT INTO users 
                        (username, email, password, full_name, phone, role, created_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''',
                        (username, email, password, fullname, phone, 'user',
                         datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
            conn.commit()
            messagebox.showinfo("Success", "Registration successful! Please login.")
            
            # Clear registration form
            self.reg_fullname_var.set("")
            self.reg_username_var.set("")
            self.reg_email_var.set("")
            self.reg_phone_var.set("")
            self.reg_password_var.set("")
            self.reg_confirm_var.set("")
            
            # Return to login screen
            self.show_login_frame()
            
        except Exception as e:
            messagebox.showerror("Error", f"Registration failed: {str(e)}")
        finally:
            conn.close()
    
    def show_forgot_password(self):
        """Display forgot password dialog"""
        # Create new popup window
        forgot_window = tk.Toplevel(self.parent)
        forgot_window.title("Reset Password")
        forgot_window.geometry("400x300")
        forgot_window.config(bg="#ffffff")
        forgot_window.transient(self.parent)
        forgot_window.grab_set()
        
        # Center the window on screen
        forgot_window.update_idletasks()
        x = (forgot_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (forgot_window.winfo_screenheight() // 2) - (300 // 2)
        forgot_window.geometry(f'400x300+{x}+{y}')
        
        # Title
        tk.Label(forgot_window, text="Reset Password", 
                font=("Segoe UI", 14, "bold"), bg="#ffffff", 
                fg="#1e3a8a").pack(pady=20)
        
        # Instructions
        tk.Label(forgot_window, 
                text="Enter your email address.\nWe will send you a new password.",
                font=("Segoe UI", 10), bg="#ffffff", justify="center").pack(pady=5)
        
        # Form frame
        form_frame = tk.Frame(forgot_window, bg="#ffffff")
        form_frame.pack(pady=10, padx=30)
        
        # Email entry
        email_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=email_var, font=("Segoe UI", 11),
                bg="#f8fafc", width=25, relief="solid", bd=1).pack(pady=10, ipady=5)
        
        def reset_password():
            email = email_var.get().strip()
            if not email:
                messagebox.showerror("Error", "Please enter email")
                return
            
            conn = get_login_connection()
            c = conn.cursor()
            
            # Check if email exists
            c.execute("SELECT username FROM users WHERE email=?", (email,))
            user = c.fetchone()
            
            if user:
                # Generate 8-character password
                new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
                
                # Update password in database
                c.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
                conn.commit()
                
                # Show new password to user
                messagebox.showinfo("Password Reset", 
                                   f"Your new password is: {new_password}\n\n"
                                   "Please login with this password and change it later.")
                forgot_window.destroy()
            else:
                messagebox.showerror("Error", "Email not found in our records")
            
            conn.close()
        
        # Reset Password button
        tk.Button(forgot_window, text="RESET PASSWORD", font=("Segoe UI", 11, "bold"),
                 bg="#1e3a8a", fg="white", width=20, cursor="hand2",
                 bd=0, command=reset_password).pack(pady=15, ipady=8)
        
        # Cancel button
        tk.Button(forgot_window, text="CANCEL", font=("Segoe UI", 11, "bold"),
                 bg="#f97316", fg="white", width=20, cursor="hand2",
                 bd=0, command=forgot_window.destroy).pack(pady=5, ipady=8)
        