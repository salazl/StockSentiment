import time
import sys

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import snscrape.modules.twitter as sntwitter #courtesy of JustAnotherArchivist
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer #courtesy of Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
import yfinance as yf #courtesy of Ran Aroussi

#function for general search
def general_search():
    tweets_list = [] #empty list to hold scraped tweets

    #user inputs for scraping tweets based on Keywords, Start date, End date
    keyword_name = input('Please enter the name of a company (only 1): ')
    keyword_ticker = input('Please input stock ticker (only 1):')
    keyword = keyword_name + ' OR ' + keyword_ticker

    start_date_raw = input('Please enter start date for search (format YYYY-MM-DD):')
    end_date_raw = input('Please enter end date for search (format YYYY-MM-DD):')
    date_text = "'"+'since:'+start_date_raw+' until:'+end_date_raw+"'" #snscrape wants '' around search terms 
    tweets_to_scrape = int(input('How many tweets would you like to obtain? (recommend <1000 to start, more will take longer!)'))

#Using TwitterSearchScraper to scrape tweets and append those with keyword to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + date_text).get_items()): #declare keyword + username + start/end dates 
        if i>tweets_to_scrape: #max number of tweets to scrape
            break
        tweets_list.append([tweet.date, tweet.content]) #specify which attributes are returned (only date and tweet contents)

    tweets_df = pd.DataFrame(tweets_list, columns=['DateTime', 'Text']) #specifying we only want date and tweet contents columns

#Performing sentiment analysis using VADER
    analyzer = SentimentIntensityAnalyzer() #create an object defined as the VADER analyzer 

    tweets_df['compound'] = [analyzer.polarity_scores(tweet) ['compound'] for tweet in tweets_df['Text']] #adds compound score column, calculated from contents in "Text" which is the column containing tweets
    tweets_df['neg'] = [analyzer.polarity_scores(tweet) ['neg'] for tweet in tweets_df['Text']] #adds negative score column
    tweets_df['neu'] = [analyzer.polarity_scores(tweet) ['neu'] for tweet in tweets_df['Text']] #adds neutral score column
    tweets_df['pos'] = [analyzer.polarity_scores(tweet) ['pos'] for tweet in tweets_df['Text']] #adds positive score column

    #Next, we will allow the user to determine if they want a copy of the .csv of the sentiment analysis + tweets
    make_csv_answers = ['Y', 'N']
    response_csv = None

    #This will keep asking until an appropriate response (i.e. in make_csv_answers) is given
    while response_csv not in make_csv_answers:
        response_csv = input('Would you like a .csv of collected tweets + sentiment scores? (Y/N)')

    if response_csv == 'Y':
        tweets_df['Score Explanation'] = pd.Series(["""positive sentiment: compound score ≥0.05
        neutral sentiment: 0.05 > compound score > -0.05 
        negative sentiment: compound score ≤ -0.05""" for x in range(len(tweets_df.index))]) #adds column explaining scores for each row

        tweets_df.to_csv(keyword_name+'_Twitter_SentimentAnalysis_'+start_date_raw+'_to_'+end_date_raw+'.csv')
        print('Making your .csv!')

    elif response_csv == 'N':
        print('Ok. No .csv was made.')
    time.sleep(1) #adding delay between modules

    #Next, we will allow the user to determine if they want a plot of sentiment analysis over time
    make_sentiment_plot = ['Y', 'N']
    response_sentiment_plot = None

    #This will keep asking until an appropriate response (i.e. in make_sentiment_plot) is given
    while response_sentiment_plot not in make_sentiment_plot:
        response_sentiment_plot = input('Would you like to plot compound sentiment score? (Y/N)')

    if response_sentiment_plot == 'Y':
      #Creates a plot of compound score over time
        sentiment_plot = tweets_df.plot(x='DateTime', y='compound', kind = 'line',
                            color = '#4b2e83', title = 'Sentiment Analysis for '+keyword_name+' tweets '+' from '+start_date_raw+' until '+end_date_raw, label='compound score', 
                            xlabel = '',
                            ylabel = 'Compound sentiment score (>0.05 = positive)', 
                            linewidth = 2,
                            figsize=(9,8)                 
                            )

        plt.axhline(y=0.05, xmin = 0.01, xmax = 0.99, color='#85754d', linestyle = '--', linewidth = 1.3, label = 'positivity threshold') #adds a horizontal line for positivity threshold

        plt.legend(frameon = False)

        plt.close() #closes figure and avoids displaying it in a seperate window

        sentiment_plot.figure.savefig(keyword_name+'_SentimentAnalysis_'+start_date_raw+'_to_'+end_date_raw+'.jpg')
        print('Making your sentiment plot!')

    elif response_sentiment_plot == 'N':
        print('Ok. No sentiment analysis plot was made.')
    time.sleep(1) #adding delay between modules

