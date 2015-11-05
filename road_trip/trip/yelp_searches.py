import json
import os
import requests
from requests_oauthlib import OAuth1, OAuth1Session


#OAuth credential placeholders that must be filled in by users.
CONSUMER_KEY = os.environ["YELP_CONSUMER"]
CONSUMER_SECRET = os.environ["YELP_CONSUMER_SECRET"]
TOKEN = os.environ["YELP_TOKEN"]
TOKEN_SECRET = os.environ["YELP_TOKEN_SECRET"]


yelp = OAuth1Session(CONSUMER_KEY,
                            client_secret=CONSUMER_SECRET,
                            resource_owner_key=TOKEN,
                            resource_owner_secret=TOKEN_SECRET)
url = 'https://api.yelp.com/v2/search/?location=San Francisco, CA'
r = yelp.get(url)
r = r.json()
print(json.dumps(r, indent=2))
