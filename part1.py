from pymongo import MongoClient
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import re

client = MongoClient('localhost', 27017)
db = client['twitterdb']
collection = db['twitter_search']
tweets_iterator = collection.find()

# for tweet in tweets_iterator:
#   print('tweet text: ',tweet['text'])
#   print('user\'s screen name: ',tweet['user']['screen_name'])
#   print('user\'s name: ',tweet['user']['name'])
#   try:
#     print('retweet count: ',tweet['retweeted_status']['retweet_count'])
#     print('retweeter\'s name: ', tweet['retweeted_status']['user']['name'])
#     print('retweeted\'s screen name: ', tweet['retweeted_status']['user']['screen_name'])
#   except KeyError:
#       pass

# A.	Find the number of tweets that have data somewhere in the tweet’s text (case insensitive search using regex)
print('PART 1-A: ')
data_text = collection.find({"text": {'$regex': '.*data.*', '$options' : 'i'}})
countOfText = data_text.count()
print('the number of tweets that have data somewhere in the tweet’s text: ', countOfText)

# B.	From all the data related objects, how many of them are geo_enabled?
print('PART 1-B: ')
NoOfGeo = collection.find({ "user.geo_enabled" : True }).count()
print('the data related objects with geo_enabled : ',NoOfGeo)

#C.	For all the data related tweets, use the TextBlob Python library to detect
# if the Tweet’s sentiment is “Positive”, “Neutral”, or “Negative”.
# You are free to use other sensible methods and libraries to do so.

print('PART 1-C: ')
#clean your Tweet’s text of unwanted characters/emoji/etc
emoji_pattern = re.compile(
    u"(\ud83d[\ude00-\ude4f])|"  # emoticons
    u"(\ud83c[\udf00-\uffff])|"  # symbols & pictographs (1 of 2)
    u"(\ud83d[\u0000-\uddff])|"  # symbols & pictographs (2 of 2)
    u"(\ud83d[\ude80-\udeff])|"  # transport & map symbols
    u"(\ud83c[\udde0-\uddff])"  # flags (iOS)
    "+", flags=re.UNICODE)

for tweet in data_text:
    text = emoji_pattern.sub(r'', tweet['text'])
    text = re.sub("\s\s+", " ", text)
    text = text.replace('\n','')

    blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
    if blob.sentiment.classification == 'pos':
        print('Positive setiment for the tweet :  ',text)
    elif blob.sentiment.classification == 'neg':
        print('Neutral setiment for the tweet  :  ',text)
    else:
        print('Negative setiment for the tweet :  ',text)