#Scraping historical stock prices from user input ticker

    #Next we ask the user if they want a plot of the price over time
    make_price_plot = ['Y', 'N']
    price_response = None

    #This will keep asking until an appropriate response (i.e. in make_price_plot) is given
    while price_response not in make_price_plot:
        price_response = input('Would you like to plot '+keyword_ticker+' price over time? (Y/N)')

    if price_response == 'Y':
        #Next we ask the user if they want to use new date ranges
        use_new_dates = ['Y', 'N']
        date_response = None

        #This will keep asking until an appropriate response (i.e. in use_new_dates) is given
        while date_response not in use_new_dates:
            date_response = input('With the same date range used for tweets? (Y/N)')

        if date_response == 'Y':
            stock_data = yf.download(keyword_ticker, start = start_date_raw, end = end_date_raw)   #creates a Pandas dataframe for desired ticker with start and end dates using YahooFinance price data

            #Creates a plot of price over time
            price_plot = stock_data.loc[:,'Close'].plot(kind = 'line', #plots only closing price
                            color = '#4b2e83', title = keyword_ticker+' closing price from '+start_date_raw+' until '+end_date_raw, label='closing price', 
                            xlabel = '',
                            ylabel = keyword_ticker+' Closing price (USD)', 
                            linewidth = 2,
                            figsize=(9,8)                 
                            )

            plt.legend(frameon = False)

            plt.close() #closes figure and avoids displaying it in a seperate window

            price_plot.figure.savefig(keyword_ticker+'_ClosingPrice_'+'from'+start_date_raw+'_until'+end_date_raw+'.jpg')
            print('Making your price plot!')

        elif date_response == 'N': #new date ranges defined
            new_price_start = input('What is the new start date? (format YYYY-MM-DD)')
            new_price_end = input('What is the new end date? (format YYYY-MM-DD)')

            stock_data = yf.download(keyword_ticker, start = new_price_start, end = new_price_end)   #creates a Pandas dataframe for desired ticker with start and end dates using YahooFinance price data

            #Creates a plot of price over time
            price_plot = stock_data.loc[:,'Close'].plot(kind = 'line', #plots only closing price
                            color = '#4b2e83', title = keyword_ticker+' closing price from '+new_price_start+' until '+new_price_end, label='closing price', 
                            xlabel = '',
                            ylabel = keyword_ticker+' Closing price (USD)', 
                            linewidth = 2,
                            figsize=(9,8)                 
                            )

            plt.legend(frameon = False)

            plt.close() #closes figure and avoids displaying it in a seperate window

            price_plot.figure.savefig(keyword_ticker+'_ClosingPrice_'+'from'+new_price_start+'_until'+new_price_end+'.jpg')
            print('Making your price plot!')

    elif price_response == 'N':
        print('Ok. No price plot was made.')

    time.sleep(1) #adds a delay between modules
    
#Allow user to repeat search
    play_again_answer = ['Y', 'N']
    response = None

    #This will keep asking until an appropriate response (i.e. in play_again_answer) is given
    while response not in play_again_answer:
        response = input('Would you like to obtain data for a new company? (Y/N)')

    if response == 'Y':     
        general_search()

    elif response == 'N':
        sys.exit() #closes program and exits python interpreter 

if __name__ == '__main__': #ensures that when the StockSentiment_functions.py is imported, function only runs when called rather than immediately upon import
    general_search()


