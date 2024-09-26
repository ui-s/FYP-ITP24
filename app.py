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
from datetime import datetime, timedelta
import traceback
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

def load_users_df():
    try:
        # Try reading the CSV file normally
        return pd.read_csv('GymAppUsersDataset.csv')
    except pd.errors.ParserError:
        # If there's an error, try to clean the file
        with open('GymAppUsersDataset.csv', 'r') as f:
            lines = f.readlines()
        
        # Remove any lines that don't have the correct number of fields
        correct_field_count = len(lines[0].strip().split(','))
        cleaned_lines = [line for line in lines if len(line.strip().split(',')) == correct_field_count]
        
        # Write the cleaned lines back to the file
        with open('GymAppUsersDataset.csv', 'w') as f:
            f.writelines(cleaned_lines)
        
        # Try reading the cleaned file
        return pd.read_csv('GymAppUsersDataset.csv')

# Use this function instead of directly reading the CSV
USERS_DF = load_users_df()

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

def ensure_file_termination():
    filename = 'GymAppUsersDataset.csv'
    with open(filename, 'ab+') as f:  # Open in binary append mode
        f.seek(-1, os.SEEK_END)
        last_char = f.read(1)
        if last_char != b'\n':
            f.write(b'\n')


@app.route('/save_workout', methods=['POST'])
def save_workout():
    try:
        data = request.json
        user_id = data['userId']
        
        # Get current date and derive day
        current_date = datetime.now()
        day = current_date.strftime('%A')
        
        # Load WorkoutDaysDataset to check for PR exercises
        workout_days_df = pd.read_csv('data/raw/WorkoutDaysDataset.csv')
        pr_exercises = {
            'Bench_pr(kg)': ['Barbell Bench Press'],
            'Squat_pr(kg)': ['Barbell Squats'],
            'Deadlift_pr(kg)': ['Deadlifts']
        }
        
        # Load existing user data
        user_data_df = pd.read_csv('GymAppUsersDataset.csv')
        user_previous_data = user_data_df[user_data_df['Id'] == user_id].sort_values('Date').tail(1)
        
        # Initialize PR values
        bench_pr = float(user_previous_data['Bench_pr(kg)'].values[0]) if not user_previous_data.empty else 0
        squat_pr = float(user_previous_data['Squat_pr(kg)'].values[0]) if not user_previous_data.empty else 0
        deadlift_pr = float(user_previous_data['Deadlift_pr(kg)'].values[0]) if not user_previous_data.empty else 0
        
        # Check for new PRs
        for exercise_card in data['exerciseData']:
            exercise_name = exercise_card['exerciseName']
            max_weight = max([float(set_data['weight']) for set_data in exercise_card['sets']], default=0)
            
            if exercise_name in pr_exercises['Bench_pr(kg)']:
                bench_pr = max(bench_pr, max_weight)
            elif exercise_name in pr_exercises['Squat_pr(kg)']:
                squat_pr = max(squat_pr, max_weight)
            elif exercise_name in pr_exercises['Deadlift_pr(kg)']:
                deadlift_pr = max(deadlift_pr, max_weight)
        
        # Prepare the row to be written to CSV
        row = [
            user_id,
            current_date.strftime('%d/%m/%Y'),
            day,
            str(bench_pr),
            str(squat_pr),
            str(deadlift_pr),
            str(data.get('chestSets', 0)),
            str(data.get('backSets', 0)),
            str(data.get('legsSets', 0)),
            str(data.get('armsSets', 0)),
            str(data.get('shoulderSets', 0)),
            str(data.get('coreSets', 0)),
            str(data['durationMins']),
            str(data['totalReps']),
            str(data['totalWeight']),
            str(data['aftworkoutWeight'])
        ]
        
        # Join the row with commas and add a newline character
        row_string = ','.join(row) + '\n'
        
        ensure_file_termination()
        
        # Append the new row to the CSV file
        with open('GymAppUsersDataset.csv', 'a') as f:
            f.write(row_string)
        
        return jsonify({'message': 'Workout saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/get_chart_data')
def get_chart_data():
    try:
        user_id = request.args.get('user_id', '')
        time_period = request.args.get('time_period', '7days')
        
        app.logger.info(f"Received request with user_id: {user_id}, time_period: {time_period}")

        columns_to_use = ['Id', 'Date', 'Day', 'Bench_pr(kg)', 'Squat_pr(kg)', 'Deadlift_pr(kg)',
                          'Chest_sets', 'Back_sets', 'Legs_sets', 'Arms_sets', 'Shoulder_sets',
                          'Core_sets', 'Duration_mins', 'Total_reps', 'Total_weight(kg)', 'aftworkout_weight']
        
        # Specify dtypes explicitly for problematic columns
        dtype_dict = {'Duration_mins': float, 'Total_reps': float, 'Total_weight(kg)': float}
        
        df = pd.read_csv('GymAppUsersDataset.csv', usecols=columns_to_use, parse_dates=['Date'], 
                         dayfirst=True, dtype=dtype_dict)
        
        app.logger.info(f"Raw Duration_mins data: {df['Duration_mins'].tolist()}")
        
        if user_id:
            df = df[df['Id'] == user_id]
        
        end_date = df['Date'].max()
        if time_period == '7days':
            start_date = end_date - timedelta(days=7)
        elif time_period == '30days':
            start_date = end_date - timedelta(days=30)
        elif time_period == '2months':
            start_date = end_date - timedelta(days=60)
        else:
            start_date = df['Date'].min()
        
        df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

        app.logger.info(f"Filtered Duration_mins data: {df_filtered['Duration_mins'].tolist()}")

        def safe_float(value):
            try:
                return float(value) if pd.notna(value) else None
            except ValueError:
                return None

        chart_data = {
            'muscle_groups': ['Chest', 'Back', 'Legs', 'Arms', 'Shoulder', 'Core'],
            'muscle_group_sets': [
                int(df_filtered['Chest_sets'].sum()),
                int(df_filtered['Back_sets'].sum()),
                int(df_filtered['Legs_sets'].sum()),
                int(df_filtered['Arms_sets'].sum()),
                int(df_filtered['Shoulder_sets'].sum()),
                int(df_filtered['Core_sets'].sum())
            ],
            'workout_days': df_filtered['Date'].dt.strftime('%Y-%m-%d').tolist(),
            'workout_durations': [safe_float(x) for x in df_filtered['Duration_mins']],
            'total_reps': [safe_float(x) for x in df_filtered['Total_reps']],
            'avg_weight': safe_float(df_filtered['aftworkout_weight'].mean()),
            'bodyweight_data': df_filtered[['Date', 'aftworkout_weight']].to_dict('records'),
            'bench_pr_data': df_filtered[['Date', 'Bench_pr(kg)']].to_dict('records'),
            'squat_pr_data': df_filtered[['Date', 'Squat_pr(kg)']].to_dict('records'),
            'deadlift_pr_data': df_filtered[['Date', 'Deadlift_pr(kg)']].to_dict('records'),
            'after_workout_weight_data': df_filtered[['Date', 'aftworkout_weight']].to_dict('records'),
            'total_weights': [safe_float(x) for x in df_filtered['Total_weight(kg)']]
        }

        # Ensure all dates are formatted as strings
        for key in ['bodyweight_data', 'bench_pr_data', 'squat_pr_data', 'deadlift_pr_data', 'after_workout_weight_data']:
            for item in chart_data[key]:
                item['Date'] = item['Date'].strftime('%Y-%m-%d') if isinstance(item['Date'], datetime) else item['Date']

        return jsonify(chart_data)


    except Exception as e:
        app.logger.error(f"Error in get_chart_data: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)