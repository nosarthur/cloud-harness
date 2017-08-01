#!/bin/bash

curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py

sudo python -m pip install virtualenv
virtualenv venv
source venv/bin/activate
sudo python -m pip install boto3

git clone https://github.com/nosarthur/cloud-harness-worker.git
