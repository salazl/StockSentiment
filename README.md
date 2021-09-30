# StockSentiment
Sentiment Analysis for the non-professional investor. 

### Why?
Recently, Jeffries Group reported that retail activity (aka activity from non-professional investors) could represent **up to one third of the USA's total equity volume** in 2021. Yet a good chunk of these indviduals are first-time investors (~15% according to Charles Schwab). 

StockSentiment allows a user to perform lexical sentiment analysis on both current and historical social media posts which mention chosen keywords, and allows for direct visual comparison of changing sentiment alongside changing price. Ultimately, my aim is that this tool helps educate and inform retail investors about external factors that can impact the financial markets. By determining whether posts (from people of interest or in general) tend to affect the price of a stock they wish to invest in, they can execute intelligent investment strategies. For example, if positive/negative sentiments tend to result in short-term gains/losses which quickly recover to original levels, they could reap additional gains or avoid potential losses (from selling prematurely). 

### Dependencies
This is my first foray into Python, and programming in general. Therefore I've leveraged 3 important tools: 
* [snscrape][1] - to retrieve tweets, as the official Twitter API only allows retrieval of tweets <7 days old (snscrape is better for historical trends!) 
* [yfinance][2] - to retrieve stock prices directly from Yahoo Finance (no need to reinvent the wheel ourselves!)
* [vaderSentiment][3] - to perform lexical sentiment analysis (super cool, super powerful) 

This program also requires Python 3.8 or higher, and basic Python libraries (Pandas, Matplotlib, etc.)

[1]: https://github.com/JustAnotherArchivist/snscrape "Title"
[2]: https://pypi.org/project/yfinance/ "Title"
[3]: https://github.com/cjhutto/vaderSentiment "Title"

### Using StockSentiment
In its current form, the program retrieves Tweets, and is intended to run by specifying a search version (general or username). The program will ask the user for this input upon initialization and then ask for further required inputs. 

Note that currently, the program is designed to search for tweets mentioning a company (keyword) + the ticker for that *same company*. Soon I will update to add an additional search method in which keyword and ticker are unrelated (i.e., “overvalued” and “QQQ” as the two search parameters). 
