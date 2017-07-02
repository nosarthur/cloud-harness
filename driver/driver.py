import requests


# curl -X POST -d "{'token': 'asdfasdfasdfasdfadf'}"
#      -H 'Content-Type: application/json' 127.0.0.1:5000/jobs/

url = 'http://127.0.0.1:5000/jobs/'
header = {'Content-Type': 'application/json', 'Accept': 'text/plain'}


class Job(object):
    def __init__(self, priority=0):
        self.priority = priority
# FIXME: calculate token from user
        self.token = 'user2'

    def submit(self):
        data = {'token': self.token, 'priority': self.priority}
        r = requests.post(url, json=data)
        print(r.status_code)


if __name__ == '__main__':
    j = Job()
    j.submit()
