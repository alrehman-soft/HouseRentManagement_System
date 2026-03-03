import tkinter as tk, os, subprocess
from tkinter import messagebox
from create_database import get_connection, get_counts, DATABASE_NAME, get_available_drives, get_free_space
from add_tenant import add_tenant_screen
from tenant_list import open_tenant_list
from payment import open_payments
from rent_collector import open_rent_collector
from main_report import open_reports_dashboard
from datetime import datetime
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


# Better font configuration for matplotlib
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def open_dashboard():
    dashboard = tk.Tk()
    dashboard.title("Abu Huraira Enterprises - Created by: .ARS")
    dashboard.geometry("1370x800")
    dashboard.config(bg="#f0f2f5")
    dashboard.state('zoomed')

    # Configure grid weights
    dashboard.grid_columnconfigure(1, weight=1)
    dashboard.grid_rowconfigure(0, weight=1)

    # ========== SIDEBAR ==========
    sidebar = tk.Frame(dashboard, bg="#1e3a8a", width=350)
    sidebar.grid(row=0, column=0, sticky="nsew")
    sidebar.grid_propagate(False)

    # Logo/Header
    tk.Label(sidebar, text="🏠 HOUSE RENT\nMANAGEMENT", 
             font=("Segoe UI", 20, "bold"),
             bg="#1e3a8a", fg="white", justify="center").pack(pady=(30, 20))

    # Sidebar Buttons
    buttons_data = [
        ("📊 Dashboard", None),
        ("👤 Add Tenant", add_tenant_screen),
        ("📋 Tenant List", open_tenant_list),
        ("💰 Payments", open_payments),
        ("💵 Rent Collector", open_rent_collector),
        ("📈 Reports", open_reports_dashboard),
    ]

    for text, command in buttons_data:
        btn_frame = tk.Frame(sidebar, bg="#1e3a8a")
        btn_frame.pack(fill="x", padx=40, pady=3)

        if command is None:
            btn = tk.Label(btn_frame, text=text, font=("Segoe UI", 12, "bold"),
                          bg="#3a7be4", fg="white", padx=40, pady=8, anchor="w", cursor="hand2")
        else:
            btn = tk.Label(btn_frame, text=text, font=("Segoe UI", 12),
                          bg="#1e3a8a", fg="white", padx=40, pady=8, anchor="w", cursor="hand2")
            btn.bind("<Enter>", lambda e, b=btn_frame: b.config(bg="#2a4a9a"))
            btn.bind("<Leave>", lambda e, b=btn_frame: b.config(bg="#1e3a8a"))
            btn.bind("<Button-1>", lambda e, cmd=command: cmd())

        btn.pack(fill="x")

    
    # ===== DATABASE INFO BUTTON =====
    db_info_frame = tk.Frame(sidebar, bg="#1e3a8a")
    db_info_frame.pack(fill="x", padx=40, pady=3)

    db_info_btn = tk.Label(db_info_frame, text="🗄️Database Info", font=("Segoe UI", 11),
                          bg="#1e3a8a", fg="white", padx=40, pady=8, anchor="w", cursor="hand2")
    db_info_btn.pack(fill="x")
    db_info_btn.bind("<Enter>", lambda e: db_info_btn.config(bg="#2a4a9a"))
    db_info_btn.bind("<Leave>", lambda e: db_info_btn.config(bg="#1e3a8a"))
    db_info_btn.bind("<Button-1>", lambda e: show_database_info(dashboard))

    # Separator
    tk.Frame(sidebar, bg="white", height=2).pack(fill="x", padx=40, pady=15)

    # Exit button
    exit_frame = tk.Frame(sidebar, bg="#1e3a8a")
    exit_frame.pack(side="bottom", fill="x", padx=40, pady=15)

    exit_btn = tk.Label(exit_frame, text="🚪 Exit", font=("Segoe UI", 12, "bold"),
                       bg="#f59e0b", fg="white", padx=40, pady=8, cursor="hand2")
    exit_btn.pack(fill="x")
    exit_btn.bind("<Button-1>", lambda e: dashboard.destroy())
    exit_btn.bind("<Enter>", lambda e: exit_btn.config(bg="#000000"))
    exit_btn.bind("<Leave>", lambda e: exit_btn.config(bg="#f59e0b"))

    # ========== MAIN CONTENT WITH SCROLLBAR ==========
    main_container = tk.Frame(dashboard, bg="#f0f2f5")
    main_container.grid(row=0, column=1, sticky="nsew")
    main_container.grid_columnconfigure(0, weight=1)
    main_container.grid_rowconfigure(0, weight=1)

    canvas = tk.Canvas(main_container, bg="#f0f2f5", highlightthickness=0)
    scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f0f2f5")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    def on_closing():
        canvas.unbind_all("<MouseWheel>")
        dashboard.destroy()
    
    dashboard.protocol("WM_DELETE_WINDOW", on_closing)

    # ========== MAIN CONTENT FRAME ==========
    main_frame = tk.Frame(scrollable_frame, bg="#f0f2f5")
    main_frame.pack(fill="both", expand=True, padx=15, pady=15)

    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_rowconfigure(3, weight=1)

    # Header
    header_frame = tk.Frame(main_frame, bg="#f0f2f5")
    header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))

    icon_frame = tk.Frame(header_frame, bg="#f0f2f5")
    icon_frame.pack(side="left", padx=10)

    # Power icon
    tk.Label(icon_frame, text="⚡", font=("Segoe UI", 20, "bold"), 
            bg="#f0f2f5", fg="#f39c12").pack(side="left")

    # Company name
    tk.Label(icon_frame, text=" Powered by .ARS ", font=("Segoe UI", 18, "bold"), 
            bg="#f0f2f5", fg="#1e3a8a").pack(side="left")

    # Separator
    tk.Label(icon_frame, text="|", font=("Segoe UI", 18, "bold"), 
            bg="#f0f2f5", fg="#95a5a6").pack(side="left", padx=5)

    # Phone icon
    tk.Label(icon_frame, text="📞", font=("Segoe UI", 18), 
            bg="#f0f2f5", fg="#27ae60").pack(side="left", padx=(5,2))

    # Phone number
    tk.Label(icon_frame, text="0333-3988781", font=("Segoe UI", 18, "bold"), 
            bg="#f0f2f5", fg="#34495e").pack(side="left")

    current_date = datetime.now().strftime("%d %B %Y")
    tk.Label(header_frame, text=f"Date: {current_date}", 
             font=("Segoe UI", 11), bg="#f0f2f5", fg="#666666").pack(side="right", padx=12)

    refresh_btn = tk.Button(header_frame, text="Refresh", 
                           command=lambda: update_dashboard(),
                           bg="#254C4B", fg="white", font=("Segoe UI", 12, "bold"),
                           padx=12, pady=4, cursor="hand2")
    refresh_btn.pack(side="right", padx=10)

    # ========== STATISTICS CARDS ==========
    stats_frame = tk.Frame(main_frame, bg="#f0f2f5")
    stats_frame.grid(row=1, column=0, sticky="ew", pady=5)

    for i in range(4):
        stats_frame.grid_columnconfigure(i, weight=1)

    cards_data = [
        ("Occupied Units", "#1e3a8a", "white"),
        ("Vacant Units", "#10b981", "white"),
        ("Active Tenants", "#f59e0b", "white"),
        ("Pending Payments", "#ef4444", "white")
    ]

    value_labels = {}

    for i, (title, bg_color, fg_color) in enumerate(cards_data):
        card = tk.Frame(stats_frame, bg=bg_color, relief="raised", bd=0)
        card.grid(row=0, column=i, padx=8, pady=8, sticky="ew")
        
        inner = tk.Frame(card, bg=bg_color)
        inner.pack(fill="both", expand=True, padx=12, pady=18)

        tk.Label(inner, text=title, font=("Segoe UI", 15, "bold"), 
                bg=bg_color, fg=fg_color).pack(anchor="w")
        
        value_label = tk.Label(inner, text="0", font=("Segoe UI", 20, "bold"), 
                              bg=bg_color, fg=fg_color)
        value_label.pack(anchor="e", pady=(3, 0))

        value_labels[title] = value_label

    # ========== CHARTS SECTION ==========
    charts_frame = tk.Frame(main_frame, bg="#f0f2f5")
    charts_frame.grid(row=2, column=0, sticky="nsew", pady=10)

    for i in range(2):
        charts_frame.grid_rowconfigure(i, weight=1, minsize=250)
        for j in range(2):
            charts_frame.grid_columnconfigure(j, weight=1, minsize=320)

    chart_frames = []
    for i in range(2):
        for j in range(2):
            chart_container = tk.Frame(charts_frame, bg="white", relief="solid", bd=1)
            chart_container.grid(row=i, column=j, padx=8, pady=8, sticky="nsew")
            chart_container.grid_propagate(False)
            chart_frames.append(chart_container)

    # ========== FOOTER WITH DATABASE LOCATION ==========
    footer_frame = tk.Frame(main_frame, bg="#f0f2f5", height=50)
    footer_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
    footer_frame.grid_columnconfigure(0, weight=1)

    # Top border line
    tk.Frame(footer_frame, bg="#cccccc", height=1).pack(fill="x", pady=(0, 8))

    # Footer content frame
    footer_content = tk.Frame(footer_frame, bg="#f0f2f5")
    footer_content.pack()

    # Left side - Copyright
    tk.Label(footer_content, text="©", font=("Segoe UI", 10, "bold"),
             bg="#f0f2f5", fg="#1e3a8a").pack(side="left", padx=(0, 5))

    current_year = datetime.now().year
    tk.Label(footer_content, text=f"{current_year} .ARS", 
             font=("Segoe UI", 9), bg="#f0f2f5", fg="#34495e").pack(side="left")

    # Separator
    tk.Label(footer_content, text="|", font=("Segoe UI", 12, "bold"),
             bg="#f0f2f5", fg="#95a5a6").pack(side="left", padx=8)

    # Database Location with Icon
    db_location = DATABASE_NAME
    drive_letter = os.path.splitdrive(db_location)[0]

    # Choose icon based on drive
    if drive_letter.upper() == 'C:':
        drive_icon = "💻"  # System drive
    else:
        drive_icon = "💾"  # Data drive

    tk.Label(footer_content, text=drive_icon, font=("Segoe UI", 10),
             bg="#f0f2f5", fg="#f39c12").pack(side="left", padx=(0, 2))
    
    # Show only drive and folder name
    db_short = os.path.dirname(db_location)
    if len(db_short) > 40:
        db_short = "..." + db_short[-40:]
    
    tk.Label(footer_content, text=f"Data: {db_short}", 
             font=("Segoe UI", 8), bg="#f0f2f5", fg="#666666").pack(side="left")

    # Separator
    tk.Label(footer_content, text="|", font=("Segoe UI", 12, "bold"),
             bg="#f0f2f5", fg="#95a5a6").pack(side="left", padx=8)

    # Contact
    tk.Label(footer_content, text="📞", font=("Segoe UI", 10),
             bg="#f0f2f5", fg="#27ae60").pack(side="left")
    tk.Label(footer_content, text="0333-3988781", font=("Segoe UI", 9),
             bg="#f0f2f5", fg="#34495e").pack(side="left", padx=(2, 0))

    # Version
    tk.Label(footer_content, text="v1.0.0", font=("Segoe UI", 8, "italic"),
             bg="#f0f2f5", fg="#95a5a6").pack(side="left", padx=(10, 0))

    # ========== FUNCTIONS ==========
    def get_pending_payments_count():
        conn = get_connection()
        c = conn.cursor()

        # Saare tenants check karo
        c.execute("SELECT COUNT(*) FROM tenants WHERE status='Active'")
        total_active_tenants = c.fetchone()[0] or 0

        # Saare paid payments count karo
        c.execute("SELECT COUNT(DISTINCT tenant_id) FROM payments WHERE status='Paid'")
        total_paid_tenants = c.fetchone()[0] or 0

        # Pending = active tenants - paid tenants
        total_pending = total_active_tenants - total_paid_tenants

        conn.close()
        return total_pending

    def get_chart_data():
        conn = get_connection()
        c = conn.cursor()

        # Total active tenants
        c.execute("SELECT COUNT(*) FROM tenants WHERE status='Active'")
        active = c.fetchone()[0] or 0

        # Total tenants who have paid at least once (any month)
        c.execute("SELECT COUNT(DISTINCT tenant_id) FROM payments WHERE status='Paid'")
        paid = c.fetchone()[0] or 0

        # Pending tenants = Active - Paid
        pending = active - paid

        # Top Buildings Collection
        c.execute("""
            SELECT 
                t.building_name, 
                COALESCE(SUM(p.paid_amount), 0) as total_collected
            FROM tenants t
            LEFT JOIN payments p ON p.tenant_id = t.id
            WHERE t.status = 'Active'
            GROUP BY t.building_name
            ORDER BY total_collected DESC
            LIMIT 5
        """)
        
        building_data = []
        for row in c.fetchall():
            name = row[0]
            amount = row[1] or 0
            name = ' '.join(name.split())
            building_data.append((name, amount))

        # Trend data last 6 months
        trend_data = []
        today = datetime.now()
        for i in range(5, -1, -1):
            date = today - relativedelta(months=i)
            month = date.strftime("%B")
            year = date.year
            month_year = f"{month}-{year}"

            c.execute("SELECT SUM(paid_amount) FROM payments WHERE month_year=?", (month_year,))
            total = c.fetchone()[0] or 0
            trend_data.append((month[:3], total))

        conn.close()
        return {
            'active': active,
            'paid': paid,
            'pending': pending,
            'building_data': building_data,
            'trend_data': trend_data
        }

    def create_charts():
        data = get_chart_data()
        
        for frame in chart_frames:
            for widget in frame.winfo_children():
                widget.destroy()

        # Chart 1: Paid vs Pending (Pie Chart)
        fig1 = Figure(figsize=(4.5, 3.2), dpi=100, facecolor='white')
        ax1 = fig1.add_subplot(111)
        
        total_tenants = data['paid'] + data['pending']
        if total_tenants > 0:
            labels = ['Paid', 'Pending']
            sizes = [data['paid'], data['pending']]
            colors = ["#F88132", "#A59D84"]
            wedges, texts, autotexts = ax1.pie(
                sizes, labels=labels, colors=colors, autopct='%1.1f%%', 
                startangle=90, textprops={'fontsize': 10}, radius=0.9
            )
            for autotext in autotexts:
                autotext.set_fontweight('bold')
                autotext.set_fontsize(10)
        else:
            ax1.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=10)
        
        ax1.set_title(f'Payment Status - {datetime.now().strftime("%B %Y")}', 
                    fontsize=10, fontweight='bold', pad=8)

        canvas1 = FigureCanvasTkAgg(fig1, chart_frames[0])
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, padx=3, pady=3)

        # Chart 2: Top Buildings Collection (Vertical Bar Chart)
        fig2 = Figure(figsize=(4.5, 3.2), dpi=100, facecolor='white')
        ax2 = fig2.add_subplot(111)

        if data['building_data']:
            buildings = []
            amounts = []
            
            for name, amount in data['building_data']:
                # Shorten long building names
                if len(name) > 15:
                    words = name.split()
                    if len(words) > 1:
                        # Take first few letters only
                        name = words[0][:10] + '...' if len(words[0]) > 10 else words[0] + '...'
                    else:
                        name = name[:12] + '...'
                buildings.append(name)
                amounts.append(amount)
            
            # Beautiful color palette
            colors = ["#f59e0b", "#2AC2B8", "#0F07F1", "#01572F", '#FFEAA7']
            
            # Create vertical bar chart
            x_pos = range(len(buildings))
            bars = ax2.bar(x_pos, amounts, color=colors[:len(buildings)], width=0.6)
            
            # Set labels
            ax2.set_xticks(x_pos)
            ax2.set_xticklabels(buildings, fontsize=9, rotation=15, ha='right')
            ax2.set_ylabel('Collection (Rs)', fontsize=9)
            ax2.set_title('Top Buildings Collection', fontsize=11, fontweight='bold', pad=10)
            
            # Add value labels on top of bars
            for i, (bar, amount) in enumerate(zip(bars, amounts)):
                if amount > 0:
                    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (max(amounts)*0.02), 
                            f'Rs {amount:,.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold')
                else:
                    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500, 
                            'Rs 0', ha='center', va='bottom', fontsize=8, fontweight='bold', color='gray')
            
            # Set y-axis limit
            if max(amounts) > 0:
                ax2.set_ylim(0, max(amounts) * 1.15)
            else:
                ax2.set_ylim(0, 10000)
            
            ax2.tick_params(axis='both', labelsize=8)
            ax2.grid(True, axis='y', alpha=0.3, linestyle='--')
            
            # Add subtle background color
            ax2.set_facecolor('#f8fafc')
            
        else:
            ax2.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=12, 
                    transform=ax2.transAxes, fontweight='bold')
            ax2.set_title('Top Buildings Collection', fontsize=11, fontweight='bold', pad=10)
            ax2.set_facecolor('#f8fafc')

        fig2.tight_layout(pad=2.0)
        canvas2 = FigureCanvasTkAgg(fig2, chart_frames[1])
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, padx=5, pady=5)
        
        # Chart 3: Monthly Trend (Line Chart)
        fig3 = Figure(figsize=(4.5, 3.2), dpi=100, facecolor='white')
        ax3 = fig3.add_subplot(111)
        
        if data['trend_data'] and any(d[1] > 0 for d in data['trend_data']):
            months = [d[0] for d in data['trend_data']]
            amounts = [d[1] for d in data['trend_data']]
            
            ax3.plot(months, amounts, marker='o', linewidth=1.5, markersize=4, color='#f59e0b')
            ax3.fill_between(months, amounts, alpha=0.1, color='#f59e0b')
            ax3.set_ylabel('Collection (Rs)', fontsize=8)
            ax3.set_title('6-Month Collection Trend', fontsize=10, fontweight='bold', pad=8)
            ax3.tick_params(axis='x', rotation=45, labelsize=7)
            ax3.tick_params(axis='y', labelsize=7)
            ax3.grid(True, alpha=0.2, linestyle='--')
            
            for i, (month, amount) in enumerate(zip(months, amounts)):
                if amount > 0:
                    ax3.annotate(f'{amount:,.0f}', (month, amount), 
                            textcoords="offset points", xytext=(0, 5), 
                            ha='center', fontsize=6, fontweight='bold')
        else:
            ax3.text(0.5, 0.5, 'No Data', ha='center', va='center', fontsize=10)
            ax3.set_title('6-Month Collection Trend', fontsize=10, fontweight='bold', pad=8)

        fig3.tight_layout(pad=1.5)
        canvas3 = FigureCanvasTkAgg(fig3, chart_frames[2])
        canvas3.draw()
        canvas3.get_tk_widget().pack(fill="both", expand=True, padx=3, pady=3)

        # ================= UPDATED SUMMARY CARD =================
        # destroy old chart
        for widget in chart_frames[3].winfo_children():
            widget.destroy()

        fig4 = Figure(figsize=(4.5, 3.2), dpi=100, facecolor='white')
        ax4 = fig4.add_subplot(111)
        ax4.axis('off')

        conn = get_connection()
        c = conn.cursor()

        # Total rent of all active tenants
        c.execute("SELECT SUM(rent_amount) FROM tenants WHERE status='Active'")
        total_rent = c.fetchone()[0] or 0

        # Total collected amount
        c.execute("SELECT SUM(paid_amount) FROM payments")
        collected = c.fetchone()[0] or 0

        # Collection rate
        collection_rate = (collected / total_rent * 100) if total_rent > 0 else 0

        # Active tenants count
        c.execute("SELECT COUNT(*) FROM tenants WHERE status='Active'")
        active = c.fetchone()[0]

        # Tenants who have paid at least once
        c.execute("SELECT COUNT(DISTINCT tenant_id) FROM payments")
        paid = c.fetchone()[0]

        # Pending tenants
        pending = active - paid

        conn.close()

        # ================= DRAW SUMMARY CARD =================
        summary_lines = [
            ("SUMMARY", 12, 'bold'),
            ("", 0, ''),
            (f"Total Rent: Rs {total_rent:,.0f}", 9, 'normal'),
            (f"Collected: Rs {collected:,.0f}", 9, 'normal'),
            (f"Collection Rate: {collection_rate:.1f}%", 9, 'bold'),
            ("", 0, ''),
            (f"Active Tenants: {active}", 9, 'normal'),
            (f"Paid Tenants: {paid}", 9, 'normal'),
            (f"Pending: {pending}", 9, 'bold'),
        ]

        y_pos = 0.9
        for line, size, weight in summary_lines:
            if line:
                ax4.text(0.1, y_pos, line, transform=ax4.transAxes,
                        fontsize=size, fontweight=weight, verticalalignment='top',
                        fontfamily='sans-serif')
            y_pos -= 0.08

        # Embed in Tkinter
        canvas4 = FigureCanvasTkAgg(fig4, chart_frames[3])
        canvas4.draw()
        canvas4.get_tk_widget().pack(fill="both", expand=True, padx=3, pady=3)


    def update_dashboard():
        total_flats, occupied, vacant, active_tenants = get_counts()
        pending_count = get_pending_payments_count()
        
        value_labels["Occupied Units"].config(text=str(occupied))
        value_labels["Vacant Units"].config(text=str(vacant))
        value_labels["Active Tenants"].config(text=str(active_tenants))
        value_labels["Pending Payments"].config(text=str(pending_count))
        
        create_charts()

    update_dashboard()
    return dashboard

