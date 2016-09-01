import secret
from app import models, db
import requests

def seed():
  all_tvshows = models.TVShow.query.all()
  
  for tvshow in all_tvshows:
    print tvshow.tvshow

    for external in tvshow.externals:
      r = requests.get("https://api-public.guidebox.com/v1.43/US/%s/search/id/imdb/%s" % (secret.GUIDEBOX_KEY, external.imdb) )
      response = r.json()
      guidebox_id = response['id']

      r2 = requests.get("https://api-public.guidebox.com/v1.43/US/%s/show/%s" % (secret.GUIDEBOX_KEY, guidebox_id))
      responses2 = r2.json()
      
      medias = responses2['channels']
      media = medias[0]
      social_media = media['social']
      facebook = social_media['facebook']
      facebook_id = facebook['facebook_id']
      
      twitter = social_media['twitter']
      twitter_id = twitter['twitter_id']
      
seed()