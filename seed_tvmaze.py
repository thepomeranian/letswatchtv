import requests
from app import models, db


payload = {'imdb': 'tt0944947'}
# BB tt0903747
# GoT tt0944947
r = requests.get(
  "http://api.tvmaze.com/lookup/shows", 
  params=payload)

response = r.json() 

tvshow = models.TVShow(name=response['name'])
db.session.add(tvshow)
db.session.commit()