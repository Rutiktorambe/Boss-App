from flask import Flask, render_template, request, redirect, session, url_for
from models import db, Employee, TimesheetEntry
from datetime import timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///emsdatabase.db'
app.config['SECRET_KEY'] = 'yoursecretkey'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)  # Set session timeout to 5 minutes

db.init_app(app)

# Check for user inactivity
@app.before_request
def session_management():
    session.permanent = True
    session.modified = True

# Login Page (Renamed from Landing)
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])  # Allow both '/' and '/login' URLs
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Employee.query.filter_by(username=username, Password=password).first()
        if user:
            session['EMPID'] = user.EMPID
            session.permanent = True  # Mark the session as permanent to use timeout
            return redirect(url_for('home'))
        else:
            return "Invalid credentials"
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('EMPID', None)
    return redirect(url_for('login'))

# Home Page
@app.route('/home')
def home():
    if 'EMPID' not in session:
        return redirect(url_for('login'))
    
    emp = Employee.query.filter_by(EMPID=session['EMPID']).first()
    return render_template('home.html', emp=emp)

# Timesheet Home Page
@app.route('/timesheet')
def timesheet_home():
    if 'EMPID' not in session:
        return redirect(url_for('login'))

    emp = Employee.query.filter_by(EMPID=session['EMPID']).first()
    is_manager = Employee.query.filter_by(LineManagerID=emp.EMPID).count() > 0
    
    return render_template('timesheet_home.html', emp=emp, is_manager=is_manager)

# Fill Timesheet
@app.route('/timesheet/fill', methods=['GET', 'POST'])
def fill_timesheet():
    if 'EMPID' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Add timesheet entry logic here
        pass

    return render_template('fill_timesheet.html')

# View Timesheet Summary
@app.route('/timesheet/summary')
def view_summary():
    if 'EMPID' not in session:
        return redirect(url_for('login'))

    emp = Employee.query.filter_by(EMPID=session['EMPID']).first()
    entries = TimesheetEntry.query.filter_by(EmpID=emp.EMPID).all()
    
    return render_template('view_summary.html', entries=entries)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
