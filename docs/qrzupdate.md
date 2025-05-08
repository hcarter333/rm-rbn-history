# QSO‑ADIF Upload Script

A command‑line Python tool to:

1. Query a local Datasette instance for ham‑radio QSO records (with and without ADIF output).
2. Merge transmission coordinates into each ADIF record.
3. Compute and insert Maidenhead grid‑square, formatted lat/lon fields.
4. Upload the enriched ADIF records to the QRZ.com Logbook API.

---

## Table of Contents

* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Usage](#usage)
* [Implementation Overview](#implementation-overview)
* [Key APIs & Endpoints](#key-apis--endpoints)
* [Functions](#functions)
* [Environment Variables](#environment-variables)
* [Error Handling & Logging](#error-handling--logging)

---

## Prerequisites

* Python 3.7+
* `requests` library
* Access to a local Datasette instance serving your QSO database at `http://192.168.0.203/sam_datasette/…`
* QRZ.com Logbook API key

```bash
pip install requests
```

---

## Installation

Clone your repo and place the script, e.g.:

```
scripts/upload_qso_adif.py
```

Make it executable:

```bash
chmod +x scripts/upload_qso_adif.py
```

---

## Usage

```bash
./scripts/upload_qso_adif.py
```

The script will prompt for:

1. **Start datetime** (ISO format, e.g. `2025-02-09T01:17:00`)
2. **End datetime** (ISO format)
3. **Optional spotter callsign** (filter QSOs by Spotter)

It then:

* Fetches TX coordinates via HTML query
* Fetches ADIF records via `.adif` endpoint
* Parses, enriches and displays modified ADIF records
* Asks for confirmation, then uploads each to QRZ

---

## Implementation Overview

1. **Build SQL query string**:

   * `build_sql_query(start, end, spotter)`
   * Validates ISO timestamps
   * Filters on `dB > 100`, date range, optional spotter. `db > 100 ` eliminates RBN spots as QSOs.

2. **Fetch Coordinates**:

   * `fetch_tx_coords(sql)` against
     `http://192.168.0.203/sam_datasette/rm_toucans?sql=…`
   * Parses HTML table rows to extract `<td class="col‑tx_lat">` & `<td class="col‑tx_lng">`

3. **Fetch ADIF**:

   * `fetch_adif_records(sql)` against
     `http://192.168.0.203/sam_datasette/rm_toucans.adif?sql=…`

4. **Enrich Records**:

   * Split on `<eor>`
   * For each record:

     * Compute Maidenhead locator (`maidenhead_locator`)
     * Format lat/lon as `NDDD MM.MMM` / `WDDD MM.MMM` (`format_coord`)
     * Insert `<MY_GRIDSQUARE:…>`, `<MY_LAT:…>`, `<MY_LON:…>`

5. **Upload to QRZ**:

   * `send_to_qrz(adif_record, key)` → `https://logbook.qrz.com/api`

---

## Key APIs & Endpoints

| Function               | Endpoint                                                                                                   | Method | Notes                             |
| ---------------------- | ---------------------------------------------------------------------------------------------------------- | ------ | --------------------------------- |
| fetch\_tx\_coords()    | [http://192.168.0.203/sam\_datasette/rm\_toucans](http://192.168.0.203/sam_datasette/rm_toucans)           | GET    | HTML table output                 |
| fetch\_adif\_records() | [http://192.168.0.203/sam\_datasette/rm\_toucans.adif](http://192.168.0.203/sam_datasette/rm_toucans.adif) | GET    | ADIF‑formatted QSO log            |
| send\_to\_qrz()        | [https://logbook.qrz.com/api](https://logbook.qrz.com/api)                                                 | POST   | QRZ Logbook API, requires API key |

---

## Functions

### maidenhead\_locator(lat, lon)

Compute 6‑character Maidenhead grid square from decimal degrees.

### extract\_field(adif\_record, field\_name)

Regex‑extract `<FIELD:len>value` from an ADIF record.

### build\_sql\_query(start, end, spotter=None)

Validate ISO datetimes and construct the SQL query string.

### parse\_coords(html\_data)

Regex‑parse TX latitude/longitude from HTML table rows.

### format\_coord(coord, is\_lat)

Format decimal degrees as `XDDD MM.MMM` with N/S/E/W prefix.

### send\_to\_qrz(adif\_record, qrz\_access\_key)

POST to QRZ Logbook API with payload `{KEY, ACTION:INSERT, ADIF}`.

---

## Environment Variables

* `QRZ_KD0FNR_LOG_KEY` — QRZ Logbook API key.
  Export before running:

  ```bash
  export QRZ_KD0FNR_LOG_KEY="your_api_key_here"
  ```

---

## Error Handling & Logging

* Network errors (non‑200 responses) raise `ConnectionError`.
* Invalid datetime formats raise `ValueError`.
* Missing coords fall back to extracting fields from ADIF.
* Warnings printed for missing or unparsable values.

---
