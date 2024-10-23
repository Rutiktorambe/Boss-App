# Boss-App

```password
HYDRAxJonathan
Latur@4255
```

### Select database

```bash
sqlite3 ems_user.db
```

### Views Table in current DB

```bash
.tables
```

### Check the Schema of Tables

```bash
.schema EMS_users
```

```bash
.schema timesheet_entries
```

### Views Data from tables

```bash
SELECT * FROM EMS_users;
```

```bash
.ta
```

### export data to csv

1. Select column Mode

```bash
   .mode column
```

2. Select CSV Mode

```bash
.mode csv
```

3.  Output file Name

```bash
    .output EMS_details.csv
```

4. Query to get export data

```bash
SELECT * FROM EMS_users;
```

.headers on

.quit

###

1.  Data Wrangler
