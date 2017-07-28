# cloud-harness

[![Build Status](https://travis-ci.org/nosarthur/cloud-harness.svg?branch=master)](https://travis-ci.org/nosarthur/cloud-harness)

A wep application for AWS management.

## features

* API access to jobs with JWT authentication
* Start/stop AWS EC2 instances

## user guide

* use a linux or mac machine
* have psql installed and running
* have python and `pip` installed

After downloading the code, go to the project root folder, create a virtual environment and install the required packages

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

To start the server locally in development mode, run 

`python manage.py runserver`

In production, an environment variable `FLASK_CONFIG` should be set to `production`.
If not set, the app configuration defaults to `development`.

To add a regular user, run 

`python manager.py adduser abc@def.com -n "John Doe"`

To add an administrator user, run 

`python manager.py adduser abc@def.com -n "John Doe" -a`

* Initialize database 

`python manager.py initDB`

To migrate database, run

```
python manager.py db migrate
python manager.py db upgrade
```

To test code, run

`python manager.py test`


