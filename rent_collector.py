import tkinter as tk
from tkinter import ttk, messagebox
from create_database import get_connection
from datetime import datetime


def open_rent_collector():
    window = tk.Toplevel()
    window.title("Abu Huraira Enterprises - Created by .ARS")
    window.geometry("1300x750")
    window.config(bg="#000000")
    window.resizable(True, True)

    # ========== SCROLLBAR FOR WHOLE PAGE ==========
    # Create main container
    main_container = tk.Frame(window, bg="#f8fafc")
    main_container.pack(fill="both", expand=True)

    # Create canvas and scrollbar
    canvas = tk.Canvas(main_container, bg="#f8fafc", highlightthickness=0)
    scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    
    # Create scrollable frame
    scrollable_frame = tk.Frame(canvas, bg="#f8fafc")
    
    # Configure canvas
    scrollable_frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    def configure_scrollregion(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(scrollable_frame_id, width=event.width)
    
    scrollable_frame.bind("<Configure>", configure_scrollregion)
    canvas.bind("<Configure>", lambda e: canvas.itemconfig(scrollable_frame_id, width=e.width))
    
    # Pack
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Mouse wheel scrolling
    def on_mousewheel(event):
        try:
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        except tk.TclError:
            canvas.unbind_all("<MouseWheel>")
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    def close_window():
        canvas.unbind_all("<MouseWheel>")
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", close_window)

    # ========== HEADER ==========
    header_frame = tk.Frame(scrollable_frame, bg="#1e3a8a", height=110)
    header_frame.pack(fill="x", pady=(0, 20))
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="Abu Huraira Management \nRent Collector Information", 
             font=("Segoe UI", 18, "bold"), bg="#1e3a8a", fg="white").pack(pady=15)

    # ========== MAIN CONTENT FRAME ==========
    main_frame = tk.Frame(scrollable_frame, bg="#f8fafc")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # LEFT FRAME - Form
    left_frame = tk.LabelFrame(main_frame, text="Add New Rent Collector", 
                               font=("Segoe UI", 12, "bold"), 
                               bg="#f8fafc", padx=15, pady=15)
    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

    # RIGHT FRAME - List
    right_frame = tk.LabelFrame(main_frame, text="Rent Collectors List", 
                                font=("Segoe UI", 12, "bold"), 
                                bg="#f8fafc", padx=15, pady=15)
    right_frame.pack(side="right", fill="both", expand=True)

    # ========== LEFT FORM FIELDS ==========
    form_frame = tk.Frame(left_frame, bg="#f8fafc")
    form_frame.pack(fill="both", expand=True)

    # Dictionary to store entry widgets
    entries = {}
    row = 0
    selected_collector_id = None

    # Building Name
    tk.Label(form_frame, text="Building Name *", bg="#f8fafc", 
             font=("Segoe UI", 11)).grid(row=row, column=0, sticky="w", pady=8, padx=5)
    building_entry = tk.Entry(form_frame, width=30, font=("Segoe UI", 11), relief="solid", bd=1)
    building_entry.grid(row=row, column=1, pady=8, padx=5)
    entries['building_name'] = building_entry
    row += 1

    # Rent Collector Name
    tk.Label(form_frame, text="Rent Collector Name *", bg="#f8fafc", 
             font=("Segoe UI", 11)).grid(row=row, column=0, sticky="w", pady=8, padx=5)
    collector_name_entry = tk.Entry(form_frame, width=30, font=("Segoe UI", 11), relief="solid", bd=1)
    collector_name_entry.grid(row=row, column=1, pady=8, padx=5)
    entries['rent_collector_name'] = collector_name_entry
    row += 1

    # Father Name
    tk.Label(form_frame, text="Father Name *", bg="#f8fafc", 
             font=("Segoe UI", 11)).grid(row=row, column=0, sticky="w", pady=8, padx=5)
    father_entry = tk.Entry(form_frame, width=30, font=("Segoe UI", 11), relief="solid", bd=1)
    father_entry.grid(row=row, column=1, pady=8, padx=5)
    entries['father_name'] = father_entry
    row += 1

    # CNIC
    tk.Label(form_frame, text="CNIC * (13 digits)", bg="#f8fafc", 
             font=("Segoe UI", 11)).grid(row=row, column=0, sticky="w", pady=8, padx=5)
    cnic_entry = tk.Entry(form_frame, width=30, font=("Segoe UI", 11), relief="solid", bd=1)
    cnic_entry.grid(row=row, column=1, pady=8, padx=5)
    entries['cnic'] = cnic_entry
    row += 1

    # Phone Number
    tk.Label(form_frame, text="Phone Number *", bg="#f8fafc", 
             font=("Segoe UI", 11)).grid(row=row, column=0, sticky="w", pady=8, padx=5)
    phone_entry = tk.Entry(form_frame, width=30, font=("Segoe UI", 11), relief="solid", bd=1)
    phone_entry.grid(row=row, column=1, pady=8, padx=5)
    entries['phone'] = phone_entry
    row += 1

    # Reporting To
    tk.Label(form_frame, text="Reporting To *", bg="#f8fafc", 
             font=("Segoe UI", 11)).grid(row=row, column=0, sticky="w", pady=8, padx=5)
    reporting_entry = tk.Entry(form_frame, width=30, font=("Segoe UI", 11), relief="solid", bd=1)
    reporting_entry.grid(row=row, column=1, pady=8, padx=5)
    entries['reporting_to'] = reporting_entry
    row += 1

    # Button Frame
    button_frame = tk.Frame(form_frame, bg="#f8fafc")
    button_frame.grid(row=row, column=0, columnspan=2, pady=20)

    # ========== RIGHT FRAME - TABLE ==========
    # Search Frame
    search_frame = tk.Frame(right_frame, bg="#f8fafc")
    search_frame.pack(fill="x", pady=(0, 10))

    tk.Label(search_frame, text="🔍 Search:", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold")).pack(side="left", padx=5)
    
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, width=30, 
                           font=("Segoe UI", 10), relief="solid", bd=1)
    search_entry.pack(side="left", padx=5, pady=5)
    search_entry.focus_set()
    
    # Clear button for search
    clear_search_btn = tk.Button(search_frame, text="✖", 
                                command=lambda: clear_search(),
                                bg="#dc3545", fg="white", font=("Segoe UI", 8, "bold"),
                                width=2, height=1, cursor="hand2")
    clear_search_btn.pack(side="left", padx=2)
    
    # Results count label
    results_var = tk.StringVar(value="")
    results_label = tk.Label(search_frame, textvariable=results_var, bg="#f8fafc", 
                            font=("Segoe UI", 9), fg="#1e3a8a")
    results_label.pack(side="left", padx=10)

    # Live search on key release
    def on_search_keyrelease(event):
        load_collectors()
    
    search_entry.bind('<KeyRelease>', on_search_keyrelease)

    def clear_search():
        search_var.set("")
        search_entry.delete(0, tk.END)
        load_collectors()
        search_entry.focus_set()

    # Treeview Frame
    tree_frame = tk.Frame(right_frame, bg="#f8fafc")
    tree_frame.pack(fill="both", expand=True)

    # Scrollbars
    v_scroll = ttk.Scrollbar(tree_frame, orient="vertical")
    h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal")

    # Treeview
    columns = ("S.No.", "Building", "Collector Name", "Father Name", "CNIC", "Phone", 
                "Reporting To", "Created Date")
    
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", 
                        yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set, height=15)

    # Configure scrollbars
    v_scroll.config(command=tree.yview)
    h_scroll.config(command=tree.xview)

    # Define headings and columns
    col_widths = [50, 120, 150, 150, 130, 100, 120, 130]
    for i, col in enumerate(columns):
        tree.heading(col, text=col)
        tree.column(col, width=col_widths[i], anchor="center")

    # Grid layout
    tree.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    h_scroll.grid(row=1, column=0, sticky="ew")

    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    # ========== FUNCTIONS DEFINITION ==========

    def validate_cnic(cnic):
        """Validate CNIC - must be 13 digits"""
        import re
        return re.match(r'^\d{13}$', cnic) is not None

    def validate_phone(phone):
        """Validate phone number - clean and check length"""
        import re
        # Extract only digits
        clean_phone = re.sub(r'\D', '', phone)
        # Allow 10-13 digits
        return 10 <= len(clean_phone) <= 13

    def load_collectors(*args):
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        conn = get_connection()
        c = conn.cursor()
        
        # Get search text
        search_text = search_var.get().strip()
        
        try:
            if search_text:
                # Search in all relevant columns
                query = """SELECT id, building_name, rent_collector_name, father_name, cnic, phone,
                            reporting_to, strftime('%d-%m-%Y', created_date) as created_date
                        FROM rent_collectors 
                        WHERE building_name LIKE ? 
                            OR rent_collector_name LIKE ? 
                            OR father_name LIKE ? 
                            OR cnic LIKE ? 
                            OR phone LIKE ?
                            OR reporting_to LIKE ?
                        ORDER BY 
                            CASE 
                                WHEN rent_collector_name LIKE ? THEN 1
                                WHEN building_name LIKE ? THEN 2
                                ELSE 3
                            END,
                            created_date DESC"""
                search_pattern = f"%{search_text}%"
                # Double pattern for ORDER BY CASE
                c.execute(query, (search_pattern, search_pattern, search_pattern, 
                                search_pattern, search_pattern, search_pattern,
                                f"{search_text}%", f"{search_text}%"))  # For exact starts with priority
            else:
                query = """SELECT id, building_name, rent_collector_name, father_name, cnic, phone,
                                reporting_to,strftime('%d-%m-%Y', created_date) as created_date
                        FROM rent_collectors ORDER BY created_date DESC"""
                c.execute(query)
            
            collectors = c.fetchall()
            
            # Update results count
            results_var.set(f"{len(collectors)} record(s) found")
            
            # Insert into treeview with ID as iid
            for idx, collector in enumerate(collectors, start=1):
                # Format phone number
                phone = collector[5] or ""
                if len(phone) == 11:
                    phone = f"{phone[:4]}-{phone[4:]}"
                
                formatted_values = [
                    idx,
                    collector[1] or "",  # building_name
                    collector[2] or "",  # rent_collector_name
                    collector[3] or "",  # father_name
                    collector[4] or "",  # cnic
                    phone,                # formatted phone
                    collector[6] or "",
                    collector[7] or "",  # reporting_to
                ]
                # Store actual ID as iid for easy access
                tree.insert("", "end", iid=str(collector[0]), values=formatted_values)
                
                # Apply alternating row colors
                if idx % 2 == 0:
                    tree.tag_configure('evenrow', background='#f0f8ff')
                    tree.item(tree.get_children()[-1], tags=('evenrow',))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load collectors: {str(e)}")
        finally:
            conn.close()

    def on_collector_select(event):
        # Fill form fields
        nonlocal selected_collector_id
        selected = tree.selection()
        if not selected:
            return
        
        # Get selected item
        collector_id = selected[0]
        item = tree.item(collector_id)
        values = item['values']
        
        if values:
            selected_collector_id = int(collector_id)
            
            # Form fields
            entries['building_name'].delete(0, tk.END)
            entries['building_name'].insert(0, values[1])
            
            entries['rent_collector_name'].delete(0, tk.END)
            entries['rent_collector_name'].insert(0, values[2])
            
            entries['father_name'].delete(0, tk.END)
            entries['father_name'].insert(0, values[3])
            
            entries['cnic'].delete(0, tk.END)
            entries['cnic'].insert(0, values[4])
            
            entries['phone'].delete(0, tk.END)
            entries['phone'].insert(0, values[5])
            
            entries['reporting_to'].delete(0, tk.END)
            entries['reporting_to'].insert(0, values[6])

    def edit_collector():
        """Edit selected collector information"""
        nonlocal selected_collector_id
        
        if not selected_collector_id:
            messagebox.showwarning("Warning", "Please select a collector to edit!")
            return
        
        try:
            # Get value from Form
            building_name = entries['building_name'].get().strip()
            collector_name = entries['rent_collector_name'].get().strip()
            father_name = entries['father_name'].get().strip()
            cnic = entries['cnic'].get().strip()
            phone = entries['phone'].get().strip()
            
            reporting_to = entries['reporting_to'].get().strip()
            # Validate required fields
            if not all([building_name, collector_name, father_name, cnic, phone, 
                    reporting_to]):
                messagebox.showerror("Error", "Please fill all required fields (*)")
                return

            # Clean phone number
            import re
            clean_phone = re.sub(r'\D', '', phone)
            
            # Validate CNIC
            if not validate_cnic(cnic):
                messagebox.showerror("Error", "Invalid CNIC! Please enter 13 digits without dashes")
                return

            # Validate Phone
            if not (clean_phone.isdigit() and 10 <= len(clean_phone) <= 13):
                messagebox.showerror("Error", "Invalid Phone Number! Please enter 10-13 digits")
                return

            # Database update
            conn = get_connection()
            c = conn.cursor()
            
            c.execute('''UPDATE rent_collectors 
                        SET building_name=?, rent_collector_name=?, father_name=?, 
                            cnic=?, phone=?, reporting_to=? WHERE id=?''',
                        (building_name, collector_name, father_name, cnic, clean_phone,
                         reporting_to, selected_collector_id))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Rent Collector updated successfully!")
            clear_form()
            load_collectors()
            selected_collector_id = None

        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {str(e)}")

        
    def delete_collector():
        """Delete selected collector"""
        nonlocal selected_collector_id
        
        if not selected_collector_id:
            messagebox.showwarning("Warning", "Please select a collector to delete!")
            return
        
        result = messagebox.askyesno("Confirm Delete", 
                                    "Are you sure you want to delete this rent collector?")
        
        if result:
            try:
                conn = get_connection()
                c = conn.cursor()
                
                c.execute("DELETE FROM rent_collectors WHERE id=?", (selected_collector_id,))
                
                conn.commit()
                conn.close()
                
                messagebox.showinfo("Success", "Rent Collector deleted successfully!")
                clear_form()
                load_collectors()
                selected_collector_id = None
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {str(e)}")

    def save_collector():
        """Save rent collector to database"""
        try:
            # Get values
            building_name = building_entry.get().strip()
            collector_name = collector_name_entry.get().strip()
            father_name = father_entry.get().strip()
            cnic = cnic_entry.get().strip()
            phone = phone_entry.get().strip()
            reporting_to = reporting_entry.get().strip()

            # Validate required fields
            if not all([building_name, collector_name, father_name, cnic, phone, 
                    reporting_to]):
                messagebox.showerror("Error", "Please fill all required fields (*)")
                return

            # Validate CNIC
            if not validate_cnic(cnic):
                messagebox.showerror("Error", "Invalid CNIC! Please enter 13 digits without dashes")
                return

            # Clean phone number
            import re
            clean_phone = re.sub(r'\D', '', phone)
            
            # Validate Phone
            if not (clean_phone.isdigit() and 10 <= len(clean_phone) <= 13):
                messagebox.showerror("Error", "Invalid Phone Number! Please enter 10-13 digits")
                return

            # Database operations
            conn = get_connection()
            c = conn.cursor()
            
            # Check if CNIC already exists
            c.execute("SELECT id FROM rent_collectors WHERE cnic = ?", (cnic,))
            if c.fetchone():
                messagebox.showerror("Error", "Rent Collector with this CNIC already exists!")
                conn.close()
                return

            # Insert data
            c.execute('''INSERT INTO rent_collectors 
                (building_name, rent_collector_name, father_name, cnic, phone, 
                 reporting_to)
                VALUES (?, ?, ?, ?, ?, ?)''',
                (building_name, collector_name, father_name, cnic, clean_phone,
                reporting_to))

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Rent Collector added successfully!")
            clear_form()
            load_collectors()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")

    def clear_form():
        """Clear all form fields"""
        nonlocal selected_collector_id
        selected_collector_id = None

        for key in ['building_name','rent_collector_name',
                'father_name','cnic','phone','reporting_to']:
            entries[key].delete(0, tk.END)

        building_entry.focus_set()
        
    # Bind treeview selection
    tree.bind('<<TreeviewSelect>>', on_collector_select)

    # ========== RIGHT FRAME ACTION BUTTONS ==========
    action_frame = tk.Frame(right_frame, bg="#f8fafc")
    action_frame.pack(fill="x", pady=10, padx=5)

    # Make sure frame has enough height
    action_frame.configure(height=50)
    action_frame.pack_propagate(False)

    # Configure grid
    action_frame.columnconfigure(0, weight=1)
    action_frame.columnconfigure(1, weight=1)
    action_frame.columnconfigure(2, weight=1)

    # Edit Button
    tk.Button(action_frame, text="✏️ Edit Collector", command=edit_collector,
            bg="#121481", fg="white", font=("Segoe UI", 11, "bold"),
            width=15, height=2, relief="raised", bd=2, cursor="hand2").grid(
            row=0, column=0, padx=5, pady=5, sticky="ew")

    # Delete Button
    tk.Button(action_frame, text="🗑️ Delete Collector", command=delete_collector,
            bg="#DC3C22", fg="white", font=("Segoe UI", 11, "bold"),
            width=15, height=2, relief="raised", bd=2, cursor="hand2").grid(
            row=0, column=1, padx=5, pady=5, sticky="ew")

    # Refresh Button
    tk.Button(action_frame, text="🔄 Refresh List", command=lambda: load_collectors(),
            bg="#090b0a", fg="white", font=("Segoe UI", 11, "bold"),
            width=15, height=2, relief="raised", bd=2, cursor="hand2").grid(
            row=0, column=2, padx=5, pady=5, sticky="ew")

    # Buttons - LEFT FRAME
    tk.Button(button_frame, text="💾 Save Collector", command=save_collector,
              bg="#069767", fg="white", font=("Segoe UI", 11, "bold"),
              width=14, height=2, relief="raised", bd=2).pack(side="left", padx=5)

    tk.Button(button_frame, text="❌ Close", command=window.destroy,
              bg="#e24040", fg="white", font=("Segoe UI", 11, "bold"),
              width=14, height=2, relief="raised", bd=2).pack(side="left", padx=5)
    
    tk.Button(button_frame, text="🧹 Clear Form", command=clear_form,
              bg="#1BABE9", fg="white", font=("Segoe UI", 11, "bold"),
              width=14, height=2, relief="raised", bd=2).pack(side="left", padx=5)

    # Load initial data
    load_collectors()