import pandas as pd
from data_merge import merge_bbh_daily

def build_acceptance(bbh_file, daily_file, lnbts_list):
    """
    Build LTE Acceptance Sheet per LNBTS and LNCEL.

    Args:
        bbh_file (str): Path to BBH raw file
        daily_file (str): Path to Daily LTE file
        lnbts_list (list): List of LNBTS names to include

    Returns:
        pd.DataFrame: Acceptance sheet
    """

    # Merge BBH + Daily (cell-level)
    df = merge_bbh_daily(bbh_file, daily_file)

    # Filter by selected LNBTS
    df = df[df["LNBTS name"].isin(lnbts_list)]

    # ---------- KPI LIST ----------
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

    # ---------- BUILD ROWS FOR PIVOT ----------
    acceptance_rows = []
    for _, row in df.iterrows():
        for kpi in kpi_list:
            if kpi not in row:
                continue
            # Special handling
            if kpi == "Total LTE Traffic (24 Hr)":
                value = row["Total LTE Payload (24)"]  # BBH + Daily
            elif kpi == "VoLTE total traffic":
                value = row["VoLTE total traffic"]  # Daily only
            else:
                value = row[kpi]

            acceptance_rows.append({
                "LNBTS name": row["LNBTS name"],
                "LNCEL name": row["LNCEL name"],
                "KPI NAME": kpi,
                "Date": row["Date"],
                "Value": value
            })

    acceptance_df = pd.DataFrame(acceptance_rows)

    # ---------- PIVOT TO ACCEPTANCE FORMAT ----------
    if not acceptance_df.empty:
        acceptance_df = acceptance_df.pivot_table(
            index=["LNBTS name", "LNCEL name", "KPI NAME"],
            columns='Date',
            values='Value',
            aggfunc="first"  # single value expected
        ).reset_index()

        # Rename columns properly
        acceptance_df.columns.name = None

    return acceptance_df

