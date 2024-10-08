import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import random
import os
import logging

logger = logging.getLogger(__name__)

class WorkoutModel:
    def __init__(self):
        self.features = ['Gender', 'Age', 'BodyGoal', 'ProblemAreas', 'Height_cm', 'Weight_kg', 'FitnessLevel', 'WorkoutDaysPerWeek']
        self.target_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.workout_types = ['Chest Day', 'Back Day', 'Leg Day', 'Arm Day', 'Upper Body', 'Lower Body', 'Cardio', 'Full Body', 'Rest']
        self.encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)

    def load_data(self):
        try:
            self.workout_schedule_data = pd.read_csv(os.path.join('data', 'processed', 'Cleaned_WorkoutScheduleRecommendationDataset.csv'))
            self.workout_exercises_data = pd.read_csv(os.path.join('data', 'processed', 'Cleaned_WorkoutDaysDataset.csv'))
            self.problem_area_data = pd.read_csv(os.path.join('data', 'processed', 'Cleaned_ProblemAreaDataset.csv'))
            
            self.workout_schedule_data = self.workout_schedule_data.dropna()
            self.workout_schedule_data['WorkoutDaysPerWeek'] = self.workout_schedule_data['WorkoutDaysPerWeek'].astype(int)
            
            for day in self.target_days:
                self.workout_schedule_data[day] = self.workout_schedule_data[day].apply(lambda x: x.title() if pd.notna(x) else 'Rest')
            
            logger.info("Data loaded and preprocessed successfully")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise

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
        
        # First pass: Use model predictions
        for day, workout in predictions.items():
            if workout != 'Rest' and workout_count < workout_days:
                schedule[day] = workout
                workout_count += 1
        
        # Second pass: Fill in remaining days if needed
        if workout_count < workout_days:
            remaining_days = [day for day in self.target_days if schedule[day] == 'Rest']
            additional_workouts = random.sample(remaining_days, workout_days - workout_count)
            for day in additional_workouts:
                schedule[day] = random.choice([wt for wt in self.workout_types if wt != 'Rest'])
        
        # Apply logical structuring
        self.apply_logical_structure(schedule, workout_days)
        
        return schedule

    def apply_logical_structure(self, schedule, workout_days):
        days = self.target_days
        
        if workout_days <= 3:
            # For 1-3 workout days, ensure at least one rest day between workouts
            workout_indices = [i for i, day in enumerate(days) if schedule[day] != 'Rest']
            new_schedule = {day: 'Rest' for day in days}
            for i, index in enumerate(workout_indices):
                new_day_index = (index + i * 2) % 7
                new_schedule[days[new_day_index]] = schedule[days[index]]
            schedule.update(new_schedule)
        elif 4 <= workout_days <= 5:
            # For 4-5 workout days, try to have a rest day after every 2-3 workouts
            workout_indices = [i for i, day in enumerate(days) if schedule[day] != 'Rest']
            for i in range(len(workout_indices) - 1):
                if workout_indices[i+1] - workout_indices[i] == 1:
                    next_day = days[(workout_indices[i+1] + 1) % 7]
                    if schedule[next_day] == 'Rest':
                        schedule[days[workout_indices[i+1]]] = 'Rest'
                        schedule[next_day] = schedule[days[workout_indices[i]]]
        # For 6-7 workout days, keep the original distribution
        
        # Ensure no duplicate workout types in a week
        used_workouts = set()
        for day in days:
            if schedule[day] != 'Rest':
                if schedule[day] in used_workouts:
                    unused_workouts = [wt for wt in self.workout_types if wt not in used_workouts and wt != 'Rest']
                    if unused_workouts:
                        schedule[day] = random.choice(unused_workouts)
                    else:
                        schedule[day] = 'Full Body'  # Fallback to full body if all workout types are used
                used_workouts.add(schedule[day])

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
    
    def get_exercises_for_workout(self, workout_type, fitness_level, problem_areas):
            try:
                suitable_exercises = self.workout_exercises_data[
                    (self.workout_exercises_data['WorkoutDay'].str.lower() == workout_type.lower()) &
                    (self.workout_exercises_data['FitnessLevel'].str.lower() == fitness_level.lower())
                ]
                
                for area in problem_areas.split(', '):
                    problem_area_exercises = self.problem_area_data[
                        (self.problem_area_data['ProblemArea'].str.lower() == area.lower()) &
                        (self.problem_area_data['FitnessLevel'].str.lower() == fitness_level.lower())
                    ]
                    suitable_exercises = pd.concat([suitable_exercises, problem_area_exercises])
                
                if len(suitable_exercises) < 5:
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
                
                # Remove any rows with NaN values
                suitable_exercises = suitable_exercises.dropna(subset=['Exercise', 'TargetedMuscle'])
                
                if suitable_exercises.empty:
                    logger.warning(f"No suitable exercises found for {workout_type} at {fitness_level} level")
                    return []
                
                selected_exercises = suitable_exercises.sample(n=min(5, len(suitable_exercises))).to_dict('records')
                logger.info(f"Selected {len(selected_exercises)} exercises for {workout_type}")
                return selected_exercises
            except Exception as e:
                logger.error(f"Error getting exercises for workout: {str(e)}")
                return []

    def generate_workout_plan(self, user_input):
        try:
            workout_schedule = self.predict_workout_types(user_input)
            workout_plan = []
            
            for day, workout_type in workout_schedule.items():
                if workout_type != 'Rest':
                    exercises = self.get_exercises_for_workout(workout_type, user_input['FitnessLevel'], user_input['ProblemAreas'])
                    if exercises:
                        workout_plan.append({
                            'Day': day,
                            'WorkoutType': workout_type,
                            'Exercises': exercises
                        })
                    else:
                        logger.warning(f"No exercises found for {day} ({workout_type}). Adding as rest day.")
                        workout_plan.append({
                            'Day': day,
                            'WorkoutType': 'Rest',
                            'Exercises': []
                        })
                else:
                    workout_plan.append({
                        'Day': day,
                        'WorkoutType': 'Rest',
                        'Exercises': []
                    })
            
            logger.info(f"Generated workout plan with {len(workout_plan)} days")
            return workout_plan
        except Exception as e:
            logger.error(f"Error generating workout plan: {str(e)}")
            raise

    
workout_model = WorkoutModel()