import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Consumer keys and access tokens, used for OAuth

# keys_file = open("keys.txt")
# lines = keys_file.readlines()
# consumer_key = lines[0].rstrip()
# consumer_secret = lines[1].rstrip()
# access_token = lines[2].rstrip()
# access_token_secret = lines[3].rstrip()

# Consumer keys and access tokens, used for OAuth
consumer_key = 'IEB7Q9795VyJyiCI5Yk07qTC6'
consumer_secret = 'P69Z3cVI0U5FjyLganwbRc5OIdeA0VdqDJd9irpAJMA58FUqaa'
access_token = '936682777222754305-shiJKC3SR1uBhVUwtWi6StBYw2P7lSl'
access_token_secret = 'uX0AeJy5O0M5jwLGpW6NHuzzuiYMxpCNUk5NBm97a0pQX'


# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
api = tweepy.API(auth)

# Sample method, used to update a status
#api.update_status('Teaching tweepy to CS660 (introduction to database systems) students at Boston University')

# Creates the user object. The me() method returns the user whose authentication keys were used.
user = api.me()

print('user\'s name: ' + user.name)
print('location: ' + user.location)
print('number of friends: ' + str(user.friends_count))


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['python'])
