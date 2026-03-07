import tkinter as tk
from tkinter import ttk
from create_database import get_connection
from datetime import datetime
import print_utils
import export_utils

def open_monthly_report(parent):
    """Monthly Report Tab"""
    
    # Clear parent frame
    for widget in parent.winfo_children():
        widget.destroy()
    
    # Main container
    main_frame = tk.Frame(parent, bg="#f8fafc")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # ========== CONTROL FRAME ==========
    control_frame = tk.LabelFrame(main_frame, text="Report Controls", 
                                  font=("Segoe UI", 11, "bold"),
                                  bg="#f8fafc", padx=10, pady=10)
    control_frame.pack(fill="x", pady=(0, 10))
    
    # Get building names
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT DISTINCT building_name FROM tenants WHERE building_name IS NOT NULL AND building_name != '' ORDER BY building_name")
    buildings = [row[0] for row in c.fetchall()]
    conn.close()
    
    # Building Selection
    tk.Label(control_frame, text="Building:", bg="#f8fafc", 
             font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    building_list = ["All Buildings"] + buildings
    building_var = tk.StringVar()
    building_combo = ttk.Combobox(control_frame, textvariable=building_var,
                                   values=building_list, state="readonly", width=20)
    building_combo.grid(row=0, column=1, padx=5, pady=5)
    if building_list:
        building_combo.current(0)
    
    # Month Selection
    tk.Label(control_frame, text="Month:", bg="#f8fafc", 
             font=("Segoe UI", 10)).grid(row=0, column=2, padx=20, pady=5, sticky="w")
    
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    month_var = tk.StringVar(value=datetime.now().strftime("%B"))
    month_combo = ttk.Combobox(control_frame, textvariable=month_var,
                                values=months, state="readonly", width=12)
    month_combo.grid(row=0, column=3, padx=5, pady=5)
    
    # Year Selection
    tk.Label(control_frame, text="Year:", bg="#f8fafc", 
             font=("Segoe UI", 10)).grid(row=0, column=4, padx=20, pady=5, sticky="w")
    
    current_year = datetime.now().year
    years = [str(i) for i in range(current_year, current_year+100)]
    year_var = tk.StringVar(value=str(current_year))
    year_combo = ttk.Combobox(control_frame, textvariable=year_var,
                               values=years, state="readonly", width=8)
    year_combo.grid(row=0, column=5, padx=5, pady=5)
    
    # Action Buttons
    tk.Button(control_frame, text="📊 Generate", 
              command=lambda: load_monthly_data(tree, building_var.get(), 
                                               month_var.get(), year_var.get()),
              bg="#1e3a8a", fg="white", font=("Segoe UI", 10, "bold"),
              width=12).grid(row=0, column=6, padx=10, pady=5)
    
    tk.Button(control_frame, text="🖨️ Print", 
              command=lambda: print_utils.send_to_printer(tree),
              bg="#f59e0b", fg="white", font=("Segoe UI", 10, "bold"),
              width=12).grid(row=0, column=7, padx=5, pady=5)
    
    tk.Button(control_frame, text="📥 Export", 
              command=lambda: export_utils.export_to_excel(tree, f"Monthly_Report_{month_var.get()}_{year_var.get()}"),
              bg="#10b981", fg="white", font=("Segoe UI", 10, "bold"),
              width=12).grid(row=0, column=8, padx=5, pady=5)
    
    # ========== REPORT DISPLAY FRAME ==========
    report_frame = tk.LabelFrame(main_frame, text="Monthly Report", 
                                 font=("Segoe UI", 11, "bold"),
                                 bg="#f8fafc", padx=10, pady=10)
    report_frame.pack(fill="both", expand=True)
    
    # ===== TABLE FRAME =====
    table_frame = tk.Frame(report_frame, bg="#f8fafc")
    table_frame.pack(fill="both", expand=True)

    columns = ("Flat", "Tenant", "Building", "Rent", "Paid", "Balance", "Status")

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

    # Headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.column("Tenant", width=220, anchor="w")
    tree.column("Building", width=150)
    tree.column("Flat", width=80)
    tree.column("Rent", width=120)
    tree.column("Paid", width=120)
    tree.column("Balance", width=120)
    tree.column("Status", width=100)

    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    style = ttk.Style(parent)
    style.configure("Treeview.Heading", font=("Segoe UI",10,"bold"), padding=5)
    style.configure("Treeview", font=("Segoe UI",10), rowheight=25)

    # Status color tags
    tree.tag_configure("paid", foreground="black")
    tree.tag_configure("pending", foreground="black")

    # alternating row colors
    tree.tag_configure("even", background="#f1f5f9")
    tree.tag_configure("odd", background="white")

    tree.tag_configure("total",
    background="#dbeafe",
    font=("Segoe UI",10,"bold"))


def load_monthly_data(tree, building, month, year):
    # clear old rows
    for row in tree.get_children():
        tree.delete(row)

    conn = get_connection()
    c = conn.cursor()

    if building == "All Buildings":
        query = '''
        SELECT t.name, t.building_name, t.flat_no, t.rent_amount,
               COALESCE(p.paid_amount,0),
               COALESCE(p.balance_amount,t.rent_amount),
               COALESCE(p.status,'Pending')
        FROM tenants t
        LEFT JOIN payments p
        ON t.id = p.tenant_id AND p.month_year=?
        WHERE t.status='Active'
        ORDER BY t.building_name, t.flat_no
        '''
        params=(f"{month}-{year}",)

    else:
        query = '''
        SELECT t.name, t.building_name, t.flat_no, t.rent_amount,
               COALESCE(p.paid_amount,0),
               COALESCE(p.balance_amount,t.rent_amount),
               COALESCE(p.status,'Pending')
        FROM tenants t
        LEFT JOIN payments p
        ON t.id = p.tenant_id AND p.month_year=?
        WHERE t.status='Active' AND t.building_name=?
        ORDER BY t.flat_no
        '''
        params=(f"{month}-{year}",building)

    c.execute(query,params)
    rows=c.fetchall()

    total_expected=0
    total_paid=0
    total_balance=0

    for name,bld,flat,rent,paid,balance,status in rows:

        row_tag = "even" if len(tree.get_children())%2==0 else "odd"
        status_tag = "paid" if status=="Paid" else "pending"

        tree.insert("", "end",
            values=(flat,name,bld,
                    f"Rs {rent:,.0f}",
                    f"Rs {paid:,.0f}",
                    f"Rs {balance:,.0f}",
                    status),
            tags=(row_tag,status_tag))

        total_expected+=rent
        total_paid+=paid
        total_balance+=balance

    conn.close()

    # Insert total row
    tree.insert("", "end",
        values=("",
                "TOTAL",
                "",
                f"Rs {total_expected:,.0f}",
                f"Rs {total_paid:,.0f}",
                f"Rs {total_balance:,.0f}",
                ""),
        tags=("total",))
