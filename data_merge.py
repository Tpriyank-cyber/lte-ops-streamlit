import pandas as pd

def merge_bbh_daily(bbh_file, daily_file):
    # Read files
    bbh = pd.read_excel(bbh_file)
    daily = pd.read_excel(daily_file)

    # Clean headers
    bbh.columns = bbh.columns.str.strip()
    daily.columns = daily.columns.str.strip()

    # ---------------- BBH TIME SPLIT ----------------
    bbh["Period start time"] = pd.to_datetime(bbh["Period start time"])

    bbh["Date"] = bbh["Period start time"].dt.date
    bbh["Hour"] = bbh["Period start time"].dt.hour

    # ---------------- DAILY TIME ----------------
    daily["Period start time"] = pd.to_datetime(daily["Period start time"])
    daily["Date"] = daily["Period start time"].dt.date

    # ---------------- AGGREGATE BBH (Hourly → Daily) ----------------
    agg_map = {}

    for col in bbh.columns:
        if col in [
            "Date", "Hour", "LNBTS name", "LNCEL name",
            "Period start time"
        ]:
            continue

        # Traffic KPIs → SUM
        if "Traffic" in col or "volume" in col or "PDU" in col:
            agg_map[col] = "sum"
        else:
            # Performance KPIs → MEAN
            agg_map[col] = "mean"

    bbh_daily = bbh.groupby(
        ["Date", "LNBTS name", "LNCEL name"],
        as_index=False
    ).agg(agg_map)

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

    # ---------------- FINAL KPI LOGIC ----------------
    merged["Total LTE Payload (Combined)"] = (
        merged["Total LTE data volume, DL + UL_BBH"].fillna(0)
        + merged["Total LTE data volume, DL + UL_DAILY"].fillna(0)
    )

    return merged
