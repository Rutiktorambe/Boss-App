from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Employee
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:  
            return redirect(url_for('login')) 
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))  # Redirect to login if accessing root

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Employee.query.filter_by(username=username).first()

        if user and user.Password == password: 
            session['user_id'] = user.EMPID
            session['username'] = user.username
            session.permanent = True  
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/home')
@login_required  
def home():
    # Fetch the logged-in user's details
    user_id = session['user_id']
    user = Employee.query.filter_by(EMPID=user_id).first()

    # Fetch the line manager's name
    line_manager_name = Employee.query.filter_by(EMPID=user.LineManagerID).first().EName if user.LineManagerID else None

    return render_template('home.html', user=user, line_manager_name=line_manager_name)

@app.route('/timesheet')
@login_required
def timesheet():
    user_id = session['user_id']
    user = Employee.query.filter_by(EMPID=user_id).first()

    # Check if user is a manager
    is_manager = user.LineManagerID is None  # Assuming managers do not have a line manager

    return render_template('timesheet.html', user=user, is_manager=is_manager)

@app.route('/logout')
@login_required  
def logout():
    session.clear() 
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables are created
    app.run(debug=True)
