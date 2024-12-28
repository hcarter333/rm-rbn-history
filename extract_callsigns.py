#extracts the callsigns from qso_update.csv starting at line 5, one per line
#written by ChatGPT
import sys

def extract_callsigns(filename):
    """
    Extracts the first CSV field (callsign) from each line starting with line 5 of the input file.

    Args:
        filename (str): The name of the input file.

    Prints:
        The callsigns, one per line.
    """
    try:
        with open(filename, 'r') as file:
            # Read all lines from the file
            lines = file.readlines()
            
            # Process lines starting from line 5 (index 4)
            for line in lines[4:]:
                # Split the line by commas and extract the first field
                callsign = line.split(',')[0].strip()
                if callsign:  # Check if callsign is not empty
                    print(callsign)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 extract_callsigns.py <filename>")
        sys.exit(1)
    
    # Get the filename from command-line arguments
    input_file = sys.argv[1]
    extract_callsigns(input_file)
