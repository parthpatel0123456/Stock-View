import os
import json
import requests
import matplotlib.pyplot as plt
import datetime

api_key = os.getenv("ALPHAVTANGE_API_KEY")

base_url = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
symbol = "AAPL"
symbol = input("Enter a symbol: ")
url = f"{base_url}{symbol}&apikey={api_key}"
r = requests.get(url)
data = r.json()

yesterday = datetime.date.today() - datetime.timedelta(days=1)
yesterday = yesterday.strftime("%Y-%m-%d")

with open("formatted.json", "w") as file:
    daily_data = data['Monthly Time Series'][yesterday]
#     for line, price in daily_data.items():
#         print(f"{line}: {price}", file=file)
    print(json.dumps(data, indent=2), file=file)

with open("formatted.json", "r") as file:
    data = json.load(file)
    month = data['Monthly Time Series']
    left = []
    height = []
    starting_month = ['2024-06-28']
    
    with open("output.txt", "w") as file:
        for month in data['Monthly Time Series']:
            if month == '2023-06-30':
                break
            if month == '2024-06-28' or month == "2024-05-31" or month == "2024-04-30" or month == "2024-03-28" or month == "2024-02-29" or month == "2024-01-31" or month == "2023-12-29" or month == "2023-11-30" or month == "2023-10-31" or month == "2023-09-29" or month == "2023-08-31" or month == "2023-07-31":
                monthly_data = [data['Monthly Time Series'][month]]
                if "-01-" in month:
                        print(f"\nJan:", file=file)
                        left.append("Jan")
                if "-02-" in month:
                        print(f"\nFeb:", file=file)
                        left.append("Feb")
                if "-03-" in month:
                        print(f"\nMar:", file=file)
                        left.append("Mar")
                if "-04-" in month:
                        print(f"\nApr:", file=file)
                        left.append("Apr")
                if "-05-" in month:
                        print(f"\nMay:", file=file)
                        left.append("May")
                if "-06-" in month:
                        print(f"\nJun:", file=file)
                        left.append("Jun")
                if "-07-" in month:
                        print(f"\nJul:", file=file)
                        left.append("Jul")
                if "-08-" in month:
                        print(f"\nAug:", file=file)
                        left.append("Aug")
                if "-09-" in month:
                        print(f"\nSep:", file=file)
                        left.append("Sep")
                if "-10-" in month:
                        print(f"\nOct:", file=file)
                        left.append("Oct")
                if "-11-" in month:
                        print(f"\nNov:", file=file)
                        left.append("Nov")
                if "-12-" in month:
                        print(f"\nDec:", file=file)
                        left.append("Dec")
                
                for info in monthly_data:
                    for field, information in info.items():
                        if field == "2. high":
                            print(f"1. High: ${float(information):,.2f}", file=file)
                            height.append(float(information))
                        if field == "3. low":
                            print(f"2. Low: ${float(information):,.2f}", file=file)
                        if field == "5. volume":
                            print(f"3. Volume: {int(information):,}", file=file)

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