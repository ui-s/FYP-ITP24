import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Load the dataset from the CSV file
df = pd.read_csv('GymAppUsersDataset.csv')

#1. Radar chart for Muscle Groups Worked
# Group by 'Week_no' and sum the sets for each muscle group
weekly_data = df.groupby('Week_no')[['Chest_sets', 'Back_sets', 'Legs_sets', 'Arms_sets', 'Shoulder_sets', 'Core_sets']].sum()

# Select the specific week for visualization, e.g., week number 1
week_no = 1  # Change as needed
values = weekly_data.loc[week_no].values.flatten().tolist()

categories = ['Chest_sets', 'Back_sets', 'Legs_sets', 'Arms_sets', 'Shoulder_sets', 'Core_sets']

# Number of variables
N = len(categories)

# Radar chart
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
values += values[:1]  # Repeat the first value to close the circle
angles += angles[:1]  # Repeat the first angle to close the circle

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.fill(angles, values, color='blue', alpha=0.25)
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)
ax.set_title('Muscle Group Worked', fontsize=14)
plt.show()

# 2. BMI Chart
height_m = df['Height_cm'].iloc[-1] / 100  # Convert height to meters
weight_kg = df['Weight_kg'].iloc[-1]  # Weight in kg
bmi = weight_kg / (height_m ** 2)

plt.figure(figsize=(6, 4))
sns.barplot(x=['BMI'], y=[bmi])
plt.ylabel('BMI')
plt.title('BMI Chart')
plt.axhline(25, color='red', linestyle='--', label='Overweight Threshold (25)')
plt.axhline(30, color='orange', linestyle='--', label='Obesity Threshold (30)')
plt.legend()
plt.show()

# 3. Chart for total reps for the week
days = df['Day'].values
total_reps = df['Total_reps'].values

plt.figure(figsize=(8, 4))
sns.barplot(x=days, y=total_reps, palette='viridis')
plt.title('Total Reps for the Week')
plt.xlabel('Days of the Week')
plt.ylabel('Total Reps')
plt.xticks(rotation=45)
plt.show()

# 4. Chart for duration for the week
duration = df['Duration_mins'].values

plt.figure(figsize=(8, 4))
sns.barplot(x=days, y=duration, palette='mako')
plt.title('Workout Duration for the Week')
plt.xlabel('Days of the Week')
plt.ylabel('Duration (minutes)')
plt.xticks(rotation=45)
plt.show()
