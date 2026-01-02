import pandas as pd
from data_merge import merge_bbh_daily

def build_acceptance(bbh_file, daily_file, lnbts_list):
    """
    Build LTE Acceptance Sheet per LNBTS and LNCEL.
    """

    # Merge BBH + Daily (cell-level)
    df = merge_bbh_daily(bbh_file, daily_file)

    # Filter by selected LNBTS
    df = df[df["LNBTS name"].isin(lnbts_list)]

    # KPI list
    kpi_list = [
        "Average CQI",
        "Avg RRC conn UE2",
        "Avg UE distance",
        "Cell Avail excl BLU",
        "E-RAB DR RAN",
        "E-UTRAN Avg PRB usage per TTI DL",
        "E-UTRAN E-RAB stp SR",
        "Init Contx stp SR for CSFB",
        "Intra eNB HO SR",
        "Avg IP thp DL QCI9",
        "Total E-UTRAN RRC conn stp SR",
        "Total LTE data volume, DL + UL",
        "Total LTE Traffic (24 Hr)",
        "VoLTE total traffic"
    ]

    # Build rows for pivot
    acceptance_rows = []
    for _, row in df.iterrows():
        for kpi in kpi_list:
            if kpi not in row:
                continue
            acceptance_rows.append({
                "LNBTS name": row["LNBTS name"],
                "LNCEL name": row["LNCEL name"],
                "KPI NAME": kpi,
                "Date": row["Date"],
                "Value": row[kpi]
            })

    acceptance_df = pd.DataFrame(acceptance_rows)

    # Pivot for acceptance format
    if not acceptance_df.empty:
        acceptance_df = acceptance_df.pivot_table(
            index=["LNBTS name", "LNCEL name", "KPI NAME"],
            columns='Date',
            values='Value',
            aggfunc="first"
        ).reset_index()

        acceptance_df.columns.name = None

    return acceptance_df

