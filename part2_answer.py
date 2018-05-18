from pymongo import MongoClient
import emoji
from emoji import UNICODE_EMOJI
import operator
from itertools import islice


client = MongoClient('localhost', 27017)
db = client['usa_db']
collection = db['usa_tweets_collection']
tweets_iterator = collection.find()

#use dictionary to store the emoji
#content include(text,city)pair
content = collection.find({},{"text":1,"place.full_name":1, "_id":0})

#store(emoji,countNo)
emojiCount = {}

#store states and count of 🎄
statesCountT = {}

# store the emoji for MA
MACount = {}

#count every state the #of emoji
statesCount = {}

#count every state have tweets
stateTweets = {}

#count the tweet used in city in California
cityCount = {}

# #for extra
# stateEmojiCount = {}

for words in content:
    # print(words)
    # emoji list
    emoji = []

    for t in words["text"]:
        if t in UNICODE_EMOJI:
            emoji.append(t);

    for symbol in emoji:
        if symbol in emojiCount:
            emojiCount[symbol] += 1
        else:
            emojiCount[symbol] = 1

    if len(words) == 2:
        address = words['place']['full_name'].split(", ")
        if len(address)== 2:
            city = address[0]
            # print(address[0])
            state = address[1]
            # print(address[1])
        else:
            state = ''

    if '🎄' in emoji:
        for symbol in emoji:
            if symbol == '🎄':
                if state in statesCountT:
                    statesCountT[state] +=1
                else:
                    statesCountT[state] = 1

    if state == 'MA':
        for symbol in emoji:
            if symbol in MACount:
                MACount[symbol] +=1
            else:
                MACount[symbol] = 1

    if len(state)== 2:
        if state in statesCount:
            statesCount[state] += len(emoji)
        else:
            statesCount[state] = len(emoji)

        if state in stateTweets:
            stateTweets[state] +=1
        else:
            stateTweets[state] =1

        if state == 'CA':
            if city in cityCount:
                cityCount[city] +=1
            else:
                cityCount[city] =1

emojiCount = sorted(emojiCount.items(),key=operator.itemgetter(1),reverse=True)
print('PART 2-B-1: ')
print('the top 15 emojis used in the entire tweets are \n', list(islice(emojiCount,15)))

statesCountT = sorted(statesCountT.items(),key=operator.itemgetter(1),reverse=True)
print('PART 2-B-2: ')
print('the top 5 states for the emoji 🎄 are \n', list(islice(statesCountT,5)))

MACount = sorted(MACount.items(),key=operator.itemgetter(1),reverse=True)
print('PART 2-B-3: ')
print('the top 5 emojis for MA are \n', list(islice(MACount,5)))

statesCount = sorted(statesCount.items(),key=operator.itemgetter(1),reverse=True)
print('PART 2-B-4: ')
print('the top 5 states that use emojis are \n', list(islice(statesCount,5)))

stateTweets = sorted(stateTweets.items(),key=operator.itemgetter(1),reverse=True)
print('PART 2-C-1: ')
print(' the top 5 states that have tweets are \n', list(islice(stateTweets,5)))

cityCount = sorted(cityCount.items(),key=operator.itemgetter(1),reverse=True)
print('PART 2-C-2: ')
print(' In the state of California, the top 5 cities that tweet are \n', list(islice(cityCount,5)))

