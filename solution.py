import requests
import smtplib
import os

stock_name = os.getenv('your_stock')
company_name = os.getenv('your_company_name')

stock_endpoint = 'https://www.alphavantage.co/query'
news_endpoint = 'https://newsapi.org/v2/everything'

stock_api_key = os.getenv('stock_api_key')
news_api_key = os.getenv('news_api_key')

stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': stock_name,
    'apikey': stock_api_key
}

response = requests.get(url='https://www.alphavantage.co/query', params=stock_params)
data = response.json()['Time Series (Daily)']
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = '🔺'
else:
    up_down = '🔻'

diff_percent = round((difference / float(yesterday_closing_price)) * 100)

if abs(diff_percent) >= 5:
    news_params = {
        'qInTitle': company_name,
        'apiKey': news_api_key
    }
    news_response = requests.get(url=news_endpoint, params=news_params)
    articles = news_response.json()['articles']
    three_articles = articles[:3]
    formatted_articles = [f'Headline: {article["title"]}. \nBrief: {article["description"]}' for article in articles]
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        connection.login(user=os.getenv('user_email'), password=os.getenv('password'))
        connection.sendmail(from_addr=os.getenv('user_email'),
                            to_addrs=os.getenv('to_email'),
                            msg=f'Subject:There is a {up_down}{diff_percent}% change in {stock_name} stock price!\n\n{formatted_articles[0]}\n{formatted_articles[1]}\n{formatted_articles[2]}')

else:
    print('No 5% changes at this time')