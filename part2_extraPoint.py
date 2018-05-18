from pymongo import MongoClient
import emoji
from emoji import UNICODE_EMOJI
import operator
from itertools import islice
import folium
import pandas as pd
import csv

client = MongoClient('localhost', 27017)
db = client['usa_db']
collection = db['usa_tweets_collection']
tweets_iterator = collection.find()

#use dictionary to store the emoji
#content include(text,city)pair
content = collection.find({},{"text":1,"place.full_name":1, "_id":0})


#for extra
stateEmojiCount = {}


for words in content:
    # emoji list
    emoji = []

    for t in words["text"]:
        if t in UNICODE_EMOJI:
            emoji.append(t);

    if len(words) == 2:
        address = words['place']['full_name'].split(", ")
        if len(address)== 2:
            city = address[0]
            state = address[1]

        else:
            state = ''

    if len(state) == 2:
        # for extra point
        if state in stateEmojiCount:
            stateEmojiCount[state] += emoji
        else:
            stateEmojiCount[state] = emoji

# for extra credit
#For part 2) B,  create the map of USA with top 2 emojis per state (you could use any language you want).
top2state = {}
for state, countNum in  stateEmojiCount.items():
    top2emoji = {}
    for i in countNum:
        if i in top2emoji:
            top2emoji[i]+=1
        else:
            top2emoji[i]=1

    top2emoji = sorted(top2emoji.items(),key=operator.itemgetter(1),reverse=True)
    top2emoji2 = list(islice(top2emoji,2))
    top2state[state] = top2emoji2


#draw
map_osm = folium.Map(location=[36.9931,-102.0518,],zoom_start=5)


with open('cetroid.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if not ''.join(row) == 'abv;latitude;longitude':
            r = ''.join(row).split(';')
            # print(r)
            for name, emo in top2state.items():
                result = ''
                if r[0] == name:
                    for emoji2 in emo:
                        result += emoji2[0] + '-' + str(emoji2[1]) + '  '


                if result:
                    result = r[0] + ': ' + result
                    print(result)
                    folium.Marker([float(r[1]), float(r[2])], popup=result).add_to(map_osm)


