import streamlit as st
import pandas as pd
from acceptance import build_acceptance
from bbh_tracker import build_bbh_tracker

st.set_page_config(page_title="LTE Ops Chatbot", layout="wide")
st.title("📡 LTE Daily RNA / Acceptance / BBH Tracker")

tab1, tab2 = st.tabs(["✅ Acceptance Sheet", "📊 BBH Tracker"])

# ---------------- ACCEPTANCE ----------------
with tab1:
    st.subheader("Acceptance Sheet Generator")

    bbh = st.file_uploader("Upload BBH RAW File", type="xlsx")
    daily = st.file_uploader("Upload Daily LTE File", type="xlsx")

    lnbts = st.text_input("LNBTS Name (or ALL)", value="ALL")

    if st.button("Generate Acceptance Sheet"):
        if bbh and daily:
            df = build_acceptance(bbh, daily, lnbts)
            st.dataframe(df)

            st.download_button(
                "⬇ Download Acceptance Sheet",
                df.to_excel(index=False, engine="xlsxwriter"),
                "Acceptance.xlsx"
            )
        else:
            st.warning("Upload both BBH and Daily files")

# ---------------- BBH TRACKER ----------------
with tab2:
    st.subheader("BBH Tracker")

    bbh = st.file_uploader("Upload BBH RAW File", type="xlsx", key="bbh2")
    daily = st.file_uploader("Upload Daily LTE File", type="xlsx", key="daily2")

    mode = st.radio("Tracker Mode", ["New BBH Tracker", "Update Existing Tracker"])

    existing = None
    if mode == "Update Existing Tracker":
        existing_file = st.file_uploader("Upload Existing BBH Tracker", type="xlsx")
        if existing_file:
            existing = pd.read_excel(existing_file)

    lnbts = st.text_input("LNBTS Name (or ALL)", value="ALL", key="lnbts2")

    if st.button("Generate BBH Tracker"):
        if bbh and daily:
            df = build_bbh_tracker(bbh, daily, lnbts, existing)
            st.dataframe(df)

            st.download_button(
                "⬇ Download BBH Tracker",
                df.to_excel(index=False, engine="xlsxwriter"),
                "BBH_Tracker.xlsx"
            )
        else:
            st.warning("Upload both BBH and Daily files")
