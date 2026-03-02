import tkinter as tk
from tkinter import ttk, messagebox
from create_database import get_connection
from datetime import datetime

def open_building_collection():
    window = tk.Toplevel()
    window.title("Building Collection Control")
    window.geometry("950x650")
    window.config(bg="#f8fafc")

    # ================= SCROLLABLE CANVAS =================
    main_canvas = tk.Canvas(window, bg="#f8fafc")
    main_canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
    scrollbar.pack(side="right", fill="y")
    main_canvas.configure(yscrollcommand=scrollbar.set)

    scroll_frame = tk.Frame(main_canvas, bg="#f8fafc")
    main_canvas.create_window((0,0), window=scroll_frame, anchor="nw")

    def on_frame_configure(event):
        main_canvas.configure(scrollregion=main_canvas.bbox("all"))
    scroll_frame.bind("<Configure>", on_frame_configure)

    # ================= HEADER =================
    header = tk.Frame(scroll_frame, bg="#1e3a8a", height=80)
    header.pack(fill="x", pady=5)
    header.pack_propagate(False)
    tk.Label(header, text="Building Collection Entry",
             bg="#1e3a8a", fg="white",
             font=("Segoe UI", 20, "bold italic")).pack(pady=20)

    # ================= FORM =================
    form = tk.Frame(scroll_frame, bg="#f8fafc")
    form.pack(pady=10)

    # Variables
    building_var = tk.StringVar()
    collector_var = tk.StringVar()
    date_var = tk.StringVar()
    total_var = tk.StringVar()
    invest_var = tk.StringVar()
    selected_id = tk.IntVar(value=0)

    tk.Label(form, text="Building *", bg="#f8fafc",
             font=("Segoe UI", 10, "bold italic")).grid(row=0, column=0, sticky="w", pady=8)
    building_combo = ttk.Combobox(form, textvariable=building_var, state="readonly", width=25)
    building_combo.grid(row=0, column=1, pady=8, padx=10)

    tk.Label(form, text="Collector Name *", bg="#f8fafc",
             font=("Segoe UI", 10, "bold italic")).grid(row=1, column=0, sticky="w", pady=8)
    collector_label = tk.Label(form, textvariable=collector_var,
                               bg="#e5e7eb", width=25, anchor="w")
    collector_label.grid(row=1, column=1, pady=8, padx=10)

    tk.Label(form, text="Collection Date *", bg="#f8fafc",
             font=("Segoe UI", 10, "bold italic")).grid(row=2, column=0, sticky="w", pady=8)
    date_entry = tk.Entry(form, textvariable=date_var, width=28)
    date_entry.grid(row=2, column=1, pady=8, padx=10)
    date_var.set(datetime.now().strftime("%d-%m-%Y"))

    tk.Label(form, text="Total Collected *", bg="#f8fafc",
             font=("Segoe UI", 10, "bold italic")).grid(row=3, column=0, sticky="w", pady=8)
    total_entry = tk.Entry(form, textvariable=total_var, width=28)
    total_entry.grid(row=3, column=1, pady=8, padx=10)

    tk.Label(form, text="Invest To", bg="#f8fafc",
             font=("Segoe UI", 10, "bold italic")).grid(row=4, column=0, sticky="w", pady=8)
    invest_combo = ttk.Combobox(form, textvariable=invest_var,
                                values=["Select Invest type", "Owner", "Bank Deposit", "Cash in Hand"],
                                state="readonly", width=25)
    invest_combo.grid(row=4, column=1, pady=8, padx=10)
    invest_combo.set("Select Invest type")

    # ================= LOAD BUILDINGS =================
    def load_buildings():
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT DISTINCT building_name FROM rent_collectors")
        buildings = [row[0] for row in c.fetchall()]
        conn.close()
        building_combo['values'] = buildings

    def load_collector(event=None):
        building = building_var.get()
        if not building:
            return
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT rent_collector_name FROM rent_collectors WHERE building_name=?", (building,))
        result = c.fetchone()
        conn.close()
        collector_var.set(result[0] if result else "Not Assigned")

    building_combo.bind("<<ComboboxSelected>>", load_collector)

    # ================= TREEVIEW =================
    tree_frame = tk.Frame(scroll_frame, bg="#f8fafc")
    tree_frame.pack(fill="both", expand=True, pady=10, padx=20)

    columns = ("ID", "Building", "Collector", "Date", "Total", "Remaining", "Invest", "Status")
    collection_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
    for col in columns:
        collection_tree.heading(col, text=col)
        collection_tree.column(col, anchor="center", width=100)
    collection_tree.pack(fill="both", expand=True, side="left")

    scrollbar_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=collection_tree.yview)
    collection_tree.configure(yscrollcommand=scrollbar_tree.set)
    scrollbar_tree.pack(side="right", fill="y")

    # ================= FUNCTIONS =================
    def load_collections():
        # Clear treeview first
        for item in collection_tree.get_children():
            collection_tree.delete(item)

        conn = get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT id, building_name, collector_name, collection_date, 
                   total_collected, remaining_amount, invest_to, status 
            FROM building_collections 
            ORDER BY id DESC
        """)
        rows = c.fetchall()
        conn.close()

        for row in rows:
            collection_tree.insert("", "end", values=row)

    def refresh_collections():
        # Clear existing rows in treeview
        for item in collection_tree.get_children():
            collection_tree.delete(item)

        # Load fresh data from database
        load_collections()


    def save_collection():
        building = building_var.get().strip()
        collector = collector_var.get().strip()
        date = date_var.get().strip()
        invest_to = invest_var.get().strip()

        if not building or not collector or not total_var.get():
            messagebox.showwarning("Input Error", "Please fill required fields")
            return

        try:
            new_amount = float(total_var.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return

        conn = get_connection()
        c = conn.cursor()

        # 🔹 Get previous remaining from last collection for this building
        c.execute("""
            SELECT remaining_amount 
            FROM building_collections 
            WHERE building_name=? 
            ORDER BY id DESC LIMIT 1
        """, (building,))
        prev_remaining = c.fetchone()
        prev_remaining = prev_remaining[0] if prev_remaining else 0

        # 🔹 Calculate new remaining correctly (just add previous remaining)
        remaining_amount = prev_remaining + new_amount

        # 🔹 Insert new collection row
        c.execute("""
            INSERT INTO building_collections
            (building_name, collector_name, collection_date, total_collected, remaining_amount, invest_to, status)
            VALUES (?, ?, ?, ?, ?, ?, 'Open')
        """, (building, collector, date, new_amount, remaining_amount, invest_to))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", f"New collection added! Remaining: {remaining_amount}")

        # Reload treeview
        load_collections()

        # Clear form
        building_var.set("")
        collector_var.set("")
        date_var.set(datetime.now().strftime("%d-%m-%Y"))
        total_var.set("")
        invest_var.set("Select Invest type")
        
    def delete_collection():
        selected = collection_tree.focus()
        if not selected:
            messagebox.showwarning("Select Row", "Please select a collection to delete.")
            return

        values = collection_tree.item(selected, 'values')
        confirm = messagebox.askyesno(
            "Confirm Delete",
            f"Are you sure you want to delete collection ID {values[0]}?"
        )
        if confirm:
            conn = get_connection()
            c = conn.cursor()
            c.execute("DELETE FROM building_collections WHERE id=?", (values[0],))
            conn.commit()
            conn.close()
            load_collections()
            messagebox.showinfo("Deleted", "Collection deleted successfully.")

    def on_treeview_select(event):
        selected = collection_tree.focus()
        if not selected:
            return
        values = collection_tree.item(selected, 'values')
        selected_id.set(int(values[0]))
        building_var.set(values[1])
        collector_var.set(values[2])
        date_var.set(values[3])
        total_var.set(values[4])
        invest_var.set(values[6])

    collection_tree.bind("<Double-1>", on_treeview_select)

    # ================= BUTTONS =================
    btn_frame = tk.Frame(scroll_frame, bg="#f8fafc")
    btn_frame.pack(pady=5)

    save_btn = tk.Button(btn_frame, text="Add Collection", command=save_collection,
                         bg="#1e3a8a", fg="white", font=("Segoe UI", 11, "bold"), width=25)
    save_btn.grid(row=0, column=0, padx=5)

    delete_btn = tk.Button(btn_frame, text="Delete Selected", command=delete_collection,
                           bg="#dc2626", fg="white", font=("Segoe UI", 11, "bold"), width=15)
    delete_btn.grid(row=0, column=1, padx=5)

    refresh_btn = tk.Button(btn_frame, text="Refresh", command=refresh_collections,
                            bg="#059669", fg="white", font=("Segoe UI", 11, "bold"), width=15)
    refresh_btn.grid(row=0, column=2, padx=5)

    # ================= INITIAL LOAD =================
    load_buildings()
    load_collections()

    # ================= MOUSE WHEEL SCROLL =================
    def _on_mousewheel(event):
        try:
            main_canvas.yview_scroll(-1 * (event.delta // 120), "units")
        except tk.TclError:
            pass

    window.bind_all("<MouseWheel>", _on_mousewheel)

    def on_closing():
        try:
            window.unbind_all("<MouseWheel>")
        except:
            pass
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)



# import tkinter as tk
# from tkinter import ttk, messagebox
# from create_database import get_connection
# from datetime import datetime

# def open_building_collection():
#     window = tk.Toplevel()
#     window.title("Building Collection Control")
#     window.geometry("950x650")
#     window.config(bg="#f8fafc")

#     # ================= SCROLLABLE CANVAS =================
#     main_canvas = tk.Canvas(window, bg="#f8fafc")
#     main_canvas.pack(side="left", fill="both", expand=True)

#     scrollbar = ttk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
#     scrollbar.pack(side="right", fill="y")
#     main_canvas.configure(yscrollcommand=scrollbar.set)

#     scroll_frame = tk.Frame(main_canvas, bg="#f8fafc")
#     main_canvas.create_window((0,0), window=scroll_frame, anchor="nw")

#     def on_frame_configure(event):
#         main_canvas.configure(scrollregion=main_canvas.bbox("all"))
#     scroll_frame.bind("<Configure>", on_frame_configure)

#     # ================= HEADER =================
#     header = tk.Frame(scroll_frame, bg="#1e3a8a", height=80)
#     header.pack(fill="x", pady=5)
#     header.pack_propagate(False)
#     tk.Label(header, text="Building Collection Entry",
#              bg="#1e3a8a", fg="white",
#              font=("Segoe UI", 20, "bold italic")).pack(pady=20)

#     # ================= FORM =================
#     form = tk.Frame(scroll_frame, bg="#f8fafc")
#     form.pack(pady=10)

#     # Variables
#     building_var = tk.StringVar()
#     collector_var = tk.StringVar()
#     date_var = tk.StringVar()
#     total_var = tk.StringVar()
#     invest_var = tk.StringVar()
#     selected_id = tk.IntVar(value=0)

#     tk.Label(form, text="Building *", bg="#f8fafc",
#              font=("Segoe UI", 10, "bold italic")).grid(row=0, column=0, sticky="w", pady=8)
#     building_combo = ttk.Combobox(form, textvariable=building_var, state="readonly", width=25)
#     building_combo.grid(row=0, column=1, pady=8, padx=10)

#     tk.Label(form, text="Collector Name *", bg="#f8fafc",
#              font=("Segoe UI", 10, "bold italic")).grid(row=1, column=0, sticky="w", pady=8)
#     collector_label = tk.Label(form, textvariable=collector_var,
#                                bg="#e5e7eb", width=25, anchor="w")
#     collector_label.grid(row=1, column=1, pady=8, padx=10)

#     tk.Label(form, text="Collection Date *", bg="#f8fafc",
#              font=("Segoe UI", 10, "bold italic")).grid(row=2, column=0, sticky="w", pady=8)
#     date_entry = tk.Entry(form, textvariable=date_var, width=28)
#     date_entry.grid(row=2, column=1, pady=8, padx=10)
#     date_var.set(datetime.now().strftime("%d-%m-%Y"))

#     tk.Label(form, text="Total Collected *", bg="#f8fafc",
#              font=("Segoe UI", 10, "bold italic")).grid(row=3, column=0, sticky="w", pady=8)
#     total_entry = tk.Entry(form, textvariable=total_var, width=28)
#     total_entry.grid(row=3, column=1, pady=8, padx=10)

#     tk.Label(form, text="Invest To", bg="#f8fafc",
#              font=("Segoe UI", 10, "bold italic")).grid(row=4, column=0, sticky="w", pady=8)
#     invest_combo = ttk.Combobox(form, textvariable=invest_var,
#                                 values=["Select Invest type", "Owner", "Bank Deposit", "Cash in Hand"],
#                                 state="readonly", width=25)
#     invest_combo.grid(row=4, column=1, pady=8, padx=10)
#     invest_combo.set("Select Invest type")

#     # ================= LOAD BUILDINGS =================
#     def load_buildings():
#         conn = get_connection()
#         c = conn.cursor()
#         c.execute("SELECT DISTINCT building_name FROM rent_collectors")
#         buildings = [row[0] for row in c.fetchall()]
#         conn.close()
#         building_combo['values'] = buildings

#     def load_collector(event=None):
#         building = building_var.get()
#         if not building:
#             return
#         conn = get_connection()
#         c = conn.cursor()
#         c.execute("SELECT rent_collector_name FROM rent_collectors WHERE building_name=?", (building,))
#         result = c.fetchone()
#         conn.close()
#         collector_var.set(result[0] if result else "Not Assigned")

#     building_combo.bind("<<ComboboxSelected>>", load_collector)

#     # ================= TREEVIEW =================
#     tree_frame = tk.Frame(scroll_frame, bg="#f8fafc")
#     tree_frame.pack(fill="both", expand=True, pady=10, padx=20)

#     columns = ("ID", "Building", "Collector", "Date", "Total", "Remaining", "Invest", "Status")
#     collection_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10)
#     for col in columns:
#         collection_tree.heading(col, text=col)
#         collection_tree.column(col, anchor="center", width=100)
#     collection_tree.pack(fill="both", expand=True, side="left")

#     scrollbar_tree = ttk.Scrollbar(tree_frame, orient="vertical", command=collection_tree.yview)
#     collection_tree.configure(yscrollcommand=scrollbar_tree.set)
#     scrollbar_tree.pack(side="right", fill="y")

#         # ================= FUNCTIONS =================
#     def load_collections():
#         conn = get_connection()
#         c = conn.cursor()
#         c.execute("""
#             SELECT id, building_name, collector_name, collection_date, 
#                    total_collected, remaining_amount, invest_to, status 
#             FROM building_collections 
#             ORDER BY id DESC
#         """)
#         rows = c.fetchall()
#         conn.close()

