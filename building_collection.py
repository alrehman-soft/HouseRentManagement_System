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

        # Get previous remaining from last collection
        c.execute("""
            SELECT remaining_amount 
            FROM building_collections 
            WHERE building_name=? 
            ORDER BY id DESC LIMIT 1
        """, (building,))
        prev_remaining = c.fetchone()
        prev_remaining = prev_remaining[0] if prev_remaining else 0

        # Calculate new remaining
        remaining_amount = prev_remaining + new_amount

        # Insert new collection
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

    def clear_form():
        # Sirf form clear
        building_var.set("")
        collector_var.set("")
        date_var.set(datetime.now().strftime("%d-%m-%Y"))
        total_var.set("")
        invest_var.set("Select Invest type")
        selected_id.set(0)
        
        # Treeview selection clear
        for item in collection_tree.selection():
            collection_tree.selection_remove(item)
        
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
                            bg="#035C40", fg="white", font=("Segoe UI", 11, "bold"), width=15)
    refresh_btn.grid(row=0, column=2, padx=5)

    clear_btn = tk.Button(btn_frame, text="Clear Form", command=clear_form,
                        bg="#171003", fg="white", font=("Segoe UI", 11, "bold"), width=15)
    clear_btn.grid(row=0, column=3, padx=5)

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
