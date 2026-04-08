import flet as ft
import httpx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import tempfile
import os

BASE_URL = "http://127.0.0.1:8000"

# ─────────────────────────────────────────
#  API Helpers
# ─────────────────────────────────────────
def fetch_employees():
    try:
        r = httpx.get(f"{BASE_URL}/employees", timeout=5)
        return r.json()
    except Exception:
        return []

def fetch_summary():
    try:
        r = httpx.get(f"{BASE_URL}/sales/summary", timeout=5)
        return r.json()
    except Exception:
        return []

def fetch_daily_sales():
    try:
        r = httpx.get(f"{BASE_URL}/sales/daily", timeout=5)
        return r.json()
    except Exception:
        return []

def fetch_monthly_sales():
    try:
        r = httpx.get(f"{BASE_URL}/sales/monthly", timeout=5)
        return r.json()
    except Exception:
        return []

def fetch_yearly_sales():
    try:
        r = httpx.get(f"{BASE_URL}/sales/yearly", timeout=5)
        return r.json()
    except Exception:
        return []

def post_sale(employee_id: int, amount: float):
    try:
        r = httpx.post(f"{BASE_URL}/sales",
                       json={"employee_id": employee_id, "amount": amount},
                       timeout=5)
        return r.status_code == 200
    except Exception:
        return False


# ─────────────────────────────────────────
#  Light Theme Colors
# ─────────────────────────────────────────
BG      = "#F0F4FF"
SURFACE = "#FFFFFF"
CARD    = "#FFFFFF"
MUTED   = "#F1F5F9"
BORDER  = "#E2E8F0"

ACCENT  = "#4361EE"
ACCENT2 = "#7B2FBE"
SUCCESS = "#06D6A0"
WARNING = "#FFB703"
DANGER  = "#EF476F"
ORANGE  = "#FB8500"

TEXT    = "#1A1A2E"
SUBTEXT = "#6B7280"

NAV_ACTIVE_BG   = "#EEF2FF"
NAV_ACTIVE_TEXT = "#4361EE"


# ─────────────────────────────────────────
#  Reusable Components
# ─────────────────────────────────────────
def ltext(value, size=14, color=TEXT, weight=None, italic=False):
    return ft.Text(value, size=size, color=color,
                   weight=weight or ft.FontWeight.NORMAL, italic=italic)

def card(content, padding=20):
    return ft.Container(
        content=content, bgcolor=CARD, border_radius=16, padding=padding,
        border=ft.Border.all(1, BORDER),
        shadow=ft.BoxShadow(blur_radius=8, color="#0A000000", offset=ft.Offset(0, 2)),
    )

def field(label, password=False, hint="", ref=None, on_change=None):
    return ft.TextField(
        label=label, password=password, can_reveal_password=password,
        hint_text=hint, ref=ref, on_change=on_change,
        bgcolor=MUTED, border_color=BORDER, focused_border_color=ACCENT,
        color=TEXT, label_style=ft.TextStyle(color=SUBTEXT),
        border_radius=10, height=60,
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=22),
    )

def primary_btn(text, on_click, expand=False, color=ACCENT):
    return ft.Button(
        text, on_click=on_click, expand=expand,
        style=ft.ButtonStyle(
            bgcolor=color, color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding.symmetric(horizontal=24, vertical=22),
            elevation=0,
        ),
    )

def kpi_card(label, value, icon, icon_bg, icon_color):
    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Icon(icon, color=icon_color, size=20),
                    bgcolor=icon_bg, border_radius=10, padding=10,
                ),
            ]),
            ft.Container(height=14),
            ltext(value, size=22, weight=ft.FontWeight.BOLD, color=TEXT),
            ft.Container(height=4),
            ltext(label, size=12, color=SUBTEXT),
        ], spacing=0),
        bgcolor=CARD, border_radius=16, padding=20,
        border=ft.Border.all(1, BORDER),
        shadow=ft.BoxShadow(blur_radius=8, color="#0A000000", offset=ft.Offset(0, 2)),
        expand=True,
    )


