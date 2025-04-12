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

image_dir = '../testing_images/'

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

                if firearm_toy_score > 0.5:
                    print(f"Toy gun detected - Toy Score: {firearm_toy_score}")
                    predicted_labels.append('no_firearm')
                elif firearm_score > 0.5:
                    print(f"Explicit firearm detected - Firearm Score: {firearm_score}")
                    predicted_labels.append('firearm')
                else:
                    print("Not a firearm (low confidence) - classifying as no_firearm")
                    predicted_labels.append('no_firearm')
                print(f"True Label: {category}, Predicted Label: {predicted_labels[-1]}")

print(f"\nTrue Labels: {true_labels}")
print(f"Predicted Labels: {predicted_labels}")

accuracy = accuracy_score(true_labels, predicted_labels)
precision = precision_score(true_labels, predicted_labels, pos_label='firearm')
recall = recall_score(true_labels, predicted_labels, pos_label='firearm')
f1 = f1_score(true_labels, predicted_labels, pos_label='firearm')

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
plt.title('Evaluation Metrics for Weapon Detection')

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.01, f'{yval:.2f}', ha='center', va='bottom')

plt.show()