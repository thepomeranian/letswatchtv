import secret
from app import models, db
import requests

def seed():
  all_tvshows = models.TVShow.query.all()
  twitter_id = None
  twitter_handle = None
  for tvshow in all_tvshows:
    print tvshow.tvshow

    for external in tvshow.externals:
      r = requests.get("https://api-public.guidebox.com/v1.43/US/%s/search/id/imdb/%s" % (secret.GUIDEBOX_KEY, external.imdb) )
      response = r.json()
      if any(response):
        guidebox_id = response['id']
      else:
        break

      r2 = requests.get("https://api-public.guidebox.com/v1.43/US/%s/show/%s" % (secret.GUIDEBOX_KEY, guidebox_id))
      responses2 = r2.json()
      
      social_media = responses2['social']
      
      facebook = social_media['facebook']

      if facebook['facebook_id']:
        facebook_id = facebook['facebook_id']
      else:
        facebook['facebook_id'] = None
        
      twitter = social_media['twitter']

      if social_media['twitter']:
        twitter_id = twitter['twitter_id']
      else: 
        twitter['twitter_id'] = None

      if twitter['link']:
        twitter_link = twitter['link']
        twitter_handle = twitter_link[20:]
      else:
        twitter['link'] = None
      
      if twitter_handle is None:
        print "No twitter handle"
        break    
        
    
    tvshow.twitter_handle = twitter_handle
    db.session.commit()
    print tvshow.twitter_handle
    twitter_handle = None


seed()