import tkinter as tk
from tkinter import ttk
import monthly_report
import annual_report
import tenant_report
import building_report
from datetime import datetime

def open_reports_dashboard():
    window = tk.Toplevel()
    window.title("Reports Dashboard")
    window.geometry("1000x700")
    window.config(bg="#f8fafc")

    # Main container
    main_frame = tk.Frame(window, bg="#f8fafc")
    main_frame.pack(fill="both", expand=True)

    header_frame = tk.Frame(main_frame, bg="#1e3a8a", height=120)
    header_frame.pack(fill="x", pady=(0, 20))
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="Abu Huraira Enterprises \nTenant All Reports List", 
             font=("Segoe UI", 20, "bold"), bg="#1e3a8a", fg="white").pack(pady=20)
    
    # Notebook container - this will take remaining space
    notebook_container = tk.Frame(main_frame, bg="#f8fafc")
    notebook_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    # Main tabs
    notebook = ttk.Notebook(notebook_container)
    notebook.pack(fill="both", expand=True, padx=10, pady=10)

    # Create tabs
    monthly_tab = ttk.Frame(notebook)
    annual_tab = ttk.Frame(notebook)
    tenant_tab = ttk.Frame(notebook)
    building_tab = ttk.Frame(notebook)

    notebook.add(monthly_tab, text="📅 Monthly Report")
    notebook.add(annual_tab, text="📆 Annual Report")
    notebook.add(tenant_tab, text="👤 Tenant Report")
    notebook.add(building_tab, text="🏢 Building Report")

    # Call functions to populate tabs
    monthly_report.open_monthly_report(monthly_tab)
    annual_report.open_annual_report(annual_tab)
    tenant_report.open_tenant_report(tenant_tab)
    building_report.open_building_report(building_tab)