#defining function for username search                      
def username_search():
    tweets_list = []

    #User inputs for scraping tweets based on Keyword, Username, Start date, End date
    keyword_name = input('Please enter the name of a company (only 1): ')
    keyword_ticker = input('Please input stock ticker (only 1):')
    keyword = keyword_name + ' OR ' + keyword_ticker

    user_raw = input('Please enter twitter username (excluding @):')
    start_date_raw = input('Please enter start date for search (format YYYY-MM-DD):')
    end_date_raw = input('Please enter end date for search (format YYYY-MM-DD):')
    user_and_date_text = "'"+'from:'+user_raw+' since:'+start_date_raw+' until:'+end_date_raw+"'" #snscrape wants '' around search terms 
    tweets_to_scrape = int(input('How many tweets would you like to obtain? (recommend <1000 to start, more will take longer!)'))

#Using TwitterSearchScraper to scrape tweets and append those with keyword to list
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(keyword + user_and_date_text).get_items()): #declare keyword + username + start/end dates 
        if i>tweets_to_scrape: #max number of tweets to scrape
            break
        tweets_list.append([tweet.date, tweet.content]) #specify which attributes are returned (only date and tweet contents)

    #Creating a dataframe from the tweets list above 
    tweets_df = pd.DataFrame(tweets_list, columns=['DateTime', 'Text']) #specifying we only want date and tweet contents columns

#Performing sentiment analysis using VADER
    analyzer = SentimentIntensityAnalyzer() #create an object defined as the VADER analyzer 

    tweets_df['compound'] = [analyzer.polarity_scores(tweet) ['compound'] for tweet in tweets_df['Text']] #adds compound score column, calculated from contents in "Text" which is the column containing tweets
    tweets_df['neg'] = [analyzer.polarity_scores(tweet) ['neg'] for tweet in tweets_df['Text']] #adds negative score column
    tweets_df['neu'] = [analyzer.polarity_scores(tweet) ['neu'] for tweet in tweets_df['Text']] #adds neutral score column
    tweets_df['pos'] = [analyzer.polarity_scores(tweet) ['pos'] for tweet in tweets_df['Text']] #adds positive score column

    #Next, we will allow the user to determine if they want a copy of the .csv of the sentiment analysis + tweets
    make_csv_answers = ['Y', 'N']
    response_csv = None

    #This will keep asking until an appropriate response (i.e. in make_csv_answers) is given
    while response_csv not in make_csv_answers:
        response_csv = input('Would you like a .csv of collected tweets + sentiment scores? (Y/N)')

    if response_csv == 'Y':
        tweets_df['Score Explanation'] = pd.Series(["""positive sentiment: compound score ≥0.05
        neutral sentiment: 0.05 > compound score > -0.05 
        negative sentiment: compound score ≤ -0.05""" for x in range(len(tweets_df.index))]) #adds column explaining scores for each row

        tweets_df.to_csv(keyword_name+'_'+user_raw+'_Twitter_SentimentAnalysis_'+start_date_raw+'_to_'+end_date_raw+'.csv')
        print('Making your .csv!')

    elif response_csv == 'N':
        print('Ok. No .csv was made.')
    time.sleep(1) #adding delay between modules

    #Next, we will allow the user to determine if they want a plot of sentiment analysis over time
    make_sentiment_plot = ['Y', 'N']
    response_sentiment_plot = None

    #This will keep asking until an appropriate response (i.e. in make_sentiment_plot) is given
    while response_sentiment_plot not in make_sentiment_plot:
        response_sentiment_plot = input('Would you like to plot compound sentiment score? (Y/N)')

    if response_sentiment_plot == 'Y':
      #Creates a plot of compound score over time
        sentiment_plot = tweets_df.plot(x='DateTime', y='compound', kind = 'line',
                            color = '#4b2e83', title = 'Sentiment Analysis for '+keyword_name+' tweets from @'+user_raw+' from '+start_date_raw+' until '+end_date_raw, label='compound score', 
                            xlabel = '',
                            ylabel = 'Compound sentiment score (>0.05 = positive)', 
                            linewidth = 2,
                            figsize=(9,8)                 
                            )

        plt.axhline(y=0.05, xmin = 0.01, xmax = 0.99, color='#85754d', linestyle = '--', linewidth = 1.3, label = 'positivity threshold')

        plt.legend(frameon = False)

        plt.close() #closes figure and avoids displaying it in a seperate window

        sentiment_plot.figure.savefig(keyword_name+'_'+user_raw+'_SentimentAnalysis_'+start_date_raw+'_to_'+end_date_raw+'.jpg')
        print('Making your sentiment plot!')

    elif response_sentiment_plot == 'N':
        print('Ok. No sentiment analysis plot was made.')
    time.sleep(1) #adding delay between modules

