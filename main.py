from datetime import date
import requests
from twilio.rest import Client

TICKER_SYMBOL = "TSLA"
ALPHA_API_KEY = API KEY
TODAY = str(date.today())
NEWS_API_KEY = API KEY
TWILIO_SID = SID
TWILIO_AUTH_TOKEN = AUTH TOKEN
PRICE_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": TICKER_SYMBOL,
    "apikey": ALPHA_API_KEY,
}
NEWS_PARAMETERS = {
    "q": "tesla",
    "from": TODAY,
    "sortBy": "published",
    "apiKey": NEWS_API_KEY,
}

response = requests.get("https://www.alphavantage.co/query", params=PRICE_PARAMETERS)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday_closing_price = float(data_list[0]["4. close"])
day_before_yesterday_closing_price = float(data_list[1]["4. close"])
percent_change = ((yesterday_closing_price - day_before_yesterday_closing_price) / day_before_yesterday_closing_price) * 100
percent_change_rounded = str(abs(round(percent_change, 2))) + "%"
if percent_change > 0:
    percent_change_rounded = (f"⬆️ " + percent_change_rounded)
elif percent_change < 0:
    percent_change_rounded = (f"⬇️ " + percent_change_rounded)
else:
    percent_change_rounded = (f"➖" + percent_change_rounded)

news_response = requests.get("https://newsapi.org/v2/everything", params=NEWS_PARAMETERS)
news_data = news_response.json()["articles"]
articles = news_data[:3]
formatted_article = [f"{TICKER_SYMBOL} performance yesterday: {percent_change_rounded}\n Headline: {article['title']}. \nBrief: {article['description']}" for article in articles]

client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
for article in formatted_article:
    message = client.messages.create(
        body=article,
        from_="+TWILIO PHONE NUMBER",
        to="YOUR PHONE NUMBER",
    )
