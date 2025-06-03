import pandas as pd

def create_balanced_dataset(input_file, output_file, size, state):
    # Parsing the dataset
    data = pd.read_csv(input_file)

    # Filter rows based on class
    non_offensive = data[data['class'] == 2].sample(n=int(size/2), random_state=state)
    print(len(non_offensive))
    hate_speech = data[data['class'] == 0].sample(n=int(size/4), random_state=state)
    print(len(hate_speech))
    offensive_language = data[data['class'] == 1].sample(n=int(size/4), random_state=state) 
    print(len(offensive_language))
    # Combine the filtered rows into a new dataset
    balanced_data = pd.concat([non_offensive, hate_speech, offensive_language])

    # Save the new dataset to a CSV file
    balanced_data.to_csv(output_file, index=False)
    print(f"Balanced dataset created and saved to {output_file}")

def create_balanced_dataset_2(input_file, output_file):
    # Parsing the dataset
    data = pd.read_csv(input_file)

    # Filter rows based on class
    non_offensive = data[data['class'] == 2].sample(n=100, random_state=42)
    print(len(non_offensive))
    hate_speech = data[data['class'] == 1].sample(n=50, random_state=42)
    print(len(hate_speech))
    offensive_language = data[data['class'] == 0].sample(n=50, random_state=6552)
    print(len(offensive_language))
    # Combine the filtered rows into a new dataset
    balanced_data = pd.concat([non_offensive, hate_speech, offensive_language])

    # Save the new dataset to a CSV file
    balanced_data.to_csv(output_file, index=False)
    print(f"Balanced dataset created and saved to {output_file}")


def create_balanced_dataset_3(input_file, output_file):
    # Parsing the dataset
    data = pd.read_csv(input_file)

    # Filter rows based on class
    non_offensive = data[data['class'] == 3].sample(n=50, random_state=42)
    print(len(non_offensive))
    hate_speech = data[data['class'] == 1].sample(n=25, random_state=42)
    print(len(hate_speech))
    offensive_language = data[data['class'] == 2].sample(n=25, random_state=42)
    print(len(offensive_language))
    # Combine the filtered rows into a new dataset
    balanced_data = pd.concat([non_offensive, hate_speech, offensive_language])

    # Save the new dataset to a CSV file
    balanced_data.to_csv(output_file, index=False)
    print(f"Balanced dataset created and saved to {output_file}")

def balance_jigsaw(input_file, output_file, size, state):

    usecols = ['id', 'target', 'comment_text', 'severe_toxicity', 'insult', 'threat']
    data = pd.read_csv(input_file, usecols=usecols)
    half_size = size // 2

    # Select offensive and non-offensive based on 'target'
    offensive = data[data['target'] >= 0.5].sample(n=half_size, random_state=state)
    non_offensive = data[data['target'] < 0.5].sample(n=half_size, random_state=state)

    print(f"Selected {len(offensive)} offensive and {len(non_offensive)} non-offensive entries for {output_file}")

    balanced_data = pd.concat([offensive, non_offensive]).sample(frac=1, random_state=state).reset_index(drop=True)
    balanced_data.to_csv(output_file, index=False)
    print(f"Balanced Jigsaw dataset created and saved to {output_file} with {len(balanced_data)} entries.")

# Call the method to create the balanced dataset
# create_balanced_dataset_3('../data/hatespeech_data_3.csv', '../data/hatespeech_data_3_small.csv')

# The random states to be
random_states = [42, 123, 2025, 6556, 8080]

# UNCOMMENT LATER
for state in random_states:
    create_balanced_dataset('../data/labeled_data.csv', f'../data/labeled_data_small_{state}.csv', 300, state)

for state in random_states:
    balance_jigsaw('../data/jigsaw.csv', f'../data/jigsaw_test_{state}.csv', 300, state)
