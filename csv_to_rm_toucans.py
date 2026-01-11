#!/usr/bin/env python3
"""
csv_to_rm_toucans.py

Read a CSV with headers:
id,tx_lng,tx_lat,rx_lng,rx_lat,timestamp,dB,frequency,Spotter,Country,State,County,City,
QSL_Sent,QSL_Rx,QSL_link,QSL_rx_link,tx_rst,park,p2p_s2,call,skcc,naqcc

Filter rows AFTER a cutoff timestamp (YYYY/MM/DD HH:MM:SS),
convert timestamps to ISO (YYYY-MM-DDTHH:MM:SS),
and insert into rm_toucans.db → rm_rnb_history_pres.
"""

import argparse
import csv
import sqlite3
from datetime import datetime
from pathlib import Path

# Timestamp formats
CSV_TIMESTAMP_FMT = "%Y/%m/%d %H:%M:%S"   # e.g. 2023/01/17 10:52:00
DB_TIMESTAMP_FMT  = "%Y-%m-%dT%H:%M:%S"   # e.g. 2023-01-17T10:52:00

# Columns in rm_rnb_history_pres
TABLE_COLUMNS = [
    "id","tx_lng","tx_lat","rx_lng","rx_lat","timestamp","dB","frequency",
    "Spotter","Country","State","County","City",
    "QSL_Sent","QSL_Rx","QSL_link","QSL_rx_link","tx_rst","park","p2p_s2",
    "call","skcc","naqcc","f2m","launchangle"
]

def parse_cutoff(ts: str) -> datetime:
    """
    Parse --after argument. Accepts either:
      - CSV format: YYYY/MM/DD HH:MM:SS
      - DB/ISO format: YYYY-MM-DDTHH:MM:SS
    """
    for fmt in (CSV_TIMESTAMP_FMT, DB_TIMESTAMP_FMT):
        try:
            return datetime.strptime(ts.strip(), fmt)
        except ValueError:
            continue
    raise ValueError(
        f"Cutoff timestamp {ts!r} does not match "
        f"{CSV_TIMESTAMP_FMT!r} or {DB_TIMESTAMP_FMT!r}"
    )

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("csv_path", help="Input CSV path")
    p.add_argument("--after", help="Cutoff timestamp YYYY/MM/DD HH:MM:SS")
    p.add_argument("--db", default="rm_toucans.db", help="SQLite DB path")
    return p.parse_args()

def parse_csv_timestamp(ts: str) -> datetime:
    return datetime.strptime(ts.strip(), CSV_TIMESTAMP_FMT)

def to_db_timestamp(dt: datetime) -> str:
    return dt.strftime(DB_TIMESTAMP_FMT)

def coerce_types(row: dict) -> dict:
    """Convert obvious numeric fields; leave others as strings or None."""
    numeric_int = {"dB","QSL_Sent","tx_rst","naqcc"}
    numeric_float = {"id","tx_lng","tx_lat","rx_lng","rx_lat","frequency"}
    out = {}
    for k,v in row.items():
        if v is None or str(v).strip() == "":
            out[k] = None
            continue
        if k in numeric_int:
            try:
                out[k] = int(v)
                continue
            except ValueError:
                out[k] = None
        elif k in numeric_float:
            try:
                out[k] = float(v)
                continue
            except ValueError:
                out[k] = None
        else:
            out[k] = str(v)
    return out

def cutoff_from_db(db_path: str) -> datetime:
    query = """
        select
        max(timestamp)
        from
          rm_rnb_history_pres
        order by
          rowid
        limit
          101
    """
    if not Path(db_path).exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    try:
        with sqlite3.connect(db_path) as conn:
            result = conn.execute(query).fetchone()
    except sqlite3.OperationalError as exc:
        raise sqlite3.OperationalError(
            f"Unable to read rm_rnb_history_pres from {db_path}: {exc}"
        ) from exc
    if not result or result[0] is None:
        return datetime.min
    return parse_cutoff(result[0])

def main():
    args = parse_args()
    if args.after:
        cutoff_dt = parse_cutoff(args.after)
    else:
        cutoff_dt = cutoff_from_db(args.db)

    # Prepare insert SQL
    placeholders = ", ".join(["?"]*len(TABLE_COLUMNS))
    colnames = ", ".join(TABLE_COLUMNS)
    sql = f"INSERT INTO rm_rnb_history_pres ({colnames}) VALUES ({placeholders})"

    conn = sqlite3.connect(args.db)
    inserted = 0
    skipped = 0
    earliest_inserted = None
    latest_inserted = None

    with open(args.csv_path,newline="",encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                dt = parse_csv_timestamp(row["timestamp"])
            except Exception:
                skipped += 1
                continue
            if dt <= cutoff_dt:
                continue

            # Transform timestamp
            row["timestamp"] = to_db_timestamp(dt)

            # Add NULLs for f2m, launchangle
            row["f2m"] = None
            row["launchangle"] = None

            # Coerce types
            row = coerce_types(row)

            # Build ordered tuple
            values = [row.get(c) for c in TABLE_COLUMNS]
            try:
                conn.execute(sql, values)
                inserted += 1
                if earliest_inserted is None or dt < earliest_inserted:
                    earliest_inserted = dt
                if latest_inserted is None or dt > latest_inserted:
                    latest_inserted = dt
            except Exception:
                skipped += 1

    conn.commit()
    conn.close()
    print(f"Done. Inserted {inserted} rows. Skipped {skipped} rows.")
    if inserted:
        print(f"Earliest inserted timestamp: {to_db_timestamp(earliest_inserted)}")
        print(f"Latest inserted timestamp: {to_db_timestamp(latest_inserted)}")
    else:
        print("Earliest inserted timestamp: N/A")
        print("Latest inserted timestamp: N/A")

if __name__ == "__main__":
    main()
