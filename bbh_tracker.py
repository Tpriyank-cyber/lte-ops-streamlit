import pandas as pd
from data_merge import merge_bbh_daily

BBH_KPIS = [
    "Cell Avail excl BLU",
    "E-UTRAN Avg PRB usage per TTI DL",
    "% MIMO RI 2",
    "% MIMO RI 1",
    "Init Contx stp SR for CSFB",
    "RACH Stp Completion SR",
    "SINR_PUSCH_AVG (M8005C95)",
    "SINR_PUCCH_AVG (M8005C92)",
    "Avg RSSI for PUSCH",
    "RSSI_PUCCH_AVG (M8005C2)",
    "Avg PDCP cell thp DL",
    "Avg IP thp DL QCI9",
    "Avg UE distance",
    "Average CQI",
    "Avg RRC conn UE",
    "inter eNB E-UTRAN HO SR X2",
    "Intra eNB HO SR",
    "E-RAB DR RAN",
    "E-UTRAN E-RAB stp SR",
    "Total E-UTRAN RRC conn stp SR",
    "Avg IP thp DL QCI6",
    "Avg IP thp DL QCI8",
    "Avg IP thp DL QCI7",
    "Avg DL User throughput",
    "Avg UL User throughput",
    "Total LTE Payload (24)",
    "VoLTE total traffic"
]

def build_bbh_tracker(bbh_file, daily_file, lnbts, existing=None):
    df = merge_bbh_daily(bbh_file, daily_file)
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%d-%b")

    if lnbts != "ALL":
        df = df[df["LNBTS name"] == lnbts]

    output = []

    for kpi in BBH_KPIS:
        if kpi not in df.columns:
            continue

        temp = df[
            ["LNBTS name", "LNCEL name", "Date", kpi]
        ].rename(columns={kpi: "Value"})

        pivot = temp.pivot_table(
            index=["LNBTS name", "LNCEL name"],
            columns="Date",
            values="Value",
            aggfunc="mean"
        ).reset_index()

        pivot.insert(2, "KPI NAME", kpi)
        output.append(pivot)

    new_data = pd.concat(output, ignore_index=True)

    if existing is not None:
        return pd.concat([existing, new_data], ignore_index=True)

    return new_data

