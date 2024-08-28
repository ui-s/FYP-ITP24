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
    return redirect(url_for('body_goal'))

@app.route('/body_goal')
def body_goal():
    return render_template('body_goal.html')

@app.route('/process_body_goal', methods=['POST'])
def process_body_goal():
    session['body_goal'] = request.form['body_goal']
    return redirect(url_for('problem_area'))



@app.route('/workout_plan')
def workout_plan():
    return render_template('workout_plan.html')

@app.route('/workout/<day>', methods=['GET', 'POST'])
def workout(day):
    if request.method == 'POST':
        # Here you would save the workout for the specified day
        session[f'{day}_workout'] = request.form
        return redirect(url_for('workout_plan'))
    return render_template('record_workout.html', day=day)

@app.route('/record_workout')
def record_workout():
    return render_template('record_workout.html')


@app.route('/problem_area', methods=['GET', 'POST'])
def problem_area():
    if request.method == 'POST':
        selected_areas = request.form.getlist('problem_area')  # Get list of selected areas
        session['problem_area'] = selected_areas  # Store in session or process as needed
        return redirect(url_for('workout_plan'))  # Redirect to the workout plan page
    return render_template('problem_area.html')


if __name__ == '__main__':
    app.run(debug=True)
