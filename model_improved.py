import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import random
import os

class WorkoutModel:
    def __init__(self):
        self.features = ['Gender', 'Age', 'BodyGoal', 'ProblemAreas', 'Height_cm', 'Weight_kg', 'FitnessLevel', 'WorkoutDaysPerWeek']
        self.target_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.workout_types = ['Chest Day', 'Back Day', 'Leg Day', 'Arm Day', 'Upper Body', 'Lower Body', 'Cardio', 'Full Body', 'Rest']
        self.encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def load_data(self):
        # Load and preprocess data
        self.workout_schedule_data = pd.read_csv(os.path.join('data', 'processed', 'Cleaned_WorkoutScheduleRecommendationDataset.csv'))
        self.workout_exercises_data = pd.read_csv(os.path.join('data', 'processed', 'Cleaned_WorkoutDaysDataset.csv'))
        
        # Ensure data is cleaned and formatted correctly
        self.workout_schedule_data = self.workout_schedule_data.dropna()
        self.workout_schedule_data['WorkoutDaysPerWeek'] = self.workout_schedule_data['WorkoutDaysPerWeek'].astype(int)
        
        # Convert workout days to workout types
        for day in self.target_days:
            self.workout_schedule_data[day] = self.workout_schedule_data[day].apply(lambda x: x.title() if pd.notna(x) else 'Rest')

    def preprocess_data(self):
        X = self.workout_schedule_data[self.features]
        y = self.workout_schedule_data[self.target_days]
        
        X_encoded = self.encoder.fit_transform(X)
        feature_names = self.encoder.get_feature_names_out(self.features)
        X_encoded = pd.DataFrame(X_encoded, columns=feature_names)
        
        return X_encoded, y

    def train_model(self):
        self.load_data()
        X, y = self.preprocess_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.models = {}
        for day in self.target_days:
            self.models[day] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.models[day].fit(X_train, y_train[day])
            
            # Evaluate model
            y_pred = self.models[day].predict(X_test)
            accuracy = accuracy_score(y_test[day], y_pred)
            print(f"Model Accuracy for {day}: {accuracy:.2f}")

    def optimize_workout_schedule(self, workout_days, predictions):
        schedule = {day: 'Rest' for day in self.target_days}
        workout_count = 0
        
        for day, workout in predictions.items():
            if workout != 'Rest' and workout_count < workout_days:
                schedule[day] = workout
                workout_count += 1
            
            if workout_count == workout_days:
                break
        
        return schedule

    def predict_workout_types(self, user_input):
        if not hasattr(self, 'models'):
            self.train_model()
        
        input_df = pd.DataFrame([user_input])
        encoded_input = self.encoder.transform(input_df[self.features])
        encoded_input = pd.DataFrame(encoded_input, columns=self.encoder.get_feature_names_out(self.features))
        
        predictions = {}
        for day in self.target_days:
            predictions[day] = self.models[day].predict(encoded_input)[0]
        
        optimized_schedule = self.optimize_workout_schedule(user_input['WorkoutDaysPerWeek'], predictions)
        return optimized_schedule

    def get_exercises_for_workout(self, workout_type, fitness_level):
        suitable_exercises = self.workout_exercises_data[
            (self.workout_exercises_data['WorkoutDay'].str.lower() == workout_type.lower()) &
            (self.workout_exercises_data['FitnessLevel'].str.lower() == fitness_level.lower())
        ]
        
        if len(suitable_exercises) < 5:
            # If not enough exercises, include exercises from adjacent fitness levels
            adjacent_levels = ['beginner', 'intermediate', 'advanced']
            idx = adjacent_levels.index(fitness_level.lower())
            if idx > 0:
                suitable_exercises = pd.concat([suitable_exercises, self.workout_exercises_data[
                    (self.workout_exercises_data['WorkoutDay'].str.lower() == workout_type.lower()) &
                    (self.workout_exercises_data['FitnessLevel'].str.lower() == adjacent_levels[idx-1])
                ]])
            if idx < 2:
                suitable_exercises = pd.concat([suitable_exercises, self.workout_exercises_data[
                    (self.workout_exercises_data['WorkoutDay'].str.lower() == workout_type.lower()) &
                    (self.workout_exercises_data['FitnessLevel'].str.lower() == adjacent_levels[idx+1])
                ]])
        
        return suitable_exercises.sample(n=min(5, len(suitable_exercises))).to_dict('records')

    def generate_workout_plan(self, user_input):
        workout_schedule = self.predict_workout_types(user_input)
        workout_plan = []
        
        for day, workout_type in workout_schedule.items():
            if workout_type != 'Rest':
                exercises = self.get_exercises_for_workout(workout_type, user_input['FitnessLevel'])
                workout_plan.append({
                    'Day': day,
                    'WorkoutType': workout_type,
                    'Exercises': exercises
                })
        
        return workout_plan
    
workout_model = WorkoutModel()
