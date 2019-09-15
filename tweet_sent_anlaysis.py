from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from unidecode import unidecode
from textblob import TextBlob
import sqlite3
import time

# Database creation
conn = sqlite3.connect('twitter.db')
c = conn.cursor()

def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
        c.execute("CREATE INDEX fast_unix ON sentiment(unix)")
        c.execute("CREATE INDEX fast_tweet ON sentiment(tweet)")
        c.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
        conn.commit()
    except Exception as e:
        print(str(e))
create_table()

# Twitter App authentication
ckey='CeFQZp0QvKg9W64IJeTcfn4Cs'
csecret ='Uce6YZGPcTOxtwf9c0gmEpgKIogRNpnZ09f9XyrwdXcyQTaif1'
atoken='1158407751904587781-y6KnexYlD5gHaNqI9j4GzhMJyC7Oyi'
asecret ='cPlN3eqFxulfF6yhHkCp1KvxJlSJf80fOTBAEewH75zwf'


class listner(StreamListener):
    
    def on_data(self,data):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']
            sentiment = TextBlob(tweet).polarity
            print(time_ms,tweet,sentiment)
            c.execute("INSERT INTO sentiment (unix,tweet,sentiment) VALUES(?,?,?)",(time_ms,tweet,sentiment))
            conn.commit()
        except KeyError as e:
            print(e)
        return True

    def on_error(self,status):
        print(status)

while True:
    try:
        auth = OAuthHandler(ckey,csecret)
        auth.set_access_token(atoken,asecret)
        twitterStream = Stream(auth,listner())
        twitterStream.filter(track=['a','e','i','o','u'])
    except Exception  as e:
        print(str(e))
        time.sleep(5)