# ========== DATABASE INFO FUNCTIONS ==========
def show_database_info(parent):
    """Show database information dialog"""
    
    info_window = tk.Toplevel(parent)
    info_window.title("Database Information")
    info_window.geometry("550x450")
    info_window.config(bg="#ffffff")
    info_window.transient(parent)
    info_window.grab_set()
    
    # Center window
    info_window.update_idletasks()
    x = (info_window.winfo_screenwidth() // 2) - (550 // 2)
    y = (info_window.winfo_screenheight() // 2) - (450 // 2)
    info_window.geometry(f'550x450+{x}+{y}')
    
    # Title
    tk.Label(info_window, text="📁 Database Information", 
             font=("Segoe UI", 18, "bold"), bg="#ffffff", 
             fg="#1e3a8a").pack(pady=20)
    
    # Main info frame
    main_frame = tk.Frame(info_window, bg="#f8fafc", relief="solid", bd=1)
    main_frame.pack(fill="both", expand=True, padx=30, pady=10)
    
    # Database path (full)
    tk.Label(main_frame, text="Full Path:", 
             font=("Segoe UI", 11, "bold"), bg="#f8fafc", 
             anchor="w").pack(anchor="w", padx=20, pady=(15,5))
    
    path_label = tk.Label(main_frame, text=DATABASE_NAME, 
                          font=("Segoe UI", 9), bg="#f8fafc", 
                          fg="#1e3a8a", wraplength=450, justify="left")
    path_label.pack(anchor="w", padx=20, pady=5)
    
    # Separator
    tk.Frame(main_frame, bg="#cccccc", height=1).pack(fill="x", padx=20, pady=10)
    
    # Drive info
    db_drive = os.path.splitdrive(DATABASE_NAME)[0]
    
    info_grid = tk.Frame(main_frame, bg="#f8fafc")
    info_grid.pack(fill="x", padx=20, pady=5)
    
    # Drive
    tk.Label(info_grid, text="💽 Drive:", font=("Segoe UI", 11, "bold"),
             bg="#f8fafc").grid(row=0, column=0, sticky="w", pady=5)
    tk.Label(info_grid, text=db_drive, font=("Segoe UI", 11),
             bg="#f8fafc", fg="#34495e").grid(row=0, column=1, sticky="w", padx=20)
    
    # Free space
    free_space = get_free_space(db_drive)
    if free_space:
        tk.Label(info_grid, text="💾 Free Space:", font=("Segoe UI", 11, "bold"),
                 bg="#f8fafc").grid(row=1, column=0, sticky="w", pady=5)
        
        color = "#27ae60" if free_space > 10 else "#e67e22"
        tk.Label(info_grid, text=f"{free_space:.2f} GB", font=("Segoe UI", 11),
                 bg="#f8fafc", fg=color).grid(row=1, column=1, sticky="w", padx=20)
    
    # Folder name
    folder_name = os.path.basename(os.path.dirname(DATABASE_NAME))
    tk.Label(info_grid, text="📂 Folder:", font=("Segoe UI", 11, "bold"),
             bg="#f8fafc").grid(row=2, column=0, sticky="w", pady=5)
    tk.Label(info_grid, text=folder_name, font=("Segoe UI", 11),
             bg="#f8fafc", fg="#34495e").grid(row=2, column=1, sticky="w", padx=20)
    
    # Database file
    db_file = os.path.basename(DATABASE_NAME)
    tk.Label(info_grid, text="📄 File:", font=("Segoe UI", 11, "bold"),
             bg="#f8fafc").grid(row=3, column=0, sticky="w", pady=5)
    tk.Label(info_grid, text=db_file, font=("Segoe UI", 11),
             bg="#f8fafc", fg="#34495e").grid(row=3, column=1, sticky="w", padx=20)
    
    # Separator
    tk.Frame(main_frame, bg="#cccccc", height=1).pack(fill="x", padx=20, pady=15)
    
    # Available drives
    tk.Label(main_frame, text="🖥️ Available Drives:", font=("Segoe UI", 11, "bold"),
             bg="#f8fafc", anchor="w").pack(anchor="w", padx=20, pady=5)
    
    drives = get_available_drives()
    drives_frame = tk.Frame(main_frame, bg="#f8fafc")
    drives_frame.pack(fill="x", padx=20, pady=5)
    
    for i, drive in enumerate(drives):
        # Highlight current drive
        if drive == db_drive:
            fg_color = "#1e3a8a"
            font_bold = ("Segoe UI", 10, "bold")
        else:
            fg_color = "#666666"
            font_bold = ("Segoe UI", 10)
        
        tk.Label(drives_frame, text=drive, font=font_bold,
                 bg="#f8fafc", fg=fg_color).grid(row=0, column=i, padx=5)
    
    # Buttons
    btn_frame = tk.Frame(info_window, bg="#ffffff")
    btn_frame.pack(pady=20)
    
    tk.Button(btn_frame, text="📂 Open Folder", 
              command=lambda: open_folder(DATABASE_NAME),
              bg="#1e3a8a", fg="white", font=("Segoe UI", 11, "bold"),
              width=15, cursor="hand2").pack(side="left", padx=5)
    
    tk.Button(btn_frame, text="❌ Close", 
              command=info_window.destroy,
              bg="#f97316", fg="white", font=("Segoe UI", 11, "bold"),
              width=15, cursor="hand2").pack(side="left", padx=5)

def open_folder(path):
    """Open folder in Windows Explorer"""
    try:
        folder = os.path.dirname(path)
        subprocess.Popen(f'explorer "{folder}"')
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open folder: {e}")


