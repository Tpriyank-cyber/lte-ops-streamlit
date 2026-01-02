import pandas as pd

def merge_bbh_daily(bbh_file, daily_file):

    # ---------------- READ FILES ----------------
    bbh = pd.read_excel(bbh_file)
    daily = pd.read_excel(daily_file)

    bbh.columns = bbh.columns.str.strip()
    daily.columns = daily.columns.str.strip()

    # ---------------- TIME HANDLING ----------------
    bbh["Period start time"] = pd.to_datetime(bbh["Period start time"])
    bbh["Date"] = bbh["Period start time"].dt.date
    bbh["Hour"] = bbh["Period start time"].dt.hour

    daily["Period start time"] = pd.to_datetime(daily["Period start time"])
    daily["Date"] = daily["Period start time"].dt.date

    # ---------------- IDENTIFY NUMERIC KPI COLUMNS ----------------
    key_cols = [
        "Period start time",
        "Date",
        "Hour",
        "MRBTS name",
        "LNBTS name",
        "LNCEL name"
    ]

    kpi_cols = [c for c in bbh.columns if c not in key_cols]

    # Convert KPI columns to numeric safely
    for col in kpi_cols:
        bbh[col] = (
            bbh[col]
            .astype(str)
            .str.replace(",", "", regex=False)
        )
        bbh[col] = pd.to_numeric(bbh[col], errors="coerce")

    # ---------------- BUILD AGG MAP ----------------
    sum_keywords = [
        "Traffic",
        "volume",
        "PDU",
        "Payload",
        "Volume"
    ]

    agg_map = {}
    for col in kpi_cols:
        if any(k.lower() in col.lower() for k in sum_keywords):
            agg_map[col] = "sum"
        else:
            agg_map[col] = "mean"

    # ---------------- HOURLY → DAILY AGGREGATION ----------------
    bbh_daily = (
        bbh
        .groupby(["Date", "LNBTS name", "LNCEL name"], as_index=False)
        .agg(agg_map)
    )

    # ---------------- MERGE WITH DAILY FILE ----------------
    merged = pd.merge(
        bbh_daily,
        daily[
            [
                "Date",
                "LNBTS name",
                "LNCEL name",
                "Total LTE data volume, DL + UL",
                "VoLTE total traffic"
            ]
        ],
        on=["Date", "LNBTS name", "LNCEL name"],
        how="left",
        suffixes=("_BBH", "_DAILY")
    )

    # ---------------- FINAL KPI DERIVATION ----------------
    merged["Total LTE Payload (Combined)"] = (
        merged["Total LTE data volume, DL + UL_BBH"].fillna(0)
        + merged["Total LTE data volume, DL + UL_DAILY"].fillna(0)
    )

    return merged
