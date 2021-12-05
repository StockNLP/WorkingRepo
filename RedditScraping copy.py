#!/usr/bin/env python
# coding: utf-8

# In[254]:


#Dependencies
import json
from psaw import PushshiftAPI
import datetime 
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
import time 
import re


# In[283]:


#Defines the DataFrame
df_reddit = pd.DataFrame(columns = ['Date','Comment', 'Tags', 'Subreddit'])


# In[171]:


#Initializes the PushshitAPI to variable 'api'
api = PushshiftAPI()


# In[172]:


#We are defining 4 different subreddits (groups)
subreddits = ['wallstreetbets', 'robinhood', 'stocks', 'investing']


# In[345]:


#We get the user's input of which subreddit they want to check. In the dashboard, this will be a dropdown menu.
channel = str(input('Please input which subreddit you want to search: '+ str(subreddits) ))


# In[284]:


#This is the start time from which the data will be pulled. 
start_time = int(datetime.datetime(2021, 10, 20).timestamp())


# In[262]:


# This function checks if the tag has a number or not. Returns True or False. 
def has_numbers(inputString):
    '''
    This function looks at the $Tag and checks if it contains a dollar value or a ticker symbol. For eg. is it $9 or
    $AMC. Returns True if it is a number and false if it is a string. 
    '''
    return (any(char.isdigit() for char in inputString))


# In[263]:


def get_subreddit_column(subreddit, df): 
    '''
    This function takes the channel variable and the dataframe of api results as input and adds a column in the same 
    dataframe of the length of the dataframe and populates it with the name of the subreddit (channel variable) name. 
    '''
    arr = []
    size = len(df)
    arr += size * [str(subreddit)]
    return list(arr)


# In[264]:


def cashtags(submissions, df):
    '''
    This function takes the api JSON values and the dataframe. It extracts the $Tags from the comments and stores them
    in a separate column, corresponding to the row of the comment. It also filters out the $Tags that are empty and 
    those that have a $Numerical value. Returns a list of tags and a list of comments. 
    '''
    tag_list = []
    comment_list = []
    date_list = []
    for submission in submissions:
        words = submission.title.split()
        cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
    #Filters out empty $Tags and numerical $Tags. Adds the filtered values to two lists. A list of tags and a list
    # of comments. 
        if  (len(cashtags) > 0) :
            val = has_numbers(str(cashtags))
            if (val == False):
                tag_list.append(cashtags)
                comment_list.append(submission.title)
                date = datetime.datetime.fromtimestamp(submission.created_utc).replace(tzinfo=datetime.timezone.utc).strftime("%m/%d/%Y")
                date_list.append(date)
    lst_tags, lst_comments, lst_date = __flatten_list(tag_list, comment_list, date_list)   
    return lst_tags, lst_comments, lst_date


# In[265]:


def __flatten_list(tags, comments, dates):
    lst_tags = []
    lst_comments = []
    lst_date = []
    length = len(tags)
    for i in range(length):
        if len(tags[i]) >= 1:
            for j in range(len(tags[i])):
                clean_tag = has_special_chars((tags[i][j]))
                lst_tags.append(clean_tag)
                lst_comments.append(comments[i])
                lst_date.append(dates[i])
    return lst_tags, lst_comments, lst_date
                
    


# In[267]:


def add_to_df(tag, comment, date, subreddit, df):
    '''
    This function takes the list of tags, list of columns, subreddit list and the working dataframe as inputs and 
    appends each values to the corresponding rows.
    '''
    for i in range(len(comment)):
        df_length = len(df)
        df.loc[df_length] = date[i], comment[i], tag[i], subreddit


# In[268]:


def has_special_chars(string):
    """ 
    This function takes a string that is stripped of the $ sign from the ticker and returns coded value.
    Codes:- 1: Valid Ticker (No special characters), -1: Trailing Special Character 
    (Requires removal of trailing character) and 0: Invalid Ticker (Contains non-trailing special characters).
    """
    regexp = re.compile('[^a-zA-Z]+')
    st = string[1:]
    dollar = string[:1]
    if __has_special_chars(st):
        st = re.sub('\W+','', st)
    clean_string = dollar+st
    return clean_string.upper()

def __has_special_chars(string):
    regexp = re.compile('[^a-zA-Z]+')
    if regexp.search(string):
        return True
    else:
        return False


# In[346]:


def main():
    """ 
    This is the main function that runs the API, and adds the results to the dataframe after corresponding Dataframe. 
    """
    start = time.time()
    df_reddit = pd.DataFrame(columns = ['Date','Comment', 'Tags', 'Subreddit'])
    df_master = pd.read_csv('Reddit_Test.csv', index_col = 0)
    submissions = list(api.search_submissions(after=start_time,
                       subreddit=channel,
                       filter=['author', 'title', 'subreddit', 'subscribers', 'comment_score_hide_mins'],
                      ))#limit=10000))
    tag, comment, date = cashtags(submissions, df_reddit)
    subreddit = get_subreddit_column(channel, df_reddit)
    add_to_df(tag, comment, date, channel,df_reddit)
    df_master = df_master.append(df_reddit)
    df_master.to_csv("Reddit_Test.csv")
    end = time.time()
    print(f'This process took {end-start} to run')
    


# In[347]:


if __name__ == "__main__": 
    main()


# In[ ]:




