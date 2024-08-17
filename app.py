from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

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
    return redirect(url_for('workout_plan'))

@app.route('/workout_plan')
def workout_plan():
    # This will be implemented in the next step
    return "Workout Plan Page - To be implemented"

if __name__ == '__main__':
    app.run(debug=True)