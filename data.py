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

# data_columns = ['subreddit_name', 'submission_titles_containing_toxic_words', 'submissions_containing_toxic_words',
#                 'total_submissions_score', 'total_comments_score', 'comments_containing_toxic_words', 'subscribers']
data_columns = [
    'subreddit_name',
    'subscribers',
    'submission_titles_containing_toxic_words',
    'submissions_containing_toxic_words',
    'total_submissions_score',
    'comments_containing_toxic_words',
    'total_comments_score',
    'is_toxic'
]

# Size of reddit query
query_size = 100

# URL to reach the pushshift API
base_url = 'https://api.pushshift.io/reddit/search/'

# List of all toxic words
toxic_words = []

toxic_words_file_path = './toxicwords.txt'

# Subreddits to check
# 1 for toxic
# 0 for non-toxic
subreddits = {
    'news': 1,
    'csgo': 1,
    'dankmemes': 1,
    'tumblrinaction': 1,
    'relationships': 1,
    'movies': 1,
    'gaming': 1,
    '4chan': 1,
    'politics': 1,
    'leagueoflegends': 1,
    'apexlegends': 1,
    'trashy': 1,
    'niceguys': 1,
    'unpopularopinion': 1,
    'insanepeoplefacebook': 1,
    'choosingbeggars': 1,
    'nottheonion': 1,
    'copypasta': 1,
    'roastme': 1,
    'publicfreakout': 1,
    'politicalhumor': 1,
    'agedlikemilk': 1,
    'sports': 1,
    'therightcantmeme': 1,
    'rareinsults': 1,
    'gamingcirclejerk': 1,
    'tifu': 1,
    'joerogan': 1,
    'quityourbullshit': 1,
    'toiletpaperusa': 1,
    'cyberpunkgame': 1,
    'bad_cop_no_donut': 1,
    'greentext': 1,
    'iamverysmart': 1,
    'notlikeothergirls': 1,
    'tumblr': 1,
    'tiktokcringe': 1,
    'shitpostcrusaders': 1,
    'relationship_advice': 1,
    'rainbow6': 1,
    'teenagers': 1,
    'truegaming': 1,
    'winstupidprizes': 1,
    'madlads': 1,
    'cursedcomments': 1,
    'iamverybadass': 1,
    'blursedimages': 1,
    'makemesuffer': 1,
    'modernwarfare': 1,
    'destiny2': 1,
    'dota2': 1,
    'jokes': 1,
    'bonehurtingjuice': 1,
    'askouija': 1,
    'tihi': 1,
    'facepalm': 1,
    'rareinsults': 1,
    'justneckbeardthings': 1,
    'gatekeeping': 1,
    'forhonor': 1,
    'holup': 1,
    'propagandaposters': 1,
    'mensrights': 1,
    'prorevenge': 1,
    'gamernews': 1,
    'okbuddyretard': 1,
    'programmerhumor': 1,
    'fragilewhiteredditor': 1,
    'insaneparents': 1,
    'entitledparents': 1,
    'announcements': 1,
    'askreddit': 0,
    'earthporn': 0,
    'lifeprotips': 0,
    'gadgets': 0,
    'absoluteunits': 0,
    'aww': 0,
    'explainlikeimfive': 0,
    'todayilearned': 0,
    'anime': 0,
    'nutrition': 0,
    'classicalmusic': 0,
    'funny': 0,
    'fishing': 0,
    'python': 0,
    'photoshopbattles': 0,
    'justrolledintotheshop': 0,
    'nostupidquestions': 0,
    'pcmasterrace': 0,
    'coolguides': 0,
    'rarepuppers': 0,
    'eatcheapandhealthy': 0,
    'cooking': 0,
    'backpacking': 0,
    'pics': 0,
    'elderscrollsonline': 0,
    'mademesmile': 0,
    'oddlysatisfying': 0,
    'showerthoughts': 0,
    'humansbeingbros': 0,
    'animalsbeingderps': 0,
    'astronomy': 0,
    'harrypotter': 0,
    'unexpected': 0,
    'wholesomememes': 0,
    'holdmyredbull': 0,
    'snowboarding': 0,
    'bicycling': 0,
    'penmanshipporn': 0,
    'tennis': 0,
    'sysadmin': 0,
    'getmotivated': 0,
    'adviceanimals': 0,
    'gifs': 0,
    'cozyplaces': 0,
    'analog': 0,
    'outoftheloop': 0,
    'startledcats': 0,
    'toptalent': 0,
    'specializedtools': 0,
    'dnd': 0,
    'seaofthieves': 0,
    'roblox': 0,
    'maybemaybemaybe': 0,
    'food': 0,
    'nevertellmetheodds': 0,
    'naturewasmetal': 0,
    'thatsinsane': 0,
    'hmmm': 0,
    'skyrim': 0,
    'compsci': 0,
    'mtb': 0,
    'stardewvalley': 0,
    'mechanicalkeyboards': 0,
    'youshouldknow': 0,
    'mechanical_gifs': 0,
    'art': 0,
    'baking': 0,
    'dadjokes': 0,
    'smashbrosultimate': 0,
    'datascience': 0,
    'persona5': 0,
    'doctorwho':0,
    'deeprockgalactic': 0,
    'diy': 0,
    'machinelearning': 0,
    'gardening': 0,
    'warframe': 0,
    'monsterhunterworld': 0,
    'edmproduction': 0,
    'borderlands3': 0
}

