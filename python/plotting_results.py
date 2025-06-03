import matplotlib.pyplot as plt
import pandas as pd
import re  # To parse the classification report text

def calculate_average():
    # Load the evaluation results CSV file
    file_path = 'evaluation_results_jigsaw_all.csv'
    data = pd.read_csv(file_path)

    # Filter the data for thresholds 0.5 and 0.61
    filtered_data = data[data['Threshold'].isin([0.30, 0.62])]

    # Group by threshold and calculate the average for Accuracy, Precision, Recall, and F1 Score
    averages = filtered_data.groupby('Threshold')[['Accuracy', 'Precision', 'Recall', 'F1 Score']].mean()

    # Print the results
    print("Averages for thresholds 0.30 and 0.61:")
    print(averages)

def extract_offensive_recall(data):
    """
    Extracts offensive recall from the classification report and adds it as a new column.

    Parameters:
    - data: DataFrame containing the 'Classification Report' column.

    Returns:
    - data: DataFrame with an added 'Offensive Recall' column.
    """
    if 'Offensive Recall' not in data.columns:
        offensive_recall = []
        for _, row in data.iterrows():
            classification_report = row['Classification Report']
            match = re.search(r"Offensive\s+\d+\.\d+\s+(\d+\.\d+)", classification_report)
            if match:
                recall_offensive = float(match.group(1))  # Extract the recall value
                offensive_recall.append(recall_offensive)
            else:
                offensive_recall.append(None)  # Handle cases where the recall value is not found
        data['Offensive Recall'] = offensive_recall
    return data

def extract_non_offensive_recall(data):
    """
    Extracts non-offensive recall from the classification report and adds it as a new column.

    Parameters:
    - data: DataFrame containing the 'Classification Report' column.

    Returns:
    - data: DataFrame with an added 'Non-Offensive Recall' column.
    """
    if 'Non-Offensive Recall' not in data.columns:
        non_offensive_recall = []
        for _, row in data.iterrows():
            classification_report = row['Classification Report']
            match = re.search(r"Non-Offensive\s+\d+\.\d+\s+(\d+\.\d+)", classification_report)
            if match:
                recall_non_offensive = float(match.group(1))  # Extract the recall value
                non_offensive_recall.append(recall_non_offensive)
            else:
                non_offensive_recall.append(None)  # Handle cases where the recall value is not found
        data['Non-Offensive Recall'] = non_offensive_recall
    return data

def plot_offensive_recall(data):
    """
    Plots offensive recall against thresholds.

    Parameters:
    - data: DataFrame containing thresholds and offensive recall.
    """
    # Ensure offensive recall is extracted
    data = extract_offensive_recall(data)

    # Group by threshold and calculate the average offensive recall
    averages = data.groupby('Threshold')['Offensive Recall'].mean()

    # Plot offensive recall
    plt.figure(figsize=(10, 6))
    plt.plot(averages.index, averages, label='Offensive Recall', marker='o', color='purple')
    plt.xlabel('Threshold', fontsize=12)
    plt.ylabel('Offensive Recall', fontsize=12)
    plt.title('Offensive Recall Across Thresholds', fontsize=14)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_average_with_offensive_recall():
    """
    Plots average metrics (Accuracy, Precision, Recall, F1 Score, and Offensive Recall) across thresholds.
    """
    # Load the evaluation results CSV file
    file_path = 'evaluation_results_jigsaw_all.csv'
    data = pd.read_csv(file_path)

    # Ensure offensive recall is extracted
    data = extract_offensive_recall(data)

    # Group by threshold and calculate the average for all metrics
    averages = data.groupby('Threshold')[['Accuracy', 'Precision', 'Recall', 'F1 Score', 'Offensive Recall']].mean()

    # Print the average values to the console
    print("\nAverage Metrics Across Thresholds:")
    print(averages)

    # Plot the results
    plt.figure(figsize=(10, 6))
    plt.plot(averages.index, averages['Accuracy'], label='Accuracy', color='red', marker='o')
    plt.plot(averages.index, averages['Precision'], label='Precision', color='green', marker='o')
    plt.plot(averages.index, averages['Recall'], label='Weighted Recall', color='blue', marker='o')
    plt.plot(averages.index, averages['F1 Score'], label='F1 Score', color='orange', marker='o')

    # Add labels, title, and legend
    plt.xlabel('Threshold', fontsize=12)
    plt.ylabel('Metric Value', fontsize=12)
    plt.title('Average Metrics Across Thresholds', fontsize=14)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True)

    # Show the plot
    plt.tight_layout()
    plt.show()