# ─────────────────────────────────────────
#  PAGE 1 — Login
# ─────────────────────────────────────────
def login_page(page: ft.Page, go_to):
    username_ref = ft.Ref[ft.TextField]()
    password_ref = ft.Ref[ft.TextField]()
    error_ref    = ft.Ref[ft.Text]()

    def on_login(e):
        u = username_ref.current.value.strip()
        p = password_ref.current.value.strip()
        if u == "admin" and p == "1234":
            go_to("dashboard")
        else:
            error_ref.current.value = "⚠ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
            error_ref.current.update()

    left_panel = ft.Container(
        content=ft.Column([
            ft.Container(expand=True),
            ft.Container(
                content=ft.Icon(ft.Icons.INSIGHTS, color="#FFFFFF", size=36),
                bgcolor="#FFFFFF30", border_radius=16, padding=16,
            ),
            ft.Container(height=20),
            ft.Text("SalesTrack", size=34, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
            ft.Container(height=10),
            ft.Text("ระบบบันทึกยอดขายพนักงาน\nติดตามผลและคอมมิชชันได้ทันที",
                    size=14, color="#FFFFFFCC", text_align=ft.TextAlign.CENTER),
            ft.Container(expand=True),
            ft.Text("© 2025 SalesTrack", size=11, color="#FFFFFF66",
                    text_align=ft.TextAlign.CENTER),
            ft.Container(height=20),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, -1), end=ft.Alignment(1, 1),
            colors=[ACCENT, ACCENT2],
        ),
        expand=True, padding=40,
    )

    right_panel = ft.Container(
        content=ft.Column([
            ft.Container(expand=True),
            ltext("ยินดีต้อนรับ 👋", size=26, weight=ft.FontWeight.BOLD),
            ft.Container(height=6),
            ltext("กรุณาเข้าสู่ระบบเพื่อดำเนินการต่อ", size=13, color=SUBTEXT),
            ft.Container(height=32),
            field("ชื่อผู้ใช้", hint="admin", ref=username_ref),
            ft.Container(height=14),
            field("รหัสผ่าน", password=True, hint="••••", ref=password_ref),
            ft.Container(height=8),
            ft.Text("", ref=error_ref, color=DANGER, size=12),
            ft.Container(height=16),
            primary_btn("เข้าสู่ระบบ", on_click=on_login, expand=False),
            ft.Container(height=8),
            ltext("demo: admin / 1234", size=11, color=SUBTEXT, italic=True),
            ft.Container(expand=True),
        ], horizontal_alignment=ft.CrossAxisAlignment.STRETCH, spacing=0),
        bgcolor=SURFACE, expand=True,
        padding=ft.Padding.symmetric(horizontal=48, vertical=32),
    )

    return ft.Row([left_panel, right_panel], expand=True, spacing=0)


# ─────────────────────────────────────────
#  PAGE 2 — บันทึกยอดขายรายวัน
# ─────────────────────────────────────────
def sales_page(page: ft.Page, go_to):
    all_employees  = fetch_employees()
    summary        = fetch_summary()
    selected_emp   = {"id": None, "name": ""}
    emp_list_col   = ft.Column(spacing=6, scroll=ft.ScrollMode.AUTO, height=240)
    selected_label = ft.Ref[ft.Text]()
    amount_ref     = ft.Ref[ft.TextField]()
    status_ref     = ft.Ref[ft.Text]()
    show_all_ref   = ft.Ref[ft.Container]()
    
    display_state = {"show_all": False}
    
    search_tf      = ft.TextField(
        hint_text="🔍 ค้นหาพนักงาน...",
        bgcolor=MUTED, border_color=BORDER, focused_border_color=ACCENT,
        color=TEXT, border_radius=10, height=50,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=14),
    )

    def build_list(keyword="", silent=False):
        keyword = keyword.lower()
        filtered = [e for e in all_employees
                    if keyword in e["name"].lower()] if keyword else all_employees
        emp_list_col.controls.clear()
        
        limit = len(filtered) if display_state["show_all"] else 10
        for i, emp in enumerate(filtered[:limit]):
            eid, name = emp["employee_id"], emp["name"]
            is_sel = selected_emp["id"] == eid
            def make_click(i, n):
                def on_pick(e):
                    selected_emp["id"]   = i
                    selected_emp["name"] = n
                    selected_label.current.value = f"✓ เลือก: {n}"
                    selected_label.current.color = SUCCESS
                    if selected_label.current.page:
                        selected_label.current.update()
                    build_list(search_tf.value or "")
                return on_pick
            emp_list_col.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Text(name[0], color="#FFFFFF", size=12,
                                            weight=ft.FontWeight.BOLD),
                            bgcolor=ACCENT if is_sel else "#CBD5E1",
                            border_radius=20, width=30, height=30,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ltext(name, size=13,
                              color=NAV_ACTIVE_TEXT if is_sel else TEXT,
                              weight=ft.FontWeight.W_600 if is_sel else ft.FontWeight.NORMAL),
                    ], spacing=10),
                    bgcolor=NAV_ACTIVE_BG if is_sel else SURFACE,
                    border_radius=8,
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    border=ft.Border.all(1, ACCENT if is_sel else BORDER),
                    on_click=make_click(eid, name), ink=True,
                )
            )
        
        if len(filtered) > 10:
            def toggle_view(e):
                display_state["show_all"] = not display_state["show_all"]
                build_list(keyword)
            
            btn_text = "ย่อกลับ" if display_state["show_all"] else "ดูเพิ่มเติม"
            emp_list_col.controls.append(
                ft.Container(height=8)
            )
            emp_list_col.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.EXPAND_MORE if not display_state["show_all"] else ft.Icons.EXPAND_LESS, 
                               color=ACCENT, size=16),
                        ltext(btn_text, size=12, color=ACCENT, weight=ft.FontWeight.W_600),
                    ], spacing=6),
                    on_click=toggle_view, ink=True, border_radius=8,
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                )
            )
        
        if not silent and emp_list_col.page:
            emp_list_col.update()

    def on_search(e):
        build_list(e.control.value)

    search_tf.on_change = on_search

    def on_submit(e):
        if not selected_emp["id"]:
            status_ref.current.value = "⚠ กรุณาเลือกพนักงาน"
            status_ref.current.color = DANGER
            if status_ref.current.page:
                status_ref.current.update()
            return
        try:
            amount = float(amount_ref.current.value)
        except (ValueError, TypeError):
            status_ref.current.value = "⚠ ยอดขายต้องเป็นตัวเลข"
            status_ref.current.color = DANGER
            if status_ref.current.page:
                status_ref.current.update()
            return
        ok = post_sale(selected_emp["id"], amount)
        if ok:
            status_ref.current.value     = f"✓ บันทึก ฿{amount:,.0f} ให้ {selected_emp['name']} สำเร็จ!"
            status_ref.current.color     = SUCCESS
            amount_ref.current.value     = ""
            selected_emp["id"]           = None
            selected_emp["name"]         = ""
            selected_label.current.value = "ยังไม่ได้เลือกพนักงาน"
            selected_label.current.color = SUBTEXT
            if selected_label.current.page:
                selected_label.current.update()
            if amount_ref.current.page:
                amount_ref.current.update()
            build_list(silent=False)
        else:
            status_ref.current.value = "❌ เกิดข้อผิดพลาด กรุณาลองใหม่"
            status_ref.current.color = DANGER
        if status_ref.current.page:
            status_ref.current.update()

    build_list(silent=True)
    
    total_sales = sum(r.get("total_sales", 0) or 0 for r in summary)
    total_comm  = sum(r.get("commission", 0) or 0 for r in summary)
    emp_count   = len(all_employees)

    return ft.Column([
        ltext("บันทึกยอดขายรายวัน", size=22, weight=ft.FontWeight.BOLD),
        ft.Container(height=4),
        ltext("เพิ่มข้อมูลยอดขายของพนักงาน", size=13, color=SUBTEXT),
        ft.Container(height=20),
        ft.Row([
            kpi_card("ยอดขายรวม (บาท)", f"฿{total_sales:,.0f}",
                     ft.Icons.TRENDING_UP, "#DBEAFE", "#2563EB"),
            kpi_card("คอมมิชชันรวม (บาท)", f"฿{total_comm:,.0f}",
                     ft.Icons.CARD_GIFTCARD, "#EDE9FE", "#7C3AED"),
            kpi_card("จำนวนพนักงาน", f"{emp_count} คน",
                     ft.Icons.PEOPLE, "#DCFCE7", "#16A34A"),
        ], spacing=14),
        ft.Container(height=24),
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ltext("เลือกพนักงาน", size=14, weight=ft.FontWeight.W_600),
                    ft.Container(height=10),
                    search_tf,
                    ft.Container(height=10),
                    emp_list_col,
                ], spacing=0),
                bgcolor=CARD, border_radius=16, padding=20,
                border=ft.Border.all(1, BORDER),
                shadow=ft.BoxShadow(blur_radius=8, color="#0A000000", offset=ft.Offset(0, 2)),
                expand=2,
            ),
            ft.Container(width=16),
            ft.Container(
                content=ft.Column([
                    ltext("กรอกยอดขาย", size=14, weight=ft.FontWeight.W_600),
                    ft.Container(height=12),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PERSON, color=ACCENT, size=16),
                            ft.Text("", ref=selected_label, size=13, color=SUBTEXT),
                        ], spacing=8),
                        bgcolor=MUTED, border_radius=8,
                        padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                    ),
                    ft.Container(height=12),
                    field("ยอดขาย (บาท)", hint="เช่น 5000.00", ref=amount_ref),
                    ft.Container(height=8),
                    ft.Text("", ref=status_ref, size=12),
                    ft.Container(height=16),
                    primary_btn("💾  บันทึกยอดขาย", on_click=on_submit, expand=True),
                ], spacing=0),
                bgcolor=CARD, border_radius=16, padding=20,
                border=ft.Border.all(1, BORDER),
                shadow=ft.BoxShadow(blur_radius=8, color="#0A000000", offset=ft.Offset(0, 2)),
                expand=3,
            ),
        ], spacing=0, vertical_alignment=ft.CrossAxisAlignment.START),
    ], spacing=0)


