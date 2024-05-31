# Asset-Price-Checker
Automate checking significant changes in asset prices and send email alerts with relevant news.
This script allows for asset prices, in this case $BTC, to be automatically checked using the alphavantage API
If assset closing prices over the last 48hrs of trading differe by more than 5% in either direction, then the 
script searches for relevant news articles that may explain the market movement. News is mined using NewsAPI.
Finally, both the asset price change and relevant news are sent by email to the recipient. The script can be set up to run 
at designated times via a task scheduler for example. 
