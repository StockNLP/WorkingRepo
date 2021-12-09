import datetime
import re

class RedditData:
    '''
    This class contains helper functions that parse through a PushShift API object to return a
    cleaned dataframe with separated Date-wise Tags and Comment values.
    '''
    def __init__(self, name):
        self.name = name
    
    def has_numbers(input_String):
        '''
        This function looks at the $Tag and checks if it contains a dollar value or a ticker symbol. For eg. is it $9 or
        $AMC. Returns True if it is a number and false if it is a string. 
        '''
        return any(char.isdigit() for char in input_String)

    def get_subreddit_column(subreddit, lst_tags): 
        '''
        This function takes the channel variable and the dataframe of api results as input and adds a column in the same 
        dataframe of the length of the dataframe and populates it with the name of the subreddit (channel variable) name.
        '''
        arr = []
        size = len(lst_tags)
        arr += size * [str(subreddit)]
        return (arr)

    def cashtags(submissions):
        '''
        This function takes the api JSON values and the dataframe. It extracts the $Tags from the comments and stores them
        in a separate column, corresponding to the row of the comment. It also filters out the $Tags that are empty and 
        those that have a $Numerical value. Returns a list of tags and a list of comments. 
        '''
        tag_list = []
        comment_list = []
        date_list = []
        lst_tag = []
        lst_comments = []
        lst_date = []
        for submission in submissions:
            words = submission.title.split()
            cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))
            if  len(cashtags) > 0:
                val = RedditData.has_numbers(str(cashtags))
                if (val == False):
                    tag_list.append(cashtags)
                    comment_list.append(submission.title)
                    date = datetime.datetime.fromtimestamp(submission.created_utc).replace(tzinfo=datetime.timezone.utc).strftime("%m/%d/%Y")
                    date_list.append(date)
        length = len(tag_list)
        for i in range(length):
            if len(tag_list[i]) >= 1:
                for j in range(len(tag_list[i])):
                    clean_tag = RedditData.has_special_chars((tag_list[i][j]))
                    lst_tag.append(clean_tag)
                    lst_comments.append(comment_list[i])
                    lst_date.append(date_list[i])  
        return lst_tag, lst_comments, lst_date
       
    def add_to_df(tag, comment, date, df):
        '''
        This function takes the list of tags, list of columns, subreddit list and the working dataframe as inputs and 
        appends each values to the corresponding rows.
        '''
        for i in range(len(comment)):
            df_length = len(df)
            df.loc[df_length] = date[i], comment[i], tag[i] 

    def has_special_chars(String):
        """ 
        This function takes a string that is stripped of the $ sign from the ticker and returns coded value.
        Codes:- 1: Valid Ticker (No special characters), -1: Trailing Special Character 
        (Requires removal of trailing character) and 0: Invalid Ticker (Contains non-trailing special characters).
        """
        Sub_str = String[1:]
        dollar = String[:1]
        if RedditData.have_special_chars(Sub_str):
            Sub_str = re.sub(r'\W+', '', Sub_str)
        clean_string = dollar + Sub_str
        return clean_string.upper()

    def have_special_chars(String):
        '''This is a helper function used inside the has_special_chars() function that takes in a string as an input 
        and returns boolean True if the passed string contains a special character.'''
        regexp = re.compile('[^a-zA-Z]+')
        if regexp.search(String):
            return True