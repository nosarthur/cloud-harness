import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import create_app
from app import db


app = create_app(os.getenv('FLASK_CONFIG') or 'development')
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def initDB(drop_first=False):
    if drop_first:
        db.drop_all()
    db.create_all()


@manager.command
def migrate():
    pass


if __name__ == '__main__':
    manager.run()
