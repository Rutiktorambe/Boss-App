# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employee'
    EMPID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    EName = db.Column(db.String(255))
    DOJRS = db.Column(db.Date)
    DOJSIPL = db.Column(db.Date, nullable=True)
    Profile = db.Column(db.String(255))
    Status = db.Column(db.String(50))
    SIPLLEvel = db.Column(db.String(50))
    RSALevel = db.Column(db.String(50))
    EEMail = db.Column(db.String(255))
    IEMail = db.Column(db.String(255))
    Landline = db.Column(db.String(20))
    Mobile = db.Column(db.String(20))
    Ext = db.Column(db.String(10))
    Secretary = db.Column(db.String(255), nullable=True)
    SecretaryID = db.Column(db.String(255), nullable=True)
    SystemID = db.Column(db.String(255), nullable=True)
    Password = db.Column(db.String(255), nullable=False)  # Plain text for now
    Team = db.Column(db.String(255))
    LineManager = db.Column(db.String(255), nullable=True)
    LineManagerID = db.Column(db.String(255), nullable=True)

class TimesheetEntry(db.Model):
    __tablename__ = 'timesheet_entries'
    Uniq_ID = db.Column(db.String(50), primary_key=True)
    EmpID = db.Column(db.String(10))
    DateofEntry = db.Column(db.Date)
    StartTime = db.Column(db.Time, nullable=True)
    EndTime = db.Column(db.Time, nullable=True)
    Hours = db.Column(db.Float, nullable=True)
    Minutes = db.Column(db.Float, nullable=True)
    billable_time = db.Column(db.Float, nullable=True)
    nonbillable_admin_time = db.Column(db.Float, nullable=True)
    nonbillable_training_time = db.Column(db.Float, nullable=True)
    unavailable_time = db.Column(db.Float, nullable=True)
    total_time = db.Column(db.Float, nullable=True)
    AllocationType = db.Column(db.String(50), nullable=True)
    Category1 = db.Column(db.String(50), nullable=True)
    Category2 = db.Column(db.String(50), nullable=True)
    Category3 = db.Column(db.String(50), nullable=True)
    ProjectCode = db.Column(db.String(10), nullable=True)
    Comment = db.Column(db.String(255), nullable=True)
    Status = db.Column(db.String(20), nullable=True)
    SubmitDate = db.Column(db.Date, nullable=True)
    LastUploadDate = db.Column(db.Date, nullable=True)
    LastUpdatedBy = db.Column(db.String(50), nullable=True)
