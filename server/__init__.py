# -*- coding: utf-8 -*-
from flask import Flask
import os
import sys
# from .conf import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
basedir = os.path.join(basedir, 'server.db')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1111@localhost/sev_steklo'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = "../sitenuxt/sevsteklo/static/img/articles/"

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from . import models, routes
