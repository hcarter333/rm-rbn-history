# csv_to_rm_toucans.py

Convert new rows from a CSV export into the SQLite table `rm_rnb_history_pres` in `rm_toucans.db`.  
Rows are **filtered to only those strictly after** a user-supplied cutoff timestamp, CSV timestamps are converted to ISO 8601, obvious numeric fields are coerced, and two extra columns are added as `NULL` placeholders (`f2m`, `launchangle`).

---

## What it does

1. **Reads** a CSV file with the required header fields (see schema below).
2. **Parses** each row’s `timestamp` (`YYYY/MM/DD HH:MM:SS` in the CSV).
3. **Keeps only** rows with `timestamp` **strictly greater than** the `--after` cutoff.
4. **Converts** timestamps to ISO 8601 (`YYYY-MM-DDTHH:MM:SS`) for the DB.
5. **Coerces** select fields to numeric types (integers / floats) when possible; blanks become `NULL`.
6. **Adds** `f2m` and `launchangle` columns as `NULL` on insert.
7. **Inserts** rows into table `rm_rnb_history_pres` in `rm_toucans.db` (or a custom DB path).


---

## Requirements

- **Python**: 3.8+ (standard library only: `argparse`, `csv`, `sqlite3`, `datetime`, `pathlib`)
- **SQLite DB** with a table named `rm_rnb_history_pres` that has the columns listed below.

---

## CSV input schema

The CSV **must** contain at least these headers (order doesn’t matter):

```
id,tx_lng,tx_lat,rx_lng,rx_lat,timestamp,dB,frequency,Spotter,Country,State,County,City,
QSL_Sent,QSL_Rx,QSL_link,QSL_rx_link,tx_rst,park,p2p_s2,call,skcc,naqcc
```

> Notes
> - `timestamp` in the CSV must be in **`YYYY/MM/DD HH:MM:SS`** (e.g., `2023/01/17 10:52:00`).
> - Extra unused columns in the CSV are ignored by `csv.DictReader` as long as required fields exist.

---

## Database table schema (expected columns)

The script inserts into `rm_rnb_history_pres` with this column order:

```
id, tx_lng, tx_lat, rx_lng, rx_lat, timestamp, dB, frequency,
Spotter, Country, State, County, City,
QSL_Sent, QSL_Rx, QSL_link, QSL_rx_link, tx_rst, park, p2p_s2,
call, skcc, naqcc, f2m, launchangle
```

> The script **does not create** the table. Create it yourself once. A minimal compatible example:

```sql
CREATE TABLE IF NOT EXISTS rm_rnb_history_pres (
  id           REAL,        -- coerced to float
  tx_lng       REAL,
  tx_lat       REAL,
  rx_lng       REAL,
  rx_lat       REAL,
  timestamp    TEXT,        -- ISO 8601 'YYYY-MM-DDTHH:MM:SS'
  dB           INTEGER,
  frequency    REAL,
  Spotter      TEXT,
  Country      TEXT,
  State        TEXT,
  County       TEXT,
  City         TEXT,
  QSL_Sent     INTEGER,
  QSL_Rx       TEXT,
  QSL_link     TEXT,
  QSL_rx_link  TEXT,
  tx_rst       INTEGER,
  park         TEXT,
  p2p_s2       TEXT,
  call         TEXT,
  skcc         TEXT,
  naqcc        INTEGER,
  f2m          REAL,        -- inserted as NULL by this script
  launchangle  REAL         -- inserted as NULL by this script
);
```

## Type coercion rules

During insert, fields are converted as follows:

- **Integers**: `dB`, `QSL_Sent`, `tx_rst`, `naqcc`
- **Floats**: `id`, `tx_lng`, `tx_lat`, `rx_lng`, `rx_lat`, `frequency`
- **Strings**: all others (e.g., `Spotter`, `Country`, …)
- **Blank / empty strings** → `NULL`
- **Unparseable numeric values** → `NULL` (row still inserted)

Additionally:

- `f2m` and `launchangle` are set to `NULL` for every inserted row.
- `timestamp` is converted to ISO 8601 text.

---

## Cutoff semantics (`--after`)

- **Required** argument.
- Accepts either:
  - CSV style: `YYYY/MM/DD HH:MM:SS` (e.g., `2025/10/01 00:00:00`)
  - ISO style: `YYYY-MM-DDTHH:MM:SS` (e.g., `2025-10-01T00:00:00`)
- The script **keeps only rows with CSV `timestamp` strictly greater than** the cutoff (`>`).

---

## Usage

```bash
# Basic usage (default DB: ./rm_toucans.db)
python3 csv_to_rm_toucans.py path/to/input.csv --after "2025/10/01 00:00:00"

# Using ISO style cutoff
python3 csv_to_rm_toucans.py path/to/input.csv --after "2025-10-01T00:00:00"

# Custom database path
python3 csv_to_rm_toucans.py path/to/input.csv --after "2025/10/01 00:00:00" --db /path/to/rm_toucans.db
```

---

## Exit behavior and logging

- Prints a one-line summary:  
  `Done. Inserted <N> rows. Skipped <M> rows.`
- Reasons a row can be **skipped**:
  - CSV `timestamp` missing or invalid
  - Row’s timestamp is **not after** the cutoff (it’s `<=`)
  - SQLite insert error (e.g., constraint violation)

*(There is no “dry run” mode; consider copying the DB before running.)*

---

