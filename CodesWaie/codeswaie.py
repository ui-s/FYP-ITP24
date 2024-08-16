import pandas as pd 
from tabulate import tabulate

# Reading Datasets
df1 = pd.read_csv('BodyGoalDataset.csv')
df2 = pd.read_csv('ProblemAreaDataset.csv')
df3 = pd.read_csv('WorkoutDaysDataset.csv')
df4 = pd.read_csv('WorkoutScheduleRecommendationDataset.csv')

# Dataframes checking
print("Dataframe 1:")
print(df1)
print("\nDataframe 2:")
print(df2)
print("Dataframe 3:")
print(df3)
print("\nDataframe 4:")
print(df4)

# Display DataFrames in tabular form
print(tabulate(df1, headers='keys', tablefmt='psql'))
print(tabulate(df2, headers='keys', tablefmt='psql'))
print(tabulate(df3, headers='keys', tablefmt='psql'))
print(tabulate(df4, headers='keys', tablefmt='psql'))

#
