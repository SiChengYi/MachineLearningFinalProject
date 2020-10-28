import pandas as pd
import requests
import json
import csv
import time
import datetime

# All data is collected based on past \query_size\ submissions/comments
########## DATASET STRUCTURE #############

# subreddit_name | submission_titles_containing_toxic_words | submissions_containing_toxic_words | total_submissions_score | total_comments_score | comments_containing_toxic_words | subreddit_subscribers | repeat_top_voted_users

##########################################

# Size of reddit query
query_size = 50

# URL to reach the pushshift API
base_url = 'https://api.pushshift.io/reddit/search/'

# List of all toxic words
toxic_words = []

toxic_words_file_path = './toxicwords.txt'

# Subreddits to check
subreddits = [
    'news',
    'csgo',
    'aww',
]

all_data = {}

def getSubmissionData(sub, query_params={}):
    url = base_url + 'submission/?subreddit=' + \
        sub + '&mod_removed=false&after=2020-10-01&before=2020-10-27&size=' + str(query_size)
    for param in query_params:
        ''' Add all requested query params to url '''
        url = url + '&' + param + '=' + str(query_params[param])
    print('URL ', url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']


def getCommentData(sub, query_params=[]):
    url = base_url + 'comment/?subreddit=' + sub + '&mod_removed=false&after=2020-10-01&before=2020-10-27&size=' + str(query_size)
    for param in query_params:
        ''' Add all requested query params to url '''
        url = url + '&' + param + '=' + str(query_params[param])
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']

if __name__ == '__main__':
    with open(toxic_words_file_path, 'r') as fp:
        # Append the toxic_words list with all of the words in our file
        [toxic_words.append(line.rstrip('\n')) for line in fp]

    # For every subreddit, search the last 400 submissions/comments for our toxic words
    for subreddit in subreddits:
        
        # SUBMISSION DATA
        submission_data = getSubmissionData(subreddit)
        number_removed = 0
        toxic_title_count = 0
        toxic_submission_count = 0
        total_submission_score = 0
        for data in submission_data:
            # Count toxic words in submission
            for word in toxic_words:
                toxic_title_count = toxic_title_count + data['title'].split(' ').count(word)
                if 'selftext' in data:
                    toxic_submission_count = toxic_submission_count + data['selftext'].split(' ').count(word)
            # Add submission score
            total_submission_score = total_submission_score + int(data['score'])

        all_data[subreddit] = {}
        all_data[subreddit]['subscribers'] = int(data['subreddit_subscribers'])
        all_data[subreddit]['submission_titles_containing_toxic_words'] = toxic_title_count
        all_data[subreddit]['submissions_containing_toxic_words'] = toxic_submission_count
        all_data[subreddit]['total_submissions_score'] = total_submission_score
        #################
        
        # COMMENT DATA
        comment_data = getCommentData(subreddit)
        toxic_comment_count = 0
        total_comment_score = 0
        for data in comment_data:
            # Count toxic words in comment
            for word in toxic_words:
                toxic_comment_count = toxic_comment_count + data['body'].split(' ').count(word)

            # Add comment score 
            total_comment_score = total_comment_score + int(data['score'])

        all_data[subreddit]['comments_containing_toxic_words'] = toxic_comment_count
        all_data[subreddit]['total_comments_score'] = total_comment_score
        ##############

        print(all_data)
