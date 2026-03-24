import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from create_database import initialize_database, resource_path, backup_database
from dashboard import open_dashboard
from login_system import LoginSystem
from datetime import datetime
from footer import create_footer

    
def start_app():
    # Initialize database
    initialize_database()
    backup_database()

    root = tk.Tk()
    root.title("Abu Huraira Enterprises - Developed by: .ARS")
    root.geometry("1050x650")
    root.config(bg="#f8fafc")

    # ===== Scrollable Content Setup =====
    main_frame = tk.Frame(root, bg="#f8fafc")
    main_frame.pack(expand=True, fill="both")

    canvas = tk.Canvas(main_frame, bg="#f8fafc", highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f8fafc")
    

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # ===== Footer =====
    footer = create_footer(root)

        # ===== Heading =====
    heading = tk.Label(scrollable_frame, text="", font=("Segoe UI", 20, "bold italic"),
                    bg="#f8fafc", fg="#163077", justify="center")
    heading.pack(padx=100, pady=(15, 20))
    welcome_text = "🏢 WELCOME TO ABU HURAIRA ENTERPRISES!\nHouse Rent Management System | Developed by .ARS"

    global anim_id, color_id, time_id
    anim_id = None
    color_id = None
    time_id = None

    def animate_text(index=0):
        global anim_id
        if index <= len(welcome_text):
            heading.config(text=welcome_text[:index])
            anim_id = root.after(50, animate_text, index + 1)

    animate_text()

    # ===== Multi Color Animation =====
    colors = ["#0E1D45", "#2563eb", "#9333ea", "#db2777", "#f59e0b", "#085424"]

    def change_color(i=0):
        global color_id
        heading.config(fg=colors[i])
        color_id = root.after(400, change_color, (i + 1) % len(colors))

    change_color()

    # ===== Time Label =====
    time_label = tk.Label(scrollable_frame, font=("Segoe UI", 14, "bold"),
                        bg="#f8fafc", fg="#475569", justify="center")
    time_label.pack(padx=100, pady=(0, 5))
    
    def update_time():
        global time_id
        current_time = datetime.now().strftime("%I:%M:%S %p  |  %A, %d %B %Y")
        time_label.config(text=current_time)
        time_id = root.after(1000, update_time)
    update_time()

    # ===== Middle Frame: Image + Login =====
    middle_frame = tk.Frame(scrollable_frame, bg="#ffffff")
    middle_frame.pack(padx=100, pady=5)

    # --- Use Grid for proper centering ---
    left_frame = tk.Frame(middle_frame, bg="#f8fafc")
    left_frame.grid(row=0, column=0, padx=20, pady=20)

    right_frame = tk.Frame(middle_frame, bg="white", width=350, bd=1, relief="solid")
    right_frame.grid(row=0, column=1, padx=20, pady=20)

    # Center the grid inside middle_frame
    middle_frame.grid_columnconfigure(0, weight=1)
    middle_frame.grid_columnconfigure(1, weight=1)

    # --- Image Section ---
    try:
        image_path = resource_path("tenant_images/Image.jpeg")
        image = Image.open(image_path).resize((500, 400), Image.Resampling.LANCZOS)

        # Rounded corners
        radius = 30
        mask = Image.new('L', image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], radius=radius, fill=255)
        rounded_image = image.copy()
        rounded_image.putalpha(mask)

        photo = ImageTk.PhotoImage(rounded_image)
        image_label = tk.Label(left_frame, image=photo, bg="#f8fafc")
        image_label.image = photo
        image_label.pack(pady=20, padx=20)
    except:
        placeholder = tk.Label(left_frame, text="🏠 House Image", font=("Segoe UI", 20, "bold"),
                            bg="#f8fafc", fg="#6b7280")
        placeholder.pack(pady=20, padx=20)

    # --- Login Section ---
    tk.Label(right_frame, text="User Login", font=("Segoe UI", 16, "bold"),
            bg="white", fg="#1e3a8a").pack(pady=10)

    login_system = LoginSystem(right_frame, lambda: open_dashboard_with_close(root))
    

    style = ttk.Style()
    style.configure("Accent.TButton", font=("Segoe UI", 12, "bold"),
                    padding=10, background="white", foreground="black")

    root.mainloop()

def open_dashboard_with_close(root):
    try:
        if anim_id: root.after_cancel(anim_id)
        if color_id: root.after_cancel(color_id)
        if time_id: root.after_cancel(time_id)
    except:
        pass
    
    root.destroy()
    open_dashboard()


if __name__ == "__main__":
    start_app()





# import tkinter as tk
# from tkinter import ttk
# from PIL import Image, ImageTk, ImageDraw
# from create_database import initialize_database, resource_path, backup_database
# from dashboard import open_dashboard
# from login_system import LoginSystem
# from datetime import datetime
# from footer import create_footer

    
# def start_app():
#     # Initialize database
#     initialize_database()
#     backup_database()

