from app import app


class AppTests:

    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

        assert not app.debug

    def tearDown(self):
        pass
