from flask import Flask, render_template, request, redirect, session, url_for
from models import db, Employee, TimesheetEntry
from datetime import timedelta ,datetime
import uuid  # For generating unique IDs

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
@app.route('/login', methods=['GET', 'POST']) 
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
                Uniq_ID=str(uuid.uuid4()),
                EName=emp.EName,
                EmpID=emp.EMPID,
                Team=emp.Team,
                LineManager=emp.LineManager,
                DateofEntry=date,
                StartTime=request.form['hours'], 
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



@app.route('/timesheet/summary', methods=['GET'])
def view_summary():
    if 'EMPID' not in session:
        return redirect(url_for('login'))

    emp = Employee.query.filter_by(EMPID=session['EMPID']).first()
    selected_date_str = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    
    selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()

    start_date = selected_date - timedelta(days=selected_date.weekday())  # Monday
    end_date = start_date + timedelta(days=6)  # Sunday

    entries = TimesheetEntry.query.filter(
        TimesheetEntry.DateofEntry >= start_date,
        TimesheetEntry.DateofEntry <= end_date,
        TimesheetEntry.EmpID== emp.EMPID
    ).all()


    summary = {}
    for i in range(7):
        day = start_date + timedelta(days=i)
        summary[day] = {
            'billable_time': 0,
            'nonbillable_admin_time': 0,
            'nonbillable_training_time': 0,
            'unavailable_time': 0,
            'total_time': 0
        }

    for entry in entries:
        entry_date = entry.DateofEntry  
        summary[entry_date]['billable_time'] += entry.billable_time or 0
        summary[entry_date]['nonbillable_admin_time'] += entry.nonbillable_admin_time or 0
        summary[entry_date]['nonbillable_training_time'] += entry.nonbillable_training_time or 0
        summary[entry_date]['unavailable_time'] += entry.unavailable_time or 0
        summary[entry_date]['total_time'] += entry.total_time or 0

    overall_totals = {
        'billable_time': sum([day_data['billable_time'] for day_data in summary.values()]),
        'nonbillable_admin_time': sum([day_data['nonbillable_admin_time'] for day_data in summary.values()]),
        'nonbillable_training_time': sum([day_data['nonbillable_training_time'] for day_data in summary.values()]),
        'unavailable_time': sum([day_data['unavailable_time'] for day_data in summary.values()]),
        'total_time': sum([day_data['total_time'] for day_data in summary.values()])
    }

    return render_template('view_summary.html', summary=summary, overall_totals=overall_totals, start_date=start_date, end_date=end_date)



@app.route('/previous_week', methods=['GET'])
def previous_week():
    selected_date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    previous_week_date = selected_date - timedelta(days=7)
    return redirect(url_for('view_summary', date=previous_week_date.strftime('%Y-%m-%d')))

@app.route('/next_week', methods=['GET'])
def next_week():
    selected_date = request.args.get('date', datetime.today().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    next_week_date = selected_date + timedelta(days=7)
    return redirect(url_for('view_summary', date=next_week_date.strftime('%Y-%m-%d')))












# # Route for home page (protected)
# @app.route('/error')
# def error():
#     if 'EMPID' not in session:
#         return redirect(url_for('login'))

#     emp = Employee.query.filter_by(EMPID=session['EMPID']).first()
#     return render_template('error/error.html',emp=emp,)

# @app.errorhandler(404)
# def page_not_found(e):
#     if 'EMPID' not in session:
#         return redirect(url_for('login'))

#     emp = Employee.query.filter_by(EMPID=session['EMPID']).first()
#     return  redirect(url_for('error'))





if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
