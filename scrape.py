import requests
import pandas as pd
from lxml import html

url = "https://www.werder.de/tickets/heimspiele/"

# Send an HTTP request to fetch the page content
headers = {"User-Agent": "Mozilla/5.0"}  # Set user-agent to avoid blocking
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    # Parse the HTML content using lxml
    tree = html.fromstring(response.content)
    
    # Use XPath to select the correct table
    table_element = tree.xpath('/html/body/section[5]/div[1]/div/div[1]/div[3]')

    if table_element:
        print("Table found using XPath!")

        # Extract rows from the table
        rows = table_element[0].xpath(".//tr")
        print(f"Total rows found in table (including header): {len(rows)}")

        # Extract headers from the first row
        headers = [th.text_content().strip() for th in rows[0].xpath(".//th")]
        print("Extracted headers:", headers)

        # Extract table data
        data = []
        for i, row in enumerate(rows[1:], start=1):  # Skip header row
            cols = row.xpath(".//td")
            row_data = [col.text_content().strip() for col in cols]
            print("Extracted row data:", row_data)
            if len(row_data) == len(headers):  # Ensure correct number of columns
                data.append(row_data)

        # Convert to DataFrame and save
        if headers and data:
            df = pd.DataFrame(data, columns=headers)
            df.to_csv(r"D:\Scripte\python\svw\bearbeitungsstand.csv", index=False)
            print(f"Table scraped and saved successfully! Total rows saved: {len(data)}")
        else:
            print("Error: No data extracted from table.")
    else:
        print("Table not found using XPath. Verify the XPath expression and page structure.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
