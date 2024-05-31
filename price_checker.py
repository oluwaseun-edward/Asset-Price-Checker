from email.message import EmailMessage
import smtplib
import os
import requests
from dotenv import load_dotenv

load_dotenv("C:/Users/Olu Edward/.env.txt")

# NewsAPI + Alphavantage settings
newsapi = os.getenv("newsapi_api_key")
alpha_api_key = os.getenv("alpha_api_key")
my_email = os.getenv("my_GMail")
email_password = os.getenv("GMail_password")
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Documentation for alphavantage: https://www.alphavantage.co/documentation/#daily
currency_params = {
    "function": "DIGITAL_CURRENCY_DAILY",
    "symbol": "BTC",
    "market": "USD",
    "apikey": alpha_api_key
}

news_params = {
    "apikey": newsapi,
    "q": "bitcoin",
    "language": "en",
    "from": "2024-05-29",
    "searchIn": "title"
}


def asset_price_change():
    """
    Function to obtain asset closing prices for the past 2 days 
    and calculate the percentage difference.
    """
    response = requests.get(
        STOCK_ENDPOINT, params=currency_params, timeout=(5, 15))
    # print(response.status_code)
    response.raise_for_status()
    currency_data = response.json()

    # Get yesterday's closing stock price.
    # [new_value for (key, value) in dictionary.items()]
    daily_prices = currency_data["Time Series (Digital Currency Daily)"]
    daily_prices_list = [value for (key, value) in daily_prices.items()]
    yesterday_prices = daily_prices_list[1]
    yesterday_close_price = float(yesterday_prices["4. close"])

    # Get the day before yesterday's closing stock price
    close_price_2days_ago = float(daily_prices_list[2]["4. close"])

    price_difference = yesterday_close_price - close_price_2days_ago

    # Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
    percentage_difference = round(
        (price_difference / yesterday_close_price * 100), 1)
    return percentage_difference


def price_change_symbol():
    """
    This function returns either an up or down arrow key depending
    if the percentage difference is negative or positive.
    """
    # up_down = None
    if percent_difference > 0:
        up_down = "\u2191"
    else:
        up_down = "\u2193"
    return up_down


def get_news_then_email():
    """
    This function retrieves relevant news stories on the asset then sends
    the news together with the asset price change as an email to the recipient.
    """
    news_response = requests.get(NEWS_ENDPOINT, news_params)
    # print(news_response.text)
    articles = news_response.json()["articles"]

    # extract the top 3 articles.
    three_articles = articles[:3]

    # Create a new list of the first 3 articles' headline and description using list comprehension.

    news = [f"BTC: {price_direction}{percent_difference}% Headline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]

    # Send each article as a separate email
    for item in news:
        mail = EmailMessage()
        mail.set_content(item)
        mail["subject"] = f'BTC price is {price_direction}{percent_difference}%'
        mail["From"] = my_email
        mail["To"] = my_email
        try:
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=email_password)
                connection.send_message(mail)
                print("Email successfully sent.")
        except Exception as e:
            print(f'Failed to send mail: {e}')


percent_difference = asset_price_change()
# print(percent_difference)

price_direction = price_change_symbol()

if abs(percent_difference) > 5:
    get_news_then_email()
