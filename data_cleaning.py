import pandas as pd
import os

def clean_workout_schedule_data():
    # Existing code remains the same
    df_WSR = pd.read_csv(os.path.join('data', 'raw', 'WorkoutScheduleRecommendationDataset.csv'))
    
    df_WSR['Id'] = df_WSR['Id'].astype(str)
    df_WSR['Gender'] = df_WSR['Gender'].str.strip().str.title()
    df_WSR['BodyGoal'] = df_WSR['BodyGoal'].str.strip().str.title()
    df_WSR['ProblemAreas'] = df_WSR['ProblemAreas'].str.strip().str.title()
    df_WSR['FitnessLevel'] = df_WSR['FitnessLevel'].str.strip().str.title()
    
    if df_WSR['Age'].isnull().sum() > 0:
        median_age = df_WSR['Age'].median()
        df_WSR['Age'].fillna(median_age, inplace=True)
    
    if df_WSR['FitnessLevel'].isnull().sum() > 0:
        mode_fitness_level = df_WSR['FitnessLevel'].mode()[0]
        df_WSR['FitnessLevel'].fillna(mode_fitness_level, inplace=True)
    
    df_WSR = df_WSR.drop_duplicates(subset='Id')
    
    columns = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for col in columns:
        df_WSR[col] = df_WSR[col].str.strip().str.title()
    
    df_WSR.drop(columns=['Id'], inplace=True)
    
    df_WSR.to_csv(os.path.join('data', 'processed', 'Cleaned_WorkoutScheduleRecommendationDataset.csv'), index=False)
    
    return df_WSR

def clean_workout_days_data():
    # Existing code remains the same
    df_WDD = pd.read_csv(os.path.join('data', 'raw', 'WorkoutDaysDataset.csv'))
    
    df_WDD['WorkoutDay'] = df_WDD['WorkoutDay'].str.strip().str.title()
    df_WDD['Exercise'] = df_WDD['Exercise'].str.strip().str.title()
    df_WDD['FitnessLevel'] = df_WDD['FitnessLevel'].str.strip().str.title()
    df_WDD['TargetedMuscle'] = df_WDD['TargetedMuscle'].str.strip().str.title()
    
    df_WDD = df_WDD.drop_duplicates()
    
    df_WDD.to_csv(os.path.join('data', 'processed', 'Cleaned_WorkoutDaysDataset.csv'), index=False)
    
    return df_WDD

def clean_problem_area_data():
    # New function to clean ProblemAreaDataset
    df_PAD = pd.read_csv(os.path.join('data', 'raw', 'ProblemAreaDataset.csv'))
    
    df_PAD['ProblemArea'] = df_PAD['ProblemArea'].str.strip().str.title()
    df_PAD['Workout'] = df_PAD['Workout'].str.strip().str.title()
    df_PAD['FitnessLevel'] = df_PAD['FitnessLevel'].str.strip().str.title()
    
    df_PAD = df_PAD.drop_duplicates()
    
    df_PAD.to_csv(os.path.join('data', 'processed', 'Cleaned_ProblemAreaDataset.csv'), index=False)
    
    return df_PAD

if __name__ == "__main__":
    # Create processed data directory if it doesn't exist
    os.makedirs(os.path.join('data', 'processed'), exist_ok=True)
    
    clean_workout_schedule_data()
    clean_workout_days_data()
    clean_problem_area_data()  # Add this line to clean the new dataset
    print("Data cleaning completed. Cleaned datasets saved in 'data/processed' directory.")