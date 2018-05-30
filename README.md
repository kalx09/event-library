### Event-library
This repository contains python based library to collect events from multiple projects into mysql database.

---

# Installation

## Requirements
- Python version 3.5
- Install external python library pymysql by executing below command on terminal:
    - pip install pymysql
- MysqlDb
    - Make sure port 3306 is open for mysql connection.
    - Create a database "event" in mysql. (user=root, password="")
    - Populate required database schema using below command, where 'event' is the database name & event_db.sql is a mysql dump file which is located under project's root directory.
		- mysql -u root event < event_db.sql

# How to run

## Example usage (app.py)
- app.py is a sample application which uses event library to create & capture events.
- To demonstrate usage of event library, app.py creates couple of events 
	- Event noun 'user-login' & event verb 'failed' with below event rule.
		- 'login-failed' - If a user login fails for 5 times within 10 minutes then event library capture & store this event details as a custom event ('login-failed-alert')
	- Event noun 'content-access' & event verb 'success' with below event rule.
		- 'access-success' - If content-access event is called for 5 times within 2 minutes then event library capture & store this event details as a custom event ('access-success-alert')
- To test this, run this file 5 times with below command within 2 minutes which shall do the login failure & content access for 5 times respectively. Hence, satisfying their respective/precreated event rules.
	- python3.5 app.py
- This module (app.py) also make a call to library's get_event_data() api which outputs the requested/filtered event data.
- If you want to create a new event with different rule on the fly, call the appropriate apis to do so.

# Documentation
- Each module of event library is documented with python docstrings along with the required & optional arguments, return type & exception thrown if any.
- PEP8 coding standard is followed throughout the project.

# Assumptions
- Event library trigger's add event when a new rule is added for a particular defined noun and verb. If the precreated rule is matched then a custom event with pattern "rulename-alert" is saved into db. For example, a rule name "access-success" with 5 no of events in 2 minutes is matched for event noun ("content-access") & verb ("success") then event library shall store custom event name "access-success-alert" to db.
