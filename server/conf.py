# -*- coding: utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1111@localhost/sev_steklo'
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = "../nuxt_app/static/img/articles/"