#         for item in collection_tree.get_children():
#             collection_tree.delete(item)

#         for row in rows:
#             collection_tree.insert("", "end", values=row)


#     def save_collection():
#         building = building_var.get().strip()
#         collector = collector_var.get().strip()
#         date = date_var.get().strip()
#         invest_to = invest_var.get().strip()

#         if not building or not collector or not total_var.get():
#             messagebox.showwarning("Input Error", "Please fill required fields")
#             return

#         try:
#             new_amount = float(total_var.get())  # new amount entered
#         except ValueError:
#             messagebox.showerror("Error", "Invalid amount")
#             return

#         conn = get_connection()
#         c = conn.cursor()

#         if selected_id.get() == 0:  # 🔹 New collection start
#             # Check if there is already a collection for this building
#             c.execute("SELECT id, total_collected FROM building_collections WHERE building_name=? AND status='Open'", (building,))
#             existing = c.fetchone()

#             if existing:
#                 collection_id = existing[0]
#                 # Add new amount to existing total_collected
#                 updated_total = existing[1] + new_amount
#                 # Get total paid so far
#                 c.execute("""
#                     SELECT IFNULL(SUM(p.paid_amount),0)
#                     FROM payments p
#                     JOIN tenants t ON p.tenant_id = t.id
#                     WHERE t.building_name=?
#                 """, (building,))
#                 total_paid = c.fetchone()[0]

