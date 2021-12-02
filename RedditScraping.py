#!/usr/bin/env python
# coding: utf-8

# In[78]:


#Dependencies
import json
from psaw import PushshiftAPI
import datetime
from pandas.io.json import json_normalize
import pandas as pd
import numpy as np
import time 
import re


# In[41]:


#Defines the DataFrame
df_reddit = pd.DataFrame(columns = ['Comment', 'Tags', 'Subreddit'])


# In[42]:


#Initializes the PushshitAPI to variable 'api'
api = PushshiftAPI()


# In[43]:


#We are defining 4 different subreddits (groups)
subreddits = ['wallstreetbets', 'robinhood', 'stocks', 'investing']


# In[71]:


#We get the user's input of which subreddit they want to check. In the dashboard, this will be a dropdown menu.
channel = str(input('Please input which subreddit you want to search: '+ str(subreddits) ))


# In[72]:


#This is the start time from which the data will be pulled. 
start_time = int(datetime.datetime(2021, 11, 24).timestamp())


# In[73]:


# This function checks if the tag has a number or not. Returns True or False. 
def has_numbers(inputString):
    '''
    This function looks at the $Tag and checks if it contains a dollar value or a ticker symbol. For eg. is it $9 or
    $AMC. Returns True if it is a number and false if it is a string. 
    '''
    return (any(char.isdigit() for char in inputString))


# In[74]:


def get_subreddit_column(subreddit, df): 
    '''
    This function takes the channel variable and the dataframe of api results as input and adds a column in the same 
    dataframe of the length of the dataframe and populates it with the name of the subreddit (channel variable) name. 
    '''
    arr = []
    size = len(df)
    arr += size * [str(subreddit)]
    return list(arr)


# In[59]:


def cashtags(submissions, df):
    '''
    This function takes the api JSON values and the dataframe. It extracts the $Tags from the comments and stores them
    in a separate column, corresponding to the row of the comment. It also filters out the $Tags that are empty and 
    those that have a $Numerical value. Returns a list of tags and a list of comments. 
    '''
    tag_list = []
    comment_list = []
    
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
    return tag_list, comment_list


# In[60]:


def add_to_df(tag, comment, subreddit, df):
    '''
    This function takes the list of tags, list of columns, subreddit list and the working dataframe as inputs and 
    appends each values to the corresponding rows.
    '''
    for i in range(len(comment)):
        df_length = len(df)
        df.loc[df_length] = comment[i], tag[i], subreddit


# In[169]:


def main():
    """ 
    This is the main function that runs the API, and adds the results to the dataframe after corresponding Dataframe. 
    """
    submissions = list(api.search_submissions(after=start_time,
                       subreddit=channel,
                       #filter=['author', 'title', 'subreddit', 'subscribers', 'comment_score_hide_mins']
                       limit=5000))
    tag, comment = cashtags(submissions, df_reddit)
    subreddit = get_subreddit_column(channel, df_reddit)
    add_to_df(tag, comment, channel, df_reddit)


# In[170]:


if __name__ == "__main__": 
    main()


# In[171]:


df_reddit


# # # Ignore from here onwards for now. 

# In[108]:


df_reddit.to_csv("Reddit_Test.csv")


# In[119]:


for i in range(len(df_reddit['Tags'])):
    if len(df_reddit['Tags'][i]) > 1:
        
    else: 
        
        
        
        


# In[98]:


df_reddit.iloc[2]


# In[167]:



def split_multi_tickers(df):
    '''
    This function takes the 
    '''
    df_multi = pd.DataFrame(columns = ['Comment', 'Tags', 'Subreddit'])
    len_tags = len(df['Tags'])
    index_drop = []
    for i in range(len_tags):
        if len(df['Tags'][i])>1:
            lst_tickers = df['Tags'][i]
            for j in range(len(lst_tickers)):
                ser = pd.Series([df['Comment'][i],lst_tickers[j], df['Subreddit'][i]],index=['Comment', 'Tags', 'Subreddit'])
                df_multi = df_multi.append(ser, ignore_index=True) 
            index_drop.append(i)
        else:
            pass
    
    print(index_drop)
    print(df_multi)
    
    #df.drop(df.index[index_drop])  
    #df = df.append(df_multi)
        
        
    


# In[168]:


split_multi_tickers(df_reddit)


# In[158]:


df_reddit


# In[112]:


split_multi_tickers


# In[84]:


def has_special_characters(string):
    """ 
    This function takes a string that is stripped of the $ sign from the ticker and returns coded value.
    Codes:- 1: Valid Ticker (No special characters), -1: Trailing Special Character 
    (Requires removal of trailing character) and 0: Invalid Ticker (Contains non-trailing special characters).
    """
    start = time.time()
    regexp = re.compile('[^a-zA-Z]+')
    string = string[-1:]
    if regexp.search(string):
        deprecated = string[:-1]
        if regexp.search(string[:-1]):
            return 1
        elif regexp.search(deprecated):
            return -1
        else:
            pass
    else:
        return 0
    end = time.time()
    print(f"Time taken to finish executing this program: {end-start} seconds")


# In[85]:


val = has_special_characters("TSLA?")


# In[86]:


val


# In[16]:


string = "T:SLA"


# In[31]:


string[:2]


# In[5]:


val = has_special_characters("T:SLA")


# In[6]:


val


# In[103]:





# In[359]:


print(symbol[:-1])


# In[360]:


print(symbol[-1:])


# In[364]:


def get_stripped_ticker(string):
    return str(string[:-1])


# In[365]:


val = get_stripped_ticker("TSLA?")


# In[366]:





# In[138]:





# In[ ]:




