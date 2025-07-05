import requests
api_key = 'b52d974c724544f:n1621yqk02f25hz'
url = f'https://api.tradingeconomics.com/indicators?c={api_key}'
data = requests.get(url).json()
print(data)