#                 new_remaining = updated_total - total_paid
#                 if new_remaining < 0: new_remaining = 0

#                 # Update existing collection
#                 c.execute("""
#                     UPDATE building_collections
#                     SET total_collected=?, remaining_amount=?, invest_to=?, collection_date=?
#                     WHERE id=?
#                 """, (updated_total, new_remaining, invest_to, date, collection_id))

#                 messagebox.showinfo("Success", f"Collection updated! New total: {updated_total}")

#             else:
#                 # No previous collection, create new
#                 c.execute("""
#                     INSERT INTO building_collections
#                     (building_name, collector_name, collection_date, total_collected, remaining_amount, invest_to, status)
#                     VALUES (?, ?, ?, ?, ?, ?, 'Open')
#                 """, (building, collector, date, new_amount, new_amount, invest_to))
#                 messagebox.showinfo("Success", "Collection started successfully!")

#         else:  # 🔹 Update existing collection by double-click
#             collection_id = selected_id.get()
#             # Get existing total_collected
#             c.execute("SELECT total_collected FROM building_collections WHERE id=?", (collection_id,))
#             existing_total = c.fetchone()[0]

#             # Add new_amount to existing total
#             updated_total = existing_total + new_amount

#             # Total paid so far
#             c.execute("""
#                 SELECT IFNULL(SUM(p.paid_amount),0)
#                 FROM payments p
#                 JOIN tenants t ON p.tenant_id = t.id
#                 WHERE t.building_name=?
#             """, (building,))
#             total_paid = c.fetchone()[0]

