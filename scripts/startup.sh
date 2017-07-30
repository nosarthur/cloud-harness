#!/bin/bash

echo "prerequisite"
pip install -r requirements.txt

echo "start the worker monitoring"


# start the http server
gunicorn cloud-harness:app -p cloud-harness.pid -D

