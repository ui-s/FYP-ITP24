import pandas as pd
import os
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

class WorkoutModel:
    def __init__(self):
        self.features = ['Gender', 'Age', 'BodyGoal', 'ProblemAreas', 'Height_cm', 'Weight_kg', 'FitnessLevel', 'WorkoutDaysPerWeek']
        self.target_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.encoder = OneHotEncoder(sparse=False, drop='first')
        self.models = {}

    def load_data(self):
        self.workout_schedule_data = pd.read_csv(os.path.join('data', 'processed', 'Cleaned_WorkoutScheduleRecommendationDataset.csv'))
        self.workout_days_data = pd.read_csv(os.path.join('data', 'processed', 'Cleaned_WorkoutDaysDataset.csv'))

    def train_models(self):
        self.load_data()
        encoded_features = self.encoder.fit_transform(self.workout_schedule_data[self.features])
        encoded_df = pd.DataFrame(encoded_features, columns=self.encoder.get_feature_names_out())
        
        for day in self.target_days:
            self.models[day] = RandomForestClassifier(random_state=42)
            self.models[day].fit(encoded_df, self.workout_schedule_data[day])

    def predict_workout(self, user_input):
        if not self.models:
            self.train_models()

        input_df = pd.DataFrame([user_input])
        encoded_input = self.encoder.transform(input_df[self.features])
        
        predictions = {}
        for day in self.target_days:
            predictions[day] = self.models[day].predict(encoded_input)[0]
        
        return predictions

    def recommend_workouts(self, predicted_day, fitness_level):
        if not hasattr(self, 'workout_days_data'):
            self.load_data()

        
        workouts_for_day = self.workout_days_data[
            (self.workout_days_data['FitnessLevel'] == fitness_level) &
            (self.workout_days_data['WorkoutDay'].str.lower() == predicted_day.lower())
        ]
        
        recommendations = []
        
        # Recommendations logic for specific workout days
        if 'chest day' in predicted_day.lower() or predicted_day.lower() == 'chest':
            recommendations = workouts_for_day.sample(n=min(4, len(workouts_for_day))).to_dict(orient='records')
        elif 'back day' in predicted_day.lower() or predicted_day.lower() == 'back':
            recommendations = workouts_for_day.sample(n=min(4, len(workouts_for_day))).to_dict(orient='records')
        elif 'leg day' in predicted_day.lower() or predicted_day.lower() == 'leg':
            recommendations = workouts_for_day.sample(n=min(4, len(workouts_for_day))).to_dict(orient='records')
        elif 'upper body' in predicted_day.lower():
            recommendations = workouts_for_day.sample(n=min(4, len(workouts_for_day))).to_dict(orient='records')
        elif 'lower body' in predicted_day.lower():
            recommendations = workouts_for_day.sample(n=min(4, len(workouts_for_day))).to_dict(orient='records')
        elif 'cardio' in predicted_day.lower():
            recommendations = workouts_for_day.sample(n=min(1, len(workouts_for_day))).to_dict(orient='records')
        elif 'full body' in predicted_day.lower():
            recommendations = workouts_for_day.sample(n=min(5, len(workouts_for_day))).to_dict(orient='records')
        elif 'arm day' in predicted_day.lower() or predicted_day.lower() == 'arms':
            bicep_exercise = workouts_for_day[workouts_for_day['TargetedMuscle'].str.lower() == 'biceps'].sample(n=1).to_dict(orient='records')
            tricep_exercise = workouts_for_day[workouts_for_day['TargetedMuscle'].str.lower() == 'triceps'].sample(n=1).to_dict(orient='records')
            shoulder_exercise = workouts_for_day[workouts_for_day['TargetedMuscle'].str.lower() == 'shoulders'].sample(n=1).to_dict(orient='records')
            forearm_exercise = workouts_for_day[workouts_for_day['TargetedMuscle'].str.lower() == 'forearms'].sample(n=1).to_dict(orient='records')
            
            recommendations = bicep_exercise + tricep_exercise + shoulder_exercise + forearm_exercise
            additional_exercises = workouts_for_day.sample(n=max(0, 4 - len(recommendations))).to_dict(orient='records')
            recommendations += additional_exercises
        
        return recommendations

workout_model = WorkoutModel()