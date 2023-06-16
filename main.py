import os
import requests
from datetime import *
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
ALPHAVANTAGE_APIKEY = os.getenv("ALPHAVANTAGE_APIKEY")
NEWS_API_APIKEY = os.getenv("NEWS_API_APIKEY")
AV_ENDPOINT = "https://www.alphavantage.co/query?"
NA_ENDPOINT = "https://newsapi.org/v2/top-headlines?"
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
SENDING_NUMBER = os.getenv("SENDING_NUMBER")
RECEIVING_NUMBER = os.getenv("RECEIVING_NUMBER")
STOCK = "TSLA"
COMPANY_NAME = "Tesla"

TODAY = date.today()
YESTERDAY = str(TODAY - timedelta(days=1))
DAY_BEFORE_YESTERDAY = str(TODAY - timedelta(days=2))

av_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK,
    "apikey": ALPHAVANTAGE_APIKEY
}

na_params = {
    "apiKey": NEWS_API_APIKEY,
    "q": COMPANY_NAME
}
response1 = requests.get(url=AV_ENDPOINT, params=av_params)
print(response1.status_code)
yesterday_price = response1.json()
yesterday_price = yesterday_price["Time Series (Daily)"][YESTERDAY]["4. close"]
day_before_yesterday_price = response1.json()
day_before_yesterday_price = day_before_yesterday_price["Time Series (Daily)"][DAY_BEFORE_YESTERDAY]["4. close"]
print("DAY BEFORE YESTERDAY :" + day_before_yesterday_price)
print("YESTERDAY :" + yesterday_price)

rate_of_change = ((float(yesterday_price) - float(day_before_yesterday_price)) / float(
    day_before_yesterday_price)) * 100
print(f"RATE_OF_CHANGE : {rate_of_change}")

if rate_of_change >= 5 or rate_of_change <= -5:
    print(f"BIG CHANGE IN {STOCK}, % CHANGE IS {rate_of_change}")

    news_response = requests.get(url=NA_ENDPOINT, params=na_params)
    news_articles = news_response.json()
    count = 0
    while count < 3:
        x = news_articles["articles"][count]["title"]
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages \
            .create(
            body=f"{STOCK} has changed by {rate_of_change}%. NEWS is {x}",
            from_=SENDING_NUMBER,
            to=RECEIVING_NUMBER
        )
        count += 1