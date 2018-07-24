import tweepy
import requests
import json
import time
import cPickle as pickle

def tweepy_access(): 
    ''' Tweepy API authentication. Consumer key and access key have been omitted. Please set these variables with values for your twitter handle from app.twitter.com '''
    consumer_key = '#############'
    consumer_secret = '#############'
    access_token = '#############'
    access_token_secret = '#############'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

def retrieve_jobs():
    ''' returns python related jobs ''' 
    keyword = "python"
    link = "https://jobs.github.com/positions.json?description=" + keyword
    r = requests.get(link)
    jobs = json.loads(r.text)
    return jobs


def load_ids():
    ''' returns job id's that are already tweeted out to avoid repetition '''
    x = open('jobs.p', 'rb')
    ids = pickle.load(x)
    x.close()
    return ids

api = tweepy_access()
ids = set()

# Try loading the jobs.p file to see if it exists. If not, we pickle the empty set, without this you may recieve errors. This is where jobs.p is created as well.
try:
    foo = pickle.load(open("jobs.p", "rb"))
except (OSError, IOError) as e:
    f = open('jobs.p', 'wb')
    pickle.dump(ids, f, -1)
    f.close()

#Posts any new listings, refreshed every 2 hours
while True:
    ids = load_ids()
    jobs = retrieve_jobs()

    for job in jobs: 
        id = job['id']

        if id in ids: 
            break
        else: 
            f = open('jobs.p', 'wb')
            ids.add(id)
            pickle.dump(ids, f, -1)
            f.close()
            message = 'Apply Now: ' + job['title'] + ' in ' + job['location'] + '\n'+ job['url'] + '\n'
            api.update_status(status=message)
    time.sleep(7200)