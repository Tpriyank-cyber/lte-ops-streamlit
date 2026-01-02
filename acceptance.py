import pandas as pd
from data_merge import merge_bbh_daily

# ---------- BUILD ACCEPTANCE SHEET ----------
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
        "Non-GBR DL Thrpt",
        "Total E-UTRAN RRC conn stp SR",
        "Total LTE data volume, DL + UL",
        "Total LTE Traffic (24 Hr)",
        "VoLTE total traffic"
    ]

    # ---------- PIVOT TO ACCEPTANCE FORMAT ----------
    acceptance_rows = []

    for _, row in df.iterrows():
        for kpi in kpi_list:
            if kpi not in row:
                continue  # skip missing KPIs
            acceptance_rows.append({
                "LNBTS name": row["LNBTS name"],
                "LNCEL name": row["LNCEL name"],
                "KPI NAME": kpi,
                str(row["Date"]): row[kpi]  # date as column
            })

    acceptance_df = pd.DataFrame(acceptance_rows)

    # ---------- COMBINE SAME KPI ROWS (MULTI-DATE) ----------
    if not acceptance_df.empty:
        acceptance_df = acceptance_df.pivot_table(
            index=["LNBTS name", "LNCEL name", "KPI NAME"],
            columns=acceptance_df.columns[-1],  # the date column
            values=acceptance_df.columns[-2],  # the KPI value
            aggfunc="first"  # should be single value
        ).reset_index()

        # Rename columns properly
        acceptance_df.columns.name = None

    return acceptance_df
