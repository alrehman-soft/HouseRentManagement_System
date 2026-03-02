import tkinter as tk
from tkinter import ttk, messagebox
from create_database import get_connection
from datetime import datetime
import print_utils

def open_tenant_report(parent):
    """Tenant Wise Report Tab (Treeview Version)"""
    
    for widget in parent.winfo_children():
        widget.destroy()
    
    main_frame = tk.Frame(parent, bg="#f8fafc")
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # ========== HURAIRA ENTERPRISES TITLE ==========
    title_frame = tk.Frame(main_frame, bg="#1e3a8a", height=70)
    title_frame.pack(fill="x", pady=(0, 10))
    title_frame.pack_propagate(False)
    
    tk.Label(title_frame, 
             text="ABU HURAIRA ENTERPRISES \nTenant Report", 
             font=("Segoe UI", 18, "bold"), 
             bg="#1e3a8a", fg="white").pack(expand=True)

    # ========= CONTROL FRAME =========
    control_frame = tk.LabelFrame(main_frame, text="Select Tenant",
                                  font=("Segoe UI",11,"bold"),
                                  bg="#f8fafc", padx=10, pady=10)
    control_frame.pack(fill="x", pady=(0,10))

    tk.Label(control_frame,text="Tenant:",bg="#f8fafc",
             font=("Segoe UI",10)).grid(row=0,column=0,padx=5,pady=5,sticky="w")

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id,name,building_name,flat_no FROM tenants ORDER BY name")
    tenants = c.fetchall()
    conn.close()

    tenant_dict={}
    tenant_names=[]

    for tid,name,bld,flat in tenants:
        label=f"{name} - {bld} (Flat {flat})"
        tenant_dict[label]=tid
        tenant_names.append(label)

    tenant_var=tk.StringVar()
    tenant_combo=ttk.Combobox(control_frame,textvariable=tenant_var,
                              values=tenant_names,state="readonly",width=40)
    tenant_combo.grid(row=0,column=1,padx=5,pady=5)

    if tenant_names:
        tenant_combo.current(0)

    # buttons
    tk.Button(control_frame,text="📊 Generate",
              command=lambda:generate_tenant_report(tree,tenant_var.get(),tenant_dict),
              bg="#1e3a8a",fg="white",font=("Segoe UI",10,"bold"),
              width=15).grid(row=0,column=2,padx=15)

    tk.Button(control_frame,text="🖨 Print",
              command=lambda: print_utils.send_to_printer(tree, title=f"Huraira Enterprises - Tenant Report: {tenant_var.get()}"),
              bg="#f59e0b",fg="white",font=("Segoe UI",10,"bold"),
              width=10).grid(row=0,column=3,padx=5)

    # ========= TABLE =========
    report_frame=tk.LabelFrame(main_frame,text="Tenant Report",
                               font=("Segoe UI",11,"bold"),
                               bg="#f8fafc",padx=10,pady=10)
    report_frame.pack(fill="both",expand=True)

    table_frame=tk.Frame(report_frame,bg="#f8fafc")
    table_frame.pack(fill="both",expand=True)

    columns=("Month","Rent","Paid","Balance","Date","Status")

    tree=ttk.Treeview(table_frame,columns=columns,show="headings",height=18)

    for col in columns:
        tree.heading(col,text=col)
        tree.column(col,anchor="center",width=120)

    tree.column("Month",width=140,anchor="w")

    tree.pack(side="left",fill="both",expand=True)

    scrollbar=ttk.Scrollbar(table_frame,orient="vertical",command=tree.yview)
    scrollbar.pack(side="right",fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    # styles
    style=ttk.Style(parent)
    style.configure("Treeview.Heading",font=("Segoe UI",10,"bold"))
    style.configure("Treeview",font=("Segoe UI",10),rowheight=25)

    tree.tag_configure("paid",foreground="green")
    tree.tag_configure("pending",foreground="red")
    tree.tag_configure("total",background="#dbeafe",font=("Segoe UI",10,"bold"))

def generate_tenant_report(tree, selected_tenant, tenant_dict):
    """Generate tenant report"""
    for row in tree.get_children():
        tree.delete(row)

    if selected_tenant not in tenant_dict:
        messagebox.showerror("Error","Select tenant first")
        return

    tenant_id=tenant_dict[selected_tenant]

    conn=get_connection()
    c=conn.cursor()

    c.execute("""
        SELECT month_year,rent_amount,paid_amount,balance_amount,
               payment_date,status
        FROM payments
        WHERE tenant_id=?
        ORDER BY month_year DESC
    """,(tenant_id,))
    rows=c.fetchall()
    conn.close()

    total_rent=0
    total_paid=0
    total_bal=0

    for r in rows:
        month,rent,paid,bal,date,status=r

        tag="paid" if status=="Paid" else "pending"

        tree.insert("", "end",
            values=(month,
                    f"Rs {rent:,.0f}",
                    f"Rs {paid:,.0f}",
                    f"Rs {bal:,.0f}",
                    date or "N/A",
                    status),
            tags=(tag,))

        total_rent+=rent
        total_paid+=paid
        total_bal+=bal

    # total row
    tree.insert("","end",
        values=("TOTAL",
                f"Rs {total_rent:,.0f}",
                f"Rs {total_paid:,.0f}",
                f"Rs {total_bal:,.0f}",
                "",
                ""),
        tags=("total",))