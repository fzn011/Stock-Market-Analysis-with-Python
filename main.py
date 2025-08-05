import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = ""
NEWS_API_KEY = ""
TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""



stock_params= {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}


response=requests.get(STOCK_ENDPOINT,params=stock_params)
data=response.json()["Time Series (Daily)"]
data_list=[value for (key,value) in data.items()]
yesterday_data=data_list[0]
yesterday_closing_price=yesterday_data["4. close"]
print(yesterday_closing_price)


day_before_yesterday_data=data_list[1]
day_before_yesterday_closing_price=day_before_yesterday_data["4. close"]
print(day_before_yesterday_closing_price)

difference=float(yesterday_closing_price)-float(day_before_yesterday_closing_price)
up_down=None
if difference>0:
    up_down="⬆️"
else:
    up_down="⬇️"

print(difference)
diff_percentage=round(difference/float(yesterday_closing_price)*100)
print(diff_percentage)
#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if abs(diff_percentage)>1:
    news_params={
    "apiKey": NEWS_API_KEY,
    "qInTitle": COMPANY_NAME,

    }
    news_response=requests.get(NEWS_ENDPOINT, params=news_params)
    articles=news_response.json()["articles"]


    three_articles=articles[:3]
    print(articles)


    formatted_articles=[f"{STOCK_NAME}: {up_down}{diff_percentage}%\nHeadline: {article['title']}. \nBrief: {article ['description']}" for article in three_articles]

    client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_="",
            to="",
        )




"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

