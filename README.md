# cloud-harness

[![Build Status](https://travis-ci.org/nosarthur/cloud-harness.svg?branch=master)](https://travis-ci.org/nosarthur/cloud-harness)

A wep application for AWS management.

## components

python driver, HTTP server, database, and AWS worker

It has five components
* an HTTP server that provides API access
* a database to keep track of the users and jobs
* python driver code
* cloud workers (not included)
* web storge (not included)

## script


`python manager.py adduser`

For database 

`python manager.py initDB`

```
python manager.py db migrate
python manager.py db upgrade
```

For testing

`python manager.py test`