#     root = tk.Tk()
#     root.title("Abu Huraira Enterprises - Developed by: .ARS")
#     root.geometry("1000x650")
#     root.config(bg="#f8fafc")

#     # ===== Scrollable Content Setup =====
#     main_frame = tk.Frame(root, bg="#f8fafc")
#     main_frame.pack(expand=True, fill="both")

#     canvas = tk.Canvas(main_frame, bg="#f8fafc", highlightthickness=0)
#     scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
#     scrollable_frame = tk.Frame(canvas, bg="#f8fafc")
    

#     scrollable_frame.bind(
#         "<Configure>",
#         lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#     )

#     canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#     canvas.configure(yscrollcommand=scrollbar.set)

#     canvas.pack(side="left", fill="both", expand=True)
#     scrollbar.pack(side="right", fill="y")

#     # ===== Footer =====
#     footer = create_footer(root)

#         # ===== Heading =====
#     heading = tk.Label(scrollable_frame, text="", font=("Segoe UI", 20, "bold italic"),
#                     bg="#f8fafc", fg="#163077", justify="center")
#     heading.pack(padx=100, pady=(15, 20))
#     welcome_text = "🏢 WELCOME TO ABU HURAIRA ENTERPRISES!\nHouse Rent Management System | Created by .ARS"

#     def animate_text(index=0):
#         try:
#             if index <= len(welcome_text):
#                 heading.config(text=welcome_text[:index])
#                 root.after(50, animate_text, index + 1)
#         except tk.TclError:
#             pass

#     animate_text()

#     # ===== Multi Color Animation =====
#     colors = ["#0E1D45", "#2563eb", "#9333ea", "#db2777", "#f59e0b", "#085424"]

#     def change_color(i=0):
#         try:
#             heading.config(fg=colors[i])
#             root.after(400, change_color, (i + 1) % len(colors))
#         except tk.TclError:
#             pass

#     change_color()

#     # ===== Time Label =====
#     time_label = tk.Label(scrollable_frame, font=("Segoe UI", 14, "bold"),
#                         bg="#f8fafc", fg="#475569", justify="center")
#     time_label.pack(padx=100, pady=(0, 5))
    
#     def update_time():
#         try:
#             current_time = datetime.now().strftime("%I:%M:%S %p  |  %A, %d %B %Y")
#             time_label.config(text=current_time)
#             time_label.after(1000, update_time)
#         except tk.TclError:
#             pass
#     update_time()

#     # ===== Middle Frame: Image + Login =====
#     middle_frame = tk.Frame(scrollable_frame, bg="#ffffff")
#     middle_frame.pack(padx=100, pady=5)

#     # --- Use Grid for proper centering ---
#     left_frame = tk.Frame(middle_frame, bg="#f8fafc")
#     left_frame.grid(row=0, column=0, padx=20, pady=20)

#     right_frame = tk.Frame(middle_frame, bg="white", width=350, bd=1, relief="solid")
#     right_frame.grid(row=0, column=1, padx=20, pady=20)

#     # Center the grid inside middle_frame
#     middle_frame.grid_columnconfigure(0, weight=1)
#     middle_frame.grid_columnconfigure(1, weight=1)

#     # --- Image Section ---
#     try:
#         image_path = resource_path("tenant_images/Image.jpeg")
#         image = Image.open(image_path).resize((500, 400), Image.Resampling.LANCZOS)

#         # Rounded corners
#         radius = 30
#         mask = Image.new('L', image.size, 0)
#         draw = ImageDraw.Draw(mask)
#         draw.rounded_rectangle([0, 0, image.size[0], image.size[1]], radius=radius, fill=255)
#         rounded_image = image.copy()
#         rounded_image.putalpha(mask)

#         photo = ImageTk.PhotoImage(rounded_image)
#         image_label = tk.Label(left_frame, image=photo, bg="#f8fafc")
#         image_label.image = photo
#         image_label.pack(pady=20, padx=20)
#     except:
#         placeholder = tk.Label(left_frame, text="🏠 House Image", font=("Segoe UI", 20, "bold"),
#                             bg="#f8fafc", fg="#6b7280")
#         placeholder.pack(pady=20, padx=20)

#     # --- Login Section ---
#     tk.Label(right_frame, text="User Login", font=("Segoe UI", 16, "bold"),
#             bg="white", fg="#1e3a8a").pack(pady=10)

#     login_system = LoginSystem(right_frame, lambda: open_dashboard_with_close(root))
    

#     style = ttk.Style()
#     style.configure("Accent.TButton", font=("Segoe UI", 12, "bold"),
#                     padding=10, background="white", foreground="black")

#     root.mainloop()

# def open_dashboard_with_close(root):
#     root.destroy()
#     open_dashboard()


# if __name__ == "__main__":
#     start_app()
