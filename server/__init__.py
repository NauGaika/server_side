# -*- coding: utf-8 -*-
from flask import Flask
import os
# from .conf import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
basedir = os.path.join(basedir, 'server.db')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:5374fa7e@localhost/sevsteklo'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from . import models, routes
