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
import logging
import csv
from werkzeug.exceptions import BadRequest
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def load_users_df():
    # Read the CSV file using csv.DictReader
    with open('GymAppUsersData.csv', 'r') as f:
        csv_reader = csv.DictReader(f)
        rows = list(csv_reader)

    # Check the CSV content
    print("Raw CSV content:")
    for row in rows:
        print(row)

    # Convert rows to DataFrame
    df = pd.DataFrame(rows)
    
    # Fix columns with list-like entries (e.g., 'Problem_Areas')
    df['Problem_Areas'] = df['Problem_Areas'].apply(lambda x: eval(x) if isinstance(x, str) else x)
    
    # Set the first column (Username) as index and convert to lowercase
    df.set_index('Username', inplace=True)
    df.index = df.index.str.strip().str.lower()

    print("DataFrame created:")
    print(df.head())
    print("DataFrame columns:", df.columns.tolist())
    print("DataFrame index (usernames):", df.index.tolist())
    
    return df

# Load user data
users_df = load_users_df()

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['user_id'].strip().lower()
    logger.info(f"Login attempt for username: {username}")
    
    if username in users_df.index:
        user_data = users_df.loc[username].to_dict()
        user_data['Username'] = username  # Add username to the user data
        logger.info(f"User found: {user_data}")
        
        try:
            # Store user data in session with consistent keys
            session['username'] = username
            session['gender'] = user_data['Gender']
            session['age_group'] = user_data['Age_Group']
            session['height'] = user_data['Height_cm']
            session['weight'] = user_data['Weight_kg']
            session['body_goal'] = user_data['Body_Goal']
            
            # Handle 'Problem_Areas' whether it's a string or a list
            if isinstance(user_data['Problem_Areas'], str):
                session['problem_areas'] = eval(user_data['Problem_Areas'])
            else:
                session['problem_areas'] = user_data['Problem_Areas']
            
            session['fitness_level'] = user_data['Fitness_Level']
            session['workout_days'] = user_data['Workout_Days']
            
            logger.info(f"Session data set for user: {username}")
            return jsonify({'success': True, 'redirect': url_for('generate_workout_plan')})
        except Exception as e:
            logger.error(f"Error setting session data for user {username}: {str(e)}")
            return jsonify({'success': False, 'message': 'An error occurred during login. Please try again.'})
    else:
        logger.warning(f"User not found: {username}")
        return jsonify({'success': False, 'message': 'User not found. Please register as a new user.'})
    
@app.route('/get-started')
def index():
    session.clear()  # Clear any existing session data
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
    session['username'] = request.form.get('username', '')
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


def ensure_file_termination():
    filename = 'GymAppUsersData.csv'
    if os.path.exists(filename):
        with open(filename, 'r+') as f:
            f.seek(0, os.SEEK_END)
            if f.tell() > 0:
                f.seek(-1, os.SEEK_END)
                last_char = f.read(1)
                if last_char != '\n':
                    f.write('\n')
    else:
        # If the file doesn't exist, create it with headers
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Username', 'Gender', 'Age_Group', 'Height_cm', 'Weight_kg', 'Body_Goal', 'Problem_Areas', 'Fitness_Level', 'Workout_Days'])

def format_problem_areas(problem_areas):
    return "[" + ", ".join(f"'{area}'" for area in problem_areas) + "]"

