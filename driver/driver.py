import requests


# curl -X POST -d "{'token': 'asdfasdfasdfasdfadf'}"
#      -H 'Content-Type: application/json' 127.0.0.1:5000/jobs/

jobs_url = 'http://127.0.0.1:5000/api/jobs/'
workers_url = 'http://127.0.0.1:5000/api/workers/'
login_url = 'http://127.0.0.1:5000/auth/login'
headers = {'Content-Type': 'application/json', 'Accept': 'text/plain',
           'Authorization': ''}


class JobControl(object):
    def __init__(self, priority=0):
        self.priority = priority
        self.token = ''
        self.headers = headers

    def login(self, email, password):
        data = {'email': email, 'password': password}
        r = requests.post(login_url, json=data)
        if r.status_code == 200:
            self.token = r.json()['token']
            self.headers['Authorization'] = 'Bearer ' + self.token
            print(self.token)
        else:
            print('Login failed.')

    def submit(self):
        data = {'priority': self.priority}
        r = requests.post(jobs_url, json=data, headers=self.headers)
        if r.status_code != 201:
            print('Submission failed.')

    def update(self, job_id, priority):
        r = requests.put(jobs_url + str(job_id), json={'priority': priority},
                         headers=self.headers)
        if r.status_code != 204:
            print('Update failed.')

    def start(self, n_workers=1, price=None, job_id=None):
        # FIXME: add support to start a single job
        data = {}
        if job_id:
            data['job_id'] = job_id
        if price:
            data['price'] = price
        r = requests.put(workers_url + 'new/', json=data, headers=self.headers)
        print(r.status_code)

    def stop(self, job_id):
        pass


if __name__ == '__main__':
    jc = JobControl()
    jc.login('a@a.com', 'aaa')
    # jc.login('test@test.com', 'aaa')
    jc.submit()
    jc.update(3, 3)
    jc.start()
