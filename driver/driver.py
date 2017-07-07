import requests


# curl -X POST -d "{'token': 'asdfasdfasdfasdfadf'}"
#      -H 'Content-Type: application/json' 127.0.0.1:5000/jobs/

url = 'http://127.0.0.1:5000/api/jobs/'
auth_url = 'http://127.0.0.1:5000/auth/'
headers = {'Content-Type': 'application/json', 'Accept': 'text/plain',
          'Authorization': 'Bearer asdfasdfa'}


class Job(object):
    def __init__(self, priority=0):
        self.priority = priority
        self.token = ''
        self.headers = headers

    def login(self, email, password):
        data = {'email': email, 'password': password}
        r = requests.post(auth_url, json=data)
        if r.status_code == 200:
            self.token = r.json()['token']
            self.headers['Authorization'] = 'Bearer ' + self.token
            print self.token
        else:
            print 'Login failed.'

    def submit(self):
        data = {'priority': self.priority}
        r = requests.post(url, json=data, headers=self.headers)
        if r.status_code != 201:
            print 'Submission failed.'

    def update(self, job_id, priority):
        r = requests.put(url + str(job_id), json={'priority': priority},
                         headers=self.headers)
        if r.status_code != 204:
            print 'Update failed.'

    def start(self, job_id):
        r = requests.put(url + 'start/'+ str(job_id), json={'status': 2},
                         headers=self.headers)
        print(r.status_code)

    def stop(self, job_id):
        pass


if __name__ == '__main__':
    j = Job()
    j.login('a@a.com', 'aaa')
    # j.login('test@test.com', 'aaa')
    j.submit()
    j.update(3, 3)