def save_user_data(user_data):
    ensure_file_termination()
    with open('GymAppUsersData.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        problem_areas = format_problem_areas(user_data['Problem_Areas'])
        writer.writerow([
            user_data['Username'],
            user_data['Gender'],
            user_data['Age_Group'],
            user_data['Height_cm'],
            user_data['Weight_kg'],
            user_data['Body_Goal'],
            problem_areas,
            user_data['Fitness_Level'],
            user_data['Workout_Days']
        ])
    logger.info(f"New user data saved: {user_data['Username']}")

@app.route('/generate_workout_plan', methods=['GET', 'POST'])
def generate_workout_plan():
    if request.method == 'GET':
        # Check if all required session data is present (for logged-in users)
        required_fields = ['username', 'gender', 'age_group', 'height', 'weight', 'body_goal', 'problem_areas', 'fitness_level', 'workout_days']
        if all(field in session for field in required_fields):
            try:
                user_data = {
                    'Username': session['username'],
                    'Gender': session['gender'],
                    'Age_Group': session['age_group'],
                    'Height_cm': session['height'],
                    'Weight_kg': session['weight'],
                    'Body_Goal': session['body_goal'],
                    'Problem_Areas': session['problem_areas'],
                    'Fitness_Level': session['fitness_level'],
                    'Workout_Days': session['workout_days']
                }
                logger.info(f"Generating plan for logged-in user: {user_data['Username']}")
                
                # Generate workout plan
                workout_plan = generate_workout(user_data)
                
                # Store the workout plan in the session
                session['workout_plan'] = workout_plan
                
                # Redirect to display_workout_plan
                return redirect(url_for('display_workout_plan'))
            except Exception as e:
                logger.error(f"Error generating workout plan: {str(e)}")
                flash("An error occurred while generating your workout plan. Please try again.", "error")
                return redirect(url_for('index'))
        else:
            missing_fields = [field for field in required_fields if field not in session]
            logger.warning(f"Incomplete user data in session. Missing fields: {missing_fields}")
            return redirect(url_for('index'))

    elif request.method == 'POST':
        try:
            # Collect user data from form submission
            user_data = {
                'Username': request.form.get('username', ''),
                'Gender': request.form.get('gender', ''),
                'Age_Group': request.form.get('age_group', ''),
                'Height_cm': request.form.get('height', ''),
                'Weight_kg': request.form.get('weight', ''),
                'Body_Goal': request.form.get('body_goal', ''),
                'Problem_Areas': request.form.getlist('problem_areas'),  # This will be a list
                'Fitness_Level': request.form.get('fitness_level', ''),
                'Workout_Days': request.form.get('workout_days', '')
            }
            
            logger.info(f"Collected user data from form: {user_data}")

            # Generate workout plan
            workout_plan = generate_workout(user_data)
            
            # Store the workout plan and user data in the session
            session['workout_plan'] = workout_plan
            session['user_data'] = user_data

            # Save new user data
            save_user_data(user_data)
            
            # Redirect to display_workout_plan
            return redirect(url_for('display_workout_plan'))
        except Exception as e:
            logger.error(f"Error in generate_workout_plan: {str(e)}", exc_info=True)
            flash("An unexpected error occurred. Please try again.", 'error')
            return redirect(url_for('index'))
        
def generate_workout(user_data):
    try:
        logger.info(f"Generating workout for user data: {user_data}")
        
        # Prepare user input for workout generation with default values and error handling
        user_input = {
            'Gender': user_data.get('Gender', '').strip() or 'Not specified',
            'Age': safe_int(user_data.get('Age_Group', '').split('-')[0], default=30),
            'BodyGoal': user_data.get('Body_Goal', '').strip() or 'Not specified',
            'ProblemAreas': ', '.join(user_data.get('Problem_Areas', [])) if isinstance(user_data.get('Problem_Areas'), list) else str(user_data.get('Problem_Areas', '')),
            'Height_cm': safe_float(user_data.get('Height_cm', ''), default=170),
            'Weight_kg': safe_float(user_data.get('Weight_kg', ''), default=70),
            'FitnessLevel': user_data.get('Fitness_Level', '').strip() or 'Beginner',
            'WorkoutDaysPerWeek': safe_int(user_data.get('Workout_Days', ''), default=3)
        }
        
        logger.info(f"Prepared user input: {user_input}")

        # Generate workout plan
        workout_model = WorkoutModel()
        workout_plan_raw = workout_model.generate_workout_plan(user_input)

        # Format the workout plan
        workout_plan = {}
        all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in all_days:
            day_plan = next((plan for plan in workout_plan_raw if plan['Day'] == day), None)
            if day_plan:
                # Filter out exercises with NaN values
                valid_exercises = [
                    exercise for exercise in day_plan['Exercises']
                    if pd.notna(exercise.get('Exercise')) and pd.notna(exercise.get('TargetedMuscle'))
                ]
                if not valid_exercises:
                    logger.warning(f"No valid exercises found for {day}. Adding rest day.")
                    workout_plan[day] = {'type': 'Rest', 'exercises': []}
                else:
                    workout_plan[day] = {
                        'type': day_plan['WorkoutType'],
                        'exercises': valid_exercises
                    }
            else:
                workout_plan[day] = {'type': 'Rest', 'exercises': []}

        # Log the generated workout plan for debugging
        logger.info(f"Generated workout plan: {workout_plan}")

        return workout_plan
    except Exception as e:
        logger.error(f"Error in generate_workout: {str(e)}", exc_info=True)
        raise BadRequest(f"Error generating workout plan: {str(e)}")

def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_float(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

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
        username = session.get('username')  # Get username from session
        
        if not username:
            return jsonify({'error': 'User not logged in'}), 401
        
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
        user_previous_data = user_data_df[user_data_df['Username'] == username].sort_values('Date').tail(1)
        
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
            username,
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
    username = session.get('username', '')
    if not username:
        flash('Please log in to view your statistics.', 'warning')
        return redirect(url_for('login'))

    # Check if user has any workout data
    df = pd.read_csv('GymAppUsersDataset.csv')
    user_data = df[df['Username'] == username]
    
    if user_data.empty:
        # User has no workout data
        return render_template('stats.html', username=username, has_data=False)
    else:
        # User has workout data
        return render_template('stats.html', username=username, has_data=True)

@app.route('/get_chart_data')
def get_chart_data():
    try:
        username = request.args.get('username', '')
        time_period = request.args.get('time_period', '7days')
        
        app.logger.info(f"Received request with username: {username}, time_period: {time_period}")

        columns_to_use = ['Username', 'Date', 'Day', 'Bench_pr(kg)', 'Squat_pr(kg)', 'Deadlift_pr(kg)',
                          'Chest_sets', 'Back_sets', 'Legs_sets', 'Arms_sets', 'Shoulder_sets',
                          'Core_sets', 'Duration_mins', 'Total_reps', 'Total_weight(kg)', 'aftworkout_weight',
                          'Calories_Burned']  
        
        dtype_dict = {'Duration_mins': float, 'Total_reps': float, 'Total_weight(kg)': float, 'Calories_Burned': float}
        
        df = pd.read_csv('GymAppUsersDataset.csv', usecols=columns_to_use, parse_dates=['Date'], 
                         dayfirst=True, dtype=dtype_dict)
        
        
        # Specify dtypes explicitly for problematic columns
        dtype_dict = {'Duration_mins': float, 'Total_reps': float, 'Total_weight(kg)': float}
        
        df = pd.read_csv('GymAppUsersDataset.csv', usecols=columns_to_use, parse_dates=['Date'], 
                         dayfirst=True, dtype=dtype_dict)
        
        if username:
            df = df[df['Username'] == username]
        
        if df.empty:
            app.logger.warning(f"No data found for username: {username}")
            return jsonify({"error": "No data found for the given username"}), 404
        
        
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
            'total_weights': [safe_float(x) for x in df_filtered['Total_weight(kg)']],
            'calories_burned': [safe_float(x) for x in df_filtered['Calories_Burned']]
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