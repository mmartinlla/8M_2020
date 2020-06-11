# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 13:07:49 2020

Code source:
    - Author: Bhaskar Karambelkar
    - Source_url: https://bhaskarvk.github.io/2015/01/how-to-use-twitters-search-rest-api-most-effectively./

Modified by: Marta Martin Llambes
"""
# Import all necessary libraries.
import sys
import jsonpickle
import time
import tweepy

# Import the file with your API credentials.
import twitter_credentials_search

# Authentication.
auth = tweepy.AppAuthHandler(twitter_credentials_search.CONSUMER_KEY, twitter_credentials_search.CONSUMER_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True,
				   wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

# Define the list of hashtags you are interested in.
searchQuery = ("#8M" or "#8M2020" or "#8deMarzo" or "#8marzo2020" or "#DiaInternacionalDeLaMujer" or "#DiaDeLaMujer" or "#8Marzo") 
# Maximum number of tweets you want to get.
maxTweets = 10000000 
# Tweets per query: 100 is the max the API permits
tweetsPerQry = 100  
# Define the name of the file where the tweets are going to be printed.
fName ='tweets'+'_'+time.strftime('%Y%m%d-%H%M%S')+'.json'

# If results from a specific ID onwards are required, set since_id to that ID.
# else default to no lower limit, and it goes as far back as API allows
sinceId = 1236788662899298305

# If results only before a specific ID are required, set max_id to that ID.
# else default to no upper limit, start from the most recent tweet matching the search query.
max_id = -1

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))
with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
                f.write(jsonpickle.encode(tweet._json) + '\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))