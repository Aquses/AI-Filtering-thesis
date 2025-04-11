from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

api_key = os.getenv('SIGHT_ENGINE_API_USER')
api_secret = os.getenv('SIGHT_ENGINE_API_SECRET')   

params = {
  'models': 'nudity-2.1,weapon,alcohol,recreational_drug,medical,offensive-2.0,gore-2.0,violence,self-harm',
  'api_user': api_key,
  'api_secret': api_secret
}

image_dir = '../python/test_images/'

files = [img for img in os.listdir(image_dir) if img.lower().endswith(('.jpg', '.png', '.jpeg'))]

# files = {'media': open('../python/test_images/Nprofile2.jpg', 'rb')}
# r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

output = json.loads(r.text)
print(output)

