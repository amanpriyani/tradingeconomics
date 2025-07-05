# in this programme , we are going to compare random indicator(user input)  of two random (user input) countries graphically 
import requests  # for fetching data from web
import matplotlib.pyplot as plt  # for plotting
from urllib.parse import quote  # For safe URL encoding
from datetime import datetime  # To convert string dates
import matplotlib.dates as mdates  # used for removing spaces from url 

# input country name 
country1 = input("Enter first country (e.g., mexico/thailand/sweden/New Zealand): ").lower()  # .lower is for lowercase
country2 = input("Enter second country (e.g., mexico/thailand/sweden/New Zealand): ").lower()
indicator = input("Enter indicator (e.g., Car Production): ").lower()
api_key = input("Enter your Trading Economics API key: ")

#  URL encode and prepare API endpoints
url1 = f"https://api.tradingeconomics.com/historical/country/{quote(country1)}/indicator/{quote(indicator)}?c={api_key}"
url2 = f"https://api.tradingeconomics.com/historical/country/{quote(country2)}/indicator/{quote(indicator)}?c={api_key}"

# Fetching  data from API
data1 = requests.get(url1).json()
data2 = requests.get(url2).json()

# Extract and convert dates and values
dates1 = [datetime.strptime(i["DateTime"][:10], "%Y-%m-%d") for i in data1]# here we are using .strptime for year,month, date format and :10 for taking date values only 
values1 = [i["Value"] for i in data1]

dates2 = [datetime.strptime(i["DateTime"][:10], "%Y-%m-%d") for i in data2]
values2 = [i["Value"] for i in data2]

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(dates1, values1, label=country1.title(), marker='o')
plt.plot(dates2, values2, label=country2.title(), marker='s')

plt.title(f"{indicator} Comparison")
plt.xlabel("Date")
plt.ylabel("Value")

# as x-axis is not clear, i am formatting x-axis to show fewer ticks (every 12 months)
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval= 12))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y')) # taking year only 
plt.legend()
plt.xticks(rotation=45) # to control lebels on x-axis 
plt.tight_layout() # for adjustment of lebels 
plt.show()
