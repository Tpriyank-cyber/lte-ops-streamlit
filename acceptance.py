import pandas as pd
from data_merge import merge_bbh_daily

ACCEPTANCE_KPIS = {
    "Cell Avail excl BLU": "Cell Avail excl BLU",
    "E-UTRAN Avg PRB usage per TTI DL": "E-UTRAN Avg PRB usage per TTI DL",
    "Average CQI": "Average CQI",
    "Avg UE distance": "Avg UE distance",
    "Avg RRC conn UE2": "Avg RRC conn UE",
    "E-RAB DR RAN": "E-RAB DR RAN",
    "E-UTRAN E-RAB stp SR": "E-UTRAN E-RAB stp SR",
    "Init Contx stp SR for CSFB": "Init Contx stp SR for CSFB",
    "Intra eNB HO SR": "Intra eNB HO SR",
    "Avg IP thp DL QCI9": "Non-GBR DL Thrpt",

    # 🔥 Special handling
    "Total LTE Payload (Combined)": "Total LTE Payload (Combined)",
    "VoLTE total traffic": "VoLTE total traffic"
}

def build_acceptance(bbh_file, daily_file, lnbts):
    df = merge_bbh_daily(bbh_file, daily_file)
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%d-%b")

    if lnbts != "ALL":
        df = df[df["LNBTS name"] == lnbts]

    final = []

    for kpi, col in ACCEPTANCE_KPIS.items():
        if col not in df.columns:
            continue

        temp = df[
            ["LNBTS name", "LNCEL name", "Date", col]
        ].rename(columns={col: "Value"})

        pivot = temp.pivot_table(
            index=["LNBTS name", "LNCEL name"],
            columns="Date",
            values="Value",
            aggfunc="mean"
        ).reset_index()

        pivot.insert(2, "KPI NAME", kpi)
        final.append(pivot)

    return pd.concat(final, ignore_index=True)