all_data = []


def getSubmissionData(sub, query_params={}):
    url = base_url + 'submission/?subreddit=' + \
        sub + '&mod_removed=false&after=2020-10-01&before=2020-10-27&size=' + \
        str(query_size)
    for param in query_params:
        ''' Add all requested query params to url '''
        url = url + '&' + param + '=' + str(query_params[param])
    print('URL ', url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']


def getCommentData(sub, query_params=[]):
    url = base_url + 'comment/?subreddit=' + sub + \
        '&mod_removed=false&after=2020-10-01&before=2020-10-27&size=' + \
        str(query_size)
    for param in query_params:
        ''' Add all requested query params to url '''
        url = url + '&' + param + '=' + str(query_params[param])
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']


def makeCsv():
    # Turn the all_data
    with open('data.csv', 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames=data_columns)
        writer.writeheader()
        for data in all_data:
            writer.writerow(data)


if __name__ == '__main__':
    with open(toxic_words_file_path, 'r') as fp:
        # Append the toxic_words list with all of the words in our file
        [toxic_words.append(line.rstrip('\n')) for line in fp]

    # For every subreddit, search the last 400 submissions/comments for our toxic words
    for subreddit, toxic in subreddits.items():

        # SUBMISSION DATA
        submission_data = getSubmissionData(subreddit)
        number_removed = 0
        toxic_title_count = 0
        toxic_submission_count = 0
        total_submission_score = 0
        new = {}
        new['subreddit_name'] = subreddit
        for data in submission_data:
            new['subscribers'] = int(data['subreddit_subscribers'])

            # Count toxic words in submission
            for word in toxic_words:
                toxic_title_count = toxic_title_count + \
                    data['title'].split(' ').count(word)
                if 'selftext' in data:
                    toxic_submission_count = toxic_submission_count + \
                        data['selftext'].split(' ').count(word)
            # Add submission score
            total_submission_score = total_submission_score + \
                int(data['score'])

        new['submission_titles_containing_toxic_words'] = toxic_title_count
        new['submissions_containing_toxic_words'] = toxic_submission_count
        new['total_submissions_score'] = total_submission_score
        #################

        # COMMENT DATA
        comment_data = getCommentData(subreddit)
        toxic_comment_count = 0
        total_comment_score = 0
        for data in comment_data:
            # Count toxic words in comment
            for word in toxic_words:
                toxic_comment_count = toxic_comment_count + \
                    data['body'].split(' ').count(word)

            # Add comment score
            total_comment_score = total_comment_score + int(data['score'])

        new['comments_containing_toxic_words'] = toxic_comment_count
        new['total_comments_score'] = total_comment_score
        new['is_toxic'] = subreddits[subreddit]
        all_data.append(new)
        ##############

    makeCsv()
