import requests

# curl -X POST -d "{'token': 'asdfasdfasdfasdfadf'}"
#      -H 'Content-Type: application/json' 127.0.0.1:5000/jobs/


class JobControl(object):
    def __init__(self, priority=0, base_url='http://127.0.0.1:5000/'):
        self.priority = priority
        self.token = ''
        self.headers = {'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Authorization': ''}
        self.base = base_url

    def login(self, email, password):
        data = {'email': email, 'password': password}
        r = requests.post(self.base + 'auth/login', json=data)
        if r.status_code == 200:
            self.token = r.json()['token']
            self.headers['Authorization'] = 'Bearer ' + self.token
            print(self.token)
        else:
            print('Login failed.')

    def submit(self):
        data = {'priority': self.priority}
        r = requests.post(self.base + 'api/jobs/', json=data,
                          headers=self.headers)
        if r.status_code != 201:
            print('Submission failed.')

    def update(self, job_id, priority):
        r = requests.put(self.base + 'api/jobs/' + str(job_id),
                         json={'priority': priority},
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
        assert n_workers > 0 and n_workers < 6
        data['n_workers'] = n_workers
        r = requests.get(self.base + 'api/workers/new',
                         json=data, headers=self.headers)
        print(r.status_code)
        print(r.json())

    def stop(self, worker_id=None):
        data = {}
        if worker_id:
            data['worker_id'] = worker_id
        r = requests.delete(self.base + 'api/workers/' + str(worker_id),
                            json=data,
                            headers=self.headers)
        print(r.status_code)


if __name__ == '__main__':
    jc = JobControl()
    jc.login('a@a.com', 'aaa')
    # jc.login('test@test.com', 'aaa')
    if 0:
        jc.submit()
        jc.update(3, 3)
        jc.start()
    jc.stop(3)
