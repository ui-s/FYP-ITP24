#app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from data_cleaning import clean_workout_schedule_data, clean_workout_days_data, clean_problem_area_data
from model_improved import WorkoutModel
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import random
from flask import jsonify


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Load dataset globally to avoid reloading for each request
USERS_DF = pd.read_csv('GymAppUsersDataset.csv')

@app.route('/')
def index():
    session['age_group'] = ''
    session['gender'] = ''
    session['height'] = ''
    session['weight'] = ''
    session['body_goal'] = ''
    session['problem_areas'] = []
    session['fitness_level'] = ''
    session['workout_days'] = ''
    return render_template('index.html')

@app.route('/process_step1', methods=['POST'])
def process_step1():
    session['age_group'] = request.form.get('age_group', '')
    session['gender'] = request.form.get('gender', '')
    session['height'] = request.form.get('height', '')
    session['weight'] = request.form.get('weight', '')
    return redirect(url_for('body_goal'))

@app.route('/body_goal')
def body_goal():
    return render_template('body_goal.html')

@app.route('/process_body_goal', methods=['POST'])
def process_body_goal():
    session['body_goal'] = request.form['body_goal']
    return redirect(url_for('problem_area'))

@app.route('/problem_area')
def problem_area():
    return render_template('problem_area.html')

@app.route('/process_problem_areas', methods=['POST'])
def process_problem_areas():
    session['problem_areas'] = request.form.getlist('problem_areas')
    return redirect(url_for('fitness_level'))

@app.route('/fitness_level')
def fitness_level():
    return render_template('fitness_level.html')

@app.route('/process_fitness_level', methods=['POST'])
def process_fitness_level():
    session['fitness_level'] = request.form['fitness_level']
    return redirect(url_for('workout_days'))

@app.route('/workout_days')
def workout_days():
    return render_template('workout_days.html')

@app.route('/process_workout_days', methods=['POST'])
def process_workout_days():
    session['workout_days'] = int(request.form['workout_days'])
    return redirect(url_for('confirmation'))

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

@app.route('/generate_workout_plan', methods=['POST'])
def generate_workout_plan():
    try:
        # Store original session data
        original_session_data = {
            'age_group': session.get('age_group', ''),
            'gender': session.get('gender', ''),
            'height': session.get('height', ''),
            'weight': session.get('weight', ''),
            'body_goal': session.get('body_goal', ''),
            'problem_areas': session.get('problem_areas', []),
            'fitness_level': session.get('fitness_level', ''),
            'workout_days': session.get('workout_days', '')
        }

        # Perform data cleaning
        clean_workout_schedule_data()
        clean_workout_days_data()
        clean_problem_area_data()

        # Initialize the workout model
        workout_model = WorkoutModel()

        # Helper function to safely convert to int
        def safe_int(value, default=0):
            try:
                return int(value)
            except (ValueError, TypeError):
                return default

        # Prepare user input
        user_input = {
            'Gender': original_session_data['gender'],
            'Age': safe_int(original_session_data['age_group'].split('-')[0]),
            'BodyGoal': original_session_data['body_goal'],
            'ProblemAreas': ', '.join(original_session_data['problem_areas']),
            'Height_cm': float(original_session_data['height'] or 0),
            'Weight_kg': float(original_session_data['weight'] or 0),
            'FitnessLevel': original_session_data['fitness_level'],
            'WorkoutDaysPerWeek': safe_int(original_session_data['workout_days'])
        }

        # Validate that essential fields are not empty or zero
        if not all([user_input['Gender'], user_input['Age'], user_input['BodyGoal'], 
                    user_input['FitnessLevel'], user_input['WorkoutDaysPerWeek']]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('confirmation'))

        # Generate workout plan
        workout_plan_raw = workout_model.generate_workout_plan(user_input)

        # Format the workout plan for the session
        workout_plan = {}
        all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        for day in all_days:
            day_plan = next((plan for plan in workout_plan_raw if plan['Day'] == day), None)
            if day_plan:
                workout_plan[day] = {
                    'type': day_plan['WorkoutType'],
                    'exercises': day_plan['Exercises']
                }
            else:
                workout_plan[day] = {'type': 'Rest', 'exercises': []}

        # Store the workout plan in the session
        session['workout_plan'] = workout_plan
        
        # Restore original session data
        session.update(original_session_data)

        print("Workout plan generated:", workout_plan)  # Debugging line

        return redirect(url_for('display_workout_plan'))
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        flash(f"An error occurred while generating the workout plan: {str(e)}", 'error')
        
        # Restore original session data in case of error
        session.update(original_session_data)
        
        return redirect(url_for('confirmation'))

