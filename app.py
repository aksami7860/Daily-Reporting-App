import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Meezan Bank - Branch Daily Performance Report", 
    layout="wide",
    page_icon="meezan_logo.png"
)

# Meezan Bank Brand Colors
MEEZAN_GREEN = "#006A4E"
MEEZAN_GOLD = "#C9A227"

# Custom CSS for Meezan theme
st.markdown(f"""
<style>
    .stApp {{
        background-color: #F8F9FA;
    }}
    [data-testid="stHeader"] {{
        background-color: {MEEZAN_GREEN};
    }}
    h1, h2, h3 {{
        color: {MEEZAN_GREEN};
        font-weight: 600;
    }}
    .stButton>button {{
        background-color: {MEEZAN_GREEN};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }}
    .stButton>button:hover {{
        background-color: #00523D;
        color: white;
    }}
    .stButton>button[kind="primary"] {{
        background-color: {MEEZAN_GOLD};
        color: {MEEZAN_GREEN};
    }}
    .stButton>button[kind="primary"]:hover {{
        background-color: #B8951F;
        color: {MEEZAN_GREEN};
    }}
    [data-testid="stForm"] {{
        background-color: white;
        padding: 2rem;
        border-radius: 12px;
        border-left: 5px solid {MEEZAN_GREEN};
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    .stSubheader {{
        color: {MEEZAN_GREEN};
        border-bottom: 2px solid {MEEZAN_GOLD};
        padding-bottom: 0.3rem;
    }}
</style>
""", unsafe_allow_html=True)

# Header with logo
col1, col2 = st.columns([1, 5])
with col1:
    st.image("meezan_logo.png", width=120)
with col2:
    st.title("Branch Daily Performance Report")
    st.caption("Meezan Bank Limited")

BRANCH_MAP = {
    "0218": "Walton Branch",
    "0220": "Zarrar Shaheed Branch",
    "0235": "Canal Road Mughalpura Branch",
    "0238": "Saddar Cantt Branch",
    "0280": "Burki Road Branch",
    "0283": "Main Boulevard Branch",
    "0296": "Tufail Road Branch",
    "1132": "LDA Tajpura Branch",
    "1139": "Nishat Colony Branch",
    "1141": "Eden City Branch",
    "1146": "Askari 10 Branch",
    "1150": "Harbanspura Branch",
    "1153": "Askari Branch",
    "1161": "Ex ParkView Branch"
}

DATA_FILE = "branch_daily_report.csv"

with st.form("report_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        report_date = st.date_input("Report Date", value=date.today())
        branch_code = st.selectbox("Branch Code", options=list(BRANCH_MAP.keys()))
        branch_name = BRANCH_MAP[branch_code]
        st.text_input("Branch Name", value=branch_name, disabled=True)
        
        st.subheader("Deposit Performance")
        day_change_ca = st.number_input("Day Change CA", value=0.0, step=1000.0, format="%.2f")
        day_change_total = st.number_input("Day Change Total", value=0.0, step=1000.0, format="%.2f")
        
        var_ca = st.number_input("Variance from Target - CA", value=0.0, step=1000.0, format="%.2f")
        var_casa = st.number_input("Variance from Target - CASA", value=0.0, step=1000.0, format="%.2f")
        var_total = st.number_input("Variance from Target - Total", value=0.0, step=1000.0, format="%.2f")
    
    with col2:
        st.subheader("NTB Performance")
        ntb_total = st.number_input("Total NTB", min_value=0, step=1)
        ntb_ca = st.number_input("CA NTB", min_value=0, step=1)
        ntb_proprietor = st.number_input("Proprietor NTB", min_value=0, step=1)
        
        st.subheader("Team Performance")
        pb_total = st.number_input("Total Number of PBs", min_value=0, step=1)
        pb_ntb = st.number_input("NTBs done by PBs", min_value=0, step=1)
        
        bdo_total = st.number_input("Total Number of BDOs", min_value=0, step=1)
        bdo_ntb = st.number_input("NTBs done by BDOs", min_value=0, step=1)
        
        bde_total = st.number_input("Total Number of BDEs", min_value=0, step=1)
        bde_ntb = st.number_input("NTBs done by BDEs", min_value=0, step=1)
        
        st.subheader("QR Performance")
        qr_total = st.number_input("Total QR Issued Today", min_value=0, step=1)
        qr_pb = st.number_input("QR Issued by PBs", min_value=0, step=1)
        qr_bdo = st.number_input("QR Issued by BDOs", min_value=0, step=1)
        qr_bde = st.number_input("QR Issued by BDEs", min_value=0, step=1)
    
    submitted = st.form_submit_button("Submit Report", type="primary", use_container_width=True)

if submitted:
    new_row = {
        "Date": report_date,
        "Branch_Code": branch_code,
        "Branch_Name": branch_name,
        "Day_Change_CA": day_change_ca,
        "Day_Change_Total": day_change_total,
        "Var_CA": var_ca,
        "Var_CASA": var_casa,
        "Var_Total": var_total,
        "NTB_Total": ntb_total,
        "NTB_CA": ntb_ca,
        "NTB_Proprietor": ntb_proprietor,
        "PB_Total": pb_total,
        "PB_NTB": pb_ntb,
        "BDO_Total": bdo_total,
        "BDO_NTB": bdo_ntb,
        "BDE_Total": bde_total,
        "BDE_NTB": bde_ntb,
        "QR_Total": qr_total,
        "QR_PB": qr_pb,
        "QR_BDO": qr_bdo,
        "QR_BDE": qr_bde
    }
    
    try:
        df = pd.read_csv(DATA_FILE)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([new_row])
    
    df.to_csv(DATA_FILE, index=False)
    st.success(f"Report submitted successfully for {branch_name} on {report_date}!")
    st.balloons()

st.divider()
st.subheader("Submitted Reports")
if st.button("Refresh Data"):
    st.rerun()

try:
    df = pd.read_csv(DATA_FILE)
    st.dataframe(df.sort_values("Date", ascending=False), use_container_width=True)
    
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download CSV",
        csv,
        f"branch_report_{date.today()}.csv",
        "text/csv",
        type="primary"
    )
except FileNotFoundError:
    st.info("No reports submitted yet.")
