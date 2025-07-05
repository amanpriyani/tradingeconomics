import requests # for fetching data from web
import pandas as pd  
from tabulate import tabulate #for printing data in tabular form 
from datetime import datetime # To convert string dates
from urllib.parse import quote  # for safe URL formatting

# User Inputs
country = input("Enter country name (e.g., sweden): ").lower().strip()
year_input = input("Enter year (e.g., 2022): ").strip()
api_key = input("Enter your Trading Economics API key: ").strip()

# Define indicators to fetch (raw names, not URL-encoded)
indicators = ["gdp", "inflation rate", "car production"]

# Fetch and filter
results = []

for indicator in indicators:
    encoded_indicator = quote(indicator)  # safely encode indicator for URL
    url = f"https://api.tradingeconomics.com/historical/country/{country}/indicator/{encoded_indicator}?c={api_key}"
    
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception as e:
        print(f" Error fetching data for {indicator}: {e}")
        continue

    # Try to get the first available value for the requested year
    found = False
    for item in data:
        date_str = item.get("DateTime", "")
        value = item.get("Value")

        try:
            year = datetime.fromisoformat(date_str).year
        except:
            continue

        if str(year) == year_input and value not in [None, 0]:
            results.append({
                "Indicator": indicator.title(),
                "Value": value,
                "Date": date_str[:10],
                "Frequency": item.get("Frequency", "N/A")
            })
            found = True
            break

    if not found:
        results.append({
            "Indicator": indicator.title(),
            "Value": "No Data",
            "Date": "-",
            "Frequency": "-"
        })

# Display Table
df = pd.DataFrame(results)
print(f"\n📊 Economic Indicators for {country.title()} in {year_input}:\n")
print(tabulate(df, headers="keys", tablefmt="fancy_grid"))
