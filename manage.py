"""manage.py."""
import os
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from bucketlist import db, create_app
# from app import models

app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


# manually create_db
@manager.command
def create_db():
    """Create db from models."""
    db.create_all()
    print ('Database created!')


# manually drop db
@manager.command
def drop_db():
    """Drop db tables."""
    if prompt_bool("Are you sure you want to drop the database?"):
        db.drop_all()
        print ('Database has been dropped!')


if __name__ == '__main__':
    manager.run()