# ─────────────────────────────────────────
#  Chart Generator
# ─────────────────────────────────────────
def create_line_chart(labels, values):
    """สร้าง line chart ของยอดขายแล้วเก็บเป็น image file"""
    try:
        fig, ax = plt.subplots(figsize=(9, 4), facecolor='#FFFFFF', dpi=100)

        xs = list(range(len(labels)))  # ใช้ index เป็น x แทน string

        # Plot line with fill
        ax.plot(xs, values, marker='o', linewidth=3.5, markersize=10,
                color='#4361EE', markerfacecolor='#4361EE', markeredgecolor='white',
                markeredgewidth=2.5, zorder=3)
        ax.fill_between(xs, values, alpha=0.1, color='#4361EE', zorder=1)

        # Value labels on each point
        for i, value in enumerate(values):
            fmt = f'฿{value/1e6:.2f}M' if value >= 1e6 else f'฿{value/1e3:.0f}K'
            ax.annotate(fmt,
                        xy=(i, value), xytext=(0, 12),
                        textcoords='offset points',
                        ha='center', fontsize=9, weight='bold', color='#4361EE',
                        bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                                  edgecolor='#4361EE', linewidth=1.2))

        # X-axis: แสดง label ที่กำหนดเอง (MM-DD หรืออื่นๆ)
        ax.set_xticks(xs)
        ax.set_xticklabels(labels, fontsize=9, color='#555555')

        ax.set_ylabel('Sales (Baht)', fontsize=10, color='#666666')
        ax.set_xlabel('')
        ax.grid(True, axis='y', alpha=0.2, linestyle='--', linewidth=0.8, zorder=0)
        ax.set_facecolor('#FFFFFF')

        # Y-axis format
        max_val = max(values) * 1.25 if values else 1000
        ax.set_ylim(0, max_val)
        ax.yaxis.set_major_formatter(
            plt.FuncFormatter(lambda x, _: f'฿{x/1e6:.1f}M' if x >= 1e6 else f'฿{x/1e3:.0f}K')
        )

        # Spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#E0E0E0')
        ax.spines['bottom'].set_color('#E0E0E0')
        ax.tick_params(colors='#666666', labelsize=9)

        plt.tight_layout()

        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            tmp_path = tmp.name
            plt.savefig(tmp_path, facecolor='#FFFFFF',
                        bbox_inches='tight', pad_inches=0.2, dpi=100)
        plt.close()
        return tmp_path
    except Exception as e:
        print(f"Chart error: {e}")
        return None


