


import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from create_database import get_connection
import re, os, uuid
from PIL import Image, ImageTk
from datetime import datetime
import cv2  # OpenCV for camera

# Create images directory if not exists
IMAGES_DIR = "tenant_images"
if not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

def validate_phone(phone):
    return len(phone.strip()) > 0

def validate_cnic(cnic):
    return re.match(r'^\d{13}$', cnic) is not None

def add_tenant_screen():
    window = tk.Toplevel()
    window.title("Abu Huraira Enterprises - Created by .ARS")
    window.geometry("1000x650")
    window.config(bg="white")
    window.resizable(True, True)
    
    # Camera window reference
    camera_window = None
    camera_running = False
    
    # Main frame with scrollbar
    main_frame = tk.Frame(window, bg="#f0f8ff")
    main_frame.pack(fill="both", expand=True, padx=20, pady=25)

    # Title
    title_label = tk.Label(main_frame, text="Abu Huraira Enterprises \nAdd New Tenant", 
                          font=("Segoe UI", 18, "bold"), bg="#f0f8ff", fg="#1e3a8a")
    title_label.pack(pady=(0, 20))

    # Create two columns layout
    content_frame = tk.Frame(main_frame, bg="#f0f8ff")
    content_frame.pack(fill="both", expand=True)

    # Left Frame - Photo Upload
    left_frame = tk.LabelFrame(content_frame, text="Tenant Photo", 
                              font=("Segoe UI", 12, "bold"), 
                              bg="#f0f8ff", padx=15, pady=20, width=300)
    left_frame.pack(side="left", fill="y", padx=(0, 20))
    left_frame.pack_propagate(False)

    # Right Frame Container
    right_container = tk.Frame(content_frame, bg="#f0f8ff")
    right_container.pack(side="right", fill="both", expand=True)

    # ========== SCROLLBAR FOR RIGHT FRAME ==========
    canvas = Canvas(right_container, bg="#f0f8ff", highlightthickness=0)
    scrollbar = Scrollbar(right_container, orient="vertical", command=canvas.yview)
    
    # Scrollable frame
    right_frame = Frame(canvas, bg="#f0f8ff")
    
    # Configure canvas
    right_frame_id = canvas.create_window((0, 0), window=right_frame, anchor="nw")
    
    def configure_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(right_frame_id, width=event.width)
    
    right_frame.bind("<Configure>", configure_scrollregion)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(right_frame_id, width=e.width))
    
    # Pack
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # ========== PHOTO UPLOAD SECTION ==========
    photo_frame = tk.Frame(left_frame, bg="#f0f8ff", width=280, height=450)
    photo_frame.pack(fill="both", expand=True)
    photo_frame.pack_propagate(False)

    # Photo display label
    photo_label = tk.Label(photo_frame, text="No Photo", bg="#e5e7eb", 
                          fg="#6b7280", font=("Segoe UI", 10), 
                          relief="solid", bd=1, width=30, height=12)
    photo_label.pack(pady=(10, 5), padx=10)

    # Photo path variable
    photo_path = tk.StringVar()
    
    def upload_photo():
        file_types = [
            ('Image files', '*.jpg *.jpeg *.png *.gif *.bmp'),
            ('All files', '*.*')
        ]
        filename = filedialog.askopenfilename(
            title="Select Tenant Photo",
            filetypes=file_types
        )
        if filename:
            try:
                # Open image
                image = Image.open(filename)
                if image.mode in ("RGBA", "P"):
                    image = image.convert("RGB")

                # Resize to fit the label area
                image = image.resize((280, 280), Image.Resampling.LANCZOS)

                photo_filename = f"{uuid.uuid4().hex}.jpg"
                save_path = os.path.join(IMAGES_DIR, photo_filename)
                image.save(save_path, "JPEG", quality=95)                                
                                
                # Display image
                photo_display = ImageTk.PhotoImage(image)
                photo_label.config(image=photo_display, text="", width=280, height=280)
                photo_label.image = photo_display
                
                photo_path.set(save_path)
                messagebox.showinfo("Success", "Photo uploaded successfully!")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to upload photo: {str(e)}")

    # ========== TAKE PHOTO FUNCTION ==========
    def take_photo():
        # Open camera to take photo
        nonlocal camera_window, camera_running
        
        # If camera open
        if camera_running:
            messagebox.showwarning("Camera", "Camera is already open!")
            return
        
        # Create camera window
        camera_window = tk.Toplevel(window)
        camera_window.title("Take Photo")
        camera_window.geometry("700x550")
        camera_window.config(bg="#1e3a8a")
        camera_window.transient(window)
        camera_window.grab_set()
        
        # Center window
        camera_window.update_idletasks()
        x = (camera_window.winfo_screenwidth() // 2) - (700 // 2)
        y = (camera_window.winfo_screenheight() // 2) - (550 // 2)
        camera_window.geometry(f'700x550+{x}+{y}')
        
        # Camera feed frame
        camera_frame = tk.Frame(camera_window, bg="black", width=640, height=480)
        camera_frame.pack(pady=10)
        camera_frame.pack_propagate(False)
        
        # Camera label for video feed
        camera_label = tk.Label(camera_frame, bg="black")
        camera_label.pack()
        
        # Control buttons frame
        btn_frame = tk.Frame(camera_window, bg="#1e3a8a")
        btn_frame.pack(pady=10)
        
        # Status label
        status_label = tk.Label(camera_window, text="Initializing camera...", 
                               font=("Segoe UI", 10), bg="#1e3a8a", fg="white")
        status_label.pack(pady=5)
        
        # Initialize camera
        cap = None
        camera_running = True
        
        def start_camera():
            # Start camera in background thread
            nonlocal cap
            try:
                # Try different camera indices
                for i in range(3):
                    cap = cv2.VideoCapture(i)
                    if cap.isOpened():
                        print(f"Camera {i} opened successfully")
                        status_label.config(text=f"Camera {i} ready - Press Capture to take photo")
                        break
                
                if not cap or not cap.isOpened():
                    status_label.config(text="❌ No camera found!")
                    camera_running = False
                    return
                
                # Start video loop
                update_camera_feed()
                
            except Exception as e:
                status_label.config(text=f"❌ Camera error: {str(e)}")
                camera_running = False
        
        def update_camera_feed():
            # Update camera feed in GUI
            nonlocal cap
            
            if not camera_running or not cap:
                return
            try:
                ret, frame = cap.read()
                if ret:
                    # Convert frame to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Resize to fit label
                    frame_resized = cv2.resize(frame_rgb, (620, 460))
                    
                    # Convert to PhotoImage
                    img = Image.fromarray(frame_resized)
                    img_tk = ImageTk.PhotoImage(img)
                    
                    # Update label
                    camera_label.config(image=img_tk)
                    camera_label.image = img_tk
                
                # Schedule next update
                if camera_running:
                    camera_window.after(30, update_camera_feed)
                    
            except Exception as e:
                print(f"Camera feed error: {e}")
        
        def capture_photo():
            # Capture photo
            nonlocal cap
            
            if not cap or not cap.isOpened():
                messagebox.showerror("Error", "Camera is not available!")
                return
            
            try:
                # Capture frame
                ret, frame = cap.read()
                if ret:
                    # Convert BGR to RGB
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Create PIL Image
                    img = Image.fromarray(frame_rgb)
                    
                    # Resize for display
                    img_resized = img.resize((280,280), Image.Resampling.LANCZOS)
                    
                    # Save image
                    photo_filename = f"{uuid.uuid4().hex}.jpg"
                    save_path = os.path.join(IMAGES_DIR, photo_filename)
                    
                    # Save as JPEG
                    img.save(save_path, "JPEG", quality=95)
                    
                    # Display in main window
                    photo_display = ImageTk.PhotoImage(img_resized)
                    photo_label.config(image=photo_display, text="", width=280, height=280)
                    photo_label.image = photo_display
                    
                    # Set photo path
                    photo_path.set(save_path)
                    
                    status_label.config(text="✅ Photo captured successfully!")
                    
                    # Close camera window after short delay
                    camera_window.after(1000, close_camera)
                    
                else:
                    messagebox.showerror("Error", "Failed to capture photo!")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to capture: {str(e)}")
        
        def close_camera():
            # Close camera and window
            nonlocal camera_running, cap
            
            camera_running = False
            
            if cap:
                cap.release()
            
            if camera_window:
                camera_window.destroy()
        
        # Buttons
        tk.Button(btn_frame, text="📸 Capture Photo", command=capture_photo,
                 bg="#1644A1", fg="white", font=("Segoe UI", 12, "bold"),
                 width=15, padx=5, pady=5).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="❌ Cancel", command=close_camera,
                 bg="#dc3545", fg="white", font=("Segoe UI", 12, "bold"),
                 width=15, padx=5, pady=5).pack(side="left", padx=5)
        
        # Handle window close
        def on_closing():
            close_camera()
        
        camera_window.protocol("WM_DELETE_WINDOW", on_closing)
        
        # Start camera
        camera_window.after(100, start_camera)

    def remove_photo():
        # Remove photo and reset photo label
        photo_label.config(image="", text="No Photo", bg="#e5e7eb", fg="#6b7280", 
                          width=30, height=12)
        photo_path.set("")
        if hasattr(photo_label, 'image'):
            photo_label.image = None

    # Photo buttons frame
    photo_buttons_frame = tk.Frame(photo_frame, bg="#f0f8ff")
    photo_buttons_frame.pack(pady=10)

    # Upload button
    tk.Button(photo_buttons_frame, text="📁 Upload Photo", 
              command=upload_photo, bg="#1644A1", fg="white",
              font=("Segoe UI", 10), width=18).pack(pady=3)

    # Take Photo button
    tk.Button(photo_buttons_frame, text="📷 Take Photo", 
              command=take_photo, bg="#FC8F54", fg="white",
              font=("Segoe UI", 10), width=18).pack(pady=3)

    # Remove Photo button
    tk.Button(photo_buttons_frame, text="🗑️ Remove Photo", 
              command=remove_photo, bg="#83868D", fg="white",
              font=("Segoe UI", 10), width=18).pack(pady=3)

    # ========== FORM SECTION ==========
    form_frame = tk.Frame(right_frame, bg="#f0f8ff")
    form_frame.pack(fill="both", expand=True, padx=10)

    # Building, Floor and Flat Selection
    location_frame = tk.LabelFrame(form_frame, text="Property Location", 
                                  font=("Segoe UI", 12, "bold"), bg="#f0f8ff", pady=10, padx=10)
    location_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)

    # Building Name
    tk.Label(location_frame, text="Building Name *", bg="#f0f8ff", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
    building_entry = tk.Entry(location_frame, width=25)
    building_entry.grid(row=0, column=1, padx=5, pady=5)

    # Floor
    tk.Label(location_frame, text="Floor *", bg="#f0f8ff", font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w", padx=20, pady=5)
    floor_var = tk.StringVar()
    floor_combo = ttk.Combobox(location_frame, textvariable=floor_var, 
                              values=[str(i) for i in range(1, 11)], state="readonly", width=22)
    floor_combo.grid(row=0, column=3, padx=5, pady=5)
    floor_combo.set("1")  # Default value

    # Flat No
    tk.Label(location_frame, text="Flat No *", bg="#f0f8ff", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
    flat_entry = tk.Entry(location_frame, width=25)
    flat_entry.grid(row=1, column=1, padx=5, pady=5)

    # Add All entries in dictionary
    entries = {}
    entries['building_name'] = building_entry
    entries['flat_no'] = flat_entry

    # Tenant Personal Information
    personal_frame = tk.LabelFrame(form_frame, text="Tenant Personal Information", 
                                  font=("Segoe UI", 12, "bold"), bg="#f0f8ff", pady=10, padx=10)
    personal_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)

    fields_personal = [
        ("Name *", "name"),
        ("Father Name", "father_name"),
        ("CNIC *", "cnic"),
        ("Phone *", "phone"),
        ("Emergency Contact", "emergency_contact"),
        ("Profession", "profession")
    ]

    for i, (label, key) in enumerate(fields_personal):
        row = i // 2
        col = (i % 2) * 2
        
        tk.Label(personal_frame, text=label, bg="#f0f8ff").grid(row=row, column=col, sticky="w", padx=5, pady=5)
        entry = tk.Entry(personal_frame, width=30)
        entry.grid(row=row, column=col+1, padx=5, pady=5)
        entries[key] = entry

    # Financial Information
    financial_frame = tk.LabelFrame(form_frame, text="Financial Information", 
                                   font=("Segoe UI", 12, "bold"), bg="#f0f8ff", pady=10, padx=10)
    financial_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

    financial_fields = [
        ("Rent Amount *", "rent_amount"),
        ("Security Deposit", "security_deposit"),
        ("Advance Payment", "advance_payment")
    ]

    for i, (label, key) in enumerate(financial_fields):
        tk.Label(financial_frame, text=label, bg="#f0f8ff").grid(row=0, column=i*2, sticky="w", padx=5, pady=5)
        entry = tk.Entry(financial_frame, width=25)
        entry.grid(row=0, column=i*2+1, padx=5, pady=5)
        entries[key] = entry

    # Dates
    dates_frame = tk.Frame(form_frame, bg="#f0f8ff")
    dates_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
    
    tk.Label(dates_frame, text="Entry Date (dd-mm-yyyy) *", bg="#f0f8ff").grid(row=0, column=0, sticky="w", padx=5)
    entry_date = tk.Entry(dates_frame, width=30)
    entry_date.grid(row=0, column=1, padx=5)
    entries['entry_date'] = entry_date

    current_date = datetime.now().strftime("%d-%m-%Y")
    entry_date.insert(0, current_date)

    tk.Label(dates_frame, text="Exit Date (dd-mm-yyyy)", bg="#f0f8ff").grid(row=0, column=2, sticky="w", padx=20)
    exit_date = tk.Entry(dates_frame, width=30)
    exit_date.grid(row=0, column=3, padx=5)
    entries['exit_date'] = exit_date

    # Owner Information
    owner_frame = tk.LabelFrame(form_frame, text="Owner Information", 
                               font=("Segoe UI", 12, "bold"), bg="#f0f8ff", pady=10, padx=10)
    owner_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)

    tk.Label(owner_frame, text="Owner Name", bg="#f0f8ff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    owner_name = tk.Entry(owner_frame, width=30)
    owner_name.grid(row=0, column=1, padx=5, pady=5)
    entries['owner_name'] = owner_name

    tk.Label(owner_frame, text="Owner Phone", bg="#f0f8ff").grid(row=0, column=2, sticky="w", padx=20, pady=5)
    owner_phone = tk.Entry(owner_frame, width=30)
    owner_phone.grid(row=0, column=3, padx=5, pady=5)
    entries['owner_phone'] = owner_phone

    # Witness Information
    witness_frame = tk.LabelFrame(form_frame, text="Witness Information (2 Witnesses Required)", 
                                 font=("Segoe UI", 12, "bold"), bg="#f0f8ff", pady=10, padx=10)
    witness_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=10)

    # Witness 1
    tk.Label(witness_frame, text="Witness 1 Name *", bg="#f0f8ff").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    entries['w1_name'] = tk.Entry(witness_frame, width=20)
    entries['w1_name'].grid(row=0, column=1, padx=5, pady=5)

    tk.Label(witness_frame, text="Witness 1 CNIC", bg="#f0f8ff").grid(row=0, column=2, sticky="w", padx=5, pady=5)
    entries['w1_cnic'] = tk.Entry(witness_frame, width=20)
    entries['w1_cnic'].grid(row=0, column=3, padx=5, pady=5)

    tk.Label(witness_frame, text="Witness 1 Phone", bg="#f0f8ff").grid(row=0, column=4, sticky="w", padx=5, pady=5)
    entries['w1_phone'] = tk.Entry(witness_frame, width=20)
    entries['w1_phone'].grid(row=0, column=5, padx=5, pady=5)

    # Witness 2
    tk.Label(witness_frame, text="Witness 2 Name *", bg="#f0f8ff").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    entries['w2_name'] = tk.Entry(witness_frame, width=20)
    entries['w2_name'].grid(row=1, column=1, padx=5, pady=5)

    tk.Label(witness_frame, text="Witness 2 CNIC", bg="#f0f8ff").grid(row=1, column=2, sticky="w", padx=5, pady=5)
    entries['w2_cnic'] = tk.Entry(witness_frame, width=20)
    entries['w2_cnic'].grid(row=1, column=3, padx=5, pady=5)

    tk.Label(witness_frame, text="Witness 2 Phone", bg="#f0f8ff").grid(row=1, column=4, sticky="w", padx=5, pady=5)
    entries['w2_phone'] = tk.Entry(witness_frame, width=20)
    entries['w2_phone'].grid(row=1, column=5, padx=5, pady=5)

    # Additional Notes
    notes_frame = tk.LabelFrame(form_frame, text="Additional Notes", 
                               font=("Segoe UI", 12, "bold"), bg="#f0f8ff", pady=10, padx=10)
    notes_frame.grid(row=6, column=0, columnspan=2, sticky="ew", pady=10)

    notes_text = tk.Text(notes_frame, width=80, height=4, font=("Segoe UI", 10))
    notes_text.pack(padx=5, pady=5)

    # Save Button
    def save_tenant():
        try:
            required_fields = [
                entries['building_name'].get().strip(),
                floor_var.get(),
                entries['flat_no'].get().strip(), 
                entries['name'].get().strip(), 
                entries['cnic'].get().strip(), 
                entries['phone'].get().strip(), 
                entries['rent_amount'].get().strip(),
                entries['entry_date'].get().strip(),
                entries['w1_name'].get().strip(), 
                entries['w2_name'].get().strip()
            ]
            
            if not all(required_fields):
                messagebox.showerror("Error", "Please fill all required fields (*)")
                return

            if not validate_cnic(entries['cnic'].get().strip()):
                messagebox.showerror("Error", "Invalid CNIC (13 digits required)")
                return

            conn = get_connection()
            c = conn.cursor()

            # Check if CNIC already exists
            c.execute("SELECT id FROM tenants WHERE cnic = ?", (entries['cnic'].get().strip(),))
            if c.fetchone():
                messagebox.showerror("Error", "CNIC already exists in system!")
                return

            notes = notes_text.get("1.0", tk.END).strip()

            # Insert tenant
            c.execute('''INSERT INTO tenants 
                (name, father_name, cnic, phone, emergency_contact, profession,
                 building_name, floor, flat_no, entry_date, exit_date, owner_name, owner_phone, 
                 rent_amount, security_deposit, advance_amount, photo_path, notes) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    entries['name'].get().strip(),
                    entries['father_name'].get().strip(),
                    entries['cnic'].get().strip(),
                    entries['phone'].get().strip(),
                    entries['emergency_contact'].get().strip(),
                    entries['profession'].get().strip(),
                    entries['building_name'].get().strip(),
                    int(floor_var.get()), 
                    entries['flat_no'].get().strip(), 
                    entries['entry_date'].get().strip(),
                    entries['exit_date'].get().strip(),
                    entries['owner_name'].get().strip(),
                    entries['owner_phone'].get().strip(),
                    float(entries['rent_amount'].get() or 0),
                    float(entries['security_deposit'].get() or 0),
                    float(entries['advance_payment'].get() or 0), 
                    photo_path.get(),
                    notes
                ))

            tenant_id = c.lastrowid

            # Insert witnesses
            c.execute('''INSERT INTO witnesses 
                (tenant_id, w1_name, w1_cnic, w1_phone,
                 w2_name, w2_cnic, w2_phone) 
                VALUES (?, ?, ?, ?, ?, ?, ?)''',
                (
                    tenant_id, 
                    entries['w1_name'].get().strip(),
                    entries['w1_cnic'].get().strip(),
                    entries['w1_phone'].get().strip(),
                    entries['w2_name'].get().strip(),
                    entries['w2_cnic'].get().strip(),
                    entries['w2_phone'].get().strip()
                ))

            conn.commit()
            conn.close()
            
            clear_form()
            messagebox.showinfo("Success", "Tenant added successfully!")
            window.destroy()

        except ValueError as e:
            messagebox.showerror("Error", "Please check number fields (rent, deposit, advance) and make sure floor is a number")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save tenant: {str(e)}")

    def clear_form():
        # Clear all fields
        
        # Property Location
        entries['building_name'].delete(0, tk.END)
        floor_combo.set("1")
        entries['flat_no'].delete(0, tk.END)
        
        # Tenant Personal Information
        entries['name'].delete(0, tk.END)
        entries['father_name'].delete(0, tk.END)
        entries['cnic'].delete(0, tk.END)
        entries['phone'].delete(0, tk.END)
        entries['emergency_contact'].delete(0, tk.END)
        entries['profession'].delete(0, tk.END)
        
        # Financial Information
        entries['rent_amount'].delete(0, tk.END)
        entries['security_deposit'].delete(0, tk.END)
        entries['advance_payment'].delete(0, tk.END)
        
        # Dates
        entries['entry_date'].delete(0, tk.END)
        entries['exit_date'].delete(0, tk.END)
        
        # Owner Information
        entries['owner_name'].delete(0, tk.END)
        entries['owner_phone'].delete(0, tk.END)
        
        # Witness Information
        entries['w1_name'].delete(0, tk.END)
        entries['w1_cnic'].delete(0, tk.END)
        entries['w1_phone'].delete(0, tk.END)
        entries['w2_name'].delete(0, tk.END)
        entries['w2_cnic'].delete(0, tk.END)
        entries['w2_phone'].delete(0, tk.END)
        
        # Additional Notes
        notes_text.delete('1.0', tk.END)
        
        # Photo
        remove_photo()
        
        # Focus on first field
        entries['building_name'].focus_set()

    # Button frame
    button_frame = tk.Frame(form_frame, bg="#f0f8ff")
    button_frame.grid(row=7, column=0, columnspan=2, pady=20)

    # buttons
    tk.Button(button_frame, text="💾 Save Tenant", bg="#1644A1", fg="white",
            font=("Segoe UI", 12, "bold"), width=13, command=save_tenant).pack(side=tk.LEFT, padx=5)

    tk.Button(button_frame, text="🧹 Clear Form", bg="#FC8F54", fg="white",
            font=("Segoe UI", 12, "bold"), width=13, command=clear_form).pack(side=tk.LEFT, padx=5)

    tk.Button(button_frame, text="❌ Cancel", bg="#83868D", fg="white",
            font=("Segoe UI", 12, "bold"), width=13, command=window.destroy).pack(side=tk.LEFT, padx=5)
        

    # Configure grid weights
    for i in range(2):
        form_frame.columnconfigure(i, weight=1)

    # Mouse wheel scrolling
    def on_mousewheel(event):
        try:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except tk.TclError:
            canvas.unbind_all("<MouseWheel>")

    # Binding
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    def close_window():
        canvas.unbind_all("<MouseWheel>")
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", close_window)