#             new_remaining = updated_total - total_paid
#             if new_remaining < 0: new_remaining = 0

#             # Update collection
#             c.execute("""
#                 UPDATE building_collections
#                 SET building_name=?, collector_name=?, collection_date=?, 
#                     total_collected=?, remaining_amount=?, invest_to=?
#                 WHERE id=?
#             """, (building, collector, date, updated_total, new_remaining, invest_to, collection_id))

#             messagebox.showinfo("Success", "Collection updated successfully!")
#             selected_id.set(0)
#             save_btn.config(text="Save / Start Collection")

#         conn.commit()
#         conn.close()

#         # Reload treeview
#         load_collections()

#         # Clear form
#         building_var.set("")
#         collector_var.set("")
#         date_var.set(datetime.now().strftime("%d-%m-%Y"))
#         total_var.set("")
#         invest_var.set("Select Invest type")

#     def delete_collection():
#         selected = collection_tree.focus()

#         if not selected:
#             messagebox.showwarning("Select Row", "Please select a collection to delete.")
#             return

#         values = collection_tree.item(selected, 'values')

#         confirm = messagebox.askyesno(
#             "Confirm Delete",
#             f"Are you sure you want to delete collection ID {values[0]}?"
#         )

#         if confirm:
#             conn = get_connection()
#             c = conn.cursor()
#             c.execute("DELETE FROM building_collections WHERE id=?", (values[0],))
#             conn.commit()
#             conn.close()