# ─────────────────────────────────────────
#  PAGE 3 — Dashboard
# ─────────────────────────────────────────
def dashboard_page(page: ft.Page, go_to):
    summary     = fetch_summary()
    employees   = fetch_employees()

    total_sales = sum(r.get("total_sales", 0) or 0 for r in summary)
    total_comm  = sum(r.get("commission", 0)  or 0 for r in summary)
    top_name    = summary[0]["name"] if summary else "-"
    emp_count   = len(employees)

    kpi_row = ft.Row([
        kpi_card("ยอดขายรวม (บาท)",    f"฿{total_sales:,.0f}",
                 ft.Icons.TRENDING_UP,   "#DBEAFE", "#2563EB"),
        kpi_card("คอมมิชชันรวม (บาท)", f"฿{total_comm:,.0f}",
                 ft.Icons.CARD_GIFTCARD, "#EDE9FE", "#7C3AED"),
        kpi_card("พนักงานยอดเยี่ยม",   top_name,
                 ft.Icons.EMOJI_EVENTS,  "#FEF9C3", "#CA8A04"),
        kpi_card("จำนวนพนักงาน",        f"{emp_count} คน",
                 ft.Icons.PEOPLE,        "#DCFCE7", "#16A34A"),
    ], spacing=14)

    BAR_COLORS = [ACCENT, ACCENT2, SUCCESS, WARNING, ORANGE, DANGER]
    max_sales_val = max((r.get("total_sales", 0) or 0 for r in summary), default=1)
    emp_list_col = ft.Column(spacing=12, scroll=ft.ScrollMode.AUTO)
    search_box = ft.TextField(
        hint_text="🔍 ค้นหาชื่อพนักงาน...",
        bgcolor=MUTED, border_color=BORDER, focused_border_color=ACCENT,
        color=TEXT, border_radius=10, height=50,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=14),
    )

    dlg_detail = ft.AlertDialog(
        title=ft.Text(""),
        content=ft.Column([], scroll=ft.ScrollMode.AUTO, expand=True),
        actions=[ft.TextButton("ปิด", on_click=lambda e: close_dialog())],
    )

    def close_dialog():
        dlg_detail.open = False
        page.update()

    def show_emp_detail(emp_data):
        sales = emp_data.get("total_sales", 0) or 0
        comm = emp_data.get("commission", 0) or 0
        color_idx = summary.index(emp_data) if emp_data in summary else 0
        color = BAR_COLORS[color_idx % len(BAR_COLORS)]
        
        pct = (sales / max((r.get("total_sales", 0) or 0 for r in summary), default=1)) if summary else 0
        
        dlg_detail.title = ft.Row([
            ft.Container(
                content=ft.Text(emp_data["name"][0], color="#FFFFFF", size=12,
                                weight=ft.FontWeight.BOLD),
                bgcolor=color, border_radius=20, width=40, height=40,
                alignment=ft.Alignment.CENTER,
            ),
            ft.Column([
                ltext(emp_data["name"], size=16, weight=ft.FontWeight.BOLD),
                ltext(emp_data.get("position", "พนักงาน"), size=12, color=SUBTEXT),
            ], spacing=2, expand=True),
        ], spacing=12, alignment=ft.MainAxisAlignment.START)
        
        dlg_detail.content.controls = [
            ft.Container(height=12),
            ltext("ยอดขายรวม", size=13, weight=ft.FontWeight.W_600),
            ft.Container(height=8),
            ltext(f"฿{sales:,.0f}", size=24, weight=ft.FontWeight.BOLD, color=color),
            ft.Container(height=16),
            ltext("คอมมิชชั่น", size=13, weight=ft.FontWeight.W_600),
            ft.Container(height=8),
            ltext(f"฿{comm:,.0f}", size=24, weight=ft.FontWeight.BOLD, color=SUCCESS),
            ft.Container(height=16),
            ltext("สัดส่วนยอดขาย", size=13, weight=ft.FontWeight.W_600),
            ft.Container(height=8),
            ft.Stack([
                ft.Container(height=12, bgcolor=MUTED, border_radius=6),
                ft.Container(height=12, bgcolor=color, border_radius=6,
                             width=max(pct * 300, 8)),
            ]),
            ft.Container(height=8),
            ltext(f"{pct*100:.1f}% ของยอดขายสูงสุด", size=11, color=SUBTEXT),
        ]
        dlg_detail.open = True
        page.dialog = dlg_detail
        page.update()

    def build_emp_list(keyword="", silent=False):
        keyword_lower = keyword.lower()
        filtered = [r for r in summary if keyword_lower in r["name"].lower()] if keyword else summary
        
        emp_list_col.controls.clear()
        
        for i, r in enumerate(filtered):  # แสดงทั้งหมด ไม่จำกัด 5 คน
            color = BAR_COLORS[i % len(BAR_COLORS)]
            sales = r.get("total_sales", 0) or 0
            comm = r.get("commission", 0) or 0
            
            def make_detail_click(emp_data):
                def on_click(e):
                    show_emp_detail(emp_data)
                return on_click
            
            emp_list_col.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Text(r["name"][0], color="#FFFFFF", size=12,
                                            weight=ft.FontWeight.BOLD),
                            bgcolor=color, border_radius=20, width=36, height=36,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Column([
                            ltext(r["name"], size=13, weight=ft.FontWeight.W_600),
                            ltext(r.get("position", "พนักงาน"), size=11, color=SUBTEXT),
                        ], spacing=2, expand=True),
                        ft.Column([
                            ltext(f"฿{sales:,.0f}", size=13, weight=ft.FontWeight.BOLD),
                            ltext("ยอดขาย", size=10, color=SUBTEXT),
                        ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.END),
                        ft.Container(width=16),
                        ft.Column([
                            ltext(f"฿{comm:,.0f}", size=13, weight=ft.FontWeight.BOLD, color=SUCCESS),
                            ltext("คอมฯ", size=10, color=SUBTEXT),
                        ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.END),
                    ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=16,
                    bgcolor=CARD, border_radius=12,
                    border=ft.Border.all(1, BORDER),
                    shadow=ft.BoxShadow(blur_radius=4, color="#06000000", offset=ft.Offset(0, 1)),
                    on_click=make_detail_click(r),
                    ink=True,
                )
            )
        
        if not silent and emp_list_col.page:
            emp_list_col.update()
    
    def on_search(e):
        build_emp_list(e.control.value)
    
    search_box.on_change = on_search
    build_emp_list(silent=True)

    medals       = ["🥇", "🥈", "🥉"]
    medal_colors = ["#FEF9C3", "#F1F5F9", "#E7E1CD"]

    def leader_card(r, i):
        return ft.Container(
            content=ft.Column([
                ft.Text(medals[i], size=40),
                ft.Container(height=12),
                ltext(r["name"], size=14, weight=ft.FontWeight.BOLD),
                ft.Container(height=8),
                ltext(f"฿{r.get('total_sales', 0):,.0f}", size=16, color=SUBTEXT, weight=ft.FontWeight.BOLD),
                ft.Container(height=4),
                ltext(f"ค่าคอมฯ ฿{r.get('commission', 0):,.0f}", size=12, color=SUBTEXT),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
            bgcolor=medal_colors[i], border_radius=14, padding=20,
            border=ft.Border.all(1, BORDER),
            alignment=ft.Alignment.CENTER,
            expand=True,
            height=200,
        )

    top3_layout = []
    if summary:
        if len(summary) >= 2:
            top3_layout.append(leader_card(summary[1], 1))
        if len(summary) >= 1:
            top3_layout.append(leader_card(summary[0], 0))
        if len(summary) >= 3:
            top3_layout.append(leader_card(summary[2], 2))

    # ── Line chart setup ──
    chart_area = ft.Container(
        content=ft.Text("กำลังโหลดกราฟ...", size=12, color=SUBTEXT,
                        text_align=ft.TextAlign.CENTER),
        height=260,
        alignment=ft.Alignment.CENTER,
    )

    def load_daily_chart():
        data   = fetch_daily_sales()
        # แสดงวันที่จริง เช่น 04-01, 04-02, 04-03
        labels = [str(row["date"])[5:] for row in data]   # ตัด YYYY- ออก เหลือ MM-DD
        values = [float(row["total"]) for row in data]
        img_path = create_line_chart(labels, values)
        if img_path:
            chart_area.content = ft.Image(
                src=img_path,
                fit="fitWidth",
                expand=True,
            )
        else:
            chart_area.content = ft.Text(
                "ไม่สามารถโหลดกราฟได้ (pip install matplotlib)",
                size=12, color=DANGER,
            )
        if chart_area.page:
            chart_area.update()

    # โหลดกราฟหลังหน้าเรนเดอร์
    page.on_load = lambda e: load_daily_chart()

    return ft.Column([
        # Header
        ft.Row([
            ft.Column([
                ltext("Dashboard", size=22, weight=ft.FontWeight.BOLD),
                ltext("ภาพรวมยอดขายพนักงาน", size=13, color=SUBTEXT),
            ], spacing=2, expand=True),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.REFRESH, color=ACCENT, size=15),
                    ltext("รีเฟรช", size=12, color=ACCENT),
                ], spacing=6),
                on_click=lambda e: go_to("dashboard"),
                border_radius=8,
                padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                bgcolor=NAV_ACTIVE_BG,
                border=ft.Border.all(1, "#C7D2FE"),
                ink=True,
            ),
        ]),
        ft.Container(height=20),

        # KPI
        kpi_row,
        ft.Container(height=20),

        # Line chart card
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ltext("กราฟยอดขายรายวัน 📈", size=15, weight=ft.FontWeight.W_600),
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.REFRESH, color=ACCENT, size=14),
                            ltext("โหลดใหม่", size=11, color=ACCENT),
                        ], spacing=4),
                        on_click=lambda e: load_daily_chart(),
                        border_radius=8,
                        padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                        bgcolor=NAV_ACTIVE_BG,
                        border=ft.Border.all(1, "#C7D2FE"),
                        ink=True,
                    ),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=12),
                chart_area,
            ], spacing=0),
            bgcolor=CARD, border_radius=16, padding=20,
            border=ft.Border.all(1, BORDER),
            shadow=ft.BoxShadow(blur_radius=8, color="#0A000000", offset=ft.Offset(0, 2)),
        ),
        ft.Container(height=20),

        # Leaderboard
        ft.Container(
            content=ft.Column([
                ltext("อันดับยอดขาย 🏆", size=15, weight=ft.FontWeight.W_600),
                ft.Container(height=16),
                ft.Row(top3_layout, spacing=12,
                       vertical_alignment=ft.CrossAxisAlignment.CENTER)
                if top3_layout else ltext("ยังไม่มีข้อมูล", color=SUBTEXT),
            ], spacing=0),
            bgcolor=CARD, border_radius=16, padding=20,
            border=ft.Border.all(1, BORDER),
            shadow=ft.BoxShadow(blur_radius=8, color="#0A000000", offset=ft.Offset(0, 2)),
        ),
        ft.Container(height=20),

        # Employee list card
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ltext("ยอดขายแยกตามพนักงาน", size=15, weight=ft.FontWeight.W_600),
                    ft.Container(expand=True),
                    # ── ปุ่มดูพนักงานทั้งหมด ──
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.PEOPLE, color=ACCENT, size=14),
                            ltext("ดูพนักงานทั้งหมด", size=11, color=ACCENT,
                                  weight=ft.FontWeight.W_600),
                        ], spacing=6),
                        on_click=lambda e: go_to("all_employees"),
                        border_radius=8,
                        padding=ft.Padding.symmetric(horizontal=12, vertical=7),
                        bgcolor=NAV_ACTIVE_BG,
                        border=ft.Border.all(1, "#C7D2FE"),
                        ink=True,
                    ),
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Container(height=14),
                search_box,
                ft.Container(height=12),
                emp_list_col,
            ], spacing=0),
            bgcolor=CARD, border_radius=16, padding=20,
            border=ft.Border.all(1, BORDER),
            shadow=ft.BoxShadow(blur_radius=8, color="#0A000000", offset=ft.Offset(0, 2)),
            expand=True,
        ),
    ], spacing=0)


