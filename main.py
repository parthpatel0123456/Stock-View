import os
import json
import requests
import matplotlib.pyplot as plt
import datetime



api_key = os.getenv("ALPHAVTANGE_API_KEY")

base_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

symbol = "TSLA"
# symbol = input("Enter a symbol: ")
url = f"{base_url}{symbol}&apikey={api_key}"
r = requests.get(url)
data = r.json()

# temp reader for offline testing
with open("formatted.json", "r") as file:
    data = json.load(file)

# monthly_data = data['Monthly Time Series']
monthly_data = data
sorted_dates = sorted(monthly_data.keys())
curr_year = str(datetime.datetime.now().year)

# testing a input feature
# year = input("Enter a year: ")
# curr_year = year
curr_year = str(2024)

# writes api data into json
with open("formatted.json", "w") as file:
    print(json.dumps(monthly_data, indent=2), file=file)

# reads json data
with open("formatted.json", "r") as file:
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

    
                

'''
# print json data into txt
with open("formatted.json", "r") as file:
    data = json.load(file)
    month = data['Monthly Time Series']
    left = []
    height = []
    starting_month = ['2024-06-28']
      
    for info in monthly_data:
        for field, information in info.items():
            if field == "2. high":
                print(f"1. High: ${float(information):,.2f}", file=file)
                height.append(float(information))
            if field == "3. low":
                print(f"2. Low: ${float(information):,.2f}", file=file)
            if field == "5. volume":
                print(f"3. Volume: {int(information):,}", file=file)

    # graph
    plt.plot(left, height, linestyle='solid', linewidth = 2,
         marker='o', markerfacecolor='black', markersize=6)

    min_height = float(10000000000.0)
    max_height = float(0.0)
    for item in height:
        if float(item) < float(min_height):
            min_height = float(item)
        if float(item) > float(max_height):
            max_height = (item)

    max_height_lim = max_height

    padding = (max_height - min_height) * 0.1
    y_lower = min_height - padding
    y_upper = max_height - padding

    plt.ylim(round(y_lower, 2), round(y_upper, 2))
    plt.xlim(1, 12)
    plt.title(f"{symbol}")
    plt.show()

'''