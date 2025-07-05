# in this ccode i am plotting graph of mexico car production 
import requests # for fetching data from web
import matplotlib.pyplot as plt  # for plotting

API_KEY = 'b52d974c724544f:n1621yqk02f25hz' #this is my API key 

#fetching data
url = f"https://api.tradingeconomics.com/historical/country/mexico/indicator/Car%20Production?c={API_KEY}" #%20 is used if there is space in indicator 
response = requests.get(url)
data = response.json()

#storing  data 
years = [i['DateTime'][:4] for i in data]
values = [i['Value'] for i in data]

#plotting data
plt.figure(figsize=(12, 6))
plt.plot(years, values, marker='o', linestyle='-', color='teal')
plt.title('Mexico Car Production over Time', fontsize=16)
plt.xlabel('Year')
plt.ylabel('Car Production')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()