# ─────────────────────────────────────────
#  PAGE 3B — All Employees
# ─────────────────────────────────────────
def all_employees_page(page: ft.Page, go_to):
    summary = fetch_summary()
    list_col = ft.Column(spacing=10)
    search_box = ft.TextField(
        hint_text="🔍 ค้นหาพนักงาน...",
        bgcolor=MUTED, border_color=BORDER, focused_border_color=ACCENT,
        color=TEXT, border_radius=10, height=50,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=14),
    )

    BAR_COLORS = [ACCENT, ACCENT2, SUCCESS, WARNING, ORANGE, DANGER]

    def build_list(keyword="", silent=False):
        keyword_lower = keyword.lower()
        filtered = [r for r in summary if keyword_lower in r["name"].lower()] if keyword else summary

        list_col.controls.clear()
        for i, r in enumerate(filtered):
            color = BAR_COLORS[i % len(BAR_COLORS)]
            sales = r.get("total_sales", 0) or 0
            comm = r.get("commission", 0) or 0

            list_col.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Text(r["name"][0], color="#FFFFFF", size=12,
                                            weight=ft.FontWeight.BOLD),
                            bgcolor=color, border_radius=20, width=40, height=40,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Column([
                            ltext(r["name"], size=14, weight=ft.FontWeight.W_600),
                            ltext(r.get("position", "พนักงาน"), size=11, color=SUBTEXT),
                        ], spacing=2, expand=True),
                        ft.Column([
                            ltext(f"฿{sales:,.0f}", size=13, weight=ft.FontWeight.BOLD),
                            ltext("ยอดขาย", size=10, color=SUBTEXT),
                        ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.END),
                        ft.Container(width=16),
                        ft.Column([
                            ltext(f"฿{comm:,.0f}", size=13, weight=ft.FontWeight.BOLD, color=SUCCESS),
                            ltext("คอมฯ", size=10, color=SUBTEXT),
                        ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.END),
                    ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=16,
                    bgcolor=CARD, border_radius=12,
                    border=ft.Border.all(1, BORDER),
                    shadow=ft.BoxShadow(blur_radius=4, color="#06000000", offset=ft.Offset(0, 1)),
                )
            )

        if not silent and list_col.page:
            list_col.update()

    def on_search(e):
        build_list(e.control.value)

    search_box.on_change = on_search
    
    # เรียก build_list ครั้งแรกเพื่อโหลดข้อมูล
    keyword_lower = ""
    filtered = summary
    list_col.controls.clear()
    for i, r in enumerate(filtered):
        color = BAR_COLORS[i % len(BAR_COLORS)]
        sales = r.get("total_sales", 0) or 0
        comm = r.get("commission", 0) or 0

        list_col.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Text(r["name"][0], color="#FFFFFF", size=12,
                                        weight=ft.FontWeight.BOLD),
                        bgcolor=color, border_radius=20, width=40, height=40,
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column([
                        ltext(r["name"], size=14, weight=ft.FontWeight.W_600),
                        ltext(r.get("position", "พนักงาน"), size=11, color=SUBTEXT),
                    ], spacing=2, expand=True),
                    ft.Column([
                        ltext(f"฿{sales:,.0f}", size=13, weight=ft.FontWeight.BOLD),
                        ltext("ยอดขาย", size=10, color=SUBTEXT),
                    ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.END),
                    ft.Container(width=16),
                    ft.Column([
                        ltext(f"฿{comm:,.0f}", size=13, weight=ft.FontWeight.BOLD, color=SUCCESS),
                        ltext("คอมฯ", size=10, color=SUBTEXT),
                    ], spacing=1, horizontal_alignment=ft.CrossAxisAlignment.END),
                ], spacing=12, vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=16,
                bgcolor=CARD, border_radius=12,
                border=ft.Border.all(1, BORDER),
                shadow=ft.BoxShadow(blur_radius=4, color="#06000000", offset=ft.Offset(0, 1)),
            )
        )

    return ft.Column([
        ft.Row([
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ARROW_BACK, color=ACCENT, size=15),
                    ltext("ย้อนกลับ", size=12, color=ACCENT),
                ], spacing=6),
                on_click=lambda e: go_to("dashboard"),
                border_radius=8,
                padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                bgcolor=NAV_ACTIVE_BG,
                border=ft.Border.all(1, "#C7D2FE"),
                ink=True,
            ),
            ft.Column([
                ltext("รายชื่อพนักงาน", size=22, weight=ft.FontWeight.BOLD),
                ltext("ดูรายการพนักงานทั้งหมด", size=13, color=SUBTEXT),
            ], spacing=2, expand=True),
        ], spacing=16),
        ft.Container(height=20),
        search_box,
        ft.Container(height=20),
        ft.Container(
            content=list_col,
            expand=True,
            bgcolor=CARD, border_radius=16, padding=20,
            border=ft.Border.all(1, BORDER),
            shadow=ft.BoxShadow(blur_radius=8, color="#0A000000", offset=ft.Offset(0, 2)),
        ),
    ], spacing=0)