#             load_collections()
#             messagebox.showinfo("Deleted", "Collection deleted successfully.")

#     # ================= DOUBLE-CLICK TO EDIT =================
#     def on_treeview_select(event):
#         selected = collection_tree.focus()
#         if not selected:
#             return
#         values = collection_tree.item(selected, 'values')

#         selected_id.set(int(values[0]))
#         building_var.set(values[1])
#         collector_var.set(values[2])
#         date_var.set(values[3])
#         total_var.set(values[4])
#         invest_var.set(values[6])
#         save_btn.config(text="Update Collection")

#     collection_tree.bind("<Double-1>", on_treeview_select)

#     # ================= BUTTONS =================
#     btn_frame = tk.Frame(scroll_frame, bg="#f8fafc")
#     btn_frame.pack(pady=5)
#     save_btn = tk.Button(btn_frame, text="Save Collection", command=save_collection,
#                          bg="#1e3a8a", fg="white", font=("Segoe UI", 11, "bold"), width=25)
#     save_btn.grid(row=0, column=0, padx=5)

#     delete_btn = tk.Button(btn_frame, text="Delete Selected", command=delete_collection,
#                            bg="#dc2626", fg="white", font=("Segoe UI", 11, "bold"), width=15)
#     delete_btn.grid(row=0, column=1, padx=5)

#     # ================= INITIAL LOAD =================
#     load_buildings()
#     load_collections()

# # ================= MOUSE WHEEL SCROLL =================
#     def _on_mousewheel(event):
#         try:
#             main_canvas.yview_scroll(-1 * (event.delta // 120), "units")
#         except tk.TclError:
#             pass

#     window.bind_all("<MouseWheel>", _on_mousewheel)

#     def on_closing():
#         try:
#             window.unbind_all("<MouseWheel>")
#         except:
#             pass
#         window.destroy()

#     window.protocol("WM_DELETE_WINDOW", on_closing)