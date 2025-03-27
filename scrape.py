import requests
import pandas as pd
from lxml import html

url = "https://www.werder.de/tickets/heimspiele/"

print(r"""\                                                                                                                          
                                                                                                                                                                                                                                                                                                                                                                                                       
                                                                      WW                                                                    
                                                                        --                                                                  
                                                                    WW  WW                                                                  
                                                                  WW  WW  WW                                                                
                                                                    WWWWWW  ..                                                              
                                                                WW  WWWWWW  WW                                                              
                                                              WW  WWWWWWWWWW  WW                                                            
                                                                WWWWWWWWWWWWWW                                                              
                                                            WW  WWWWWWWWWWWWWW  WW                                                          
                                                          WW  WWWW            WW  WW                                                        
                                                            WWWWWW              WW                                                          
                                                        WW  WWWWWW              WW  WW                                                      
                                                      WW  WWWW--WW                WW  WW                                                    
                                                        WW        WWWWWWWW        WWWW                                                      
                                                    WW  WW        WWWWWWWWWW        WW  WW                                                  
                                                  WW  WWWW        WWWWWWWWWWWW      WWWW  WW                                                
                                                    WWWW      WWWWWWWWWWWWWWWW      WWWWWW                                                  
                                                WW  WWWW      WWWWWWWWWWWWWWWWWW    WWWWWW  WW                                              
                                              WW  WWWWWW      WWWWWWWWWWWWWWWWWW    WWWWWWWW  WW                                            
                                                WWWWWWWW::    WWWWWWWW  WWWWWWWW    WWWWWWWWWW                                              
                                            WW  WWWWWWWWWW    WWWWWWWW  WWWWWWWW    WWWWWWWWWW  WW                                          
                                              WW  WWWWWWWW    WWWWWWWW  WWWWWWWW    WWWWWWWW  WW                                            
                                                  WWWWWWWW    WWWWWW      WWWWWW    WWWWWWWW                                                
                                                WW  WWWWWW    WWWWWW      WWWWWW    WWWWWW  WW                                              
                                                  WW  WWWWWW  WWWW          WWWW  WWWWWW  WW                                                
                                                      WWWWWW    WW          WW    WWWWWW                                                    
                                                    WW  WWWW                      WWWW  WW                                                  
                                                      WW  WWWW        WW        WWWW  WW                                                    
                                                          WWWW        WW        WWWW  --                                                    
                                                        WW  WW      WWWWWW      WW  WW                                                      
                                                          WW  WW    WWWWWW    WW  WW                                                        
                                                              WW  WWWWWWWWWW  WW  ++                                                        
                                                            WW  WWWWWWWWWWWWWW  WW                                                          
                                                              WW  WWWWWWWWWW  WW                                                            
                                                                  WWWWWWWWWW  WW                                                            
                                                                WW  WWWWWW  WW                                                              
                                                                  WW  WW  ++                                                                
                                                                  ..  WW  WW                                                                
                                                                    WW  WW                                                                  
                                                                      WW                                                                    
                                                                      ::                                                                    
                                                            LEBENSLANG GRÜN-WEISS                                                                                                                                                                                                                                                                                                                                                                                                              
    """)


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
