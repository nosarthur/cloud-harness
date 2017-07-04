# cloud-harness

[![Build Status](https://travis-ci.org/nosarthur/cloud-harness.svg?branch=master)](https://travis-ci.org/nosarthur/cloud-harness)

A wep application for AWS management.

## features

* API access to jobs with JWT authentication
* S3 storage

## script

* Add user

`python manager.py adduser`

* Initialize database 

`python manager.py initDB`

* Migrate database

```
python manager.py db migrate
python manager.py db upgrade
```

* Testing

`python manager.py test`

* Run local server 

`python manage.py runserver`
