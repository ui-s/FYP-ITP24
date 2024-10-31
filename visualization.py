import matplotlib.pyplot as plt
import pandas as pd

# Your results in a DataFrame format
data = {
    "Day": ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    "Random Forest Accuracy": [0.975309, 0.938272, 0.975309, 0.975309, 0.975309, 0.950617, 0.913580],
    "Logistic Regression Accuracy": [0.938272, 0.925926, 0.975309, 0.913580, 0.876543, 0.925926, 0.913580],
    "Random Forest Precision": [0.976286, 0.952365, 0.957099, 0.967593, 0.980796, 0.945946, 0.850553],
    "Logistic Regression Precision": [0.915996, 0.928760, 0.957124, 0.895967, 0.892857, 0.923814, 0.846914],
    "Random Forest Recall": [0.975309, 0.938272, 0.975309, 0.975309, 0.975309, 0.950617, 0.913580],
    "Logistic Regression Recall": [0.938272, 0.925926, 0.975309, 0.913580, 0.876543, 0.925926, 0.913580],
    "Random Forest F1-Score": [0.973026, 0.938495, 0.965099, 0.970435, 0.975206, 0.940712, 0.880082],
    "Logistic Regression F1-Score": [0.926078, 0.920829, 0.965105, 0.902263, 0.867400, 0.900815, 0.878493]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Set figure size
plt.figure(figsize=(14, 8))

# Define a function to create grouped bar charts for each metric
def plot_grouped_bar_chart(metric, title):
    plt.figure(figsize=(10, 6))
    
    # Set positions of bars
    bar_width = 0.35
    index = range(len(df["Day"]))
    
    # Plot bars for both models
    plt.bar(index, df[f"Random Forest {metric}"], bar_width, label="Random Forest", color='r')
    plt.bar([i + bar_width for i in index], df[f"Logistic Regression {metric}"], bar_width, label="Logistic Regression", color='b')
    
    # Labels, title, and legend
    plt.xlabel('Day of the Week')
    plt.ylabel(metric)
    plt.title(title)
    plt.xticks([i + bar_width / 2 for i in index], df["Day"])
    plt.legend()
    plt.tight_layout()
    plt.show()

# Visualize Accuracy, Precision, Recall, and F1-Score
plot_grouped_bar_chart('Accuracy', 'Accuracy Comparison: Random Forest vs Logistic Regression')
plot_grouped_bar_chart('Precision', 'Precision Comparison: Random Forest vs Logistic Regression')
plot_grouped_bar_chart('Recall', 'Recall Comparison: Random Forest vs Logistic Regression')
plot_grouped_bar_chart('F1-Score', 'F1-Score Comparison: Random Forest vs Logistic Regression')
