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
# categories = ['firearm', 'no_firearm']
# categories = ['nude', 'non_nude']
categories = ['explicit', 'non_explicit']

params = {
  'models': 'nudity-2.1,weapon',
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
                firearm_gesture_score = output.get('weapon', {}).get('classes', {}).get('firearm_gesture', 0)
                firearm_toy_score = output.get('weapon', {}).get('classes', {}).get('firearm_toy', 0)
                sexual_activity_score = output.get('nudity', {}).get('sexual_activity', 0)
                sexual_display_score = output.get('nudity', {}).get('sexual_display', 0)
                erotica_score = output.get('nudity', {}).get('erotica', 0)
                very_suggestive_score = output.get('nudity', {}).get('very_suggestive', 0)
                suggestive_score = output.get('nudity', {}).get('suggestive', 0)
                mildly_suggestive_score = output.get('nudity', {}).get('mildly_suggestive', 0)

                nudity_score = max(sexual_activity_score, sexual_display_score, erotica_score, 
                                   very_suggestive_score, suggestive_score, mildly_suggestive_score)

                if (firearm_score > 0.5 or firearm_toy_score > 0.5 or nudity_score > 0.5):
                    predicted_labels.append('explicit')
                else:
                    predicted_labels.append('non_explicit')

                print(f"True Label: {category}, Predicted Label: {predicted_labels[-1]}")

print(f"\nTrue Labels: {true_labels}")
print(f"Predicted Labels: {predicted_labels}")

accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels, pos_label='explicit')
recall = recall_score(true_labels, predicted_labels, pos_label='explicit')
f1 = f1_score(true_labels, predicted_labels, pos_label='explicit')

print("\nEvaluation Metrics:")
print(f"Accuracy: {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:4f}")
print(f"F1 Score: {f1:.4f}")

metrics = {'Accuracy': accuracy, 'Precision': precision, 'Recall': recall, 'F1 Score': f1}

plt.figure(figsize=(8, 6))
bars = plt.bar(metrics.keys(), metrics.values(), color=['blue', 'green', 'orange', 'red'])

plt.xlabel('Metrics')
plt.ylabel('Scores')
plt.title('Evaluation Metrics for Firearm and Nudity Detection')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.01, f'{yval:.2f}', ha='center', va='bottom')

plt.show()