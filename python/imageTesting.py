from dotenv import load_dotenv
import requests
import json
import os

load_dotenv()

api_key = os.getenv('SIGHT_ENGINE_API_USER')
api_secret = os.getenv('SIGHT_ENGINE_API_SECRET')
true_labels = []
predicted_labels = []

params = {
  'models': 'weapon',
  'api_user': api_key,
  'api_secret': api_secret
}

image_dir = '../python/test_images/'

image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png','.jpg', '.jpeg'))]

for image_file in image_files:
    image_path = os.path.join(image_dir, image_file)
    with open(image_path, 'rb') as image:
        files = {'media': image}
        r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)
        output = json.loads(r.text)
        print(f"Results for {image_file}:")
        print(json.dumps(output, indent=2))

        is_explicit = False

        firearm_score = output.get('weapon', {}).get('classes', {}).get('firearm', 0)
        if firearm_score > 0.7:
            is_firearm = True
            print(f"Result: Firearm detected with a score of {firearm_score}")