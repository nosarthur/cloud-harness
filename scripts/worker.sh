#!/bin/bash

curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py

python -m pip install virtualenv
cd /home/ec2-user/
virtualenv venv
source venv/bin/activate
python -m pip install requests
python -m pip install boto3

yum update -y
yum install git -y
git clone https://github.com/nosarthur/cloud-harness-worker.git
