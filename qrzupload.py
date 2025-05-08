#!/usr/bin/env python3
import os
import re
import requests
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

def maidenhead_locator(latitude, longitude):
    """
    Given a latitude and longitude in decimal degrees,
    return the Maidenhead grid square (6-character locator).
    """
    # Adjust coordinates
    adj_lon = longitude + 180.0
    adj_lat = latitude + 90.0

    # Field (first two characters)
    lon_field = int(adj_lon // 20)
    lat_field = int(adj_lat // 10)
    field = chr(lon_field + ord('A')) + chr(lat_field + ord('A'))

    # Square (next two digits)
    lon_square = int((adj_lon % 20) // 2)
    lat_square = int(adj_lat % 10)
    square = f"{lon_square}{lat_square}"

    # Subsquare (last two characters)
    lon_subsquare = int(((adj_lon % 2) / 2) * 24)
    lat_subsquare = int(((adj_lat % 1)) * 24)
    subsquare = chr(lon_subsquare + ord('a')) + chr(lat_subsquare + ord('a'))

    return field + square + subsquare

def extract_field(adif_record, field_name):
    """
    Extract the value of a given ADIF field from an ADIF record.
    Assumes the field is in the format <FIELD_NAME:len>value.
    The search is case-insensitive.
    """
    pattern = r"<{}:(\d+)>([^<\s]+)".format(re.escape(field_name))
    match = re.search(pattern, adif_record, re.IGNORECASE)
    if match:
        return match.group(2)
    return None

def build_sql_query(start_str, end_str, spotter=None):
    """
    Build the SQL query using the provided date range.
    Uses the ISO datetime strings as provided (keeping the 'T' between date and time).

    If a spotter callsign is provided (non-empty), adds a case-insensitive condition
    to filter QSOs where the Spotter field matches the given callsign.
    """
    try:
        datetime.fromisoformat(start_str)
        datetime.fromisoformat(end_str)
    except Exception as e:
        raise ValueError("Invalid datetime format. Please use ISO format like 2025-02-09T01:17:00") from e

    query = (
        "select\r\n"
        "  rowid,\r\n"
        "  id,\r\n"
        "  tx_lng,\r\n"
        "  tx_lat,\r\n"
        "  rx_lng,\r\n"
        "  rx_lat,\r\n"
        "  timestamp,\r\n"
        "  strftime('%Y%m%d', timestamp) as date,\r\n"
        "  strftime('%H%M', timestamp) as time,\r\n"
        "  dB,\r\n"
        "  frequency,\r\n"
        "  Spotter,\r\n"
        "  Country,\r\n"
        "  State,\r\n"
        "  County,\r\n"
        "  City,\r\n"
        "  QSL_Sent,\r\n"
        "  QSL_Rx,\r\n"
        "  QSL_link,\r\n"
        "  QSL_rx_link,\r\n"
        "  tx_rst,\r\n"
        "  325 as ionosonde,\r\n"
        "  -5 as elev_tx,\r\n"
        "  \"US-4578\" as park,\r\n"
        "  'KD0FNR' as call,\r\n"
        "  p2p_s2,\r\n"
        "  301 as f2m,\r\n"
        "  call\r\n"
        "from\r\n"
        "  rm_rnb_history_pres\r\n"
        "where\r\n"
        "  dB > 100\r\n"
        f"  and timestamp > '{start_str}'\r\n"
        f"  and timestamp < '{end_str}'\r\n"
    )
    if spotter:
        query += f"  and lower(Spotter) = '{spotter.lower()}'\r\n"
    query += "order by\r\n  timestamp\r\n"
    return query

def fetch_tx_coords(sql_query):
    """
    Fetch the QSOs (without .adif) to retrieve the tx_lat and tx_lng values.
    Returns the HTML page as text.
    """
    base_url = "http://192.168.0.203/sam_datasette/rm_toucans"  # no .adif here
    params = {'sql': sql_query}
    url = base_url + "?" + urllib.parse.urlencode(params)
    print("Fetching TX coordinates from:")
    print(url)
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError(f"Error fetching TX coordinates: {response.status_code}")
    return response.text

#We'll eventually ship off adif records to QRZ, so this is an easy shortcut using the 
#already existing adif generator for POTA logs
#That generator never included lat and lng, so the tx_lat and tx_lng coordinates are 
#pulled directly from QSO records above
def fetch_adif_records(sql_query):
    """
    Fetch the full ADIF records from the local endpoint using the .adif URL.
    Returns the response text.
    """
    base_url = "http://192.168.0.203/sam_datasette/rm_toucans.adif"
    params = {'sql': sql_query}
    url = base_url + "?" + urllib.parse.urlencode(params)
    print("Fetching ADIF records from:")
    print(url)
    response = requests.get(url)
    if response.status_code != 200:
        raise ConnectionError(f"Error fetching ADIF records: {response.status_code}")
    return response.text

def parse_coords(html_data):
    """
    Parse the provided HTML page to extract a list of (tx_lat, tx_lng) tuples.
    This function looks for each <tr> row and then extracts the values from
    the <td> cells with class "col-tx_lat" and "col-tx_lng".
    """
    coords = []
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html_data, re.DOTALL | re.IGNORECASE)
    for row in rows:
        lat_match = re.search(r'<td[^>]*class=["\']col-tx_lat["\'][^>]*>(.*?)</td>', row, re.DOTALL | re.IGNORECASE)
        lng_match = re.search(r'<td[^>]*class=["\']col-tx_lng["\'][^>]*>(.*?)</td>', row, re.DOTALL | re.IGNORECASE)
        if lat_match and lng_match:
            lat_text = lat_match.group(1).strip().replace('&nbsp;', '')
            lng_text = lng_match.group(1).strip().replace('&nbsp;', '')
            try:
                lat = float(lat_text)
                lng = float(lng_text)
                coords.append((lat, lng))
            except Exception:
                coords.append((None, None))
    return coords

def format_coord(coord, is_lat):
    """
    Format a coordinate as an 11-character string in the format:
    XDDD MM.MMM
    where:
      X is a directional character (for latitude: N if coord>=0, S if <0;
         for longitude: E if coord>=0, W if <0),
      DDD is the 3-digit degrees with leading zeroes,
      MM.MMM is the minutes with its decimal point in the third position.
    """
    if is_lat:
        direction = "N" if coord >= 0 else "S"
    else:
        direction = "E" if coord >= 0 else "W"
    abs_val = abs(coord)
    deg = int(abs_val)
    minutes = (abs_val - deg) * 60
    # Format minutes as exactly MM.MMM (6 characters)
    return f"{direction}{deg:03d} {minutes:06.3f}"

def send_to_qrz(adif_record, qrz_access_key):
    """
    Send a single ADIF record to the QRZ logbook API using the INSERT action.
    """
    api_url = "https://logbook.qrz.com/api"
    payload = {
        'KEY': qrz_access_key,
        'ACTION': 'INSERT',
        'ADIF': adif_record
    }
    headers = {
        'User-Agent': "MyCoolUploadScript.py/1.0.0 (KD0FNR)"
    }
    print("Sending record to QRZ Logbook API...")
    response = requests.post(api_url, data=payload, headers=headers)
    return response.text

def main():
    # Step 1: Get the date range and optional spotter callsign from the user.
    start_input = input("Enter start datetime (ISO format, e.g. 2025-02-09T01:17:00): ").strip()
    end_input = input("Enter end datetime (ISO format, e.g. 2025-02-10T01:17:00): ").strip()
    spotter_input = input("Enter a spotter callsign to filter by (or leave blank for all): ").strip()

    # Build the SQL query with the provided date range and optional spotter filter.
    try:
        sql_query = build_sql_query(start_input, end_input, spotter_input if spotter_input else None)
    except Exception as e:
        print("Error building SQL query:", e)
        return

    # Step 2: Retrieve TX coordinates (tx_lat and tx_lng) from the non-ADIF URL.
    try:
        coords_html = fetch_tx_coords(sql_query)
        coords_list = parse_coords(coords_html)
    except Exception as e:
        print("Error fetching TX coordinates:", e)
        return

    # Step 3: Retrieve the full ADIF records (using the .adif URL).
    try:
        adif_data = fetch_adif_records(sql_query)
    except Exception as e:
        print("Error fetching ADIF records:", e)
        return

    # Step 4: Split the ADIF data into individual records.
    raw_records = [rec.strip() for rec in adif_data.split("<eor>") if rec.strip()]
    modified_records = []
    for idx, rec in enumerate(raw_records, 1):
        # Append <eor> if missing.
        if not rec.endswith("<eor>"):
            rec = rec + " <eor>"
        # Use the corresponding coordinate from the list (if available).
        if idx - 1 < len(coords_list):
            tx_lat, tx_lng = coords_list[idx - 1]
        else:
            tx_lat, tx_lng = None, None

        if tx_lat is None or tx_lng is None:
            print(f"Warning: Missing tx_lat/tx_lng for record {idx}. Attempting to extract from record.")
            tx_lat_str = extract_field(rec, "tx_lat")
            tx_lng_str = extract_field(rec, "tx_lng")
            try:
                tx_lat = float(tx_lat_str) if tx_lat_str is not None else None
                tx_lng = float(tx_lng_str) if tx_lng_str is not None else None
            except Exception:
                tx_lat, tx_lng = None, None

        # Calculate grid square field if possible.
        if tx_lat is not None and tx_lng is not None:
            try:
                grid_square = maidenhead_locator(tx_lat, tx_lng)
                grid_field = f" <MY_GRIDSQUARE:{len(grid_square)}>{grid_square}"
            except Exception as e:
                print(f"Error calculating grid square for record {idx}: {e}")
                grid_field = ""
        else:
            grid_field = ""

        # Compute MY_LAT and MY_LON fields in the required format.
        if tx_lat is not None and tx_lng is not None:
            formatted_lat = format_coord(tx_lat, True)
            formatted_lon = format_coord(tx_lng, False)
            my_lat_field = f" <MY_LAT:{len(formatted_lat)}>{formatted_lat}"
            my_lon_field = f" <MY_LON:{len(formatted_lon)}>{formatted_lon}"
        else:
            my_lat_field = ""
            my_lon_field = ""

        # Insert the new fields (grid, MY_LAT, and MY_LON) before the <eor> tag.
        if rec.strip().endswith("<eor>"):
            record_modified = rec.rstrip()[:-5] + grid_field + my_lat_field + my_lon_field + " <eor>"
        else:
            record_modified = rec + grid_field + my_lat_field + my_lon_field
        modified_records.append(record_modified)

    if not modified_records:
        print("No records found to send.")
        return

    # Step 5: Display each modified record for confirmation.
    print("\n--- Modified ADIF Records to be Sent ---")
    for idx, rec in enumerate(modified_records, 1):
        print(f"\nRecord {idx}:\n{rec}\n")
    print("----------------------------\n")
    confirm = input("Send all of the above records to QRZ? (Y/n): ").strip().lower()
    if confirm not in ['', 'y', 'yes']:
        print("Aborted by user.")
        return

    # Step 6: Retrieve the QRZ logbook key from the environment variable.
    qrz_access_key = os.getenv("QRZ_KD0FNR_LOG_KEY")
    if not qrz_access_key:
        print("Error: QRZ_KD0FNR_LOG_KEY environment variable is not set!")
        return

    # Step 7: Send each modified record to QRZ individually.
    for idx, record in enumerate(modified_records, 1):
        print(f"\nSending record {idx}/{len(modified_records)}...")
        try:
            result = send_to_qrz(record, qrz_access_key)
            print(f"QRZ Response for record {idx}:")
            print(result)
        except Exception as e:
            print(f"Error sending record {idx} to QRZ:", e)

if __name__ == '__main__':
    main()
