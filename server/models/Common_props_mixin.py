# -*- coding: utf-8 -*-
import json
import html
import os
import hashlib
from .. import db
from flask import abort

class Common_props_mixin(object):

    @classmethod
    def get_param(cls, r_name):
        find_param = cls.query.filter(cls.name == r_name).first()
        if find_param:
            return json.dumps(find_param.value)
        else:
            return json.dumps('Параметр {} не найден'.format(r_name))

    @classmethod
    def check_pass(cls, password):
        pass_db = cls.query.filter_by(name= 'admin_pass').first()
        password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        if pass_db.value == password:
            return 'ok'
        print(pass_db)
        abort(403)
