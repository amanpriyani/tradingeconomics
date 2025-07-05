from flask import Flask, render_template, request, send_file
import requests, os, pandas as pd
from dotenv import load_dotenv
from io import StringIO
from urllib.parse import quote
from datetime import datetime

app = Flask(__name__)
load_dotenv()
API_KEY = os.getenv("API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    table_html, csv_data, error = None, None, None

    if request.method == 'POST':
        country = request.form['country'].strip().lower()
        year_input = request.form['year'].strip()
        indicators = [i.strip().lower() for i in request.form.get('indicators', 'gdp,inflation rate,population').split(',')]

        if not country.isalpha():
            return render_template('index.html', error="Country name must contain only letters.")
        if not year_input.isdigit():
            return render_template('index.html', error="Please enter a valid year.")
        if not API_KEY:
            return render_template('index.html', error="API key not configured.")

        records = []

        for indicator in indicators:
            encoded_indicator = quote(indicator)
            url = f"https://api.tradingeconomics.com/historical/country/{country}/indicator/{encoded_indicator}?c={API_KEY}"

            try:
                data = requests.get(url, timeout=10).json()
            except Exception as e:
                return render_template('index.html', error=f"API error for {indicator}: {str(e)}")

            if not isinstance(data, list):
                continue

            found = False
            for item in data:
                date_str = item.get("DateTime", "")
                value = item.get("Value")
                freq = (item.get("Frequency") or "").title()

                try:
                    year = datetime.fromisoformat(date_str).year
                except:
                    continue

                if str(year) == year_input and value not in [None, 0]:
                    records.append({
                        "Indicator": indicator.title(),
                        "Value": value,
                        "Date": date_str[:10],
                        "Frequency": freq
                    })
                    found = True
                    break

            if not found:
                records.append({
                    "Indicator": indicator.title(),
                    "Value": "No Data",
                    "Date": "-",
                    "Frequency": "-"
                })

        if records:
            df = pd.DataFrame(records)
            table_html = df.to_html(classes='table table-bordered', index=False)
            csv_data = quote(df.to_csv(index=False))
        else:
            error = "No matching data found."

    return render_template('index.html', table=table_html, csv=csv_data, error=error)

@app.route('/download')
def download_csv():
    csv = request.args.get('csv')
    if csv:
        return send_file(StringIO(csv), mimetype='text/csv', download_name='indicators.csv', as_attachment=True)
    return "No CSV content."

if __name__ == '__main__':
    app.run(debug=True, port=5001)

