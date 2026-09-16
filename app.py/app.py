import streamlit as st
import pandas as pd

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="คลังพร้อม", page_icon="📦", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #0F1E1A; color: #F3EFE4; }
    div[data-testid="stMetric"] {
        background-color: #15271F;
        border: 1px solid #2A4038;
        border-radius: 4px;
        padding: 14px 16px;
    }
    div[data-testid="stMetricLabel"] { color: #93AA9C; }
    div[data-testid="stMetricValue"] { color: #F3EFE4; }
    .stButton>button {
        background-color: #C9A227;
        color: #1B1608;
        border: none;
        font-weight: 600;
    }
    .stDataFrame { background-color: #15271F; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Mock data — institutional kitchens (hospital, prison, school)
# ---------------------------------------------------------------------------
PO_ROWS = pd.DataFrame(
    [
        {"วัตถุดิบ": "ข้าวสาร (กก.)", "หน่วยงาน": "โรงพยาบาลรัฐ (ครัวกลาง)", "สั่ง (PO)": 500, "คงเหลือจริง": 210, "เบิกใช้เฉลี่ย/รอบ": 340, "สถานะ": "สั่งเกิน"},
        {"วัตถุดิบ": "ไข่ไก่ (แผง)", "หน่วยงาน": "เรือนจำกลาง", "สั่ง (PO)": 300, "คงเหลือจริง": 40, "เบิกใช้เฉลี่ย/รอบ": 260, "สถานะ": "สั่งขาด"},
        {"วัตถุดิบ": "นมกล่อง UHT (ลัง)", "หน่วยงาน": "โรงเรียนประจำ", "สั่ง (PO)": 200, "คงเหลือจริง": 130, "เบิกใช้เฉลี่ย/รอบ": 70, "สถานะ": "สั่งเกิน"},
        {"วัตถุดิบ": "ผักรวม (กก.)", "หน่วยงาน": "โรงพยาบาลรัฐ (ครัวกลาง)", "สั่ง (PO)": 150, "คงเหลือจริง": 12, "เบิกใช้เฉลี่ย/รอบ": 145, "สถานะ": "ใกล้เคียงการเบิกใช้จริง"},
        {"วัตถุดิบ": "เนื้อหมู (กก.)", "หน่วยงาน": "เรือนจำกลาง", "สั่ง (PO)": 220, "คงเหลือจริง": 95, "เบิกใช้เฉลี่ย/รอบ": 110, "สถานะ": "สั่งเกิน"},
        {"วัตถุดิบ": "ซอสปรุงรส (ขวด)", "หน่วยงาน": "โรงเรียนประจำ", "สั่ง (PO)": 60, "คงเหลือจริง": 45, "เบิกใช้เฉลี่ย/รอบ": 20, "สถานะ": "สั่งเกิน"},
    ]
)

EXPIRY_SEED = [
    {"id": "e1", "item": "นมกล่อง UHT", "branch": "โรงเรียนประจำ", "days_left": 2, "qty": 45, "unit": "ลัง", "discount": 25, "base_value": 13500},
    {"id": "e2", "item": "เนื้อหมู", "branch": "เรือนจำกลาง", "days_left": 1, "qty": 60, "unit": "กก.", "discount": 30, "base_value": 10800},
    {"id": "e3", "item": "ผักรวม", "branch": "โรงพยาบาลรัฐ (ครัวกลาง)", "days_left": 1, "qty": 38, "unit": "กก.", "discount": 20, "base_value": 3040},
]

WASTE_TREND = pd.DataFrame(
    {
        "เดือน": ["เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย."],
        "ก่อนใช้ระบบ": [18.2, 18.6, 19.0, 18.4, 19.3, 18.9],
        "หลังใช้ระบบ": [18.2, 14.1, 10.8, 8.6, 6.9, 5.4],
    }
).set_index("เดือน")

STATUS_COLOR = {
    "สั่งเกิน": "🔴",
    "สั่งขาด": "🟠",
    "ใกล้เคียงการเบิกใช้จริง": "🟢",
}

# ---------------------------------------------------------------------------
# Session state for the promotion demo
# ---------------------------------------------------------------------------
if "promoted" not in st.session_state:
    st.session_state.promoted = {}

def recovered_revenue():
    total = 0
    for e in EXPIRY_SEED:
        if st.session_state.promoted.get(e["id"]):
            total += e["base_value"] * (1 - e["discount"] / 100)
    return total

# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.markdown("## คลังพร้อม")
st.sidebar.caption("รู้ก่อนหมด สั่งได้แม่น ขายได้ก่อนเสีย")
page = st.sidebar.radio(
    "เมนู",
    ["ภาพรวม", "เทียบใบสั่งซื้อกับสต๊อกจริง", "จัดการวัตถุดิบใกล้หมดอายุ"],
    label_visibility="collapsed",
)
st.sidebar.info(
    "เดโมสำหรับกลุ่ม **โรงพยาบาล โรงเรียน และเรือนจำ** — "
    "หน่วยงานที่มีโรงครัวขนาดใหญ่และสั่งวัตถุดิบปริมาณมากต่อรอบ"
)

# ---------------------------------------------------------------------------
# Page: Overview
# ---------------------------------------------------------------------------
if page == "ภาพรวม":
    st.title("ภาพรวมระบบ")
    st.caption("สรุปผลตั้งแต่เริ่มใช้ระบบเทียบ PO กับสต๊อกจริงและระบบแจ้งเตือนวัตถุดิบใกล้หมดอายุ")

    over_count = (PO_ROWS["สถานะ"] == "สั่งเกิน").sum()
    revenue = recovered_revenue()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Food waste ที่ลดได้", "71%", "ลดจาก 18.9% เหลือ 5.4%")
    c2.metric("ความแม่นยำของ PO", "89%", "เทียบย้อนหลัง 6 เดือน")
    c3.metric(
        "รายได้จากโปรโมชั่น Resale",
        f"{revenue:,.0f} บาท/เดือน",
        "จากรายการที่กดสร้างโปรโมชั่นแล้ว" if revenue else "ยังไม่มีการสร้างโปรโมชั่น",
    )
    c4.metric("รายการสั่งเกินตอนนี้", f"{over_count} SKU", "ควรปรับปริมาณรอบถัดไป", delta_color="inverse")

    st.markdown("#### แนวโน้ม Food Waste ต่อเดือน (% ของสต๊อกที่ทิ้ง)")
    st.caption("เทียบก่อนและหลังเริ่มใช้ระบบในเดือนพฤษภาคม")
    st.line_chart(WASTE_TREND, color=["#93AA9C", "#C9A227"])

# ---------------------------------------------------------------------------
# Page: PO reconciliation
# ---------------------------------------------------------------------------
elif page == "เทียบใบสั่งซื้อกับสต๊อกจริง":
    st.title("เทียบใบสั่งซื้อ (PO) กับสต๊อกจริง")
    st.caption(
        "ระบบเทียบปริมาณที่สั่งกับสต๊อกคงเหลือจริงและปริมาณเบิกใช้เฉลี่ยของแต่ละหน่วยงาน "
        "เพื่อชี้ว่ารายการไหนสั่งเกินหรือสั่งขาด"
    )
    display_df = PO_ROWS.copy()
    display_df["สถานะ"] = display_df["สถานะ"].apply(lambda s: f"{STATUS_COLOR.get(s, '')} {s}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.caption("รอบ PO ถัดไป ระบบจะแนะนำปรับปริมาณสั่งซื้ออัตโนมัติตามปริมาณเบิกใช้เฉลี่ยที่สะสมไว้")

# ---------------------------------------------------------------------------
# Page: Expiry & resale
# ---------------------------------------------------------------------------
else:
    st.title("วัตถุดิบใกล้หมดอายุ & โปรโมชั่นอัตโนมัติ")
    st.caption("กดสร้างโปรโมชั่นเพื่อจำลองการแปลงวัตถุดิบใกล้หมดอายุให้เป็นรายได้ก่อนที่จะถูกทิ้ง")

    for e in EXPIRY_SEED:
        is_promoted = st.session_state.promoted.get(e["id"], False)
        recovered = e["base_value"] * (1 - e["discount"] / 100)

        with st.container(border=True):
            col1, col2, col3 = st.columns([3, 1.3, 1.4])
            with col1:
                st.markdown(f"**{e['item']} · {e['qty']} {e['unit']}**")
                urgency = "🔴" if e["days_left"] <= 1 else "🟠"
                st.caption(
                    f"{e['branch']} — เหลืออีก {urgency} {e['days_left']} วัน ก่อนหมดอายุ · "
                    f"มูลค่าตั้งต้น {e['base_value']:,} บาท"
                )
            with col2:
                if is_promoted:
                    st.markdown(f"**+{recovered:,.0f} บาท**")
                    st.caption("กู้คืนเป็นรายได้แล้ว")
                else:
                    st.markdown(f"**ลด {e['discount']}%**")
                    st.caption("ส่วนลดที่ระบบแนะนำ")
            with col3:
                label = "ยกเลิกโปรโมชั่น" if is_promoted else "✨ สร้างโปรโมชั่นอัตโนมัติ"
                if st.button(label, key=f"btn_{e['id']}"):
                    st.session_state.promoted[e["id"]] = not is_promoted
                    st.rerun()

