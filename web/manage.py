#!/usr/bin/env python

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from citizens.app import create_app
from citizens.database import db

app = create_app()
manager = Manager(app)


migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

if __name__ == "__main__":
    manager.run()
