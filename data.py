import pandas as pd
import requests
import json
import csv
import time
import datetime

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
    'csgo',
    'aww',
]


def getSubmissionData(sub):
    url = base_url + 'submission/?subreddit=' + \
        sub + '&size=' + str(query_size)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']


def getCommentData(sub):
    url = base_url + 'comment/?subreddit=' + sub + '&size=' + str(query_size)
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
        comment_data = getCommentData(subreddit)
        print(comment_data)
