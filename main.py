import os
import json
import requests
import matplotlib.pyplot as plt
import datetime
from website import create_app

app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)



api_key = os.getenv("ALPHAVTANGE_API_KEY")

base_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='
base_earnings_url = 'https://www.alphavantage.co/query?function=EARNINGS&symbol='
base_news_url = 'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers='

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

symbol = "TSLA"
# symbol = input("Enter a symbol: ")
stock_url = f"{base_url}{symbol}&apikey={api_key}"
r = requests.get(stock_url)
data = r.json()

earnings_url = f"{base_earnings_url}{symbol}&apikey={api_key}"
e_r = requests.get(earnings_url)
e_data = e_r.json()

news_url = f"{base_news_url}{symbol}&apikey={api_key}"
n_r = requests.get(news_url)
n_data = n_r.json()


# temp base reader for offline testing
with open("base_raw.json", "r") as file:
    data = json.load(file)

# temp earnings reader for offline testing
with open("earnings_raw.json", "r") as file:
    e_data = json.load(file)

# monthly_data = data['Monthly Time Series']
monthly_data = data
sorted_dates = sorted(monthly_data.keys())
curr_year = str(datetime.datetime.now().year)

# testing a input feature
# year = input("Enter a year: ")
# curr_year = year
curr_year = str(2024)

# writes base url api data into json
with open("base_raw.json", "w") as file:
    print(json.dumps(monthly_data, indent=2), file=file)

# reads base url json data
with open("base_raw.json", "r") as file:
    # internal variables
    ytd_month = []
    ytd_data = []

    # variables to be used for plotting
    ytd_price = []
    ytd_month_plot = []

    # adds month for ytd
    for month in sorted_dates:
        if month.startswith(curr_year):
            ytd_month.append(month)

    # adds data for ytd
    for month in ytd_month:
        ytd_data.append({
            "month": month,
            "price": monthly_data[month]["4. close"]
        })

    # writes month and price data into txt
    with open("output.txt", "w") as file:
        print(f"{symbol} {curr_year} YTD Stock Data:\n", file=file)

        # iterates the ytd monthly data for the values inside
        for entry in ytd_data:
            # format example: "2024-01-10" -> "Jan"
            month_obj = datetime.datetime.strptime(entry['month'], "%Y-%m-%d")
            curr_month_name = month_obj.strftime("%B")
            curr_month_name = curr_month_name[0:3]

            ytd_month_plot.append(curr_month_name)
            ytd_price.append(float(entry['price']))

            print(f"{curr_month_name}: ${float(entry['price']):,.2f}", file=file)

    # plot data into graph
    plt.title(f"{symbol} - {curr_year} YTD")
    x = ytd_month_plot
    y = ytd_price

    plt.plot(x, y, marker = "o")
    plt.grid(alpha = 0.3)

    # ensures enough graph spacing
    min_price = 100000000
    max_price = 0
    padding = 0.33

    for price in ytd_price:
        if min_price > price:
            min_price = price
        if max_price < price:
            max_price = price
            
    min_price_lim = min_price - (min_price * padding)
    max_price_lim = max_price + (max_price * padding)
    plt.ylim(min_price_lim, max_price_lim)

    plt.show()
 
# writes earnings url api data into json
with open("earnings_raw.json", "w") as file:
    print(json.dumps(e_data, indent=2), file=file)

# writes raw earnings data from json into filtered json
with open("earnings_raw.json", "r") as file:
    quarterly_data = []

    for quarter in e_data['quarterlyEarnings']:
        if quarter['reportedDate'].startswith(curr_year):
            quarterly_data.append(quarter)
    with open("earnings_filtered.json", "w") as file:
        print(json.dumps(quarterly_data, indent=2), file=file)

# writes news data from json into filtered json
with open("news_raw.json", "w") as file:
    print(json.dumps(n_data, indent=2), file=file) 

# writes raw news data from json into filtered json
with open("news_raw.json", "r") as file:
    news_articles = []
    for article in n_data['feed']:
        if symbol in article['title']:
            news_articles.append({'title': article['title'], 'url': article['url']})

    with open("news_filtered.json", "w") as file:
        print(json.dumps(news_articles, indent=2), file=file)