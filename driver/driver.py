import requests


# curl -X POST -d "{'token': 'asdfasdfasdfasdfadf'}"
#      -H 'Content-Type: application/json' 127.0.0.1:5000/jobs/

url = 'http://127.0.0.1:5000/jobs/'
auth_url = 'http://127.0.0.1:5000/auth/'
header = {'Content-Type': 'application/json', 'Accept': 'text/plain',
          'Authorization': 'JWT asdfasdfa'}


class Job(object):
    def __init__(self, priority=0):
        self.priority = priority
        self.token = ''

    def login(self, email, password):
        data = {'email': email, 'password': password}
        r = requests.post(auth_url, json=data)
        if r.status_code == 200:
            self.token = r.json()['token']
            print self.token
        else:
            print 'Login failed.'

    def submit(self):
        data = {'token': self.token, 'priority': self.priority}
        r = requests.post(url, json=data)
        if r.status_code != 201:
            print 'Submission failed.'

    def update(self, job_id, priority):
        r = requests.put(url + str(job_id), json={'priority': priority})
        if r.status_code != 204:
            print 'Update failed.'

    def start(self, job_id):
        r = requests.put(url + str(job_id), json={'status': 2})
        print(r.status_code)

    def stop(self, job_id):
        pass


if __name__ == '__main__':
    j = Job()
    j.login('a@a.com', 'aaa')
    # j.login('test@test.com', 'aaa')
    j.submit()
    j.update(3, 3)
