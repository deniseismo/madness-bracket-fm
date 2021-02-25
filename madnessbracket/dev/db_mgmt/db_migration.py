import os
import sys

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from madnessbracket import create_app, db
from madnessbracket.models import Album, Artist, Song, User

app = create_app()
app.app_context().push()


migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
