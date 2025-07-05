# in this programme , we are going to plot random indicator(user input) of selected country ( free available) 
import requests # for fetching data from web
import matplotlib.pyplot as plt # for plotting
import matplotlib.dates as mdates # used for removing spaces from url

# User Inputs-country name, indicator and API key 
country = input("Enter country (e.g., mexico/sweden/thailand/ New zealand): ").lower()
indicator = input("Enter indicator (e.g., Car Production): ").lower()
api_key = input("Enter your Trading Economics API key: ")

# API URL
url = f"https://api.tradingeconomics.com/historical/country/{country}/indicator/{indicator}?c={api_key}"

# Getting  data
response = requests.get(url)
data = response.json()

# Preparing data for plotting
dates = [i['DateTime'][:10] for i in data]
values = [i['Value'] for i in data]

# Plotting 
plt.figure(figsize=(10, 5))
plt.plot(dates, values, marker='o')
plt.title(f"{indicator} for {country.title()}")
plt.xlabel("Date")
plt.ylabel("Value")
# as x-axis is not clear, i am formatting x-axis to show fewer ticks (every 12 months)
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval= 12))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y')) # taking year only
plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)
plt.show()
