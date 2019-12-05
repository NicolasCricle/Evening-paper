from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand  

from apps import create_app
from apps.wechat.models import db


app = create_app("config")
manager = Manager(app)

migrate = Migrate(app, db)  
manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()

