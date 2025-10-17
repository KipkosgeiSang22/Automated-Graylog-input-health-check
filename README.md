# Overview

This Python script utilizes `asyncio` and `aiohttp` to fetch data from a specified API, process it, and export the results to Excel files. The data processing includes sanitizing values, converting timestamps to local timezones, and ensuring valid sheet names for Excel.

---

## Features

- Asynchronous HTTP requests for efficient data fetching  
- Data sanitization to remove control characters and non-ASCII characters  
- Conversion of UTC timestamps to a specified local timezone  
- Dynamic Excel sheet creation based on input data  

---

## Dependencies

- `aiohttp`  
- `pandas`  
- `pytz`  

Install the required packages using pip:

```bash
pip install aiohttp pandas pytz



Usage
1. Prepare clients.json
Create a JSON file named clients.json in the same directory. It should contain the base URLs and any other relevant data for the clients. Example structure:
{
    "client1": {
        "base_url": "https://api.example.com"
    },
    "client2": {
        "base_url": "https://api.anotherexample.com"
    }
}


2. Run the Script
Execute the script using Python 3.7 or higher:
python script_name.py



Functions
sanitize_value(value)
Recursively sanitizes a value, list, or dictionary by removing control and non-ASCII characters.
convert_utc_to_local(utc_timestamp, local_tz_str='Africa/Nairobi')
Converts a UTC timestamp to the specified local timezone and formats it as a string.
sanitize_sheet_title(title)
Removes invalid characters from the sheet title and truncates it to a maximum length.
fetch_inputs(session, base_url)
Fetches input data from the API.
fetch_search(session, base_url, input_id)
Fetches messages for a specific input ID from the API.
process_client(client_name, data)
Processes each client by fetching inputs and exporting data to an Excel file.
main()
Main function that reads the clients.json file and initiates the data processing for all clients.

Licensing
This project is licensed under the MIT License.

Author
© 2025 Joshua

Acknowledgments
This script leverages:
- pandas for data manipulation
- aiohttp for asynchronous HTTP requests
- pytz for accurate timezone conversions
