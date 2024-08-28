from flask import Flask, render_template, request, redirect, url_for, session, flash
from data_cleaning import clean_workout_schedule_data, clean_workout_days_data
from model import WorkoutModel
import os
import random

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_planner.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    height_cm = db.Column(db.Float)
    weight_kg = db.Column(db.Float)

class WorkoutData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    day = db.Column(db.String(10), nullable=False)
    week_no = db.Column(db.Integer, nullable=False)
    bench_pr = db.Column(db.Float)
    squat_pr = db.Column(db.Float)
    deadlift_pr = db.Column(db.Float)
    chest_sets = db.Column(db.Integer)
    back_sets = db.Column(db.Integer)
    legs_sets = db.Column(db.Integer)
    arms_sets = db.Column(db.Integer)
    shoulder_sets = db.Column(db.Integer)
    core_sets = db.Column(db.Integer)
    duration_mins = db.Column(db.Integer)
    total_reps = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        gender = request.form['gender']
        age = int(request.form['age'])
        height_cm = float(request.form['height_cm'])
        weight_kg = float(request.form['weight_kg'])
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('register'))
        
        new_user = User(username=username, 
                        password_hash=generate_password_hash(password),
                        gender=gender,
                        age=age,
                        height_cm=height_cm,
                        weight_kg=weight_kg)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# ^ END REGSITER/LOGIN CODE

@app.route('/')
def index():
    # Initialize session variables with default values
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
        # Clean the data
        clean_workout_schedule_data()
        clean_workout_days_data()

        # Initialize and train the model
        workout_model = WorkoutModel()

        # Prepare user input
        user_input = {
            'Gender': session.get('gender', ''),
            'Age': int(session.get('age_group', '0').split('-')[0]),
            'BodyGoal': session.get('body_goal', ''),
            'ProblemAreas': session.get('problem_areas', [''])[0] if session.get('problem_areas') else '',
            'Height_cm': float(session.get('height', 0)),
            'Weight_kg': float(session.get('weight', 0)),
            'FitnessLevel': session.get('fitness_level', ''),
            'WorkoutDaysPerWeek': int(session.get('workout_days', 0))
        }
        
        # Generate initial predictions
        initial_predictions = workout_model.predict_workout(user_input)
        
        # Ensure we have the correct number of workout days
        workout_days = int(user_input['WorkoutDaysPerWeek'])
        all_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Create a list of unique workout types from initial predictions
        workout_types = list(set(initial_predictions.values()))
        workout_types = [wt for wt in workout_types if wt != 'Rest']
        
        # If we don't have enough workout types, add some generic ones
        generic_types = ['Cardio', 'Strength', 'Flexibility', 'HIIT', 'Core']
        while len(workout_types) < workout_days:
            workout_types.extend(generic_types)
        
        # Randomly select the required number of workout days and types
        selected_days = random.sample(all_days, workout_days)
        selected_types = random.sample(workout_types, workout_days)
        
        # Create the workout plan
        workout_plan = {}
        for day, workout_type in zip(selected_days, selected_types):
            workouts = workout_model.recommend_workouts(workout_type, user_input['FitnessLevel'])
            workout_plan[day] = {'type': workout_type, 'exercises': workouts}
        
        # Add rest days for the remaining days
        for day in all_days:
            if day not in workout_plan:
                workout_plan[day] = {'type': 'Rest', 'exercises': ['Rest']}
        
        # Store the workout plan in the session for display
        session['workout_plan'] = workout_plan
        
        return redirect(url_for('display_workout_plan'))
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        flash(f"An error occurred: {str(e)}", 'error')
        return redirect(url_for('confirmation'))

@app.route('/workout_plan')
@login_required
def display_workout_plan():
    workout_plan = session.get('workout_plan', {})
    
    # Fetch workout data for the current week
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    workout_data = WorkoutData.query.filter(
        WorkoutData.user_id == current_user.id,
        WorkoutData.date >= start_of_week,
        WorkoutData.date <= end_of_week
    ).all()
    
    # Prepare data for charts
    muscle_groups = ['Chest', 'Back', 'Legs', 'Arms', 'Shoulders', 'Core']
    muscle_group_sets = [sum(getattr(wd, f'{mg.lower()}_sets') for wd in workout_data) for mg in muscle_groups]
    
    workout_durations = [wd.duration_mins for wd in workout_data]
    total_reps = [wd.total_reps for wd in workout_data]
    
    # Calculate BMI
    height_m = current_user.height_cm / 100
    bmi = current_user.weight_kg / (height_m ** 2)
    
    chart_data = {
        'muscle_groups': muscle_groups,
        'muscle_group_sets': muscle_group_sets,
        'workout_days': [wd.day for wd in workout_data],
        'workout_durations': workout_durations,
        'total_reps': total_reps,
        'bmi': bmi
    }
    
    return render_template('weekly_workout_plan.html', workout_plan=workout_plan, chart_data=chart_data)


@app.route('/workout/<day>')
def workout(day):
    workout_plan = session.get('workout_plan', {})
    day_workout = workout_plan.get(day.capitalize(), {})
    return render_template('workout_day.html', day=day, workout=day_workout)

@app.route('/record_workout/<day>', methods=['GET', 'POST'])
@login_required
def record_workout(day):
    if request.method == 'POST':
        workout_plan = session.get('workout_plan', {})
        day_workout = workout_plan.get(day.capitalize(), {})

        chest_sets = back_sets = legs_sets = arms_sets = shoulder_sets = core_sets = total_reps = 0

        for exercise in day_workout.get('exercises', []):
            exercise_name = exercise['Exercise'].lower()
            targeted_muscle = exercise['TargetedMuscle'].lower()
            
            sets = len(request.form.getlist(f"{exercise_name.replace(' ', '_')}_weight[]"))
            reps = sum([int(r) for r in request.form.getlist(f"{exercise_name.replace(' ', '_')}_reps[]")])
            
            if 'chest' in exercise_name or 'chest' in targeted_muscle:
                chest_sets += sets
            elif 'back' in exercise_name or 'back' in targeted_muscle:
                back_sets += sets
            elif 'leg' in exercise_name or 'leg' in targeted_muscle:
                legs_sets += sets
            elif any(muscle in exercise_name or muscle in targeted_muscle for muscle in ['bicep', 'tricep', 'forearm']):
                arms_sets += sets
            elif 'shoulder' in exercise_name or 'shoulder' in targeted_muscle:
                shoulder_sets += sets
            elif 'core' in exercise_name or 'abs' in exercise_name or 'core' in targeted_muscle or 'abs' in targeted_muscle:
                core_sets += sets
            
            total_reps += reps

        workout_data = WorkoutData(
            user_id=current_user.id,
            date=datetime.now().date(),
            day=day,
            week_no=1,  # You need to implement week number logic
            chest_sets=chest_sets,
            back_sets=back_sets,
            legs_sets=legs_sets,
            arms_sets=arms_sets,
            shoulder_sets=shoulder_sets,
            core_sets=core_sets,
            duration_mins=int(request.form['workout_duration']) // 60,
            total_reps=total_reps
        )
        db.session.add(workout_data)
        db.session.commit()
        
        flash('Workout recorded successfully!', 'success')
        return redirect(url_for('display_workout_plan'))
    
    workout_plan = session.get('workout_plan', {})
    day_workout = workout_plan.get(day.capitalize(), {})
    return render_template('record_workout.html', day=day, workout=day_workout)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)