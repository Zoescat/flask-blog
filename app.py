from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from apps import create_app
from exts import db
from apps.user.models import User
from apps.article.models import *
app = create_app()

manager = Manager(app=app)

# 命令工具
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    print(app.url_map)
    manager.run()
