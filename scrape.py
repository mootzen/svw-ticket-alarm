import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage
url = "https://www.werder.de/tickets/heimspiele/"

# Send an HTTP request to fetch the page content
headers = {"User-Agent": "Mozilla/5.0"}  # Set user-agent to avoid blocking
response = requests.get(url, headers=headers)

# Check if request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Debug: Print the first 500 characters of the HTML to verify content
    print("Page content preview:")
    print(response.text[:500])
    
    # Find the table with the relevant class
    table = soup.find("table", class_="contenttable")
    
    if table:
        print("Table found!")
        rows = table.find_all("tr")
        data = []
        
        # Debug: Print raw table rows
        for row in rows:
            print("Row HTML:", row)
        
        # Extract table headers from <strong> tags
        headers = [th.text.strip() for th in rows[0].find_all("td") if th.text.strip()]
        print("Extracted headers:", headers)
        
        # Extract table rows
        for row in rows[1:]:  # Skip header row
            cols = row.find_all("td")
            row_data = [col.text.strip() for col in cols]
            print("Extracted row data:", row_data)
            if len(row_data) == len(headers):  # Ensure correct number of columns
                data.append(row_data)
        
        # Convert to DataFrame
        if headers and data:
            df = pd.DataFrame(data, columns=headers)
            df.to_csv("bearbeitungsstand.csv", index=False)
            print("Table scraped and saved successfully!")
        else:
            print("Error: No data extracted from table.")
    else:
        print("Table not found. Check if the class name has changed or if JavaScript is required to render the table.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
