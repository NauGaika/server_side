# -*- coding: utf-8 -*-
from flask import Flask
import os
import sys
from .conf import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from . import models, routes
