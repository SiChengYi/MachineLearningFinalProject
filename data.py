import pandas as pd
import requests
import json
import csv
import time
import datetime

# All data is collected based on past \query_size\ submissions/comments
########## DATASET STRUCTURE #############
# subreddit_name | number_of_posts_removed_by_mod | submissions_containing_toxic_words | comments_containing_toxic_words | subreddit_subscribers | repeat_top_voted_users
# aww            | 10                             | 2                                  | 10                              | 5                     | 2
##########################################

# Size of reddit query
query_size = 1

# URL to reach the pushshift API
base_url = 'https://api.pushshift.io/reddit/search/'

# List of all toxic words
toxic_words = []

toxic_words_file_path = './toxicwords.txt'

# Subreddits to check
subreddits = [
    'news',
    # 'csgo',
    # 'aww',
]


def getSubmissionData(sub, query_params={}):
    url = base_url + 'submission/?subreddit=' + \
        sub + '&size=' + str(query_size)
    for param in query_params:
        ''' Add all requested query params to url '''
        url = url + '&' + param + '=' + str(query_params[param])
    print('URL ', url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']


def getCommentData(sub, query_params=[]):
    url = base_url + 'comment/?subreddit=' + sub + '&size=' + str(query_size)
    for param in query_params:
        ''' Add all requested query params to url '''
        url = url + '&' + param + '=' + str(query_params[param])
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']


if __name__ == '__main__':
    with open(toxic_words_file_path, 'r') as fp:
        # Append the toxic_words list with all of the words in our file
        [toxic_words.append(line) for line in fp]

    # For every subreddit, search the last 400 submissions/comments for our toxic words
    for subreddit in subreddits:
        submission_data = getSubmissionData(subreddit)
        # comment_data = getCommentData(subreddit)
        print(submission_data)