#Scraping historical stock prices from user input ticker

    #Next we ask the user if they want a plot of the price over time
    make_price_plot = ['Y', 'N']
    price_response = None

    #This will keep asking until an appropriate response (i.e. in make_sentiment_plot) is given
    while price_response not in make_price_plot:
        price_response = input('Would you like to plot '+keyword_ticker+' price over time? (Y/N)')

    if price_response == 'Y':
        #Next we ask the user if they want to use new date ranges
        use_new_dates = ['Y', 'N']
        date_response = None

        #This will keep asking until an appropriate response (i.e. in use_new_dates) is given
        while date_response not in use_new_dates:
            date_response = input('With the same date range used for tweets? (Y/N)')

        if date_response == 'Y':
            stock_data = yf.download(keyword_ticker, start = start_date_raw, end = end_date_raw)   #creates a Pandas dataframe for desired ticker with start and end dates 

            #Creates a plot of price over time
            price_plot = stock_data.loc[:,'Close'].plot(kind = 'line', #plots only closing price
                            color = '#4b2e83', title = keyword_ticker+' closing price from '+start_date_raw+' until '+end_date_raw, label='closing price', 
                            xlabel = '',
                            ylabel = keyword_ticker+' Closing price (USD)', 
                            linewidth = 2,
                            figsize=(9,8)                 
                            )

            plt.legend(frameon = False)

            plt.close() #closes figure and avoids displaying it in a seperate window

            price_plot.figure.savefig(keyword_ticker+'_ClosingPrice_'+'from'+start_date_raw+'_until'+end_date_raw+'.jpg')
            print('Making your price plot!')

        elif date_response == 'N':
            new_price_start = input('What is the new start date? (format YYYY-MM-DD)')
            new_price_end = input('What is the new end date? (format YYYY-MM-DD)')

            stock_data = yf.download(keyword_ticker, start = new_price_start, end = new_price_end)   #creates a Pandas dataframe for desired ticker with start and end dates 

            #Creates a plot of price over time
            price_plot = stock_data.loc[:,'Close'].plot(kind = 'line', #plots only closing price
                            color = '#4b2e83', title = keyword_ticker+' closing price from '+new_price_start+' until '+new_price_end, label='closing price', 
                            xlabel = '',
                            ylabel = keyword_ticker+' Closing price (USD)', 
                            linewidth = 2,
                            figsize=(9,8)                 
                            )

            plt.legend(frameon = False)

            plt.close() #closes figure and avoids displaying it in a seperate window

            price_plot.figure.savefig(keyword_ticker+'_ClosingPrice_'+'from'+new_price_start+'_until'+new_price_end+'.jpg')
            print('Making your price plot!')

    elif price_response == 'N':
        print('Ok. No price plot was made.')

    time.sleep(1) #adds delay between modules 
    
    #Allow user to repeat process again
    play_again_answer = ['Y','N']
    response = None

    #This will keep asking until an appropriate response (i.e. in play_again_answer) is given
    while response not in play_again_answer:
        response = input('Would you like to obtain data for a new company and/or username? (Y/N)')

    if response == 'Y':     
        username_search()

    elif response == 'N':
        sys.exit()
        
if __name__ == '__main__': #ensures that when the StockSentiment_functions.py is imported, function only runs when called rather than immediately upon import
    username_search()






