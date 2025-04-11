from dotenv import load_dotenv
import requests
import json
import os
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt


load_dotenv()

api_key = os.getenv('SIGHT_ENGINE_API_USER')
api_secret = os.getenv('SIGHT_ENGINE_API_SECRET')
true_labels = []
predicted_labels = []
categories = ['firearm', 'no_firearm']

params = {
  'models': 'weapon',
  'api_user': api_key,
  'api_secret': api_secret
}

image_dir = '../python/test_images/'

categories = [category for category in os.listdir(image_dir) if os.path.isdir(os.path.join(image_dir, category))]

for category in categories:
    category_dir = os.path.join(image_dir, category)

    for image_file in os.listdir(category_dir):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(category_dir, image_file)
            true_labels.append(category)
            with open(image_path, 'rb') as image:
                files = {'media': image}
                r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)
                output = json.loads(r.text)
                print(json.dumps(output, indent=2))

                firearm_score = output.get('weapon', {}).get('classes', {}).get('firearm', 0)
                if firearm_score > 0.5:
                    print('Explicit content')
                    predicted_labels.append('firearm')
                else:
                    print('Not explicit content')
                    predicted_labels.append('no_firearm')

accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels, pos_label='firearm')
recall = recall_score(true_labels, predicted_labels, pos_label='firearm')
f1 = f1_score(true_labels, predicted_labels, pos_label='firearm')

print("\nEvaluation Metrics:")
print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F1 Score: {f1:.2f}")

metrics = {'Accuracy': accuracy, 'Precision': precision, 'Recall': recall, 'F1 Score': f1}

plt.figure(figsize=(8, 6))
plt.bar(metrics.keys(), metrics.values(), color=['blue', 'green', 'orange', 'red'])

plt.xlabel('Metrics')
plt.ylabel('Scores')
plt.title('Evaluation Metrics for Weapon Detection')

plt.show()