# ─────────────────────────────────────────
#  PAGE 4 — คอมมิชชัน
# ─────────────────────────────────────────
def commission_page(page: ft.Page, go_to):
    all_summary = fetch_summary()
    list_col    = ft.Column(spacing=10)
    search_box  = ft.TextField(
        hint_text="🔍 ค้นหาพนักงาน...",
        bgcolor=MUTED, border_color=BORDER, focused_border_color=ACCENT,
        color=TEXT, border_radius=10, height=50, expand=True,
        content_padding=ft.Padding.symmetric(horizontal=14, vertical=14),
    )

    def build_list(keyword="", silent=False):
        keyword = keyword.lower()
        data = ([r for r in all_summary if keyword in r["name"].lower()]
                if keyword else all_summary)
        list_col.controls.clear()
        if not data:
            list_col.controls.append(ltext("ไม่พบรายชื่อพนักงาน", color=SUBTEXT))
        for i, r in enumerate(data):
            medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"
            comm  = r.get("commission", 0) or 0
            sales = r.get("total_sales", 0) or 0
            rate  = (comm / sales * 100) if sales else 0
            list_col.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Text(medal, size=16),
                            width=40, alignment=ft.Alignment.CENTER,
                        ),
                        ft.Container(width=8),
                        ft.Column([
                            ltext(r["name"], size=14, weight=ft.FontWeight.W_600),
                            ltext(r.get("position", "พนักงาน"), size=11, color=SUBTEXT),
                        ], spacing=2, expand=True),
                        ft.Column([
                            ltext(f"฿{sales:,.0f}", size=13),
                            ltext(f"อัตรา {rate:.1f}%", size=11, color=SUBTEXT),
                        ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END),
                        ft.Container(width=16),
                        ft.Container(
                            content=ltext(f"฿{comm:,.0f}", size=14,
                                          weight=ft.FontWeight.BOLD, color="#059669"),
                            bgcolor="#ECFDF5", border_radius=8,
                            padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                            border=ft.Border.all(1, "#A7F3D0"),
                        ),
                    ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                    bgcolor=CARD, border_radius=12,
                    padding=ft.Padding.symmetric(horizontal=16, vertical=14),
                    border=ft.Border.all(1, BORDER),
                    shadow=ft.BoxShadow(blur_radius=4, color="#06000000",
                                        offset=ft.Offset(0, 1)),
                )
            )
        if not silent and list_col.page:
            list_col.update()

    def on_search(e):
        build_list(e.control.value)

    search_box.on_change = on_search

    total_comm  = sum(r.get("commission", 0) or 0 for r in all_summary)
    total_sales = sum(r.get("total_sales", 0) or 0 for r in all_summary)

    build_list(silent=True)

    return ft.Column([
        ltext("คำนวณคอมมิชชัน", size=22, weight=ft.FontWeight.BOLD),
        ft.Container(height=4),
        ltext("คอมมิชชัน = ยอดขายรวม × อัตราค่าคอมมิชชัน", size=13, color=SUBTEXT),
        ft.Container(height=20),
        ft.Container(
            content=ft.Row([
                ft.Column([
                    ltext("คอมมิชชันรวมทั้งหมด", size=12, color="#FFFFFF99"),
                    ltext(f"฿{total_comm:,.0f}", size=22,
                          weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                ], spacing=2, expand=True),
                ft.Column([
                    ltext("ยอดขายรวมทั้งหมด", size=12, color="#FFFFFF99"),
                    ltext(f"฿{total_sales:,.0f}", size=22,
                          weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                ], spacing=2),
            ]),
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, 0), end=ft.Alignment(1, 0),
                colors=[ACCENT, ACCENT2],
            ),
            border_radius=16,
            padding=ft.Padding.symmetric(horizontal=24, vertical=20),
        ),
        ft.Container(height=20),
        ft.Container(
            content=ft.Column([
                ft.Row([
                    ltext("รายละเอียดคอมมิชชัน", size=15,
                          weight=ft.FontWeight.W_600),
                    ft.Container(expand=True),
                    search_box,
                ], vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=12),
                ft.Container(height=14),
                list_col,
            ], spacing=0),
            bgcolor=CARD, border_radius=16, padding=20,
            border=ft.Border.all(1, BORDER),
            shadow=ft.BoxShadow(blur_radius=8, color="#0A000000", offset=ft.Offset(0, 2)),
        ),
    ], spacing=0)


