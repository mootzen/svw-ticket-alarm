import requests
import pandas as pd
from lxml import html

url = "https://web.archive.org/web/20240903034300/https://www.werder.de/tickets/heimspiele/"

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
        print("Tabelle Bestellfristen über XPath gefunden!")

        # Extract rows from the table
        rows = table_element[0].xpath(".//tr")
        print(f"Total rows found in table (including header): {len(rows)}")

        # Extract headers from the first row
        headers = [th.text_content().strip() for th in rows[0].xpath(".//th")]
        if not headers:
            # If headers are not found, manually assign them or handle the case
            headers = ["Date", "Opponent", "Order Period", "Link"]
        print("Extracted headers:", headers)

        # Extract table data
        data = []
        for i, row in enumerate(rows[1:], start=1):  # Skip header row
            cols = row.xpath(".//td")
            row_data = []
            stehplatz_link = None  # Initialize the variable to hold the Stehplätze link
            sitzplatz_link = None  # Initialize the variable to hold the Sitzplätze link
            for col in cols:
                links = col.xpath(".//a")
                if links:
                    for a in links:
                        link_text = a.text_content().strip()
                        link_url = a.get('href')
                        print(f"Link text: {link_text}, Link URL: {link_url}")  # Debugging line
                        row_data.append(link_url)
                
                        # Check for the "Stehplätze" link
                        if "Stehplätze" in link_text:
                            stehplatz_link = link_url
                        # Check for the "Sitzplätze" link
                        if "Sitzplätze" in link_text:
                            sitzplatz_link = link_url
                else:
                    row_data.append(col.text_content().strip())
            
            print("Extracted row data:", row_data)

            # If a "Stehplätze" link was found, print the order period and link
            if stehplatz_link:
                print(f"Aktive Bestellphase gefunden! VS {row_data[1]} Bestellfenster: {row_data[2]} Stehplatz: {stehplatz_link}")
            if sitzplatz_link:
                print(f"Sitzplatz Bestellphase gefunden! VS {row_data[1]} Bestellfenster: {row_data[2]} Sitzplatz: {sitzplatz_link}")

            if len(row_data) == len(headers):  # Ensure correct number of columns
                data.append(row_data)

        # Convert to DataFrame and save
        if headers and data:
            df = pd.DataFrame(data, columns=headers)
            df.to_csv(r"bearbeitungsstand.csv", index=False)
            print(f"Table scraped and saved successfully! Total rows saved: {len(data)}")
        else:
            print("Error: No data extracted from table.")
    else:
        print("Table not found using XPath. Verify the XPath expression and page structure.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
