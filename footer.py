# footer.py
import tkinter as tk
from datetime import datetime

def create_footer(parent_frame):
    
    # Main footer frame
    footer_frame = tk.Frame(parent_frame,bg="#1e3a8a",height=40,relief="solid",bd=0)
    footer_frame.pack(side="bottom", fill="x", padx=20, pady=(5, 10))
    footer_frame.pack_propagate(False)

    # Top border line
    tk.Frame(footer_frame,bg="#3498db",height=2).pack(fill="x", pady=(0, 8))

    # Footer content frame
    footer_content = tk.Frame(footer_frame,bg="#1e3a8a")
    footer_content.pack()

    # Left
    tk.Label(footer_content,text="©",font=("Segoe UI", 12, "bold"),bg="#1e3a8a",
                fg="white").pack(side="left", padx=(0, 5))
    
    current_year = datetime.now().year
    tk.Label(footer_content, text=f"{current_year} Abu Huraira Enterprises", 
        font=("Segoe UI", 12),bg="#1e3a8a",fg="white").pack(side="left")

    # Separator
    tk.Label(footer_content,text="|",font=("Segoe UI", 14, "bold"),
             bg="#1e3a8a",fg="#95a5a6").pack(side="left", padx=8)

    # Powered by
    tk.Label(footer_content,text="⚡",font=("Segoe UI", 12),bg="#1e3a8a", 
        fg="#f39c12").pack(side="left", padx=(0, 2))
    
    tk.Label(footer_content,text="Powered by",font=("Segoe UI", 12),
             bg="#1e3a8a",fg="white").pack(side="left")
    
    tk.Label(footer_content, text=".ARS", font=("Segoe UI", 12, "bold"),
             bg="#1e3a8a",fg="#f39c12").pack(side="left", padx=(2, 8))

    # Separator
    tk.Label(footer_content,text="|",font=("Segoe UI", 14, "bold"),
            bg="#1e3a8a", fg="#95a5a6").pack(side="left", padx=8)

    # Contact
    tk.Label(footer_content,text="📞",font=("Segoe UI", 12),bg="#1e3a8a", 
            fg="#2ecc71").pack(side="left")
    
    tk.Label(footer_content,text="0333-3988781",font=("Segoe UI", 12, "bold"),
            bg="#1e3a8a",fg="white").pack(side="left", padx=(2, 8))

    # Version
    tk.Label(footer_content,text="v1.0.0", font=("Segoe UI", 10, "italic"),
            bg="#1e3a8a",fg="#95a5a6").pack(side="left")
    
    return footer_frame