import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from create_database import initialize_database
from create_database import resource_path
from dashboard import open_dashboard
from login_system import LoginSystem
from datetime import datetime
from create_database import backup_database
from footer import create_footer

def start_app():
    # Initialize database
    initialize_database()
    backup_database()
    
    # Create main window
    root = tk.Tk()
    root.title("Abu Huraira Enterprises - Created by: .ARS")
    root.geometry("1000x600")
    root.config(bg="#ffffff")

    # Main content frame
    content_frame = tk.Frame(root, bg="#ffffff")
    content_frame.pack(expand=True, fill="both", padx=50, pady=20)

    # Heading
    heading = tk.Label(content_frame, text="WELCOME TO ABU HURAIRA ENTERPRISES! \nHouse Rent Management System | Created by .ARS" ,
                       font=("Bookman Old Style", 20, "bold italic "), bg="#ffffff", fg="#163077")
    heading.pack(pady=(0, 20))

    # Middle frame for image and login
    middle_frame = tk.Frame(content_frame, bg="#ffffff")
    middle_frame.pack(expand=True, fill="both")

    # Left side - Image
    left_frame = tk.Frame(middle_frame, bg="#ffffff")
    left_frame.pack(side="left", expand=True, fill="both")

    try:
        # Load image
        image_path = resource_path("tenant_images/Image.jpeg")
        image = Image.open(image_path)
        image = image.resize((500, 400), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        
        image_label = tk.Label(left_frame, image=photo, bg="#ffffff")
        image_label.image = photo
        image_label.pack(pady=20)
        
    except Exception as e:
        placeholder = tk.Label(left_frame, text="🏠 House Image", 
                              font=("Segoe UI", 16), bg="#ffffff", fg="#6b7280")
        placeholder.pack(pady=20)

    # Right side - Login System
    right_frame = tk.Frame(middle_frame, bg="#ffffff", width=350)
    right_frame.pack(side="right", expand=True, fill="both")
    
    # Login system
    login_system = LoginSystem(right_frame, lambda: open_dashboard_with_close(root))

    # Configure styles
    style = ttk.Style()
    style.configure("Accent.TButton",
                    font=("Segoe UI", 12, "bold"),
                    padding=10,
                    background="white",
                    foreground="black")

    # ========== FOOTER ==========
    footer = create_footer(root)
    root.mainloop()

def open_dashboard_with_close(root):
    root.destroy()
    open_dashboard()

if __name__ == "__main__":
    start_app()