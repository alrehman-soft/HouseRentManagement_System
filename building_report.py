import tkinter as tk
from tkinter import ttk, messagebox
from create_database import get_connection
from datetime import datetime
from tkinter import filedialog
from openpyxl import Workbook
import print_utils

def open_building_report(parent):
    # Building Report Tab
    
    # Clear parent frame
    for widget in parent.winfo_children():
        widget.destroy()
    
    # Main container
    main_frame = tk.Frame(parent, bg="#f8fafc")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ========== HURAIRA ENTERPRISES TITLE ==========
    title_frame = tk.Frame(main_frame, bg="#1e3a8a", height=70)
    title_frame.pack(fill="x", pady=(0, 10))
    title_frame.pack_propagate(False)
    
    tk.Label(title_frame, 
             text="ABU HURAIRA ENTERPRISES \nBuilding Report", 
             font=("Segoe UI", 18, "bold"), 
             bg="#1e3a8a", fg="white").pack(expand=True)

    # ========== CONTROL FRAME ==========
    control_frame = tk.LabelFrame(main_frame, text="Report Controls", 
                                  font=("Segoe UI", 11, "bold"),
                                  bg="#f8fafc", padx=10, pady=10)
    control_frame.pack(fill="x", pady=(0, 10))

    # Year Selection
    tk.Label(control_frame, text="Select Year:", bg="#f8fafc", 
             font=("Segoe UI", 10)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    
    year_var = tk.StringVar()
    current_year = datetime.now().year
    years = [str(i) for i in range(current_year-2, current_year+2)]
    year_combo = ttk.Combobox(control_frame, textvariable=year_var, 
                              values=years, state="readonly", width=12)
    year_combo.grid(row=0, column=1, padx=5, pady=5)
    year_combo.set(str(current_year))

    # Report Type
    tk.Label(control_frame, text="Report Type:", bg="#f8fafc", 
             font=("Segoe UI", 10)).grid(row=0, column=2, padx=20, pady=5, sticky="w")
    
    report_type_var = tk.StringVar(value="Building Summary")
    report_type_combo = ttk.Combobox(control_frame, textvariable=report_type_var, 
                                     values=["Building Summary", "Monthly Comparison", "Tenant Distribution"],
                                     state="readonly", width=18)
    report_type_combo.grid(row=0, column=3, padx=5, pady=5)

    # Generate Button
    tk.Button(control_frame, text="📊 Generate Report", 
              command=lambda: generate_building_report(tree, year_var.get(), report_type_var.get()),
              bg="#1e3a8a", fg="white", font=("Segoe UI", 10, "bold"),
              width=15).grid(row=0, column=4, padx=20, pady=5)

    # Print Button
    tk.Button(control_frame, text="🖨️ Print", 
              command=lambda: print_utils.send_to_printer(tree, 
                  title=f"Huraira Enterprises - Building Report: {report_type_var.get()} {year_var.get()}", 
                  orientation="landscape"),
              bg="#f59e0b", fg="white", font=("Segoe UI", 10, "bold"),
              width=12).grid(row=0, column=5, padx=5, pady=5)

    # Export Button
    tk.Button(control_frame, text="📥 Export", 
              command=lambda: export_report(tree, f"Building_Report_{year_var.get()}"),
              bg="#10b981", fg="white", font=("Segoe UI", 10, "bold"),
              width=12).grid(row=0, column=6, padx=5, pady=5)

    # ========== REPORT DISPLAY FRAME ==========
    report_frame = tk.LabelFrame(main_frame, text="Building Report", 
                                 font=("Segoe UI", 11, "bold"),
                                 bg="#f8fafc", padx=10, pady=10)
    report_frame.pack(fill="both", expand=True)

    # ========== TABLE FRAME ==========
    table_frame = tk.Frame(report_frame, bg="#f8fafc")
    table_frame.pack(fill="both", expand=True)

    columns = ("Building","Tenants","Collected","Pending","Rate")

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150)

    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    scrollbar.pack(side="right", fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

def generate_building_report(tree, year, report_type):
    """Generate building report based on type"""
    # Clear old data
    for row in tree.get_children():
        tree.delete(row)

    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT DISTINCT building_name FROM tenants WHERE building_name != '' ORDER BY building_name")
    buildings = [row[0] for row in c.fetchall()]

    if not buildings:
        messagebox.showwarning("Warning", "No buildings found")
        conn.close()
        return

    months = ["January","February","March","April","May","June",
              "July","August","September","October","November","December"]

    if report_type == "Building Summary":
        show_building_summary(tree, c, buildings, months, year)
    elif report_type == "Monthly Comparison":
        show_monthly_comparison(tree, c, buildings, months, year)
    else:
        show_tenant_distribution(tree, c, buildings)

    conn.close()

def show_building_summary(tree, c, buildings, months, year):
    """Show building summary"""
    tree["columns"] = ("Building","Tenants","Collected","Pending","Rate")
    tree["show"] = "headings"

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    for building in buildings:
        c.execute("SELECT COUNT(*) FROM tenants WHERE building_name=? AND status='Active'", (building,))
        tenant_count = c.fetchone()[0] or 0

        total_collected = 0
        total_pending = 0

        for month in months:
            month_year = f"{month}-{year}"
            c.execute("""
                SELECT SUM(p.paid_amount), SUM(p.balance_amount)
                FROM payments p
                JOIN tenants t ON p.tenant_id=t.id
                WHERE t.building_name=? AND p.month_year=?
            """,(building, month_year))
            paid, balance = c.fetchone()
            total_collected += paid or 0
            total_pending += balance or 0

        rate = (total_collected / (total_collected + total_pending) * 100) if (total_collected + total_pending) > 0 else 0

        tree.insert("", "end", values=(
            building,
            tenant_count,
            f"Rs {total_collected:,.0f}",
            f"Rs {total_pending:,.0f}",
            f"{rate:.1f}%"
        ))

def show_monthly_comparison(tree, c, buildings, months, year):
    """Show monthly comparison"""
    tree["columns"] = ["Month"] + buildings
    tree["show"] = "headings"

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    for month in months:
        row = [month]
        month_year = f"{month}-{year}"

        for building in buildings:
            c.execute("""SELECT SUM(paid_amount)
                         FROM payments p
                         JOIN tenants t ON p.tenant_id=t.id
                         WHERE t.building_name=? AND p.month_year=?""",
                      (building, month_year))
            collected = c.fetchone()[0] or 0
            row.append(f"Rs {collected:,.0f}")

        tree.insert("", "end", values=row)

def show_tenant_distribution(tree, c, buildings):
    """Show tenant distribution"""
    tree["columns"] = ("Building","Total","Active","Vacated","Occupancy")
    tree["show"] = "headings"

    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor="center")

    for building in buildings:
        c.execute("SELECT COUNT(*) FROM tenants WHERE building_name=?", (building,))
        total = c.fetchone()[0]

        c.execute("SELECT COUNT(*) FROM tenants WHERE building_name=? AND status='Active'", (building,))
        active = c.fetchone()[0]

        vacated = total - active
        occ = (active / total * 100) if total > 0 else 0

        tree.insert("", "end", values=(
            building,
            total,
            active,
            vacated,
            f"{occ:.1f}%"
        ))

def export_report(tree, filename):
    """Export report to Excel"""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel file", "*.xlsx")],
        initialfile=f"{filename}.xlsx"
    )

    if not file_path:
        return

    wb = Workbook()
    ws = wb.active
    ws.title = "Report"

    # headers
    headers = tree["columns"]
    ws.append(headers)

    # rows
    for row in tree.get_children():
        ws.append(tree.item(row)["values"])

    # auto column width
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        ws.column_dimensions[col_letter].width = max_length + 2

    wb.save(file_path)
    messagebox.showinfo("Success", "Report exported to Excel successfully!")