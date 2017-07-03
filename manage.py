import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app import db
from app.models import User


app = create_app(os.getenv('FLASK_CONFIG') or 'development')
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def initDB(drop=False):
    drop and db.drop_all()
    db.create_all()


@manager.command
def adduser(email, name='test'):
    '''Register a new user.'''
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    db.create_all()
    user = User(name, email, password)
    db.session.add(user)
    db.session.commit()
    print('User {0} was registered successfully.'.format(user))


@manager.command
def test():
    from subprocess import call
    call()


if __name__ == '__main__':
    manager.run()