def plot_normalized_average(data):
    """
    Plots the normalized average metrics (F1 Score and Offensive Recall) across thresholds.

    Parameters:
    - data: DataFrame containing thresholds, F1 scores, and offensive recall.
    """
    # Ensure offensive recall is extracted
    data = extract_offensive_recall(data)

    # Group by threshold and calculate the average for F1 Score and Offensive Recall
    averages = data.groupby('Threshold')[['F1 Score', 'Offensive Recall']].mean()

    # Normalize the values using z-score normalization
    averages['Normalized F1 Score'] = (averages['F1 Score'] - averages['F1 Score'].mean()) / averages['F1 Score'].std()
    averages['Normalized Offensive Recall'] = (averages['Offensive Recall'] - averages['Offensive Recall'].mean()) / averages['Offensive Recall'].std()

    # Plot the normalized values
    plt.figure(figsize=(10, 6))
    plt.plot(averages.index, averages['Normalized F1 Score'], label='Normalized F1 Score', marker='o', color='orange')
    plt.plot(averages.index, averages['Normalized Offensive Recall'], label='Normalized Offensive Recall', marker='o', color='purple')
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.8)  # Reference line at 0
    plt.xlabel('Threshold', fontsize=12)
    plt.ylabel('Normalized Metric Value', fontsize=12)
    plt.title('Normalized Average Metrics Across Thresholds', fontsize=14)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_false_positives(data):
    """
    Plots the threshold against the raw number of false positives (FP).

    Parameters:
    - data: DataFrame containing thresholds and confusion matrices.
    """
    # Extract false positives from the confusion matrix
    false_positives = []
    for _, row in data.iterrows():
        confusion_matrix = row['Confusion Matrix']
        # Parse the confusion matrix to extract the FP value
        match = re.search(r"\[\[\d+\s+(\d+)\]", confusion_matrix)
        if match:
            fp = int(match.group(1))  # Extract the false positive value
            false_positives.append(fp)
        else:
            false_positives.append(None)  # Handle cases where the FP value is not found

    # Add the false positives as a new column to the DataFrame
    data['False Positives'] = false_positives

    # Group by threshold and calculate the average number of false positives
    averages = data.groupby('Threshold')['False Positives'].mean()

    # Plot the false positives against thresholds
    plt.figure(figsize=(10, 6))
    plt.plot(averages.index, averages, label='False Positives', marker='o', color='red')
    plt.xlabel('Threshold', fontsize=12)
    plt.ylabel('Number of False Positives', fontsize=12)
    plt.title('False Positives Across Thresholds', fontsize=14)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_compare_f1_and_offensive_recall(file1, label1, file2, label2):
    """
    Plots averaged F1 Score, Offensive Recall, and Non-Offensive Recall per threshold for two datasets,
    considering only thresholds <= 0.60.
    """
    # Load and process first dataset
    data1 = pd.read_csv(file1)
    data1 = extract_offensive_recall(data1)
    data1 = extract_non_offensive_recall(data1)
    data1 = data1[data1['Threshold'] <= 0.60]
    avg1 = data1.groupby('Threshold')[['F1 Score', 'Offensive Recall', 'Non-Offensive Recall']].mean()

    # Load and process second dataset
    data2 = pd.read_csv(file2)
    data2 = extract_offensive_recall(data2)
    data2 = extract_non_offensive_recall(data2)
    data2 = data2[data2['Threshold'] <= 0.60]
    avg2 = data2.groupby('Threshold')[['F1 Score', 'Offensive Recall', 'Non-Offensive Recall']].mean()

    # Plot F1 Score comparison
    plt.figure(figsize=(10, 6))
    plt.plot(avg1.index, avg1['F1 Score'], marker='o', label=f'F1 Score ({label1})', color='blue')
    plt.plot(avg2.index, avg2['F1 Score'], marker='o', label=f'F1 Score ({label2})', color='orange')
    plt.xlabel('Threshold', fontsize=12)
    plt.ylabel('F1 Score', fontsize=12)
    plt.title('F1 Score Comparison Across Thresholds (≤ 0.60)', fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot Offensive Recall comparison
    plt.figure(figsize=(10, 6))
    plt.plot(avg1.index, avg1['Offensive Recall'], marker='o', label=f'Offensive Recall ({label1})', color='purple')
    plt.plot(avg2.index, avg2['Offensive Recall'], marker='o', label=f'Offensive Recall ({label2})', color='green')
    plt.xlabel('Threshold', fontsize=12)
    plt.ylabel('Offensive Recall', fontsize=12)
    plt.title('Offensive Recall Comparison Across Thresholds (≤ 0.60)', fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Plot Non-Offensive Recall comparison
    plt.figure(figsize=(10, 6))
    plt.plot(avg1.index, avg1['Non-Offensive Recall'], marker='o', label=f'Non-Offensive Recall ({label1})', color='red')
    plt.plot(avg2.index, avg2['Non-Offensive Recall'], marker='o', label=f'Non-Offensive Recall ({label2})', color='teal')
    plt.xlabel('Threshold', fontsize=12)
    plt.ylabel('Non-Offensive Recall', fontsize=12)
    plt.title('Non-Offensive Recall Comparison Across Thresholds (≤ 0.60)', fontsize=14)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Example usage
file_path = 'evaluation_results_jigsaw_all.csv'
data = pd.read_csv(file_path)

# Plot average metrics with offensive recall
plot_average_with_offensive_recall()

# Plot offensive recall separately
plot_offensive_recall(data)

# Call the function to plot normalized averages
plot_normalized_average(data)

# Call the function to plot false positives
plot_false_positives(data)

# Example usage for comparison:
plot_compare_f1_and_offensive_recall(
    'evaluation_results_jigsaw_all.csv', 'Jigsaw Dataset',
    'evaluation_results_all.csv', 'Hatespeech Dataset'
)