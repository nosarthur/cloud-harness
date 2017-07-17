pip install -r requirements.txt

gunicorn cloud-harness:app -p cloud-harness.pid -D
