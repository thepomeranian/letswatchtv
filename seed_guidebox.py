import secret
from app import models, db
import requests

def seed():
  all_tvshows = models.TVShow.query.filter_by(id).all()
  print tvshow.externals.imdb
  # for tvshow in all_tvshows:
    
  #   r = requests.get("https://api-public.guidebox.com/v1.43/US/%s/search/id/imdb/%s" % secret.GUIDEBOX_KEY, tvshow.externals.imdb )

  #   response = r.json()

  # for tvshow_obj in response:
  #   pass