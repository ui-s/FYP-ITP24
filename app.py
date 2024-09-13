#app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from data_cleaning import clean_workout_schedule_data, clean_workout_days_data
from model_improved import WorkoutModel
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
import random


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

        # Data Cleaning
        clean_workout_schedule_data()
        clean_workout_days_data()

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
    return render_template('workout_day.html', day=day, workout=day_workout)

@app.route('/record_workout/<day>', methods=['GET', 'POST'])
def record_workout(day):
    workout_plan = session.get('workout_plan', {})
    day_workout = workout_plan.get(day.capitalize(), {})
    
    if request.method == 'POST':
        # Logic to save the recorded workout data
        flash('Workout recorded successfully!', 'success')
        return redirect(url_for('display_workout_plan'))
    
    return render_template('record_workout.html', day=day, workout=day_workout)

# Statistics routes
@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/get_radar_chart/<int:week_no>')
def get_radar_chart(week_no):
    # Group by 'Week_no' and sum the sets for each muscle group
    weekly_data = USERS_DF.groupby('Week_no')[['Chest_sets', 'Back_sets', 'Legs_sets', 'Arms_sets', 'Shoulder_sets', 'Core_sets']].sum()
    
    # Ensure week_no exists in the data
    if week_no not in weekly_data.index:
        return "Week number not available", 404

    values = weekly_data.loc[week_no].values.flatten().tolist()
    categories = ['Chest_sets', 'Back_sets', 'Legs_sets', 'Arms_sets', 'Shoulder_sets', 'Core_sets']
    N = len(categories)

    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values += values[:1]  # Repeat the first value to close the circle
    angles += angles[:1]  # Repeat the first angle to close the circle

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, values, color='blue', alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)
    ax.set_title('Muscle Group Worked this week', fontsize=14)

    chart_path = f'static/charts/radar_chart_week_{week_no}.png'
    plt.savefig(chart_path)
    plt.close(fig)
    return send_file(chart_path)

@app.route('/get_bmi_chart')
def get_bmi_chart():
    # Make sure data isn't empty
    if USERS_DF.empty:
        return "Dataset is empty", 404

    height_m = USERS_DF['Height_cm'].iloc[-1] / 100  # Convert height to meters
    weight_kg = USERS_DF['Weight_kg'].iloc[-1]  # Weight in kg
    bmi = weight_kg / (height_m ** 2)

    plt.figure(figsize=(6, 4))
    sns.barplot(x=['BMI'], y=[bmi])
    plt.ylabel('BMI')
    plt.title('BMI Chart')
    plt.axhline(25, color='red', linestyle='--', label='Overweight Threshold (25)')
    plt.axhline(30, color='orange', linestyle='--', label='Obesity Threshold (30)')
    plt.legend()

    chart_path = 'static/charts/bmi_chart.png'
    plt.savefig(chart_path)
    plt.close()
    return send_file(chart_path)

@app.route('/get_total_reps_chart')
def get_total_reps_chart():
    days = USERS_DF['Day'].values
    total_reps = USERS_DF['Total_reps'].values

    plt.figure(figsize=(8, 4))
    sns.barplot(x=days, y=total_reps, palette='viridis')
    plt.title('Total Reps for the Week')
    plt.xlabel('Days of the Week')
    plt.ylabel('Total Reps')
    plt.xticks(rotation=45)

    chart_path = 'static/charts/total_reps_chart.png'
    plt.savefig(chart_path)
    plt.close()
    return send_file(chart_path)

@app.route('/get_duration_chart')
def get_duration_chart():
    duration = USERS_DF['Duration_mins'].values
    days = USERS_DF['Day'].values

    plt.figure(figsize=(8, 4))
    sns.barplot(x=days, y=duration, palette='mako')
    plt.title('Workout Duration for the Week')
    plt.xlabel('Days of the Week')
    plt.ylabel('Duration (minutes)')
    plt.xticks(rotation=45)

    chart_path = 'static/charts/duration_chart.png'
    plt.savefig(chart_path)
    plt.close()
    return send_file(chart_path)

if __name__ == '__main__':
    app.run(debug=True)