markdown
# Log Fetching and Export Script

This Python script retrieves logs from multiple Graylog instances and exports the data into an Excel file. It utilizes asynchronous programming to fetch data efficiently and ensures the output is well-formatted.

## 🚀 Features

- **Asynchronous Fetching**: Utilizes `asyncio` and `aiohttp` for non-blocking API calls to fetch log data.
- **Data Sanitization**: Cleans log entries by removing control characters and non-ASCII text.
- **Date Conversion**: Converts UTC timestamps to a specified local timezone.
- **Excel Export**: Exports data to an Excel file with customized sheet names and formatting.

## 📄 Setup

### Prerequisites

Make sure you have Python 3.7 or later installed along with the necessary packages. You can install the required packages using pip:

    ```bash
    pip install aiohttp pandas openpyxl pytz

Configuration
Create a clients.json file in the same directory as the script. The file should contain the following structure:

    ```json
    {
    "clients": {
            "client1": {
                "base_url": "https://api.example.com"
            },
            "client2": {
                "base_url": "https://api.anotherexample.com"
        }
        }
    }

Authentication
The script uses HTTP Basic Authentication. Edit the following variable in the script with your credentials:

    ```python
    ENCODED_AUTH_STRING = 'YourBase64EncodedCredentials'

Run

🛠️ How to Run
To execute the script, run the following command in your terminal:

    ```bash
    python <script_filename>.py

This will generate an Excel file named All_Clients.xlsx, containing data from each client.

🗒️ Code Explanation
Imports: The script begins by importing necessary libraries for handling asynchronous HTTP requests, data processing, JSON handling, and Excel file creation.

Constants:

ENCODED_AUTH_STRING: Base64-encoded string for HTTP Basic Authentication.
HEADERS: HTTP headers for API requests.
Sanitization Functions:

sanitize_value(value): Recursively removes unwanted characters from logs.
convert_utc_to_local(utc_timestamp, local_tz_str='Africa/Nairobi'): Converts UTC timestamps to a local timezone.
API Interaction:

fetch_inputs(session, base_url): Fetches input details from the Graylog API.
fetch_search(session, base_url, input_id): Fetches message logs for a specific input ID.
Data Processing:

process_input(session, base_url, input_item): Fetches the last log message for each input.
process_client(writer, client_name, data): Processes each client and writes the results to an Excel sheet.
Main Functionality:

async def main(): The entry point that loads client configurations and orchestrates log fetching and Excel writing.
