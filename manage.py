"""manage.py."""
import os
from flask_script import Manager, prompt_bool
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
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


if __name__ == '__main__':
    manager.run()
