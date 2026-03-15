import tkinter as tk
from tkinter import ttk, messagebox
from create_database import get_connection
from datetime import datetime
from building_collection import open_building_collection


editing_payment_id = None
def open_payments():
    global editing_payment_id
    editing_payment_id = None

    window = tk.Toplevel()
    window.title("Abu Huraira Enterprises - Created by .ARS")
    window.geometry("1400x930")
    window.config(bg="#f8fafc")

    # Header
    header_frame = tk.Frame(window, bg="#1e3a8a", height=120)
    header_frame.pack(fill="x", pady=(0, 20))
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="Abu Huraira Enterprises \nPayments & Bills Management", 
             font=("Segoe UI", 18, "bold"), bg="#1e3a8a", fg="white").pack(pady=20)

    # Container frame for horizontal placement
    top_frame = tk.Frame(window, bg="#f8fafc")
    top_frame.pack(fill="x", pady=10, padx=10)

    # --------------- Building Collection Button ---------------
    tk.Button(top_frame, text="Building Collection", command=open_building_collection,
            bg="#065021", fg="white", font=("Segoe UI", 10, "bold"), width=20, height=2, cursor="hand2").pack(side="left")
    
    # ========== MAIN CONTENT WITH SCROLLBAR ==========
    # Create a container for canvas and scrollbar
    main_container = tk.Frame(window, bg="#f8fafc")
    main_container.pack(fill="both", expand=True, padx=20, pady=10)

    # Create canvas and scrollbar
    canvas = tk.Canvas(main_container, bg="#f8fafc", highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    
    # Scrollable frame
    scrollable_frame = tk.Frame(canvas, bg="#f8fafc")
    
    # Configure canvas
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    # Canvas width
    def configure_canvas(event):
        canvas.itemconfig(frame_id, width=event.width)
    
    canvas.bind("<Configure>", configure_canvas)
    
    # Create window in canvas
    frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    
    # Configure canvas scrolling
    canvas.configure(yscrollcommand=scrollbar.set)
    
    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Mouse wheel scrolling
    def on_mousewheel(event):
        # Check if widget under mouse
        widget = window.winfo_containing(event.x_root, event.y_root)
        
        # Don't scroll if we're over a combobox or entry
        if widget and isinstance(widget, (ttk.Combobox, tk.Entry, tk.Spinbox, tk.Listbox)):
            return "break"
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"
    
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mousewheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    # Unbind mousewheel
    def on_closing():
        canvas.unbind_all("<MouseWheel>")
        window.destroy()
    
    window.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Main Content Frame
    main_frame = tk.Frame(scrollable_frame, bg="#f8fafc")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ========== LEFT FRAME WITH SCROLLBAR ==========
    left_container = tk.Frame(main_frame, bg="#f8fafc")
    left_container.pack(side="left", fill="both", expand=True, padx=(0, 10))

    # Left Frame - Payment Entry
    left_frame = tk.LabelFrame(left_container, text="Payment Entry", 
                              font=("Segoe UI", 12, "bold"), 
                              bg="#f8fafc", padx=15, pady=15)
    left_frame.pack(fill="both", expand=True)

    # ========== RIGHT FRAME - WITH TWO TABLES ==========
    right_frame = tk.LabelFrame(main_frame, text="Payment History", 
                               font=("Segoe UI", 12, "bold"), 
                               bg="#f8fafc", padx=15, pady=15)
    right_frame.pack(side="right", fill="both", expand=True)

    # Create a PanedWindow to split into two sections
    right_paned = tk.PanedWindow(right_frame, orient="vertical", bg="#f8fafc", 
                                 sashrelief="raised", sashwidth=5, sashpad=2)
    right_paned.pack(fill="both", expand=True)

    # ========== TOP SECTION - PAID PAYMENTS ==========
    top_frame = tk.Frame(right_paned, bg="#f8fafc")
    right_paned.add(top_frame, height=350, minsize=200)

    # Search Frame for top section
    search_frame_top = tk.Frame(top_frame, bg="#f8fafc")
    search_frame_top.pack(fill="x", pady=(0, 10))

    tk.Label(search_frame_top, text="Search:", bg="#f8fafc", 
             font=("Segoe UI", 9)).grid(row=0, column=0, padx=2)
    search_var_top = tk.StringVar()
    search_entry_top = tk.Entry(search_frame_top, textvariable=search_var_top, width=20)
    search_entry_top.grid(row=0, column=1, padx=2)

    tk.Label(search_frame_top, text="Month:", bg="#f8fafc", 
             font=("Segoe UI", 9)).grid(row=0, column=2, padx=(10,2))
    search_month_var_top = tk.StringVar()
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    search_month_combo_top = ttk.Combobox(search_frame_top, 
                                         textvariable=search_month_var_top, 
                                         values=["All"] + months, 
                                         state="readonly", width=10)
    search_month_combo_top.grid(row=0, column=3, padx=2)

    # Disable mouse wheel change
    search_month_combo_top.bind("<MouseWheel>", lambda e: "break")
    search_month_combo_top.set("All")

    tk.Label(search_frame_top, text="Status:", bg="#f8fafc", 
             font=("Segoe UI", 9)).grid(row=0, column=4, padx=(10,2))
    search_status_var_top = tk.StringVar()
    search_status_combo_top = ttk.Combobox(search_frame_top, 
                                          textvariable=search_status_var_top, 
                                          values=["All", "Paid", "Partial"], 
                                          state="readonly", width=10)
    search_status_combo_top.grid(row=0, column=5, padx=2)
    search_status_combo_top.set("All")
    
    # Treeview for Top Table
    tree_frame_top = tk.Frame(top_frame, bg="#f8fafc")
    tree_frame_top.pack(fill="both", expand=True)

    # Columns for top table
    columns_top = ("S.No.", "Tenant", "Building", "Collector", "Month-Year", 
                   "Rent", "Gas", "Water", "Electric", "Total", "Paid", "Balance", "Status")
    
    tree_top = ttk.Treeview(tree_frame_top, columns=columns_top, show="headings", height=8)
    
    # Define headings
    for col in columns_top:
        tree_top.heading(col, text=col)
        tree_top.column(col, stretch=False)
    
    # Column widths
    tree_top.column("S.No.", width=50, anchor="center")
    tree_top.column("Tenant", width=120, anchor="center")
    tree_top.column("Building", width=100, anchor="center")
    tree_top.column("Collector", width=120, anchor="center")
    tree_top.column("Month-Year", width=100, anchor="center")
    tree_top.column("Rent", width=90, anchor="center")
    tree_top.column("Gas", width=70, anchor="center")
    tree_top.column("Water", width=70, anchor="center")
    tree_top.column("Electric", width=70, anchor="center")
    tree_top.column("Total", width=90, anchor="center")
    tree_top.column("Paid", width=90, anchor="center")
    tree_top.column("Balance", width=90, anchor="center")
    tree_top.column("Status", width=80, anchor="center")

    # Scrollbars for top table
    v_scroll_top = ttk.Scrollbar(tree_frame_top, orient="vertical")
    h_scroll_top = ttk.Scrollbar(tree_frame_top, orient="horizontal")
    
    # Configure treeview with scrollbars
    tree_top.configure(yscrollcommand=v_scroll_top.set, xscrollcommand=h_scroll_top.set)
    v_scroll_top.configure(command=tree_top.yview)
    h_scroll_top.configure(command=tree_top.xview)

    # Grid layout
    tree_top.grid(row=0, column=0, sticky="nsew")
    v_scroll_top.grid(row=0, column=1, sticky="ns")
    h_scroll_top.grid(row=1, column=0, columnspan=2, sticky="ew")

    # Make sure the frame expands properly
    tree_frame_top.grid_rowconfigure(0, weight=1)
    tree_frame_top.grid_columnconfigure(0, weight=1)
    
    # ========== BOTTOM SECTION - PENDING PAYMENTS ==========
    bottom_frame = tk.Frame(right_paned, bg="#f8fafc")
    right_paned.add(bottom_frame, height=330, minsize=150)

    # Summary Frame for pending payments
    summary_frame = tk.Frame(bottom_frame, bg="#e6f7ff", height=40)
    summary_frame.pack(fill="x", pady=(0, 10))

    pending_count_var = tk.StringVar(value="Current Month Pending: 0")
    pending_amount_var = tk.StringVar(value="Amount: Rs. 0")

    tk.Label(summary_frame, textvariable=pending_count_var, bg="#e6f7ff", 
            font=("Segoe UI", 11, "bold"), fg="#131062").pack(side="left", padx=20)
    tk.Label(summary_frame, textvariable=pending_amount_var, bg="#e6f7ff", 
            font=("Segoe UI", 11, "bold"), fg="#173474").pack(side="left", padx=20)


    # Search Frame for bottom section
    search_frame_bottom = tk.Frame(bottom_frame, bg="#f8fafc")
    search_frame_bottom.pack(fill="x", pady=(0, 10))

    tk.Label(search_frame_bottom, text="Month:", bg="#f8fafc", 
             font=("Segoe UI", 9)).grid(row=0, column=0, padx=2)
    
    
    search_month_var_bottom = tk.StringVar()
    current_month = datetime.now().strftime("%B")
    search_month_combo_bottom = ttk.Combobox(search_frame_bottom, 
                                            textvariable=search_month_var_bottom, 
                                            values=months, state="readonly", width=10)
    search_month_combo_bottom.grid(row=0, column=1, padx=2)

    # Disable mouse wheel change
    search_month_combo_bottom.bind("<MouseWheel>", lambda e: "break")
    search_month_combo_bottom.set(current_month)

    tk.Label(search_frame_bottom, text="Year:", bg="#f8fafc", 
             font=("Segoe UI", 9)).grid(row=0, column=2, padx=(10,2))
    
    search_year_var_bottom = tk.StringVar()
    current_year = str(datetime.now().year)
    years = [str(i) for i in range(2026, 2031)]
    search_year_combo_bottom = ttk.Combobox(search_frame_bottom, 
                                           textvariable=search_year_var_bottom, 
                                           values=years, state="readonly", width=8)
    search_year_combo_bottom.grid(row=0, column=3, padx=2)
    # Disable mouse wheel change
    search_year_combo_bottom.bind("<MouseWheel>", lambda e: "break")
    search_year_combo_bottom.set(str(current_year))

    # Treeview for Bottom Table
    tree_frame_bottom = tk.Frame(bottom_frame, bg="#f8fafc")
    tree_frame_bottom.pack(fill="both", expand=True)

    # Columns for bottom table
    columns_bottom = ("S.No.", "Tenant", "Building", "Flat", "Phone", "Rent Amount", "Status")
    
    tree_bottom = ttk.Treeview(tree_frame_bottom, columns=columns_bottom, show="headings", height=6)
    
    # Define headings
    tree_bottom.heading("S.No.", text="S.No.")
    tree_bottom.heading("Tenant", text="Tenant")
    tree_bottom.heading("Building", text="Building")
    tree_bottom.heading("Flat", text="Flat No")
    tree_bottom.heading("Phone", text="Phone")
    tree_bottom.heading("Rent Amount", text="Rent Amount")
    tree_bottom.heading("Status", text="Status")
    
    # Column widths
    tree_bottom.column("S.No.", width=10, anchor="center")
    tree_bottom.column("Tenant", width=120, anchor="center")
    tree_bottom.column("Building", width=120, anchor="center")
    tree_bottom.column("Flat", width=30, anchor="center")
    tree_bottom.column("Phone", width=60, anchor="center")
    tree_bottom.column("Rent Amount", width=60, anchor="center")
    tree_bottom.column("Status", width=110, anchor="center")

    # Scrollbars for bottom table
    v_scroll_bottom = ttk.Scrollbar(tree_frame_bottom, orient="vertical")
    h_scroll_bottom = ttk.Scrollbar(tree_frame_bottom, orient="horizontal")
    
    # Configure treeview
    tree_bottom.configure(yscrollcommand=v_scroll_bottom.set, xscrollcommand=h_scroll_bottom.set)
    v_scroll_bottom.configure(command=tree_bottom.yview)
    h_scroll_bottom.configure(command=tree_bottom.xview)

    # Grid layout
    tree_bottom.grid(row=0, column=0, sticky="nsew")
    v_scroll_bottom.grid(row=0, column=1, sticky="ns")
    h_scroll_bottom.grid(row=1, column=0, sticky="ew")

    tree_frame_bottom.grid_rowconfigure(0, weight=1)
    tree_frame_bottom.grid_columnconfigure(0, weight=1)

    # ========== PAYMENT ENTRY FORM ==========
    form_frame = tk.Frame(left_frame, bg="#f8fafc")
    form_frame.pack(fill="both", expand=True, padx=5, pady=5)

    # Row 0: Select Tenant
    tk.Label(form_frame, text="Select Tenant *", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=0, column=0, sticky="w", pady=8)
    
    tenant_var = tk.StringVar()
    tenant_combo = ttk.Combobox(form_frame, textvariable=tenant_var, 
                               state="readonly", width=22, font=("Segoe UI", 10))
    tenant_combo.grid(row=0, column=1, pady=8, padx=10, sticky="w")

    tenant_combo.bind("<MouseWheel>", lambda e: "break")
    tenant_combo.set("-- Select Tenant --")

    # Row 1: Building Name
    tk.Label(form_frame, text="Building Name", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=1, column=0, sticky="w", pady=8)
    
    building_var = tk.StringVar()
    building_label = tk.Label(form_frame, textvariable=building_var, bg="#f0f0f0", 
                             font=("Segoe UI", 10), width=25, anchor="w", relief="sunken", bd=1)
    building_label.grid(row=1, column=1, pady=8, padx=10, sticky="w")

    # Row 2: Rent Collector
    tk.Label(form_frame, text="Rent Collector", bg="#f8fafc", 
            font=("Segoe UI", 10, "bold italic")).grid(row=2, column=0, sticky="w", pady=8)

    collector_var = tk.StringVar()
    collector_label = tk.Label(form_frame, textvariable=collector_var, bg="#f0f0f0", 
                            font=("Segoe UI", 10), width=25, anchor="w", relief="sunken", bd=1)
    collector_label.grid(row=2, column=1, pady=8, padx=10, sticky="w")
    collector_var.set("Not Assigned")

    # Row 3: Month
    tk.Label(form_frame, text="Month *", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=3, column=0, sticky="w", pady=8)
    
    month_var = tk.StringVar()
    month_combo = ttk.Combobox(form_frame, textvariable=month_var, 
                              values=months, state="readonly", width=22, font=("Segoe UI", 10))
    month_combo.grid(row=3, column=1, pady=8, padx=10, sticky="w")

    month_combo.bind("<MouseWheel>", lambda e: "break")
    month_combo.set("February")

    # Row 4: Year
    tk.Label(form_frame, text="Year *", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=4, column=0, sticky="w", pady=8)
    
    year_var = tk.StringVar()
    year_combo = ttk.Combobox(form_frame, textvariable=year_var, 
                             values=years, state="readonly", width=22, font=("Segoe UI", 10))
    year_combo.grid(row=4, column=1, pady=8, padx=10, sticky="w")
    
    # Disable mouse wheel change
    year_combo.bind("<MouseWheel>", lambda e: "break")
    year_combo.set("2026")

    # Row 5: Payment Date
    tk.Label(form_frame, text="Payment Date *", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=5, column=0, sticky="w", pady=8)
    
    payment_date_var = tk.StringVar()
    payment_date_entry = tk.Entry(form_frame, textvariable=payment_date_var, 
                                  width=25, font=("Segoe UI", 10), relief="solid", bd=1)
    payment_date_entry.grid(row=5, column=1, pady=8, padx=10, sticky="w")
    payment_date_var.set(datetime.now().strftime("%d-%m-%Y"))

    # Row 6: Rent Amount
    tk.Label(form_frame, text="Rent Amount *", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=6, column=0, sticky="w", pady=8)
    
    rent_var = tk.StringVar()
    rent_entry = tk.Entry(form_frame, textvariable=rent_var, 
                          width=25, font=("Segoe UI", 10), relief="solid", bd=1)
    rent_entry.grid(row=6, column=1, pady=8, padx=10, sticky="w")

    # Row 7: Utility Bills Label
    tk.Label(form_frame, text="Utility Bills", bg="#f8fafc", 
             font=("Segoe UI", 11, "bold italic"), fg="#1e3a8a").grid(row=7, column=0, columnspan=2, sticky="w", pady=(15,5))

    # Row 8: Gas Bill
    tk.Label(form_frame, text="Gas Bill", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=8, column=0, sticky="w", pady=5, padx=(20,0))
    
    gas_var = tk.StringVar(value="0")
    gas_entry = tk.Entry(form_frame, textvariable=gas_var, width=20, font=("Segoe UI", 10))
    gas_entry.grid(row=8, column=1, pady=5, padx=10, sticky="w")

    # Row 9: Water Bill
    tk.Label(form_frame, text="Water Bill", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=9, column=0, sticky="w", pady=5, padx=(20,0))
    
    water_var = tk.StringVar(value="0")
    water_entry = tk.Entry(form_frame, textvariable=water_var, width=20, font=("Segoe UI", 10))
    water_entry.grid(row=9, column=1, pady=5, padx=10, sticky="w")

    # Row 10: Electricity Bill
    tk.Label(form_frame, text="Electricity Bill", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=10, column=0, sticky="w", pady=5, padx=(20,0))
    
    electricity_var = tk.StringVar(value="0")
    electricity_entry = tk.Entry(form_frame, textvariable=electricity_var, width=20, font=("Segoe UI", 10))
    electricity_entry.grid(row=10, column=1, pady=5, padx=10, sticky="w")

    # Row 11: Other Charges
    tk.Label(form_frame, text="Other Charges", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=11, column=0, sticky="w", pady=5, padx=(20,0))
    
    other_var = tk.StringVar(value="0")
    other_entry = tk.Entry(form_frame, textvariable=other_var, width=20, font=("Segoe UI", 10))
    other_entry.grid(row=11, column=1, pady=5, padx=10, sticky="w")

    # Row 12: Total Amount
    tk.Label(form_frame, text="Total Amount", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=12, column=0, sticky="w", pady=10)
    
    total_var = tk.StringVar(value="0")
    total_label = tk.Label(form_frame, textvariable=total_var, bg="#f8fafc", 
                          font=("Segoe UI", 11, "bold"), fg="#1e3a8a")
    total_label.grid(row=12, column=1, pady=10, padx=10, sticky="w")

    # Row 13: Paid Amount
    tk.Label(form_frame, text="Paid Amount *", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=13, column=0, sticky="w", pady=8)
    
    paid_var = tk.StringVar()
    paid_entry = tk.Entry(form_frame, textvariable=paid_var, 
                          width=25, font=("Segoe UI", 10), relief="solid", bd=1)
    paid_entry.grid(row=13, column=1, pady=8, padx=10, sticky="w")

    # Row 14: Balance Amount
    tk.Label(form_frame, text="Balance Amount", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=14, column=0, sticky="w", pady=8)
    
    balance_var = tk.StringVar(value="0")
    balance_label = tk.Label(form_frame, textvariable=balance_var, bg="#f8fafc", 
                            font=("Segoe UI", 11, "bold"), fg="#dc2626")
    balance_label.grid(row=14, column=1, pady=8, padx=10, sticky="w")

    # Row 15: Payment Method
    tk.Label(form_frame, text="Payment Method", bg="#f8fafc", 
             font=("Segoe UI", 10, "bold italic")).grid(row=15, column=0, sticky="w", pady=8)
    
    method_var = tk.StringVar(value="Cash")
    method_combo = ttk.Combobox(form_frame, textvariable=method_var, 
                               values=["Cash", "Bank Transfer", "Cheque", "Online"], 
                               state="readonly", width=22, font=("Segoe UI", 10))
    method_combo.grid(row=15, column=1, pady=8, padx=10, sticky="w")

    # Row 16: Buttons Frame
    button_frame = tk.Frame(form_frame, bg="#f8fafc")
    button_frame.grid(row=16, column=0, columnspan=2, pady=20)

    # ======= Add numeric validation =======
    def validate_numeric(P):
        if P == "":
            return True
        try:
            float(P)
            return True
        except ValueError:
            return False

    vcmd = window.register(validate_numeric)
    rent_entry.config(validate='key', validatecommand=(vcmd, '%P'))
    gas_entry.config(validate='key', validatecommand=(vcmd, '%P'))
    water_entry.config(validate='key', validatecommand=(vcmd, '%P'))
    electricity_entry.config(validate='key', validatecommand=(vcmd, '%P'))
    other_entry.config(validate='key', validatecommand=(vcmd, '%P'))
    paid_entry.config(validate='key', validatecommand=(vcmd, '%P'))
    # ========== FUNCTIONS==========
    
    def load_tenants():
        # Load active tenants
        global tenant_info
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, name, flat_no, building_name, rent_amount FROM tenants WHERE status='Active' ORDER BY name")
        tenants = c.fetchall()
        conn.close()
        
        tenant_combo.tenant_data = {}
        tenant_combo.building_data = {}
        tenant_info = {}
        
        values_list = ["-- Select Tenant --"]
        for id, name, flat_no, building, rent_amount in tenants:
            display_text = f"{name} (Flat: {flat_no}) {building}"
            values_list.append(display_text)
            tenant_combo.tenant_data[display_text] = id
            tenant_combo.building_data[display_text] = building
            tenant_info[display_text] = {
                "id": id,
                "name": name,
                "flat_no": flat_no,
                "building": building,
                "rent_amount": rent_amount
            }
        tenant_combo['values'] = values_list
        tenant_var.set("-- Select Tenant --")

    def load_tenant_details(event=None):
        tenant_display = tenant_var.get()
        if tenant_display in tenant_info:
            info = tenant_info[tenant_display]
            building_var.set(info['building'])
            rent_var.set(str(info['rent_amount']))
            load_rent_collector(info['building'])
        else:
            building_var.set("")
            collector_var.set("Not Assigned")
            rent_var.set("0")

    def load_rent_collector(building_name):
        # Load rent collector name
        if not building_name:
            collector_var.set("Not Assigned")
            return
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT rent_collector_name FROM rent_collectors WHERE building_name=?", 
                (building_name,))
        result = c.fetchone()
        conn.close()
        
        if result:
            collector_var.set(result[0])
        else:
            collector_var.set("Not Assigned")

    def calculate_totals(*args):
        # Calculate amounts
        try:
            rent = float(rent_var.get() or 0)
            gas = float(gas_var.get() or 0)
            water = float(water_var.get() or 0)
            electricity = float(electricity_var.get() or 0)
            other = float(other_var.get() or 0)
            paid = float(paid_var.get() or 0)
            
            total = rent + gas + water + electricity + other
            balance = total - paid
            
            total_var.set(f"{total:,.2f}")
            balance_var.set(f"{balance:,.2f}")
            
            if balance > 0:
                balance_label.config(fg="#dc2626")
            elif balance < 0:
                balance_label.config(fg="#f59e0b")
            else:
                balance_label.config(fg="#16a34a")

            if total == 0:
                total_label.config(fg="#6b7280")
            else:
                total_label.config(fg="#1e3a8a")
                
        except ValueError:
            pass

    def save_payment():
        """Save payment to database"""
        global editing_payment_id
        try:
            if not all([tenant_var.get(), month_var.get(), year_var.get(), 
                    payment_date_var.get(), rent_var.get(), paid_var.get()]):
                messagebox.showwarning("Input Error", "Please fill all required fields (*)")
                return

            if tenant_var.get() not in tenant_combo.tenant_data:
                messagebox.showwarning("Input Error", "Please select a valid tenant")
                return

            tenant_id = tenant_combo.tenant_data[tenant_var.get()]
            month_year = f"{month_var.get()}-{year_var.get()}"
            
            conn = get_connection()
            c = conn.cursor()

            # Get building name of tenant
            c.execute("SELECT building_name FROM tenants WHERE id=?", (tenant_id,))
            building_row = c.fetchone()

            if not building_row:
                messagebox.showerror("Error", "Building not found for this tenant.")
                conn.close()
                return

            building_name = building_row[0]

            if editing_payment_id is None:
                c.execute("SELECT id FROM payments WHERE tenant_id=? AND month_year=?", 
                        (tenant_id, month_year))
                if c.fetchone():
                    messagebox.showwarning("Duplicate", "Payment for this month already exists!")
                    conn.close()
                    return

            rent = float(rent_var.get() or 0)
            gas = float(gas_var.get() or 0)
            water = float(water_var.get() or 0)
            electricity = float(electricity_var.get() or 0)
            other = float(other_var.get() or 0)
            paid = float(paid_var.get() or 0)
            total = rent + gas + water + electricity + other
            balance = total - paid

            # ================= CHECK ALL OPEN COLLECTIONS =================
            c.execute("""
                SELECT id, remaining_amount
                FROM building_collections
                WHERE building_name=? AND status='Open'
                ORDER BY id ASC
            """, (building_name,))

            collections = c.fetchall()

            if not collections:
                messagebox.showerror("Error", "No open building collection found.")
                conn.close()
                return

            # Calculate total available amount across ALL collections
            total_available = sum([col[1] for col in collections])
            
            # Check if paid amount exceeds total available
            if paid > total_available:
                messagebox.showerror("Error", 
                    f"Payment of Rs. {paid:,.2f} exceeds total available amount (Rs. {total_available:,.2f}) across all collections.")
                conn.close()
                return

            # Determine payment status
            if balance == 0:
                status = "Paid"
            elif paid == 0:
                status = "Pending"
            else:
                status = "Partial"

            # ===== DISTRIBUTE PAYMENT ACROSS COLLECTIONS =====
            remaining_to_pay = paid
            collection_ids_used = []
            
            for collection in collections:
                if remaining_to_pay <= 0:
                    break
                    
                collection_id = collection[0]
                collection_remaining = collection[1]
                
                if collection_remaining >= remaining_to_pay:
                    new_remaining = collection_remaining - remaining_to_pay
                    c.execute("""
                        UPDATE building_collections
                        SET remaining_amount=?
                        WHERE id=?
                    """, (new_remaining, collection_id))
                    
                    collection_ids_used.append(collection_id)
                    remaining_to_pay = 0
                    
                else:
                    # Use all of this collection
                    c.execute("""
                        UPDATE building_collections
                        SET remaining_amount=0
                        WHERE id=?
                    """, (collection_id,))
                    
                    collection_ids_used.append(collection_id)
                    remaining_to_pay -= collection_remaining

            # Use first collection ID for reference
            main_collection_id = collections[0][0] if collections else None

            if editing_payment_id is None:
                c.execute('''INSERT INTO payments 
                    (tenant_id, month_year, rent_amount, gas_bill, water_bill, electricity_bill, 
                    total_amount, paid_amount, balance_amount, payment_date, status, collection_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (tenant_id, month_year, rent, gas, water, electricity, 
                    total, paid, balance, payment_date_var.get(), status, main_collection_id))

            else:
                c.execute('''UPDATE payments SET
                    tenant_id=?, month_year=?, rent_amount=?, gas_bill=?, water_bill=?,
                    electricity_bill=?, total_amount=?, paid_amount=?, balance_amount=?,
                    payment_date=?, status=?
                    WHERE id=?''',
                    (tenant_id, month_year, rent, gas, water, electricity,
                    total, paid, balance, payment_date_var.get(), status,
                    editing_payment_id))

                editing_payment_id = None

            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Payment recorded successfully!")
            clear_form()
            load_paid_payments()
            load_pending_payments()
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in amount fields")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save payment: {str(e)}")

    
    def clear_form():
        # Clear the payment form
        global editing_payment_id
        editing_payment_id = None

        tenant_var.set("-- Select Tenant --")
        building_var.set("")
        collector_var.set("Not Assigned")
        rent_var.set("")
        gas_var.set("0")
        water_var.set("0")
        electricity_var.set("0")
        other_var.set("0")
        paid_var.set("")
        total_var.set("0.00")
        balance_var.set("0.00")
        save_btn.config(text="Save Payment", bg="#1e3a8a")

        payment_date_var.set(datetime.now().strftime("%d-%m-%Y"))
        month_combo.set(datetime.now().strftime("%B"))
        year_combo.set(str(current_year))

    def edit_payment():
        global editing_payment_id

        selected = tree_top.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select a payment to edit")
            return

        values = tree_top.item(selected[0])['values']
        tenant_name = values[1]
        month_year = values[4]

        conn = get_connection()
        c = conn.cursor()

        c.execute("""
            SELECT p.*, t.name 
            FROM payments p
            JOIN tenants t ON p.tenant_id = t.id
            WHERE t.name=? AND p.month_year=?
        """, (tenant_name, month_year))

        record = c.fetchone()
        conn.close()

        if not record:
            messagebox.showerror("Error", "Record not found")
            return

        editing_payment_id = record[0]

        # split month year
        month, year = record[2].split("-")

        # Get tenant ID
        tenant_id = record[1]

        # Find the correct display text
        for display_text, tid in tenant_combo.tenant_data.items():
            if tid == tenant_id:
                tenant_var.set(display_text)
                load_tenant_details()
                break

        month_var.set(month)
        year_var.set(year)
        rent_var.set(record[3])
        gas_var.set(record[4])
        water_var.set(record[5])
        electricity_var.set(record[6])
        paid_var.set(record[8])
        payment_date_var.set(record[10])

        calculate_totals()

        save_btn.config(text="Update Payment", bg="#2563eb")
        
        messagebox.showinfo("Edit Mode", "You can now update this payment and click Save.")
        
    # Delete Payment
    def delete_payment():
        selected = tree_top.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a payment to delete")
            return
        
        values = tree_top.item(selected[0])['values']
        if len(values) < 5:
            return
            
        tenant_name = values[1] 
        month_year = values[4]
        
        if messagebox.askyesno("Confirm Delete", 
                            f"Delete payment record for {tenant_name} ({month_year})?"):
            
            conn = get_connection()
            c = conn.cursor()
            
            # Find payment ID and collection info
            c.execute("""
                SELECT p.id, p.paid_amount, p.collection_id, t.building_name 
                FROM payments p
                JOIN tenants t ON p.tenant_id = t.id
                WHERE t.name=? AND p.month_year=?
            """, (tenant_name, month_year))
            
            result = c.fetchone()
            if result:
                payment_id = result[0]
                paid_amount = float(result[1])
                collection_id = result[2]
                building_name = result[3]

                # Add the amount back to the collection
                c.execute("""
                    UPDATE building_collections
                    SET remaining_amount = remaining_amount + ?
                    WHERE id = ?
                """, (paid_amount, collection_id))

                # Delete payment
                c.execute("DELETE FROM payments WHERE id=?", (payment_id,))
                conn.commit()
                messagebox.showinfo("Success", "Payment deleted successfully and amount restored to building collection!")
                
                # Refresh both tables
                load_paid_payments()
                load_pending_payments()
            else:
                messagebox.showerror("Error", "Payment not found!")
            
            conn.close()


    def load_paid_payments():
        # Load paid/partial payments
        for item in tree_top.get_children():
            tree_top.delete(item)
        
        conn = get_connection()
        c = conn.cursor()
        
        query = """SELECT 
                    t.name as tenant_name,
                    t.building_name,
                    COALESCE(rc.rent_collector_name, 'Not Assigned') as collector_name,
                    p.month_year,
                    p.rent_amount,
                    p.gas_bill,
                    p.water_bill,
                    p.electricity_bill,
                    p.total_amount,
                    p.paid_amount,
                    p.balance_amount,
                    p.status
                FROM payments p
                JOIN tenants t ON p.tenant_id = t.id
                LEFT JOIN rent_collectors rc ON t.building_name = rc.building_name
                WHERE p.status IN ('Paid', 'Partial')"""
        params = []
        
        search_text = search_var_top.get().strip()
        if search_text:
            query += " AND (t.name LIKE ? OR t.building_name LIKE ? OR p.month_year LIKE ?)"
            search_pattern = f"%{search_text}%"
            params.extend([search_pattern, search_pattern, search_pattern])
        
        if search_month_var_top.get() != "All":
            query += " AND p.month_year LIKE ?"
            params.append(f"%{search_month_var_top.get()}%")
        
        if search_status_var_top.get() != "All":
            query += " AND p.status = ?"
            params.append(search_status_var_top.get())
        
        query += " ORDER BY p.month_year DESC, t.name"
        
        c.execute(query, params)
        payments = c.fetchall()
        conn.close()
        
        for idx, payment in enumerate(payments, start=1):
            formatted_values = [
                idx,
                payment[0], payment[1], payment[2], payment[3],
                f"{payment[4]:,.2f}" if payment[4] else "0.00",
                f"{payment[5]:,.2f}" if payment[5] else "0.00",
                f"{payment[6]:,.2f}" if payment[6] else "0.00",
                f"{payment[7]:,.2f}" if payment[7] else "0.00",
                f"{payment[8]:,.2f}" if payment[8] else "0.00",
                f"{payment[9]:,.2f}" if payment[9] else "0.00",
                f"{payment[10]:,.2f}" if payment[10] else "0.00",
                payment[11]
            ]
            tree_top.insert("", "end", values=formatted_values)

    def load_pending_payments():
        # Clear table
        for item in tree_bottom.get_children():
            tree_bottom.delete(item)
        
        conn = get_connection()
        c = conn.cursor()
        
        current_month = datetime.now().strftime("%B")
        current_year = str(datetime.now().year)
        current_month_year = f"{current_month}-{current_year}"
        
        # GET SEARCH FILTERS
        selected_month = search_month_var_bottom.get().strip()
        selected_year = search_year_var_bottom.get().strip()
        
        # Create search month-year
        if selected_month and selected_year:
            search_month_year = f"{selected_month}-{selected_year}"
        else:
            search_month_year = None
        
        # Get current date for comparison
        current_date = datetime.now()
        
        # Get ALL active tenants
        c.execute("""
            SELECT id, name, building_name, flat_no, phone, rent_amount
            FROM tenants 
            WHERE status='Active'
            ORDER BY building_name, flat_no
        """)
        all_tenants = c.fetchall()
        
        # Get ALL payments
        c.execute("""
            SELECT tenant_id, month_year, status, paid_amount, total_amount
            FROM payments
            ORDER BY tenant_id, month_year
        """)
        all_payments = c.fetchall()
        conn.close()
        
        # Organize payments by tenant
        payments_by_tenant = {}
        for payment in all_payments:
            tenant_id = payment[0]
            month_year = payment[1]
            
            # Future month check
            try:
                month, year = month_year.split('-')
                payment_date = datetime.strptime(f"01-{month}-{year}", "%d-%B-%Y")
                
                # Ignore Future month pending
                if payment_date > current_date:
                    continue 
            except:
                continue
            
            if tenant_id not in payments_by_tenant:
                payments_by_tenant[tenant_id] = []
            payments_by_tenant[tenant_id].append({
                'month_year': month_year,
                'status': payment[2],
                'paid': payment[3],
                'total': payment[4]
            })
        
        pending_count = 0
        pending_amount = 0
        row_num = 0
        
        # Track tenants already shown
        tenants_shown = set()
        
        # FILTER APPLY FUNCTION
        def should_show_month(month_year):
            if not search_month_year:
                return True 
            
            # Exact match
            return month_year == search_month_year
        
        # FIRST: Current month pending check
        if should_show_month(current_month_year):
            for tenant in all_tenants:
                tenant_id, name, building, flat, phone, rent = tenant
                tenant_payments = payments_by_tenant.get(tenant_id, [])
                
                # Check if current month payment exists
                current_month_found = False
                
                for payment in tenant_payments:
                    if payment['month_year'] == current_month_year:
                        current_month_found = True
                        # SIRF PURE PENDING (paid = 0) dikhao, partial nahi
                        if payment['status'] == 'Pending' and payment['paid'] == 0:
                            # Current month pure pending
                            pending_count += 1
                            pending_amount += rent
                            tenants_shown.add(tenant_id)
                            
                            row_num += 1
                            tree_bottom.insert("", "end", values=(
                                row_num, name, building, flat, phone,
                                f"{rent:,.2f}" if rent else "0.00",
                                f"Pending - {current_month_year}"
                            ), tags=('current_pending',))
                        # PARTIAL PAYMENTS KO YAHAN NAHI DIKHAOGE
                        break
                
                # No payment record for current month = PENDING
                if not current_month_found:
                    pending_count += 1
                    pending_amount += rent
                    tenants_shown.add(tenant_id)
                    
                    row_num += 1
                    tree_bottom.insert("", "end", values=(
                        row_num, name, building, flat, phone,
                        f"{rent:,.2f}" if rent else "0.00",
                        f"No Payment - {current_month_year}"
                    ), tags=('no_payment',))
        
        # SECOND: Past pending months (only pure pending)
        for tenant in all_tenants:
            tenant_id, name, building, flat, phone, rent = tenant
            tenant_payments = payments_by_tenant.get(tenant_id, [])
            
            for payment in tenant_payments:
                month_year = payment['month_year']
                
                # Skip if doesn't match search filter
                if not should_show_month(month_year):
                    continue
                
                # Skip current month
                if month_year == current_month_year:
                    continue
                
                # Double-check future months
                try:
                    month, year = month_year.split('-')
                    payment_date = datetime.strptime(f"01-{month}-{year}", "%d-%B-%Y")
                    
                    # Skip Future month
                    if payment_date > current_date:
                        continue
                except:
                    continue
                
                # SIRF PURE PENDING (paid = 0) dikhao, partial nahi
                if payment['status'] == 'Pending' and payment['paid'] == 0:
                    row_num += 1
                    tree_bottom.insert("", "end", values=(
                        row_num, name, building, flat, phone,
                        f"{rent:,.2f}" if rent else "0.00",
                        f"📅 Pending - {month_year}"
                    ), tags=('past_pending',))
        
        # Update summary
        if should_show_month(current_month_year):
            pending_count_var.set(f"Current Month ({current_month_year}) Pending: {pending_count}")
            pending_amount_var.set(f"Amount: Rs. {pending_amount:,.2f}")
        else:
            
            pending_count_var.set(f"Search Results for {search_month_year}: {row_num} records")
            pending_amount_var.set(f"Amount: Rs. 0")
        
        # Configure tags
        tree_bottom.tag_configure('current_pending', background="#f2e9e9")
        tree_bottom.tag_configure('no_payment', background="#fdc8c8")
        tree_bottom.tag_configure('past_pending', background="#fbeec1")
        
        if row_num == 0:
            if search_month_year:
                tree_bottom.insert("", "end", values=(
                    1, f"No pending for {search_month_year}", "-", "-", "-", "-", "-"
                ))
            else:
                tree_bottom.insert("", "end", values=(
                    1, "All payments up to date!", "-", "-", "-", "-", "No Pending"
                ))
                

    def on_pending_double_click(event):
        # Add payment for selected pending tenant
        selected = tree_bottom.selection()
        if not selected:
            return
        
        values = tree_bottom.item(selected[0])['values']
        if len(values) < 2 or "No pending" in str(values[1]):
            return
        
        tenant_name = values[1]
        
        # Find and select the tenant in dropdown
        for item in tenant_combo['values']:
            if tenant_name in item:
                tenant_var.set(item)
                load_tenant_details()
                
                # Auto-set month and year
                month_var.set(search_month_var_bottom.get())
                year_var.set(search_year_var_bottom.get())
                
                messagebox.showinfo("Info", f"Selected {tenant_name} for {month_var.get()}-{year_var.get()}. Please enter payment details.")
                break

    # ========== BUTTONS ==========
    # Buttons for form
    save_btn = tk.Button(button_frame, text="Save Payment", command=save_payment,
              bg="#1e3a8a", fg="white", font=("Segoe UI", 11, "bold"),
              width=14, height=1, relief="raised", bd=2, cursor="hand2")
    save_btn.pack(side="left", padx=5)

    def check_form_validity(*args):
        if tenant_var.get() != "-- Select Tenant --" and paid_var.get().strip():
            save_btn.config(state="normal")
        else:
            save_btn.config(state="disabled")

    tenant_var.trace('w', check_form_validity)
    paid_var.trace('w', check_form_validity)

    tk.Button(button_frame, text="Clear Form", command=clear_form,
              bg="#fb822c", fg="white", font=("Segoe UI", 11, "bold"),
              width=14, height=1, relief="raised", bd=2, cursor="hand2").pack(side="left", padx=5)

    # Buttons for top table
    button_frame_top = tk.Frame(search_frame_top, bg="#f8fafc")
    button_frame_top.grid(row=0, column=6, columnspan=2, padx=(20,0))

    tk.Button(button_frame_top, text="Refresh", 
              command=load_paid_payments,
              bg="#147b58", fg="white", font=("Segoe UI", 10, "bold"),
              width=8, cursor="hand2").pack(side="left", padx=2)
    
    tk.Button(button_frame_top, text="Edit",command=edit_payment,
                bg="#2563eb", fg="white", font=("Segoe UI", 10, "bold"),
                width=8, cursor="hand2").pack(side="left", padx=2)
    
    tk.Button(button_frame_top, text="Delete", command=delete_payment,
                bg="#ff0404", fg="white", font=("Segoe UI", 10, "bold"),
                width=8, cursor="hand2").pack(side="left", padx=2)

    # Buttons for bottom section
    tk.Button(search_frame_bottom, text="🔍 Check Pending", 
              command=load_pending_payments,
              bg="#1e3a8a", fg="white", font=("Segoe UI", 9, "bold"), cursor="hand2").grid(row=0, column=4, padx=10)


    # ========== BIND EVENTS ==========
    rent_var.trace('w', calculate_totals)
    gas_var.trace('w', calculate_totals)
    water_var.trace('w', calculate_totals)
    electricity_var.trace('w', calculate_totals)
    other_var.trace('w', calculate_totals)
    paid_var.trace('w', calculate_totals)
    
    tenant_combo.bind('<<ComboboxSelected>>', load_tenant_details)
    
    # Top table search events
    search_entry_top.bind('<KeyRelease>', lambda e: load_paid_payments())
    search_month_combo_top.bind('<<ComboboxSelected>>', lambda e: load_paid_payments())
    search_status_combo_top.bind('<<ComboboxSelected>>', lambda e: load_paid_payments())
    
    # Bottom table search events
    search_month_combo_bottom.bind('<<ComboboxSelected>>', lambda e: load_pending_payments())
    search_year_combo_bottom.bind('<<ComboboxSelected>>', lambda e: load_pending_payments())
    
    # Double click event
    tree_bottom.bind('<Double-1>', on_pending_double_click)
    
    # ========== INITIAL LOAD ==========
    load_tenants()
    load_paid_payments()
    load_pending_payments()
    clear_form()
    return window

