```bash

CREATE TABLE IF NOT EXISTS employee (
    EMPID INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    EName VARCHAR(255),
    DOJRS TEXT,
    DOJSIPL TEXT,
    Profile VARCHAR(255),
    Status VARCHAR(50),
    SIPLLevel VARCHAR(50),
    RSALevel VARCHAR(50),
    EEMail VARCHAR(255),
    IEMail VARCHAR(255),
    Landline VARCHAR(20),
    Mobile VARCHAR(20),
    Ext VARCHAR(10),
    Secretary VARCHAR(255),
    SecretaryID VARCHAR(255),
    SystemID VARCHAR(255),
    Password VARCHAR(255) NOT NULL,
    Team VARCHAR(255),
    LineManager VARCHAR(255),
    LineManagerID VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS timesheet_entries (
    Uniq_ID VARCHAR(50) PRIMARY KEY,
    EName VARCHAR(255),
    EmpID VARCHAR(10),
    Team VARCHAR(255),
    LineManager VARCHAR(255),
    DateofEntry  DATE,
    TimestampEntry REAL,
    StartTime TEXT,
    EndTime TEXT,
    Hours REAL,
    Minutes REAL,
    billable_time REAL,
    nonbillable_admin_time REAL,
    nonbillable_training_time REAL,
    unavailable_time REAL,
    total_time REAL,
    AllocationType VARCHAR(50),
    Category1 VARCHAR(50),
    Category2 VARCHAR(50),
    Category3 VARCHAR(50),
    Category4 VARCHAR(50),
    Category5 VARCHAR(50),
    Category6 VARCHAR(50),
    ProjectCode VARCHAR(10),
    Comment VARCHAR(255),
    Status VARCHAR(20),
    SubmitDate TEXT,
    LastUploadDate DATE,
    Timestampupdate REAL,
    LastUpdatedBy VARCHAR(50)
);
```
