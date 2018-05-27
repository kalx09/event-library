### Event-library
This repository contains python based library to collect events from multiple projects into mysql database.

---

# Installation

## Requirements
- Install external python library pymysql by executing below command on terminal:
    - pip install pymysql
- MysqlDb
    - Make sure port 3306 is open for mysql connection.
    - Populate required database schema using below command, where event is the database name.
		- mysql -u root event < event_db.sql

# How to run

## app.py
- app.py is a sample application which is using event library to create & capture events.
- To demonstrate usage of event library, app.py creates a 'user-login' event with event rule 'login-failed' & event verb 'failed'.
- If a user login fails for 5 times within 10 minutes then event library stores this event data.
- To test this, run this file 5 times within 10 minutes which will do the loging failure for 5 times. Hence,
it shall satisfy the event rule.
- This file also call get_event_data() which outputs the event data.
- If you want to create a new event with different rule, call the appropriate apis to do so.

# Documentation
- Each module of event library is documented with python docstrings along with the required & optional arguments.
- PEP8 coding standard is followed throughout the project.

# Assumptions
- Each event name (noun) is unique. For example, event db holds only one record with name 'user-login'.
- There needs to be a event rule for each event. For example, user login needs to be failed for atleast 5 times within 10 minutes in order to store it into the database.
