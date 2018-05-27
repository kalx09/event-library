### Event-library
This repository contains python based library to collect events from multiple projects into mysql database.

---

# Installation

## Requirements
- Install external python library pymysql by executing below command on terminal:
    pip install pymysql
- MysqlDb
    - Make sure port 3306 is open for mysql connection.
    - Populate required database schema using below command, where event is the database name.
		mysql -u root event < event_db.sql

