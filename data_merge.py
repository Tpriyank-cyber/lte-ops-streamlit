import pandas as pd

def merge_bbh_daily(bbh_file, daily_file):

    # -------- READ FILES --------
    bbh = pd.read_excel(bbh_file)
    daily = pd.read_excel(daily_file)

    bbh.columns = bbh.columns.str.strip()
    daily.columns = daily.columns.str.strip()

    # -------- TIME HANDLING --------
    bbh["Period start time"] = pd.to_datetime(bbh["Period start time"])
    bbh["Date"] = bbh["Period start time"].dt.date
    bbh["Hour"] = bbh["Period start time"].dt.hour

    daily["Period start time"] = pd.to_datetime(daily["Period start time"])
    daily["Date"] = daily["Period start time"].dt.date

    # -------- CLEAN NUMERIC KPIs --------
    id_cols = [
        "Period start time", "Date", "Hour",
        "MRBTS name", "LNBTS name", "LNCEL name"
    ]

    kpi_cols = [c for c in bbh.columns if c not in id_cols]

    for col in kpi_cols:
        bbh[col] = (
            bbh[col]
            .astype(str)
            .str.replace(",", "", regex=False)
        )
        bbh[col] = pd.to_numeric(bbh[col], errors="coerce")

    # -------- RENAME DAILY PAYLOAD --------
    daily = daily.rename(columns={"Total LTE data volume, DL + UL": "Total LTE Traffic (24 Hr)"})

    # -------- MERGE DAILY FILE (KEEP BBH CELLS AND DAILY PAYLOAD) --------
    merged = pd.merge(
        bbh,
        daily[["Date", "LNBTS name", "LNCEL name", "Total LTE Traffic (24 Hr)", "VoLTE total traffic"]],
        on=["Date", "LNBTS name", "LNCEL name"],
        how="left",
        suffixes=("_BBH", "_DAILY")
    )

    return merged
