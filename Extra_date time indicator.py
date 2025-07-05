import requests

api_key = 'b52d974c724544f:n1621yqk02f25hz'
country = 'mexico'
indicator = 'Car Production'

url = f"https://api.tradingeconomics.com/historical/country/{country}/indicator/{indicator}?c={api_key}"
data = requests.get(url).json()
print(data)
