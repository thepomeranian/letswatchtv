from app import models, db
import json

raw_data = open('twitter_python.txt', 'r')

data = json.load(raw_data)
tweet = raw_data["created_at"]
print tweet
# tweets = models.Tweets(username, location, created_at, text)
# db.session.add(tvshow)
# db.session.commit()