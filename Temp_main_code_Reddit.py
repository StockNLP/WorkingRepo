#!/usr/bin/env python
# coding: utf-8

# In[25]:


from psaw import PushshiftAPI
import datetime 
import pandas as pd
import numpy as np
from Scraper import RedditData as rd


# In[26]:


def main():
    '''
    This is the main function that runs the API, and adds the results to the dataframe after corresponding Dataframe. 
    '''
    start = time.time()
    df_reddit = pd.DataFrame(columns = ['Date','Comment', 'Tags'])
    subreddits = ['wallstreetbets', 'robinhood', 'stocks', 'investing']
    channel = str(input('Please input which subreddit you want to search: '+ str(subreddits) ))
    start_time = int(datetime.datetime(2021, 10, 1).timestamp())
    api = PushshiftAPI()
    df_master = pd.read_csv('Reddit_Test.csv', index_col = 0)
    #start_time = int(datetime.datetime(2021, 10, 1).timestamp())
    submissions = list(api.search_submissions(after=start_time,
                       subreddit=channel,
                       filter=['author', 'title', 'subreddit', 'subscribers', 'comment_score_hide_mins'],
                      limit=1000))
    tag, comment, date = rd.cashtags(submissions)
    #tag_flat, comment_flat, date_flat = flatten_list(tag, comment, date)
    #subreddit = rd.get_subreddit_column(channel, tag)
    rd.add_to_df(tag, comment, date, df_reddit)
    df_master = df_master.append(df_reddit)
    df_master.to_csv("Reddit_Final.csv")
    end = time.time()
    print(f'This process took {end-start} to run')
    


# In[27]:


if __name__ == "__main__": 
    main()  


# In[28]:


df = pd.read_csv('Reddit_Final.csv', index_col=0)


# In[29]:


df 


# In[22]:





# In[ ]:




