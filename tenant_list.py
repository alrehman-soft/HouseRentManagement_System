import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from create_database import get_connection
from datetime import datetime
from PIL import Image, ImageTk
import pandas as pd
import os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def open_tenant_list():
    window = tk.Toplevel()
    window.title("Abu Huraira Enterprises - Created by .ARS")
    window.geometry("1200x700")
    window.config(bg="#f8fafc")

    # Main container
    main_frame = tk.Frame(window, bg="#f8fafc")
    main_frame.pack(fill="both", expand=True)

    # Header
    header_frame = tk.Frame(main_frame, bg="#1e3a8a", height=120)
    header_frame.pack(fill="x", pady=(0, 20))
    header_frame.pack_propagate(False)
    
    tk.Label(header_frame, text="Abu Huraira Enterprises \nTenant Management List", 
             font=("Segoe UI", 20, "bold"), bg="#1e3a8a", fg="white").pack(pady=20)

    # Content container
    content_frame = tk.Frame(main_frame, bg="#f8fafc")
    content_frame.pack(fill="both", expand=True, padx=20)

    # Search and Filter Frame
    filter_frame = tk.Frame(content_frame, bg="#f8fafc", padx=20, pady=10)
    filter_frame.pack(fill="x")

    tk.Label(filter_frame, text="Search by Phone #:", bg="#f8fafc", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5)
    search_var = tk.StringVar()
    search_entry = tk.Entry(filter_frame, textvariable=search_var, width=30, font=("Segoe UI", 10))
    search_entry.grid(row=0, column=1, padx=5)

    search_frame = tk.Frame(filter_frame, bg="#f8fafc")
    search_frame.grid(row=0, column=0, columnspan=2, sticky="w")

    tk.Label(filter_frame, text="Floor:", bg="#f8fafc", font=("Segoe UI", 10)).grid(row=0, column=2, padx=20)
    floor_var = tk.StringVar()
    floor_combo = ttk.Combobox(filter_frame, textvariable=floor_var, 
                              values=["All"] + [str(i) for i in range(1, 11)], 
                              state="readonly", width=15)
    floor_combo.grid(row=0, column=3, padx=5)
    floor_combo.set("All")

    tk.Label(filter_frame, text="Status:", bg="#f8fafc", font=("Segoe UI", 10)).grid(row=0, column=4, padx=20)
    status_var = tk.StringVar()
    status_combo = ttk.Combobox(filter_frame, textvariable=status_var, 
                               values=["All", "Active", "Vacated"], 
                               state="readonly", width=15)
    status_combo.grid(row=0, column=5, padx=5)
    status_combo.set("All")

    # Buttons Frame
    button_frame = tk.Frame(content_frame, bg="#f8fafc", pady=10)
    button_frame.pack(fill="x")

    # Treeview Frame
    tree_frame = tk.Frame(content_frame, bg="#f8fafc")
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Create Treeview
    columns = ("S.No.","ID", "Name", "Father Name", "CNIC", "Phone", "Building Name", "Floor", "Flat No", 
               "Entry Date", "Status", "Rent Amount", "Advance Amount")
    
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=20)
    
    # Define headings
    for col in columns:
        tree.heading(col, text=col)
        if col == "S.No.":
            tree.column(col, width=60, anchor="center")
        elif col == "ID":
            tree.column(col, width=0, anchor="center", minwidth=0, stretch=False)
        else:
            tree.column(col, width=100, anchor="center")

    # Specific column widths
    tree.column("Name", width=120)
    tree.column("Father Name", width=120)
    tree.column("CNIC", width=120)
    tree.column("Phone", width=100)
    tree.column("Building Name", width=120)
    tree.column("Floor", width=60)
    tree.column("Flat No", width=70)
    tree.column("Entry Date", width=90)
    tree.column("Status", width=80)
    tree.column("Rent Amount", width=100)
    tree.column("Advance Amount", width=100)

    # Scrollbars
    v_scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    h_scroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

    # Pack tree and scrollbars
    tree.grid(row=0, column=0, sticky="nsew")
    v_scroll.grid(row=0, column=1, sticky="ns")
    h_scroll.grid(row=1, column=0, sticky="ew")

    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)

    # ========== FUNCTIONS DEFINITION ==========
    def load_tenants():
        # Load tenants into treeview
        for item in tree.get_children():
            tree.delete(item)
        
        conn = get_connection()
        c = conn.cursor()
        
        # UPDATED QUERY
        query = """SELECT t.id, t.name, t.father_name, t.cnic, t.phone, 
                          t.building_name, t.floor, t.flat_no, t.entry_date, 
                          t.status, t.rent_amount, t.advance_amount
                   FROM tenants t
                   ORDER BY t.floor, t.flat_no"""
        
        c.execute(query)
        tenants = c.fetchall()
        conn.close()
        
        for idx, tenant in enumerate(tenants, start=1):
            # Format amounts
            formatted_tenant = list(tenant)
            formatted_tenant[10] = f"{tenant[10]:,.2f}" if tenant[10] else "0.00"
            formatted_tenant[11] = f"{tenant[11]:,.2f}" if tenant[11] else "0.00"
            
            # Add S.No. in 1st column
            values_with_sno = [idx] + formatted_tenant
            tree.insert("", "end", values=values_with_sno)

    def filter_tenants():
        # Filter tenants
        for item in tree.get_children():
            tree.delete(item)
        
        conn = get_connection()
        c = conn.cursor()
        
        # Base query
        query = """SELECT t.id, t.name, t.father_name, t.cnic, t.phone, 
                        t.building_name, t.floor, t.flat_no, t.entry_date, 
                        t.status, t.rent_amount, t.advance_amount
                FROM tenants t WHERE 1=1"""
        params = []
        
        # Search filter
        search_text = search_var.get().strip()
        if search_text:
            query += " AND t.phone LIKE ?"
            search_pattern = f"%{search_text}%"
            params.append(search_pattern)
        
        # Floor filter
        if floor_var.get() != "All":
            query += " AND t.floor = ?"
            params.append(int(floor_var.get()))
        
        # Status filter
        if status_var.get() != "All":
            query += " AND t.status = ?"
            params.append(status_var.get())
        
        query += " ORDER BY t.floor, t.flat_no"
        
        c.execute(query, params)
        tenants = c.fetchall()
        conn.close()
        
        for idx, tenant in enumerate(tenants, start=1):
            # Format amounts
            formatted_tenant = list(tenant)
            formatted_tenant[10] = f"{tenant[10]:,.2f}" if tenant[10] else "0.00"
            formatted_tenant[11] = f"{tenant[11]:,.2f}" if tenant[11] else "0.00"
            
            # Add S.No.
            values_with_sno = [idx] + formatted_tenant 
            tree.insert("", "end", values=values_with_sno)

    def view_tenant_details():
        # View detailed information
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a tenant to view details")
            return
        
        tenant_id = tree.item(selected[0])['values'][1]
        show_tenant_details(tenant_id)

    def edit_tenant():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a tenant to edit")
            return

        tenant_id = tree.item(selected[0])['values'][1]

        conn = get_connection()
        c = conn.cursor()

        # Fetch tenant data
        c.execute("SELECT * FROM tenants WHERE id=?", (tenant_id,))
        tenant = c.fetchone()
        conn.close()

        if not tenant:
            messagebox.showerror("Error", "Tenant not found!")
            return
        open_edit_window(tenant)

    def open_edit_window(tenant):
        edit_win = tk.Toplevel()
        edit_win.title("Edit Tenant")
        edit_win.geometry("750x700")
        edit_win.resizable(False, False)

        edit_win.configure(bg="#f0f2f5")

        # ================= Scrollable Frame Setup =================
        canvas = tk.Canvas(edit_win)
        scrollbar = ttk.Scrollbar(edit_win, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0,0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ================= Photo Section =================
        photo_path = tenant[18] if tenant[18] else ""

        photo_label = tk.Label(scroll_frame,bg="#f0f2f5",relief="solid",bd=1)
        photo_label.grid(row=0, column=2, rowspan=8, padx=30, pady=10)

        def show_photo(path):
            if path and os.path.exists(path):           
                try:
                    img = Image.open(path)
                    img = img.resize((250, 300), Image.LANCZOS)
                    img = ImageTk.PhotoImage(img)

                    photo_label.config(image=img, text="")
                    photo_label.image = img 
                    
                except Exception as e:
                    photo_label.config(text="No Photo", image="", font=("Arial, 12"),
                                        anchor="center")
                    photo_label.image = None

            else:
                photo_label.config(text="No Photo", image="", font=("Arial, 12"), anchor="center")
                photo_label.image = None
        show_photo(photo_path)

        def change_photo():
            from tkinter import filedialog
            file = filedialog.askopenfilename(
                filetypes=[('Image files', '*.jpg *.jpeg *.png *.gif *.bmp'),
                           ('All files', '*.*')
                ]
            )
            if file:
                nonlocal photo_path
                photo_path = file
                show_photo(photo_path)

        tk.Button(scroll_frame, text="Change Photo",
                command=change_photo).grid(row=8, column=2, pady=10)

        # ================= Form Fields =================
        labels = [
            "Name", "Father Name", "CNIC", "Phone",
            "Emergency Contact", "Profession", "Building Name",
            "Floor", "Flat No", "Entry Date", "Exit Date",
            "Status", "Owner Name", "Owner Phone", "Rent Amount",
            "Security Deposit", "Advance Amount", "Additional Note"
        ]
        entries = []

        for i, label in enumerate(labels):
            tk.Label(scroll_frame, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="w")

            if label == "Status":
                entry = ttk.Combobox(scroll_frame, values=["Active", "Inactive"], state="readonly")
                entry.set(tenant[12])
            else:
                entry = tk.Entry(scroll_frame, width=30)
                if label == "Additional Note":
                    entry.insert(0, tenant[20] if len(tenant) > 20 else "")
                else:
                    entry.insert(0, tenant[i+1])
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

        # ================= Update Function =================
        def update_tenant():
            try:

                conn = get_connection()
                c = conn.cursor()

                c.execute("""
                    UPDATE tenants
                    SET name=?, father_name=?, cnic=?, phone=?, emergency_contact=?,
                        profession=?, building_name=?, floor=?, flat_no=?, entry_date=?,
                        exit_date=?, status=?, owner_name=?, owner_phone=?, rent_amount=?,
                        security_deposit=?, advance_amount=?, photo_path=?, notes=?
                    WHERE id=?
                """, (
                    entries[0].get(),
                    entries[1].get(),
                    entries[2].get(),
                    entries[3].get(),
                    entries[4].get(),
                    entries[5].get(),
                    entries[6].get(),
                    entries[7].get(),
                    entries[8].get(),
                    entries[9].get(),
                    entries[10].get(),
                    entries[11].get(),
                    entries[12].get(),
                    entries[13].get(),
                    entries[14].get(),
                    entries[15].get(),
                    entries[16].get(),
                    photo_path,
                    entries[17].get(),  # Notes
                    tenant[0]
                ))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Tenant updated successfully!")
                edit_win.destroy()
                load_tenants()
            except ValueError as e:
                messagebox.showerror("Error", "Please check numeric fields (Rent, Security, Advance)")
            except Exception as e:
                messagebox.showerror("Error", f"Update failed: {str(e)}")

        tk.Button(scroll_frame, text="Update",
                bg="#397112", fg="white", width=18,height=2,font=("Arial, 12"),
                command=update_tenant).grid(row=len(labels)+1,
                                            columnspan=2, pady=20)

    def mark_vacated():
        # Mark selected tenant as vacated
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a tenant to mark as vacated")
            return

        values = tree.item(selected[0])['values']
        tenant_id = values[1]
        tenant_name = values[2]
        flat_no = values[8]
        
        if messagebox.askyesno("Confirm", f"Mark {tenant_name} as vacated?"):
            conn = get_connection()
            c = conn.cursor()
            
            try:
                c.execute("UPDATE tenants SET status='Vacated', exit_date=date('now') WHERE id=?", (tenant_id,))
                
                conn.commit()
                messagebox.showinfo("Success", "Tenant marked as vacated successfully!")
                load_tenants()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update: {str(e)}")
                conn.rollback()
            finally:
                conn.close()

    def undo_vacated():
        # Mark tenant as Active again
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a tenant")
            return

        values = tree.item(selected[0])['values']
        tenant_id = values[1]
        tenant_name = values[2]
        flat_no = values[8]

        if messagebox.askyesno("Confirm", f"Mark {tenant_name} as Active again?"):
            conn = get_connection()
            c = conn.cursor()

            try:
                c.execute("""
                    UPDATE tenants 
                    SET status='Active', exit_date=NULL 
                    WHERE id=?
                """, (tenant_id,))

                conn.commit()
                messagebox.showinfo("Success", "Tenant restored successfully!")
                load_tenants()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to update: {str(e)}")
                conn.rollback()
            finally:
                conn.close()

    def delete_tenant():
        # Delete tenant
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a tenant to delete")
            return
        
        values = tree.item(selected[0])['values']
        tenant_id = values[1]
        tenant_name = values[2]
        flat_no = values[8]
        
        if messagebox.askyesno("Confirm Delete", 
                            f"Are you sure you want to PERMANENTLY delete {tenant_name}?\n\nThis action cannot be undone!"):
            conn = get_connection()
            c = conn.cursor()
            
            try:
                c.execute("DELETE FROM payments WHERE tenant_id=?", (tenant_id,))
                
                c.execute("DELETE FROM witnesses WHERE tenant_id=?", (tenant_id,))
                
                c.execute("DELETE FROM tenants WHERE id=?", (tenant_id,))
                
                conn.commit()
                messagebox.showinfo("Success", "Tenant deleted successfully!")
                load_tenants()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete tenant: {str(e)}")
                conn.rollback()
            finally:
                conn.close()


    def export_tenant_list_pdf_table():
        try:
            # Ask user for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Save Tenant List As PDF"
            )
            if not file_path:
                return
            
            # Fetch tenants from database
            conn = get_connection()
            c = conn.cursor()
            c.execute("""SELECT t.name, t.father_name, t.cnic, t.phone, t.building_name,
                                t.floor, t.flat_no, t.entry_date, t.status, t.rent_amount, t.advance_amount
                        FROM tenants t
                        ORDER BY t.floor, t.flat_no""")
            tenants = c.fetchall()
            conn.close()
            
            # Use LANDSCAPE orientation
            doc = SimpleDocTemplate(
                file_path,
                pagesize=landscape(A4),
                rightMargin=30,
                leftMargin=30,
                topMargin=40,
                bottomMargin=30
            )
            elements = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Title'],
                fontSize=20,
                alignment=1,
                spaceAfter=20,
                textColor=colors.HexColor('#1e3a8a')
            )
            
            # Title
            title = Paragraph("ABU HURAIRA ENTERPRISES <br/>TENANT LIST REPORT", title_style)
            elements.append(title)
            
            # Info line
            info_style = ParagraphStyle(
                'InfoStyle',
                parent=styles['Normal'],
                fontSize=16,
                alignment=1,
                spaceAfter=20
            )
            info_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} <br/> <br/>Total Tenants: {len(tenants)}"
            info = Paragraph(info_text, info_style)
            elements.append(info)
            
            elements.append(Spacer(1, 10))
            
            # Table data preparation
            headers = ["Name", "Father's \nName", "CNIC", "Phone", "Building", 
                    "Floor", "Flat", "Entry Date", "Status", "Rent \nAmount", "Advance \nPayment"]
            data = [headers]
            
            for tenant in tenants:
                row = list(tenant)
                
                # Format amounts
                row[9] = f"{int(row[9]):,}" if row[9] and row[9] != 0 else "-"
                row[10] = f"{int(row[10]):,}" if row[10] and row[10] != 0 else "-"
                
                # Format entry date
                if row[7]:
                    if hasattr(row[7], 'strftime'):
                        row[7] = row[7].strftime('%d-%m-%Y')
                    else:
                        # Try to parse string date
                        try:
                            date_str = str(row[7])
                            if '-' in date_str:
                                parts = date_str.split('-')
                                if len(parts) == 3:
                                    if len(parts[0]) == 4:  # YYYY-MM-DD format
                                        row[7] = f"{parts[2]}-{parts[1]}-{parts[0]}"
                        except:
                            row[7] = str(row[7])
                else:
                    row[7] = "-"
                
                for i in range(len(row)):
                    if row[i] is None or row[i] == "":
                        row[i] = "-"
                
                data.append(row)
            
            # Calculate column widths
            page_width, page_height = landscape(A4)
            available_width = page_width - 60
            
            # UPDATED WIDTH RATIOS
            col_ratios = [
                1.8, 1.8, 1.6, 1.3, 2.0, 0.8, 0.8, 1.2, 0.9, 1.2, 1.2
            ]
            
            total_ratio = sum(col_ratios)
            col_widths = [available_width * r / total_ratio for r in col_ratios]
            
            # Create table
            table = Table(data, colWidths=col_widths, repeatRows=1, hAlign='CENTER')
            
            # Table style
            table_style = TableStyle([
                # Header row
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1e3a8a')),
                ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 11),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('TOPPADDING', (0,0), (-1,0), 8),
                
                # Data rows
                ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,1), (-1,-1), 10), 
                ('TOPPADDING', (0,1), (-1,-1), 6),
                ('BOTTOMPADDING', (0,1), (-1,-1), 6),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
                
                # Grid
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cccccc')),
                
                # Alignment
                ('ALIGN', (5,1), (7,-1), 'CENTER'),
                ('ALIGN', (8,1), (8,-1), 'CENTER'),
                ('ALIGN', (9,1), (10,-1), 'RIGHT'),
            ])
            
            # Add alternating row colors
            for i in range(1, len(data)):
                if i % 2 == 0:
                    table_style.add('BACKGROUND', (0,i), (-1,i), colors.HexColor('#f5f5f5'))
            
            table.setStyle(table_style)
            
            elements.append(table)
            
            # Add footer
            def add_page_number(canvas, doc):
                page_num = canvas.getPageNumber()
                canvas.saveState()
                canvas.setFont('Helvetica', 9)
                canvas.drawCentredString(page_width/2, 15, f"Page {page_num}")
                canvas.restoreState()
            
            # Build PDF
            doc.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
            
            messagebox.showinfo("Success", f"Tenant list exported to PDF successfully!\n\nFile: {file_path}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")
            import traceback
            traceback.print_exc()
            
    def export_to_excel():
        # Export tenant list to Excel
        try:
            conn = get_connection()
            c = conn.cursor()
            
            # Get all tenants
            c.execute("""SELECT t.name, t.father_name, t.cnic, t.phone, t.emergency_contact,
                                t.profession, t.building_name, t.floor, t.flat_no, t.entry_date, t.exit_date,
                                t.status, t.owner_name, t.owner_phone, t.rent_amount,
                                t.security_deposit, t.advance_amount
                         FROM tenants t
                         ORDER BY t.floor, t.flat_no""")
            tenants = c.fetchall()
            conn.close()
            
            # Create DataFrame
            columns = ['Name', 'Father Name', 'CNIC', 'Phone', 'Emergency Contact', 
                      'Profession', 'Building Name', 'Floor', 'Flat No', 'Entry Date', 'Exit Date',
                      'Status', 'Owner Name', 'Owner Phone', 'Rent Amount', 
                      'Security Deposit', 'Advance Amount']
            
            df = pd.DataFrame(tenants, columns=columns)
            
            # Ask for save location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Save Tenant List As Excel"
            )
            
            if not file_path:
                return
            
            # Save to Excel
            df.to_excel(file_path, engine="openpyxl", index=False)
            messagebox.showinfo("Success", f"Tenant list exported to Excel successfully!\n\nFile: {file_path}")
            
        except ImportError:
            messagebox.showerror("Error", "Pandas library not installed. Please install it using: pip install pandas openpyxl")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export to Excel: {str(e)}")

    def show_tenant_details(tenant_id):
        conn = get_connection()
        c = conn.cursor()
        
        # Get tenant details
        c.execute("""SELECT t.*, w.w1_name, w.w1_cnic, w.w1_phone, 
                            w.w2_name, w.w2_cnic, w.w2_phone
                    FROM tenants t
                    LEFT JOIN witnesses w ON t.id = w.tenant_id
                    WHERE t.id = ?""", (tenant_id,))
        tenant_data = c.fetchone()
        conn.close()
        
        if not tenant_data:
            messagebox.showerror("Error", "Tenant not found!")
            return
        
        # Check photo path
        photo_path = tenant_data[18]
        
        # Create details window
        details_win = tk.Toplevel(window)
        details_win.title("Abu Huraira Enterprises - Tenant Details")
        details_win.geometry("1000x750")
        details_win.config(bg="#f8fafc")
        
        # Main frame
        main_frame = tk.Frame(details_win, bg="#f8fafc")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, text="Abu Huraira Enterprises\nTenant Details", 
                            font=("Segoe UI", 18, "bold"), bg="#f8fafc", fg="#1e3a8a")
        title_label.pack(pady=(0, 20))
        
        # Photo and basic info in two columns
        top_frame = tk.Frame(main_frame, bg="#f8fafc")
        top_frame.pack(fill="x", pady=(0, 20))
        
        # Left column - Photo
        left_col = tk.Frame(top_frame, bg="#f8fafc", width=300)
        left_col.pack(side="left", padx=(0, 20), fill="y")
        left_col.pack_propagate(False)
        
        # Photo frame
        photo_frame = tk.LabelFrame(left_col, text="Tenant Photo", 
                                font=("Segoe UI", 11, "bold"), bg="#f8fafc")
        photo_frame.pack(fill="both", expand=True)
        
        photo_label = tk.Label(photo_frame, text="No Photo Available", 
                            bg="#e5e7eb", fg="#6b7280", font=("Segoe UI", 10),
                            width=35, height=18, relief="solid", bd=1)
        photo_label.pack(padx=10, pady=10)
        
        # Load and display photo if exists
        if photo_path and os.path.exists(photo_path):
            try:
                image = Image.open(photo_path)
                # Resize image to fit
                image.thumbnail((260, 320), Image.Resampling.LANCZOS)
                photo_img = ImageTk.PhotoImage(image)
                
                photo_label.config(image=photo_img, text="", width=260, height=320)
                photo_label.image = photo_img
                
            except Exception as e:
                print(f"Error loading photo: {e}")
                photo_label.config(text="Error Loading Photo", bg="#fecaca")
        
        # Right column - Basic Info
        right_col = tk.Frame(top_frame, bg="#f8fafc")
        right_col.pack(side="left", fill="both", expand=True)
        
        # Info frame with scrollbar
        info_canvas = tk.Canvas(right_col, bg="#f8fafc", highlightthickness=0)
        info_scrollbar = ttk.Scrollbar(right_col, orient="vertical", command=info_canvas.yview)
        info_inner = tk.Frame(info_canvas, bg="#f8fafc")
        
        info_canvas.create_window((0, 0), window=info_inner, anchor="nw")
        info_canvas.configure(yscrollcommand=info_scrollbar.set)
        
        info_inner.bind("<Configure>", lambda e: info_canvas.configure(scrollregion=info_canvas.bbox("all")))
        
        info_canvas.pack(side="left", fill="both", expand=True)
        info_scrollbar.pack(side="right", fill="y")
        
        # Basic Information
        basic_info_frame = tk.LabelFrame(info_inner, text="Basic Information", 
                                        font=("Segoe UI", 11, "bold"), bg="#f8fafc", pady=10)
        basic_info_frame.pack(fill="x", pady=(0, 10))
        
        basic_fields = [
            ("Name:", tenant_data[1] or "N/A", 0, 0),
            ("Father Name:", tenant_data[2] or "N/A", 0, 2),
            ("CNIC:", tenant_data[3] or "N/A", 1, 0),
            ("Phone:", tenant_data[4] or "N/A", 1, 2),
            ("Emergency Contact:", tenant_data[5] or "N/A", 2, 0),
            ("Profession:", tenant_data[6] or "N/A", 2, 2),
        ]
        
        for label, value, row, col in basic_fields:
            tk.Label(basic_info_frame, text=label, font=("Segoe UI", 10, "bold"), 
                    bg="#f8fafc").grid(row=row, column=col, sticky="w", padx=10, pady=5)
            tk.Label(basic_info_frame, text=value, font=("Segoe UI", 10), 
                    bg="#f8fafc", wraplength=200).grid(row=row, column=col+1, sticky="w", padx=5, pady=5)
        
        # Property Information
        property_frame = tk.LabelFrame(info_inner, text="Property Information", 
                                    font=("Segoe UI", 11, "bold"), bg="#f8fafc", pady=10)
        property_frame.pack(fill="x", pady=(0, 10))
        
        property_fields = [
            ("Building:", tenant_data[7] or "N/A", 0, 0),
            ("Floor:", str(tenant_data[8]) if tenant_data[8] else "N/A", 0, 2),
            ("Flat No:", tenant_data[9] or "N/A", 1, 0),
            ("Entry Date:", tenant_data[10] or "N/A", 1, 2),
            ("Exit Date:", tenant_data[11] or "N/A", 2, 0),
            ("Status:", tenant_data[12] or "N/A", 2, 2),
        ]
        
        for label, value, row, col in property_fields:
            tk.Label(property_frame, text=label, font=("Segoe UI", 10, "bold"), 
                    bg="#f8fafc").grid(row=row, column=col, sticky="w", padx=10, pady=5)
            tk.Label(property_frame, text=value, font=("Segoe UI", 10), 
                    bg="#f8fafc").grid(row=row, column=col+1, sticky="w", padx=5, pady=5)
        
        # Owner Information
        owner_frame = tk.LabelFrame(info_inner, text="Owner Information", 
                                font=("Segoe UI", 11, "bold"), bg="#f8fafc", pady=10)
        owner_frame.pack(fill="x", pady=(0, 10))
        
        owner_fields = [
            ("Owner Name:", tenant_data[13] or "N/A", 0, 0),
            ("Owner Phone:", tenant_data[14] or "N/A", 0, 2),
        ]
        
        for label, value, row, col in owner_fields:
            tk.Label(owner_frame, text=label, font=("Segoe UI", 10, "bold"), 
                    bg="#f8fafc").grid(row=row, column=col, sticky="w", padx=10, pady=5)
            tk.Label(owner_frame, text=value, font=("Segoe UI", 10), 
                    bg="#f8fafc").grid(row=row, column=col+1, sticky="w", padx=5, pady=5)
        
        # Financial Information
        financial_frame = tk.LabelFrame(info_inner, text="Financial Information", 
                                    font=("Segoe UI", 11, "bold"), bg="#f8fafc", pady=10)
        financial_frame.pack(fill="x", pady=(0, 10))
        
        financial_fields = [
            ("Rent Amount:", f"Rs. {(tenant_data[15] or 0):,.2f}", 0, 0),
            ("Security Deposit:", f"Rs. {(tenant_data[16] or 0):,.2f}", 0, 2),
            ("Advance Amount:", f"Rs. {(tenant_data[17] or 0):,.2f}", 1, 0),
        ]
        
        for label, value, row, col in financial_fields:
            tk.Label(financial_frame, text=label, font=("Segoe UI", 10, "bold"), 
                    bg="#f8fafc").grid(row=row, column=col, sticky="w", padx=10, pady=5)
            tk.Label(financial_frame, text=value, font=("Segoe UI", 10), 
                    bg="#f8fafc").grid(row=row, column=col+1, sticky="w", padx=5, pady=5)
        
        # Additional Note
        if tenant_data[20]:  # If note exists
            note_frame = tk.LabelFrame(info_inner, text="Additional Note", 
                                    font=("Segoe UI", 11, "bold"), bg="#f8fafc", pady=10)
            note_frame.pack(fill="x", pady=(0, 10))
            
            note_text = tk.Text(note_frame, height=3, width=50, font=("Segoe UI", 10), 
                            wrap="word", bg="#f8fafc", relief="solid", bd=1)
            note_text.pack(padx=10, pady=5)
            note_text.insert("1.0", tenant_data[20])
            note_text.config(state="disabled")
        
        # Witness Information
        witness_frame = tk.LabelFrame(main_frame, text="Witness Information", 
                                    font=("Segoe UI", 12, "bold"), bg="#f8fafc", pady=10)
        witness_frame.pack(fill="x", pady=10)
        
        # Witness 1
        tk.Label(witness_frame, text="Witness 1:", font=("Segoe UI", 11, "bold"), 
                bg="#f8fafc").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        tk.Label(witness_frame, text=f"Name: {tenant_data[21] or 'N/A'}", 
                bg="#f8fafc").grid(row=0, column=1, sticky="w", padx=10, pady=2)
        tk.Label(witness_frame, text=f"CNIC: {tenant_data[22] or 'N/A'}", 
                bg="#f8fafc").grid(row=1, column=1, sticky="w", padx=10, pady=2)
        tk.Label(witness_frame, text=f"Phone: {tenant_data[23] or 'N/A'}", 
                bg="#f8fafc").grid(row=2, column=1, sticky="w", padx=10, pady=2)
        
        # Witness 2
        tk.Label(witness_frame, text="Witness 2:", font=("Segoe UI", 11, "bold"), 
                bg="#f8fafc").grid(row=0, column=2, sticky="w", padx=20, pady=5)
        tk.Label(witness_frame, text=f"Name: {tenant_data[24] or 'N/A'}", 
                bg="#f8fafc").grid(row=0, column=3, sticky="w", padx=10, pady=2)
        tk.Label(witness_frame, text=f"CNIC: {tenant_data[25] or 'N/A'}", 
                bg="#f8fafc").grid(row=1, column=3, sticky="w", padx=10, pady=2)
        tk.Label(witness_frame, text=f"Phone: {tenant_data[26] or 'N/A'}", 
                bg="#f8fafc").grid(row=2, column=3, sticky="w", padx=10, pady=2)
        
        # Close button
        button_frame = tk.Frame(main_frame, bg="#f8fafc")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Close", command=details_win.destroy,
                bg="#1e3a8a", fg="white", font=("Segoe UI", 12, "bold"),
                width=15, padx=10, pady=5).pack()  
    
    # ========== BUTTONS CREATION ==========
    ttk.Button(button_frame, text="Refresh", command=load_tenants).pack(side="left", padx=5)
    ttk.Button(button_frame, text="View Details", command=view_tenant_details).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Edit Tenant", command=edit_tenant).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Mark as Vacated", command=mark_vacated).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Mark as UnVacated", command=undo_vacated).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Delete Tenant", command=delete_tenant).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Print Tenant List", command=export_tenant_list_pdf_table).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Export to Excel", command=export_to_excel).pack(side="left", padx=5)

    # ========== EVENT BINDING ==========
    search_entry.bind('<KeyRelease>', lambda e: filter_tenants())
    floor_combo.bind('<<ComboboxSelected>>', lambda e: filter_tenants())
    status_combo.bind('<<ComboboxSelected>>', lambda e: filter_tenants())
    tree.bind("<Double-1>", lambda e: view_tenant_details())

    # Right-click context menu
    context_menu = tk.Menu(window, tearoff=0)
    context_menu.add_command(label="View Details", command=view_tenant_details)
    context_menu.add_command(label="Mark as Vacated", command=mark_vacated)
    context_menu.add_separator()
    context_menu.add_command(label="Delete Tenant", command=delete_tenant)
    
    def show_context_menu(event):
        item = tree.identify_row(event.y)
        if item:
            tree.selection_set(item)
            context_menu.post(event.x_root, event.y_root)
    
    tree.bind("<Button-3>", show_context_menu)
    load_tenants()