#Queries the POTA user databse to find hte input callsign
#usage: python3 extract_callsigns.py qso_update.csv | python3 missingpota.py | grep "cannot be found"

import sys
import requests
import json

def lookup_callsign(callsign):
    """
    Look up a ham radio callsign using the POTA API.

    Args:
        callsign (str): The ham radio callsign to search for.

    Returns:
        dict: The JSON response from the API.
    """
    url = f"https://api.pota.app/lookup?search={callsign}&size=10"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Return the JSON response as a dictionary
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        return None

def main():
    # Read callsigns from piped input
    print("Reading callsign from input...")
    callsigns = [line.strip() for line in sys.stdin if line.strip()]

    if not callsigns:
        print("No callsigns provided. Please pipe a callsign into the script.")
        return

    for callsign in callsigns:
        print(f"Looking up callsign: {callsign}")
        result = lookup_callsign(callsign)

        if result is None:
            print("Error occurred while contacting the API.")
            continue

        # Check if the JSON response is empty
        if not result:
            print(f"The callsign '{callsign}' cannot be found in the POTA database.")
        else:
            print(f"JSON response for '{callsign}':")
            print(json.dumps(result, indent=4))

if __name__ == "__main__":
    main()
