from flask import Flask, render_template, request, redirect, url_for, session, flash
from data_cleaning import clean_workout_schedule_data, clean_workout_days_data
from model import WorkoutModel
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_step1', methods=['POST'])
def process_step1():
    session['age_group'] = request.form['age_group']
    session['gender'] = request.form['gender']
    session['height'] = float(request.form['height'])
    session['weight'] = float(request.form['weight'])
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
        # Clean the data
        clean_workout_schedule_data()
        clean_workout_days_data()

        # Initialize and train the model
        workout_model = WorkoutModel()

        # Prepare user input
        user_input = {
            'Gender': session.get('gender', ''),
            'Age': int(session.get('age_group', '0').split('-')[0]),  # Take the lower bound of the age range
            'BodyGoal': session.get('body_goal', ''),
            'ProblemAreas': session.get('problem_areas', [''])[0] if session.get('problem_areas') else '',  # Take the first problem area
            'Height_cm': float(session.get('height', 0)),
            'Weight_kg': float(session.get('weight', 0)),
            'FitnessLevel': session.get('fitness_level', ''),
            'WorkoutDaysPerWeek': int(session.get('workout_days', 0))
        }
        
        print("User input before prediction:", user_input)
        
        # Generate predictions
        predicted_days = workout_model.predict_workout(user_input)
        workout_plan = {}
        
        for day, workout_type in predicted_days.items():
            workouts = workout_model.recommend_workouts(workout_type, user_input['FitnessLevel'])
            workout_plan[day] = {'type': workout_type, 'exercises': workouts}
        
        # Store the workout plan in the session for display
        session['workout_plan'] = workout_plan
        
        return redirect(url_for('display_workout_plan'))
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        flash(f"An error occurred: {str(e)}", 'error')
        return redirect(url_for('confirmation'))

@app.route('/workout_plan')
def display_workout_plan():
    workout_plan = session.get('workout_plan', {})
    return render_template('workout_plan.html', workout_plan=workout_plan)

if __name__ == '__main__':
    app.run(debug=True)