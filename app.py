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
    # This will be implemented in the next step
    return "Body Goal Page - To be implemented"

if __name__ == '__main__':
    app.run(debug=True)