# ─────────────────────────────────────────
#  SHELL — Sidebar + Router
# ─────────────────────────────────────────
def main(page: ft.Page):
    page.title         = "SalesTrack"
    page.bgcolor       = BG
    page.padding       = 0
    page.theme_mode    = ft.ThemeMode.LIGHT
    page.window_width  = 1020
    page.window_height = 680

    PAGES = {
        "dashboard":      ("Dashboard",     ft.Icons.DASHBOARD,  dashboard_page),
        "sales":          ("บันทึกยอดขาย", ft.Icons.ADD_CHART,  sales_page),
        "commission":     ("คอมมิชชัน",    ft.Icons.PAYMENTS,   commission_page),
        "all_employees":  ("รายชื่อพนักงาน", None, all_employees_page),
    }

    nav_refs    = {k: ft.Ref[ft.Container]() for k in PAGES if PAGES[k][1] is not None}
    content_col = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

    def render_page(route):
        for k, ref in nav_refs.items():
            if ref.current:
                is_active = k == route
                ref.current.bgcolor = NAV_ACTIVE_BG if is_active else "transparent"
                row = ref.current.content
                row.controls[0].color = NAV_ACTIVE_TEXT if is_active else SUBTEXT
                row.controls[1].color = NAV_ACTIVE_TEXT if is_active else TEXT
                ref.current.update()
        fn   = PAGES[route][2]
        view = fn(page, go_to=render_page)
        content_col.controls = [
            ft.Container(content=view, padding=ft.Padding.all(28), expand=True)
        ]
        content_col.update()

    def nav_item(route, label, icon):
        def on_click(e):
            render_page(route)
        return ft.Container(
            ref=nav_refs[route],
            content=ft.Row([
                ft.Icon(icon, color=SUBTEXT, size=19),
                ft.Text(label, size=13, color=TEXT),
            ], spacing=12),
            padding=ft.Padding.symmetric(horizontal=14, vertical=11),
            border_radius=10, on_click=on_click,
            bgcolor="transparent", ink=True,
        )

    def go_to_login():
        page.controls.clear()
        page.controls.append(login_view)
        page.update()

    sidebar = ft.Container(
        content=ft.Column([
            ft.Container(height=24),
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.INSIGHTS, color="#FFFFFF", size=18),
                    bgcolor=ACCENT, border_radius=10, padding=8,
                ),
                ft.Text("SalesTrack", size=16, weight=ft.FontWeight.BOLD, color=TEXT),
            ], spacing=10),
            ft.Container(height=6),
            ltext("ระบบจัดการยอดขาย", size=11, color=SUBTEXT, italic=True),
            ft.Container(height=20),
            ft.Divider(color=BORDER, height=1),
            ft.Container(height=12),
            ltext("เมนูหลัก", size=10, color=SUBTEXT),
            ft.Container(height=8),
            *[nav_item(r, PAGES[r][0], PAGES[r][1]) for r in PAGES if PAGES[r][1] is not None],
            ft.Container(expand=True),
            ft.Divider(color=BORDER, height=1),
            ft.Container(height=8),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.LOGOUT, color=DANGER, size=17),
                    ltext("ออกจากระบบ", size=12, color=DANGER),
                ], spacing=8),
                on_click=lambda e: go_to_login(),
                border_radius=8,
                padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                ink=True,
            ),
            ft.Container(height=16),
        ], spacing=4),
        width=210, bgcolor=SURFACE,
        padding=ft.Padding.symmetric(horizontal=10),
        border=ft.Border.only(right=ft.BorderSide(1, BORDER)),
        shadow=ft.BoxShadow(blur_radius=12, color="#0A000000", offset=ft.Offset(2, 0)),
    )

    main_shell = ft.Row([sidebar, content_col], expand=True, spacing=0)

    login_view = ft.Container(
        content=login_page(page, go_to=lambda _: show_shell()),
        expand=True, bgcolor=BG,
    )

    def show_shell():
        page.controls.clear()
        page.controls.append(main_shell)
        page.update()
        render_page("dashboard")

    page.controls.append(login_view)
    page.update()


ft.run(main)