import datetime
import os
import requests
from datetime import *
from twilio.rest import Client
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_api_key ="W6T6D4UOBL5DLX1D"
stock_params ={
   "function":"TIME_SERIES_DAILY",
    "symbol":STOCK,
    "apikey":stock_api_key
}
stock_response = requests.get("https://www.alphavantage.co/query",params=stock_params)
stock_status = stock_response.raise_for_status()


today = datetime.today()
print(today)

yesterday = datetime.date(today - timedelta(days=1))
print(yesterday)
dayBeforeYesterday =datetime.date(today - timedelta(days=2))
yesterday_price = float(stock_response.json()["Time Series (Daily)"][yesterday.strftime('%Y-%m-%d')]["2. high"])
DBY_price =float(stock_response.json()["Time Series (Daily)"][dayBeforeYesterday.strftime('%Y-%m-%d')]["2. high"])
difference =abs(DBY_price-yesterday_price)
difference_percentage =(difference/ yesterday_price)* 100
print(f"the differnce between  prices is {(difference/ yesterday_price)* 100}" )



## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
if difference_percentage > 2:
    news_api_key = "ee7f806fc5904e728b29d53047c432ca"

    news_params = {
        "q":COMPANY_NAME,
        "apiKey":news_api_key
    }
    news_response = requests.get("https://newsapi.org/v2/everything",params=news_params)
    my_articles =[]
    articles = news_response.json()["articles"]
    for x in range(3):
        title = articles[x]["title"]
        description = articles[x]["description"]
        my_articles.append({"title":title,"des":description})
    symbol=""
    print(my_articles[0])
    if yesterday_price > DBY_price:
        symbol ="⬆"
    else:
        symbol = "⬇"
    for x in range(3):
        headline = my_articles[x]["title"]
        brief = my_articles[x]["des"]
        message_text = f"Tesla {symbol} {difference_percentage:.2f}%\nHeadline: {headline}\nBrief: {brief}  "
        account_sid= "AC229cece7f98b8a01baef45ca46162fea"
        auth_token="f6f85684e77e9d68c31e3e19176f248e"
        client = Client(account_sid, auth_token)
        message = client.messages \
                        .create(
                             body= message_text,
                             from_='+13159035197',#dummy number from twillo
                             to='your verified number'
                         )
        print(message.status)


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and  each article's title and description to your phone number.



#Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

#+13159035197
