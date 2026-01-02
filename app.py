import streamlit as st
import pandas as pd
import io
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
    lnbts_input = st.text_input("LNBTS Name (or ALL)", value="ALL")

    if st.button("Generate Acceptance Sheet"):
        if bbh and daily:
            # Handle LNBTS
            if lnbts_input.upper() != "ALL":
                lnbts_list = [x.strip() for x in lnbts_input.split(",")]
            else:
                lnbts_list = None

            df = build_acceptance(bbh, daily, lnbts_list)
            st.dataframe(df)

            # Download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False)
            st.download_button(
                "⬇ Download Acceptance Sheet",
                data=output.getvalue(),
                file_name="Acceptance.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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

    lnbts_input2 = st.text_input("LNBTS Name (or ALL)", value="ALL", key="lnbts2")

    if st.button("Generate BBH Tracker"):
        if bbh and daily:
            if lnbts_input2.upper() != "ALL":
                lnbts_list2 = [x.strip() for x in lnbts_input2.split(",")]
            else:
                lnbts_list2 = None

            df = build_bbh_tracker(bbh, daily, lnbts_list2, existing)
            st.dataframe(df)

            # Download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                df.to_excel(writer, index=False)
            st.download_button(
                "⬇ Download BBH Tracker",
                data=output.getvalue(),
                file_name="BBH_Tracker.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Upload both BBH and Daily files")
