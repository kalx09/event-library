### Event-library
This repository contains python based library to collect events from multiple projects into mysql database.

---

# Installation

## Requirements
- Install external python library pymysql by executing below command on terminal:
    - pip install pymysql
- MysqlDb
    - Make sure port 3306 is open for mysql connection.
    - Populate required database schema using below command, where 'event' is the database name & event_db.sql is a mysql dump file which is located under project's root directory.
		- mysql -u root event < event_db.sql

# How to run

## app.py
- app.py is a sample application which uses event library to create & capture events.
- To demonstrate usage of event library, app.py creates a 'user-login' event with event rule 'login-failed' & event verb 'failed'.
	- If a user login fails for 5 times within 10 minutes then event library capture & store this event details.
- To test this, run this file 5 times within 10 minutes which will do the loging failure for 5 times. Hence, it satisfies the event rule 'login-failed'.
- This module (app.py) also make a call to library's get_event_data() api which outputs the requsted event data.
- If you want to create a new event with different rule on the fly, call the appropriate apis to do so.

# Documentation
- Each module of event library is documented with python docstrings along with the required & optional arguments, return type & exception thrown if any.
- PEP8 coding standard is followed throughout the project.

# Assumptions
- Each event name (noun) needs to be unique. For example, event db can hold only one record with name 'user-login'. However, it can hold 'n' no of event data related to 'user-login'.
- There needs to be a event rule for each event. For example, user login needs to be failed for atleast 5 times within 10 minutes in order to store it into the database.
