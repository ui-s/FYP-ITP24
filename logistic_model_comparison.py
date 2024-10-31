import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import os
import logging

logger = logging.getLogger(__name__)

class WorkoutModelComparison:
    def __init__(self):
        self.features = ['Gender', 'Age', 'BodyGoal', 'ProblemAreas', 'Height_cm', 'Weight_kg', 'FitnessLevel', 'WorkoutDaysPerWeek']
        self.target_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        self.encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')

    def load_data(self):
        try:
            # Load dataset as in your current model
            self.workout_schedule_data = pd.read_csv(os.path.join('data', 'processed', 'Cleaned_WorkoutScheduleRecommendationDataset.csv'))
            self.workout_schedule_data = self.workout_schedule_data.dropna()
            self.workout_schedule_data['WorkoutDaysPerWeek'] = self.workout_schedule_data['WorkoutDaysPerWeek'].astype(int)
            logger.info("Data loaded successfully.")
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

    def train_models(self):
        self.load_data()
        X, y = self.preprocess_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Dataframe to hold results
        results = {
            "Day": [],
            "Model": [],
            "Accuracy": [],
            "Precision": [],
            "Recall": [],
            "F1-Score": []
        }

        # Train Random Forest and Logistic Regression
        self.random_forest_models = {}
        self.logistic_regression_models = {}

        for day in self.target_days:
            print(f"--- Evaluation for {day} ---")

            # Train Random Forest
            rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
            rf_model.fit(X_train, y_train[day])
            y_pred_rf = rf_model.predict(X_test)

            # Train Logistic Regression
            lr_model = LogisticRegression(max_iter=1000)
            lr_model.fit(X_train, y_train[day])
            y_pred_lr = lr_model.predict(X_test)

            # Random Forest metrics
            accuracy_rf = accuracy_score(y_test[day], y_pred_rf)
            precision_rf = precision_score(y_test[day], y_pred_rf, average='weighted', zero_division=0)
            recall_rf = recall_score(y_test[day], y_pred_rf, average='weighted', zero_division=0)
            f1_rf = f1_score(y_test[day], y_pred_rf, average='weighted', zero_division=0)

            # Logistic Regression metrics
            accuracy_lr = accuracy_score(y_test[day], y_pred_lr)
            precision_lr = precision_score(y_test[day], y_pred_lr, average='weighted', zero_division=0)
            recall_lr = recall_score(y_test[day], y_pred_lr, average='weighted', zero_division=0)
            f1_lr = f1_score(y_test[day], y_pred_lr, average='weighted', zero_division=0)

            # Add Random Forest results to dataframe
            results["Day"].append(day)
            results["Model"].append("Random Forest")
            results["Accuracy"].append(accuracy_rf)
            results["Precision"].append(precision_rf)
            results["Recall"].append(recall_rf)
            results["F1-Score"].append(f1_rf)

            # Add Logistic Regression results to dataframe
            results["Day"].append(day)
            results["Model"].append("Logistic Regression")
            results["Accuracy"].append(accuracy_lr)
            results["Precision"].append(precision_lr)
            results["Recall"].append(recall_lr)
            results["F1-Score"].append(f1_lr)

        # Create a DataFrame for the results
        df_results = pd.DataFrame(results)
        print(df_results)
    def compare_models(self):
        
        self.train_models()
        # Further analysis and comparison can be added here# Extend the train_models function

if __name__ == "__main__":
    model_comparison = WorkoutModelComparison()
    model_comparison.train_models()