import streamlit as st
import pandas as pd

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="คลังพร้อม", page_icon="📦", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #FFFFFF; color: #1B3A2B; }
    section[data-testid="stSidebar"] {
        background-color: #F1F8F0;
        border-right: 1px solid #D9EDD9;
    }
    div[data-testid="stMetric"] {
        background-color: #F1F8F0;
        border: 1px solid #D9EDD9;
        border-radius: 8px;
        padding: 14px 16px;
    }
    div[data-testid="stMetricLabel"] { color: #4B7A5C; }
    div[data-testid="stMetricValue"] { color: #1B3A2B; }
    div[data-testid="stMetricDelta"] { color: #2F9E44; }
    .stButton>button {
        background-color: #2F9E44;
        color: #FFFFFF;
        border: none;
        border-radius: 6px;
        font-weight: 600;
    }
    .stButton>button:hover { background-color: #257A37; color: #FFFFFF; }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FAFDF9;
        border: 1px solid #D9EDD9 !important;
        border-radius: 8px;
    }
    .stDataFrame, div[data-testid="stDataEditor"] { border: 1px solid #D9EDD9; border-radius: 8px; }
    h1, h2, h3, h4 { color: #1B3A2B; }
    p, span, label, .stCaption { color: #4B5F55 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Starting data — kept in session_state so it can be edited live in the app.
# NOTE: this resets when the app reboots/redeploys (Streamlit Cloud does not
# keep a database by default). Use the download/upload buttons at the bottom
# of each page to save your work and load it back next time.
# ---------------------------------------------------------------------------
if "po_df" not in st.session_state:
    st.session_state.po_df = pd.DataFrame(
        [
            {"วัตถุดิบ": "ข้าวสาร (กก.)", "หน่วยงาน": "โรงพยาบาลรัฐ (ครัวกลาง)", "สั่ง (PO)": 500, "คงเหลือจริง": 210, "เบิกใช้เฉลี่ย/รอบ": 340},
            {"วัตถุดิบ": "ไข่ไก่ (แผง)", "หน่วยงาน": "เรือนจำกลาง", "สั่ง (PO)": 300, "คงเหลือจริง": 40, "เบิกใช้เฉลี่ย/รอบ": 260},
            {"วัตถุดิบ": "นมกล่อง UHT (ลัง)", "หน่วยงาน": "โรงเรียนประจำ", "สั่ง (PO)": 200, "คงเหลือจริง": 130, "เบิกใช้เฉลี่ย/รอบ": 70},
            {"วัตถุดิบ": "ผักรวม (กก.)", "หน่วยงาน": "โรงพยาบาลรัฐ (ครัวกลาง)", "สั่ง (PO)": 150, "คงเหลือจริง": 12, "เบิกใช้เฉลี่ย/รอบ": 145},
            {"วัตถุดิบ": "เนื้อหมู (กก.)", "หน่วยงาน": "เรือนจำกลาง", "สั่ง (PO)": 220, "คงเหลือจริง": 95, "เบิกใช้เฉลี่ย/รอบ": 110},
            {"วัตถุดิบ": "ซอสปรุงรส (ขวด)", "หน่วยงาน": "โรงเรียนประจำ", "สั่ง (PO)": 60, "คงเหลือจริง": 45, "เบิกใช้เฉลี่ย/รอบ": 20},
        ]
    )

if "expiry_df" not in st.session_state:
    st.session_state.expiry_df = pd.DataFrame(
        [
            {"รายการ": "นมกล่อง UHT", "หน่วยงาน": "โรงเรียนประจำ", "จำนวน": 45, "หน่วย": "ลัง", "วันคงเหลือ": 2, "ส่วนลดแนะนำ (%)": 25, "มูลค่าตั้งต้น (บาท)": 13500, "สร้างโปรโมชั่นแล้ว": False},
            {"รายการ": "เนื้อหมู", "หน่วยงาน": "เรือนจำกลาง", "จำนวน": 60, "หน่วย": "กก.", "วันคงเหลือ": 1, "ส่วนลดแนะนำ (%)": 30, "มูลค่าตั้งต้น (บาท)": 10800, "สร้างโปรโมชั่นแล้ว": False},
            {"รายการ": "ผักรวม", "หน่วยงาน": "โรงพยาบาลรัฐ (ครัวกลาง)", "จำนวน": 38, "หน่วย": "กก.", "วันคงเหลือ": 1, "ส่วนลดแนะนำ (%)": 20, "มูลค่าตั้งต้น (บาท)": 3040, "สร้างโปรโมชั่นแล้ว": False},
        ]
    )

WASTE_TREND = pd.DataFrame(
    {
        "เดือน": ["เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย."],
        "ก่อนใช้ระบบ": [18.2, 18.6, 19.0, 18.4, 19.3, 18.9],
        "หลังใช้ระบบ": [18.2, 14.1, 10.8, 8.6, 6.9, 5.4],
    }
).set_index("เดือน")

REVENUE_BREAKDOWN = pd.DataFrame(
    {
        "แหล่งรายได้": ["ค่าสมัครสมาชิกรายเดือน (Subscription)", "ค่าบริการแรกเข้า (Setup Fee)", "โมดูลเสริม (Premium Add-on)"],
        "สัดส่วนปีแรก (บาท)": [1255500, 540000, 167400],
        "สัดส่วน (%)": [64.0, 27.5, 8.5],
    }
).set_index("แหล่งรายได้")

GROWTH_TREND = pd.DataFrame(
    {"ช่วงเวลา": ["เดือนแรก", "เดือนที่ 12"], "รายได้ต่อเดือน (บาท)": [85800, 228600]}
).set_index("ช่วงเวลา")


def calc_status(po, stock, used):
    if used <= 0:
        return "ไม่มีข้อมูลเบิกใช้"
    if po > used * 1.3:
        return "🔴 สั่งเกิน"
    if stock < used * 0.5:
        return "🟠 สั่งขาด"
    return "🟢 ใกล้เคียงการเบิกใช้จริง"


def recovered_revenue(df: pd.DataFrame) -> float:
    promoted = df[df["สร้างโปรโมชั่นแล้ว"] == True]  # noqa: E712
    if promoted.empty:
        return 0.0
    return (promoted["มูลค่าตั้งต้น (บาท)"] * (1 - promoted["ส่วนลดแนะนำ (%)"] / 100)).sum()


# ---------------------------------------------------------------------------
# Sidebar navigation
# ---------------------------------------------------------------------------
st.sidebar.markdown("## คลังพร้อม")
st.sidebar.caption("รู้ก่อนหมด สั่งได้แม่น ขายได้ก่อนเสีย")
page = st.sidebar.radio(
    "เมนู",
    [
        "ภาพรวม",
        "เทียบใบสั่งซื้อกับสต๊อกจริง",
        "จัดการวัตถุดิบใกล้หมดอายุ",
        "แผนธุรกิจ & รายได้",
    ],
    label_visibility="collapsed",
)
st.sidebar.info(
    "เดโมสำหรับกลุ่ม **โรงพยาบาล โรงเรียน และเรือนจำ** — "
    "หน่วยงานที่มีโรงครัวขนาดใหญ่และสั่งวัตถุดิบปริมาณมากต่อรอบ"
)
st.sidebar.caption(
    "⚠️ ข้อมูลที่คีย์ในหน้านี้เก็บไว้เฉพาะระหว่างที่แอปยังไม่รีสตาร์ท "
    "ให้กดดาวน์โหลด CSV เก็บไว้ทุกครั้งหลังแก้ไข"
)

# ---------------------------------------------------------------------------
# Page: Overview
# ---------------------------------------------------------------------------
if page == "ภาพรวม":
    st.title("ภาพรวมระบบ")
    st.caption("สรุปผลตั้งแต่เริ่มใช้ระบบเทียบ PO กับสต๊อกจริงและระบบแจ้งเตือนวัตถุดิบใกล้หมดอายุ")

    po_df = st.session_state.po_df
    expiry_df = st.session_state.expiry_df

    status_series = po_df.apply(
        lambda r: calc_status(r["สั่ง (PO)"], r["คงเหลือจริง"], r["เบิกใช้เฉลี่ย/รอบ"]), axis=1
    )
    over_count = status_series.str.contains("สั่งเกิน").sum()
    revenue = recovered_revenue(expiry_df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Food waste ที่ลดได้", "71%", "ลดจาก 18.9% เหลือ 5.4% (ข้อมูลอ้างอิง)")
    c2.metric("จำนวนวัตถุดิบที่ติดตามอยู่", f"{len(po_df)} SKU")
    c3.metric(
        "รายได้จากโปรโมชั่น Resale",
        f"{revenue:,.0f} บาท",
        "จากรายการที่ติ๊กสร้างโปรโมชั่นแล้ว" if revenue else "ยังไม่มีการสร้างโปรโมชั่น",
    )
    c4.metric("รายการสั่งเกินตอนนี้", f"{over_count} SKU", "ควรปรับปริมาณรอบถัดไป", delta_color="inverse")

    st.markdown("#### แนวโน้ม Food Waste ต่อเดือน (% ของสต๊อกที่ทิ้ง)")
    st.caption("ข้อมูลอ้างอิงสำหรับสาธิต — เทียบก่อนและหลังเริ่มใช้ระบบ")
    st.line_chart(WASTE_TREND, color=["#B8CFC0", "#2F9E44"])

# ---------------------------------------------------------------------------
# Page: PO reconciliation — editable
# ---------------------------------------------------------------------------
elif page == "เทียบใบสั่งซื้อกับสต๊อกจริง":
    st.title("เทียบใบสั่งซื้อ (PO) กับสต๊อกจริง")
    st.caption(
        "แก้ไขตัวเลขในตารางได้โดยตรง กดที่แถวว่างล่างสุดเพื่อเพิ่มวัตถุดิบใหม่ "
        "หรือติ๊กเลือกแถวแล้วกดถังขยะเพื่อลบ"
    )

    edited = st.data_editor(
        st.session_state.po_df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "สั่ง (PO)": st.column_config.NumberColumn(min_value=0, step=1),
            "คงเหลือจริง": st.column_config.NumberColumn(min_value=0, step=1),
            "เบิกใช้เฉลี่ย/รอบ": st.column_config.NumberColumn(min_value=0, step=1),
        },
        key="po_editor",
    )
    st.session_state.po_df = edited

    st.markdown("#### ผลวิเคราะห์อัตโนมัติ")
    result_df = edited.copy()
    result_df["สถานะ"] = result_df.apply(
        lambda r: calc_status(r["สั่ง (PO)"], r["คงเหลือจริง"], r["เบิกใช้เฉลี่ย/รอบ"]), axis=1
    )
    st.dataframe(result_df, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ ดาวน์โหลดข้อมูล PO เป็น CSV",
        edited.to_csv(index=False).encode("utf-8-sig"),
        file_name="po_data.csv",
        mime="text/csv",
    )
    uploaded = st.file_uploader("⬆️ อัปโหลด CSV เพื่อโหลดข้อมูลเดิมกลับมา", type="csv", key="po_upload")
    if uploaded is not None:
        st.session_state.po_df = pd.read_csv(uploaded)
        st.rerun()

# ---------------------------------------------------------------------------
# Page: Expiry & resale — editable
# ---------------------------------------------------------------------------
elif page == "จัดการวัตถุดิบใกล้หมดอายุ":
    st.title("วัตถุดิบใกล้หมดอายุ & โปรโมชั่นอัตโนมัติ")
    st.caption(
        "เพิ่ม/แก้ไขรายการวัตถุดิบใกล้หมดอายุในตาราง แล้วติ๊กช่อง "
        "'สร้างโปรโมชั่นแล้ว' เพื่อจำลองการแปลงเป็นรายได้"
    )

    edited = st.data_editor(
        st.session_state.expiry_df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "จำนวน": st.column_config.NumberColumn(min_value=0, step=1),
            "วันคงเหลือ": st.column_config.NumberColumn(min_value=0, step=1),
            "ส่วนลดแนะนำ (%)": st.column_config.NumberColumn(min_value=0, max_value=100, step=5),
            "มูลค่าตั้งต้น (บาท)": st.column_config.NumberColumn(min_value=0, step=100),
            "สร้างโปรโมชั่นแล้ว": st.column_config.CheckboxColumn(),
        },
        key="expiry_editor",
    )
    st.session_state.expiry_df = edited

    revenue = recovered_revenue(edited)
    st.metric("รวมรายได้ที่กู้คืนจากโปรโมชั่น", f"{revenue:,.0f} บาท")

    st.download_button(
        "⬇️ ดาวน์โหลดข้อมูลใกล้หมดอายุเป็น CSV",
        edited.to_csv(index=False).encode("utf-8-sig"),
        file_name="expiry_data.csv",
        mime="text/csv",
    )
    uploaded = st.file_uploader("⬆️ อัปโหลด CSV เพื่อโหลดข้อมูลเดิมกลับมา", type="csv", key="expiry_upload")
    if uploaded is not None:
        st.session_state.expiry_df = pd.read_csv(uploaded)
        st.rerun()

# ---------------------------------------------------------------------------
# Page: Business model & revenue
# ---------------------------------------------------------------------------
else:
    st.title("แผนธุรกิจ & รายได้")
    st.caption("สรุปโมเดลรายได้ ต้นทุน และเป้าหมายการเติบโตในปีแรก สำหรับกลุ่มโรงเรียน โรงพยาบาล และเรือนจำ")

    st.markdown("#### คุณค่าที่ส่งมอบให้หน่วยงาน")
    st.markdown(
        "- **ความแม่นยำ & ลด Food Waste** — เสริมความแม่นยำให้การสั่งซื้อวัตถุดิบของโรงครัวส่วนกลาง "
        "ด้วยข้อมูลการเบิกใช้จริงแบบเรียลไทม์ ลดต้นทุนวัตถุดิบและของเสียในครัว\n"
        "- **ลดงานเอกสารและเวลา** — เปลี่ยนงานเช็กสต๊อกและเปิดใบสั่งซื้อ (PO) จากทำมือให้เป็นระบบอัตโนมัติ\n"
        "- **กู้คืนรายได้จากของใกล้หมดอายุ** — แปลงวัตถุดิบใกล้หมดอายุให้กลับมาเป็นมูลค่าผ่านโปรโมชั่นอัตโนมัติ\n"
        "- **ตัดสินใจด้วยข้อมูล** — ฝ่ายจัดซื้อและครัวกลางทำงานซิงค์กันด้วยข้อมูลชุดเดียว ไม่ต้องเดาปริมาณสั่งซื้อ"
    )

    st.markdown("#### การเติบโตของฐานลูกค้าในปีแรก")
    c1, c2, c3 = st.columns(3)
    c1.metric("หน่วยงานที่ใช้งาน (เดือนแรก)", "5 หน่วยงาน", "15 จุดบริการ")
    c2.metric("หน่วยงานที่ใช้งาน (เดือนที่ 12)", "34 หน่วยงาน", "108 จุดบริการ")
    c3.metric("เป้าหมายรายได้รวมปีแรก", "1,962,900 บาท")

    st.bar_chart(GROWTH_TREND, color=["#2F9E44"])
    st.caption("จุดบริการ = แผนก/โรงครัวย่อยของแต่ละหน่วยงาน เช่น หลายแผนกในโรงพยาบาล หรือหลายโรงอาหารในโรงเรียน")

    st.markdown("#### โครงสร้างรายได้ (Revenue Streams)")
    st.dataframe(REVENUE_BREAKDOWN, use_container_width=True)
    st.caption(
        "ค่าสมัครสมาชิกคิดตามจำนวนจุดบริการ/SKU ที่ติดตาม · ค่าแรกเข้าคำนวณจากการตั้งค่าระบบผูกสูตร/ปริมาณเบิกใช้ "
        "และเชื่อมต่อระบบจัดซื้อเดิมของหน่วยงาน · โมดูลเสริมคือ AI พยากรณ์ความต้องการและระบบโปรโมชั่นขั้นสูง"
    )

    st.markdown("#### โครงสร้างต้นทุน (Cost Structure)")
    st.markdown(
        "- ค่าพัฒนา/ดูแลระบบและโมเดล AI\n"
        "- ค่า Server/Cloud\n"
        "- เงินเดือนทีมขาย-ซัพพอร์ต และค่าการตลาดสำหรับกลุ่มหน่วยงานภาครัฐ/สถาบัน"
    )

        border-radius: 8px;
    }
    .stDataFrame, div[data-testid="stDataEditor"] { border: 1px solid #D9EDD9; border-radius: 8px; }
    h1, h2, h3, h4 { color: #1B3A2B; }
    p, span, label, .stCaption { color: #4B5F55 !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Starting data — kept in session_state so it can be edited live in the app.
# NOTE: this resets when the app reboots/redeploys (Streamlit Cloud does not
# keep a database by default). Use the download/upload buttons at the bottom
# of each page to save your work and load it back next time.
# ---------------------------------------------------------------------------
if "po_df" not in st.session_state:
    st.session_state.po_df = pd.DataFrame(
        [
            {"วัตถุดิบ": "ข้าวสาร (กก.)", "หน่วยงาน": "โรงพยาบาลรัฐ (ครัวกลาง)", "สั่ง (PO)": 500, "คงเหลือจริง": 210, "เบิกใช้เฉลี่ย/รอบ": 340},
            {"วัตถุดิบ": "ไข่ไก่ (แผง)", "หน่วยงาน": "เรือนจำกลาง", "สั่ง (PO)": 300, "คงเหลือจริง": 40, "เบิกใช้เฉลี่ย/รอบ": 260},
            {"วัตถุดิบ": "นมกล่อง UHT (ลัง)", "หน่วยงาน": "โรงเรียนประจำ", "สั่ง (PO)": 200, "คงเหลือจริง": 130, "เบิกใช้เฉลี่ย/รอบ": 70},
            {"วัตถุดิบ": "ผักรวม (กก.)", "หน่วยงาน": "โรงพยาบาลรัฐ (ครัวกลาง)", "สั่ง (PO)": 150, "คงเหลือจริง": 12, "เบิกใช้เฉลี่ย/รอบ": 145},
            {"วัตถุดิบ": "เนื้อหมู (กก.)", "หน่วยงาน": "เรือนจำกลาง", "สั่ง (PO)": 220, "คงเหลือจริง": 95, "เบิกใช้เฉลี่ย/รอบ": 110},
            {"วัตถุดิบ": "ซอสปรุงรส (ขวด)", "หน่วยงาน": "โรงเรียนประจำ", "สั่ง (PO)": 60, "คงเหลือจริง": 45, "เบิกใช้เฉลี่ย/รอบ": 20},
        ]
    )

if "expiry_df" not in st.session_state:
    st.session_state.expiry_df = pd.DataFrame(
        [
            {"รายการ": "นมกล่อง UHT", "หน่วยงาน": "โรงเรียนประจำ", "จำนวน": 45, "หน่วย": "ลัง", "วันคงเหลือ": 2, "ส่วนลดแนะนำ (%)": 25, "มูลค่าตั้งต้น (บาท)": 13500, "สร้างโปรโมชั่นแล้ว": False},
            {"รายการ": "เนื้อหมู", "หน่วยงาน": "เรือนจำกลาง", "จำนวน": 60, "หน่วย": "กก.", "วันคงเหลือ": 1, "ส่วนลดแนะนำ (%)": 30, "มูลค่าตั้งต้น (บาท)": 10800, "สร้างโปรโมชั่นแล้ว": False},
            {"รายการ": "ผักรวม", "หน่วยงาน": "โรงพยาบาลรัฐ (ครัวกลาง)", "จำนวน": 38, "หน่วย": "กก.", "วันคงเหลือ": 1, "ส่วนลดแนะนำ (%)": 20, "มูลค่าตั้งต้น (บาท)": 3040, "สร้างโปรโมชั่นแล้ว": False},
        ]
    )

WASTE_TREND = pd.DataFrame(
    {
        "เดือน": ["เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย."],
        "ก่อนใช้ระบบ": [18.2, 18.6, 19.0, 18.4, 19.3, 18.9],
        "หลังใช้ระบบ": [18.2, 14.1, 10.8, 8.6, 6.9, 5.4],
    }
).set_index("เดือน")


def calc_status(po, stock, used):
    if used <= 0:
        return "ไม่มีข้อมูลเบิกใช้"
    if po > used * 1.3:
        return "🔴 สั่งเกิน"
    if stock < used * 0.5:
        return "🟠 สั่งขาด"
    return "🟢 ใกล้เคียงการเบิกใช้จริง"


def recovered_revenue(df: pd.DataFrame) -> float:
    promoted = df[df["สร้างโปรโมชั่นแล้ว"] == True]  # noqa: E712
    if promoted.empty:
        return 0.0
    return (promoted["มูลค่าตั้งต้น (บาท)"] * (1 - promoted["ส่วนลดแนะนำ (%)"] / 100)).sum()


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
st.sidebar.caption(
    "⚠️ ข้อมูลที่คีย์ในหน้านี้เก็บไว้เฉพาะระหว่างที่แอปยังไม่รีสตาร์ท "
    "ให้กดดาวน์โหลด CSV เก็บไว้ทุกครั้งหลังแก้ไข"
)

# ---------------------------------------------------------------------------
# Page: Overview
# ---------------------------------------------------------------------------
if page == "ภาพรวม":
    st.title("ภาพรวมระบบ")
    st.caption("สรุปผลตั้งแต่เริ่มใช้ระบบเทียบ PO กับสต๊อกจริงและระบบแจ้งเตือนวัตถุดิบใกล้หมดอายุ")

    po_df = st.session_state.po_df
    expiry_df = st.session_state.expiry_df

    status_series = po_df.apply(
        lambda r: calc_status(r["สั่ง (PO)"], r["คงเหลือจริง"], r["เบิกใช้เฉลี่ย/รอบ"]), axis=1
    )
    over_count = status_series.str.contains("สั่งเกิน").sum()
    revenue = recovered_revenue(expiry_df)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Food waste ที่ลดได้", "71%", "ลดจาก 18.9% เหลือ 5.4% (ข้อมูลอ้างอิง)")
    c2.metric("จำนวนวัตถุดิบที่ติดตามอยู่", f"{len(po_df)} SKU")
    c3.metric(
        "รายได้จากโปรโมชั่น Resale",
        f"{revenue:,.0f} บาท",
        "จากรายการที่ติ๊กสร้างโปรโมชั่นแล้ว" if revenue else "ยังไม่มีการสร้างโปรโมชั่น",
    )
    c4.metric("รายการสั่งเกินตอนนี้", f"{over_count} SKU", "ควรปรับปริมาณรอบถัดไป", delta_color="inverse")

    st.markdown("#### แนวโน้ม Food Waste ต่อเดือน (% ของสต๊อกที่ทิ้ง)")
    st.caption("ข้อมูลอ้างอิงสำหรับสาธิต — เทียบก่อนและหลังเริ่มใช้ระบบ")
    st.line_chart(WASTE_TREND, color=["#B8CFC0", "#2F9E44"])

# ---------------------------------------------------------------------------
# Page: PO reconciliation — editable
# ---------------------------------------------------------------------------
elif page == "เทียบใบสั่งซื้อกับสต๊อกจริง":
    st.title("เทียบใบสั่งซื้อ (PO) กับสต๊อกจริง")
    st.caption(
        "แก้ไขตัวเลขในตารางได้โดยตรง กดที่แถวว่างล่างสุดเพื่อเพิ่มวัตถุดิบใหม่ "
        "หรือติ๊กเลือกแถวแล้วกดถังขยะเพื่อลบ"
    )

    edited = st.data_editor(
        st.session_state.po_df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "สั่ง (PO)": st.column_config.NumberColumn(min_value=0, step=1),
            "คงเหลือจริง": st.column_config.NumberColumn(min_value=0, step=1),
            "เบิกใช้เฉลี่ย/รอบ": st.column_config.NumberColumn(min_value=0, step=1),
        },
        key="po_editor",
    )
    st.session_state.po_df = edited

    st.markdown("#### ผลวิเคราะห์อัตโนมัติ")
    result_df = edited.copy()
    result_df["สถานะ"] = result_df.apply(
        lambda r: calc_status(r["สั่ง (PO)"], r["คงเหลือจริง"], r["เบิกใช้เฉลี่ย/รอบ"]), axis=1
    )
    st.dataframe(result_df, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️ ดาวน์โหลดข้อมูล PO เป็น CSV",
        edited.to_csv(index=False).encode("utf-8-sig"),
        file_name="po_data.csv",
        mime="text/csv",
    )
    uploaded = st.file_uploader("⬆️ อัปโหลด CSV เพื่อโหลดข้อมูลเดิมกลับมา", type="csv", key="po_upload")
    if uploaded is not None:
        st.session_state.po_df = pd.read_csv(uploaded)
        st.rerun()

# ---------------------------------------------------------------------------
# Page: Expiry & resale — editable
# ---------------------------------------------------------------------------
else:
    st.title("วัตถุดิบใกล้หมดอายุ & โปรโมชั่นอัตโนมัติ")
    st.caption(
        "เพิ่ม/แก้ไขรายการวัตถุดิบใกล้หมดอายุในตาราง แล้วติ๊กช่อง "
        "'สร้างโปรโมชั่นแล้ว' เพื่อจำลองการแปลงเป็นรายได้"
    )

    edited = st.data_editor(
        st.session_state.expiry_df,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        column_config={
            "จำนวน": st.column_config.NumberColumn(min_value=0, step=1),
            "วันคงเหลือ": st.column_config.NumberColumn(min_value=0, step=1),
            "ส่วนลดแนะนำ (%)": st.column_config.NumberColumn(min_value=0, max_value=100, step=5),
            "มูลค่าตั้งต้น (บาท)": st.column_config.NumberColumn(min_value=0, step=100),
            "สร้างโปรโมชั่นแล้ว": st.column_config.CheckboxColumn(),
        },
        key="expiry_editor",
    )
    st.session_state.expiry_df = edited

    revenue = recovered_revenue(edited)
    st.metric("รวมรายได้ที่กู้คืนจากโปรโมชั่น", f"{revenue:,.0f} บาท")

    st.download_button(
        "⬇️ ดาวน์โหลดข้อมูลใกล้หมดอายุเป็น CSV",
        edited.to_csv(index=False).encode("utf-8-sig"),
        file_name="expiry_data.csv",
        mime="text/csv",
    )
    uploaded = st.file_uploader("⬆️ อัปโหลด CSV เพื่อโหลดข้อมูลเดิมกลับมา", type="csv", key="expiry_upload")
    if uploaded is not None:
        st.session_state.expiry_df = pd.read_csv(uploaded)
        st.rerun()
