import asyncio
import aiohttp
import pandas as pd
import re
import json
from datetime import datetime
import pytz
import ssl
from aiohttp import TCPConnector
from openpyxl.styles import PatternFill

copyright = "© 2025 Joshua"

ENCODED_AUTH_STRING = ''
AUTH = f'Basic {ENCODED_AUTH_STRING}'

HEADERS = {
    'Authorization': AUTH,
    'X-Requested-By': 'export-script',
    'Accept': 'application/json'
}

MAX_SHEET_NAME_LENGTH = 31
MAX_BATCH_SIZE = 5  # Adjust this size as needed

def sanitize_value(value):
    """Recursively sanitizes a value, list, or dictionary."""
    if isinstance(value, dict):
        return {k: sanitize_value(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [sanitize_value(v) for v in value]
    elif isinstance(value, str):
        cleaned_str = re.sub(r'[\x00-\x1F]', '', value)  # Remove control characters
        cleaned_str = re.sub(r'[^\x00-\x7F]+', '', cleaned_str)  # Remove non-ASCII characters
        return cleaned_str
    else:
        return value

def convert_utc_to_local(utc_timestamp, local_tz_str='Africa/Nairobi'):
    """Convert UTC timestamp to local timezone and format it."""
    try:
        utc_time = datetime.fromisoformat(utc_timestamp.replace("Z", "+00:00"))
        local_tz = pytz.timezone(local_tz_str)
        local_time = utc_time.astimezone(local_tz)
        return local_time.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Error converting timestamp: {e}")
        return utc_timestamp  # Return original if there's an error

def sanitize_sheet_title(title):
    """Remove invalid characters from the sheet title."""
    return re.sub(r'[<>:"/\\|?*]', '', title)[:MAX_SHEET_NAME_LENGTH]

async def fetch_inputs(session, base_url):
    """Fetch inputs from the API."""
    async with session.get(f"{base_url}/api/system/inputs", headers=HEADERS, timeout=20) as response:
        response.raise_for_status()
        return await response.json()

async def fetch_search(session, base_url, input_id):
    """Fetch messages for the specific input ID."""
    async with session.get(
        f"{base_url}/api/search/universal/relative",
        params={"query": f"gl2_source_input:{input_id}", "range": 86400, "limit": 1, "fields": "*"},  
        headers=HEADERS,
        timeout=900
    ) as response:
        response.raise_for_status()
        return await response.json()

async def process_input(session, base_url, input_item):
    """Process each input to fetch the last message."""
    input_id = input_item.get('id')
    input_title = input_item.get('title', f"Input_{input_id}")

    print(f"Fetching last message for input: {input_title}")
    try:
        search = await fetch_search(session, base_url, input_id)
        messages_raw = search.get("messages", [])

        if not messages_raw:
            print(f"No messages found for input '{input_title}'.")
            return [input_title, None, "No last log found."]

        msg_item = messages_raw[0].get("message", {})
        last_timestamp = convert_utc_to_local(msg_item.get("timestamp", None))
        sanitized_message = sanitize_value(msg_item)

        return [input_title, last_timestamp, sanitized_message]

    except Exception as e:
        print(f"Failed to fetch last message for input '{input_title}': {e}")
        return [input_title, None, f"Error: {str(e)}"]

async def process_client(writer, client_name, data):
    """Process each client and export data to a specific sheet."""
    print(f"Processing client: {client_name}")
    base_url = data['base_url'].rstrip('/')

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    connector = TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=connector) as session:
        inputs = await fetch_inputs(session, base_url)
        print("Inputs response:", inputs)

        all_inputs_data = []
        input_items = inputs.get('inputs', [])

        for i in range(0, len(input_items), MAX_BATCH_SIZE):
            batch = input_items[i:i + MAX_BATCH_SIZE]
            tasks = [process_input(session, base_url, input_item) for input_item in batch]
            batch_results = await asyncio.gather(*tasks)

            all_inputs_data.extend(batch_results)

        df = pd.DataFrame(all_inputs_data, columns=["Input Title", "Last Timestamp", "Last Message"])
        sheet_name = sanitize_sheet_title(client_name)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

        worksheet = writer.sheets[sheet_name]
        for column in worksheet.columns:
            max_length = max(len(str(cell.value)) for cell in column) if column else 0
            adjusted_width = max(max_length, 30)
            worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

        fill = PatternFill(start_color='9BC2E6', end_color='9BC2E6', fill_type='solid')
        for cell in worksheet[1]:
            cell.fill = fill

async def main():
    with open('clients.json', 'r') as f:
        clients_data = json.load(f)

    with pd.ExcelWriter("All_Clients.xlsx", engine='openpyxl') as writer:
        tasks = [process_client(writer, client_name, data) for client_name, data in clients_data.items()]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
