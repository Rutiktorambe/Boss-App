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
from flask import Flask, render_template, request, redirect, session, url_for
from models import db, Employee, TimesheetEntry
from datetime import datetime
import uuid  # For generating unique IDs
@app.route('/timesheet/fill', methods=['GET', 'POST'])
def fill_timesheet():
    if 'EMPID' not in session:
        return redirect(url_for('login'))

    emp = Employee.query.filter_by(EMPID=session['EMPID']).first()

    if request.method == 'POST':
        dates = request.form['date_of_entry'].split(',')  # Handling multiple date selection

        for date in dates:
            total_time = (float(request.form['hours']) * 60 + float(request.form['minutes'])) / 60  # Total time in hours

            # Determine the allocation type and assign the correct billable or non-billable time
            allocation_type = request.form['allocation_type']
            category_1 = request.form.get('category_1', None)
                # Debugging
            print(f"Allocation Type: {allocation_type}")
            print(f"Category 1: {category_1}")
            billable_time = 0
            nonbillable_admin_time = 0
            nonbillable_training_time = 0

            if allocation_type == 'billable':
                billable_time = total_time
            elif allocation_type == 'non-billable':
                if category_1 == 'Admin':
                    nonbillable_admin_time = total_time
                elif category_1 == 'Training':
                    nonbillable_training_time = total_time

            entry = TimesheetEntry(
                Uniq_ID=str(uuid.uuid4()),  # Generate unique ID
                EName=emp.EName,
                EmpID=emp.EMPID,
                Team=emp.Team,
                LineManager=emp.LineManager,
                DateofEntry=date,
                StartTime=request.form['hours'],  # Hours worked
                EndTime=request.form['minutes'],
                Hours=request.form['hours'],
                Minutes=request.form['minutes'],
                billable_time=billable_time,
                nonbillable_admin_time=nonbillable_admin_time,
                nonbillable_training_time=nonbillable_training_time,
                AllocationType=allocation_type,
                Category1=category_1,
                Category2=request.form.get('category_2', None),
                Category3=request.form.get('category_3', None),
                ProjectCode=request.form['project_code'],
                Comment=request.form['comments'],
                Status='Pending',
                SubmitDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                LastUploadDate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                LastUpdatedBy=emp.username
            )
            # Insert into the database
            db.session.add(entry)

        db.session.commit()
        return redirect(url_for('timesheet_home'))

    return render_template('fill_timesheet.html', emp=emp)


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
