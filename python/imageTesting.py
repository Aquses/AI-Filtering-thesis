from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

api_key = os.getenv('SIGHT_ENGINE_API_USER')
api_secret = os.getenv('SIGHT_ENGINE_API_SECRET')   

params = {
  'models': 'weapon',
  'api_user': api_key,
  'api_secret': api_secret
}
files = {'media': open('../python/test_images/Glock_17.jpg', 'rb')}
r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

output = json.loads(r.text)
print(output)