@app.route('/workout_plan')
def display_workout_plan():
    workout_plan = session.get('workout_plan', {})
    return render_template('weekly_workout_plan.html', workout_plan=workout_plan)


@app.route('/workout/<day>')
def workout(day):
    workout_plan = session.get('workout_plan', {})
    day_workout = workout_plan.get(day.capitalize(), {})
    
    # Load the WorkoutDaysDataset
    df = pd.read_csv('data/processed/Cleaned_WorkoutDaysDataset.csv')
    
    # Filter exercises based on the workout type
    workout_type = day_workout.get('type', '')
    available_exercises = df[df['WorkoutDay'] == workout_type]['Exercise'].tolist()
    
    return render_template('workout_day.html', day=day, workout=day_workout, available_exercises=available_exercises)

@app.route('/update_workout/<day>', methods=['POST'])
def update_workout(day):
    data = request.json
    exercises = data.get('exercises', [])
    
    workout_plan = session.get('workout_plan', {})
    day_workout = workout_plan.get(day.capitalize(), {})
    
    # Load the WorkoutDaysDataset to get exercise details
    df = pd.read_csv('data/processed/Cleaned_WorkoutDaysDataset.csv')
    
    # Update the exercises for the day
    updated_exercises = []
    for exercise_name in exercises:
        exercise_data = df[df['Exercise'] == exercise_name].to_dict('records')
        if exercise_data:
            updated_exercises.append(exercise_data[0])
        else:
            updated_exercises.append({'Exercise': exercise_name, 'TargetedMuscle': 'To be determined'})
    
    day_workout['exercises'] = updated_exercises
    workout_plan[day.capitalize()] = day_workout
    session['workout_plan'] = workout_plan
    
    return jsonify({'success': True})

@app.route('/record_workout/<day>')
def record_workout(day):
    workout_plan = session.get('workout_plan', {})
    day_workout = workout_plan.get(day.capitalize(), {})
    return render_template('record_workout.html', day=day, workout=day_workout)
@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/get_chart_data')
def get_chart_data():
    try:
        # Load the GymAppUsersDataset
        df = pd.read_csv('GymAppUsersDataset.csv')
        print("DataFrame loaded:", df.head())  # Print first few rows

        # Process data for Muscle Group Chart
        muscle_groups = ['Chest', 'Back', 'Legs', 'Arms', 'Shoulder', 'Core']
        muscle_group_sets = [
            int(df['Chest_sets'].sum()),
            int(df['Back_sets'].sum()),
            int(df['Legs_sets'].sum()),
            int(df['Arms_sets'].sum()),
            int(df['Shoulder_sets'].sum()),
            int(df['Core_sets'].sum())
        ]
        print("Muscle group sets:", muscle_group_sets)

        # Process data for Workout Duration Chart
        workout_days = df['Day'].tolist()
        workout_durations = df['Duration_mins'].tolist()
        workout_durations = [int(d) for d in workout_durations]  # Convert to regular Python int
        print("Workout days:", workout_days)
        print("Workout durations:", workout_durations)

        # Process data for Total Reps Chart
        total_reps = df['Total_reps'].tolist()
        total_reps = [int(r) for r in total_reps]  # Convert to regular Python int
        print("Total reps:", total_reps)

        # Calculate BMI (using the last row of data)
        last_record = df.iloc[-1]
        height_m = float(last_record['Height_cm']) / 100
        weight_kg = float(last_record['Weight_kg'])
        bmi = weight_kg / (height_m ** 2)
        print("Calculated BMI:", bmi)

        chart_data = {
            'muscle_groups': muscle_groups,
            'muscle_group_sets': muscle_group_sets,
            'workout_days': workout_days,
            'workout_durations': workout_durations,
            'total_reps': total_reps,
            'bmi': float(bmi)  # Ensure BMI is a regular float
        }

        print("Returning chart data:", chart_data)
        return jsonify(chart_data)
    except Exception as e:
        print(f"Error in get_chart_data: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)