#!/usr/bin/env python
# coding: utf-8
"""
high level support for doing this and that. (NEEDS TO BE EDITED)
"""
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import warnings
import re
import pandas as pd
warnings.filterwarnings("ignore")
nltk.download('vader_lexicon')
warnings.filterwarnings("ignore")


df_t = pd.DataFrame(columns=['Tweet','Tick', 'Source','Date','Likes', 'Retweet Count'])

#get_tick = ['$AMC','$GMC','$TSLA','$MSFT','$AAPL','$DOGE','$SHIB','$ETH','$PROG','$BTC','$ADA',
#'$NKLA','$GOOGL','$RIVN','$FB']

class TwitterData:
    '''
    The class TwitterData essentially has helper functions.
    '''
    def __init__(self,get_tick):
        '''
        The class TwitterData essentially has helper functions.
        '''
        self.get_tick = get_tick
    @staticmethod
    def add_to_df(lst, df, tck, src, date,like_count, retweet_count):
        """
        This function essentially takes three arguments search_stock, start_date & tweet_count
        It basically returns a list with tweets and its respective information.
        Extended description of function:

        The function as per the parameters take the required information and subsequently filters
        API search and grabs tweets in english language with latest tweet count as mentioned in the
        parameter. We store them in a list and return the list that contains information
        of the tweets pulled on that day and their respective.


        Parameters
        ----------
        arg1 : string
            This essentially takes in the stock ticker symbol.
        arg2 : Date-time
            This essentially takes in the the date of the tweets that we want to pull.
        arg3: int
            This argument takes in the count of the tweets that we want to pull from twitter.

        Returns
        -------
        list
            This function returns the list of tweets with all other information that we require.

        """
        for i in range(len(lst)):
            df_length = len(df)
            df.loc[df_length] = lst[i], tck[i], src[i], date[i],like_count[i], retweet_count[i]
    @staticmethod
    def tick_list(tick,ls):
        '''
        The function apparently takes in two arguments ticker and the length of the list.
        It essentially computes the length of the list and appends the respective stock ticker
        We return the stock ticker and the source of the data
        '''
        arr = []
        arr_two = []
        size = len(ls)
        arr += size * [tick]
        arr_two += size * ["Twitter"]
        return arr, arr_two
    @staticmethod
    def get_like_retweet_lst(ls):
        '''
        This function essentially takes in takes the list that we generated from twitter API call
        that contains information such as tweet, tweet_id, date etc and apparently stores the 
        likes, tweet date and re-tweets count and accordingly appends and returns them. 
        '''
        like = []
        rtweet = []
        date = []
        for i in range(len(ls)):
            date.append(ls[i][2])
            like.append(ls[i][3])
            rtweet.append(ls[i][4])
        return date,like, rtweet

    @staticmethod
    def PreProcessing( df_t):
        '''
        This function is to pre_process the data that we extracted from the earlier function
        It takes in the dataframe that we extracted earlier and subsequently preprocesses them
        using the following steps and apparently creates a new column for hastag and cleaned tweet
        and appends it to the existing dataframe.
        '''
        df_t['hashtag'] = df_t['Tweet'].apply(lambda x: re.findall(r"#(\w+)", str(x)))
        df_t['clean_tweet'] = df_t['Tweet']
        #html
        df_t.clean_tweet = df_t.clean_tweet.apply(lambda x: re.sub(r'https?:\/\/\S+', '', str(x)))
        df_t.clean_tweet.apply(lambda x: re.sub(r"www\.[a-z]?\.?(com)+|[a-z]+\.(com)", '', str(x)))
        df_t.clean_tweet = df_t.clean_tweet.apply(lambda x: re.sub(r'@[\w]+', '', x))
        df_t.clean_tweet = df_t.clean_tweet.apply(lambda x: re.sub(r'{link}', '', x))
        df_t.clean_tweet = df_t.clean_tweet.apply(lambda x: re.sub(r"\[video\]", '', x))
    @staticmethod
    def VaderScoreGenerator(df_t):
        '''
        This function takes in the dataframe that we appeneded earlier and computes the sentiment
        scores and extracts the polarity scores using the Vader Sentiment Analyzer
        '''
        sia = SentimentIntensityAnalyzer()
        df_t['Negative'] = df_t['clean_tweet'].apply(lambda x:sia.polarity_scores(str(x))['neg'])
        df_t['Neutral'] = df_t['clean_tweet'].apply(lambda x:sia.polarity_scores(str(x))['neu'])
        df_t['Positive'] = df_t['clean_tweet'].apply(lambda x:sia.polarity_scores(str(x))['pos'])
        df_t['Compound'] = df_t['clean_tweet'].apply(lambda x:sia.polarity_scores(str(x))
        ['compound'])
        df_t['Weights'] = df_t.apply(lambda row: (0.01
                                          if row['Likes'] == 0 and row['Retweet Count'] == 0
                                          else (int(row['Likes'])+int(row['Retweet Count']))*10
                                                     ), axis=1)
        df_t['Total_Weighted_Score'] = df_t.apply(lambda row: (row['Compound']* row['Weights']),
        axis=1)
    @staticmethod
    def AppendToMaster(df_t):
        '''
        This function apparently takes the data frame that we preprocessed earlier and appends it 
        to the master csv file that we have been collecting.
        '''
        df_t.to_csv('/Users/adityachalla/Desktop/CSE 583 Project/Twitter_Data_Master.csv',
        mode='a', header=False)

    @staticmethod
    def GenerateDataforEachStock():
        '''
        This function essentially reads the master csv file reads it and subsets the ticker
        to get the average sentiment score overall.
        '''
        df_twitter_master = pd.read_csv(
        "/Users/adityachalla/Desktop/CSE 583 Project/Twitter_Data_Master.csv")

        def get_subset(stock_name, df_twitter_master):
            '''
            This function apparently takes the stock name and the data frame that we read above
            and subseqiuently returns the mastert ticker
            '''
            df_master_ticker = df_twitter_master.loc[df_twitter_master['Tick'] == stock_name]
            return df_master_ticker

        def get_score(df_twitter_master):
            '''
            This function groups the total weighted score metric by date and aggreates it by sum
            We then return the dataframe which gives the mean sentiment score of a particular stock 
            '''
            df_grp = df_twitter_master.groupby('Date')['Total_Weighted_Score'].aggregate(['sum',
            'count'])
            df_grp['Sentiment_Score'] = df_grp.apply(lambda x: (x['sum']/x['count']), axis=1)
            return df_grp


        df_re = get_subset('$AMC', df_twitter_master)
        df_grp = get_score(df_re)
        return df_grp
