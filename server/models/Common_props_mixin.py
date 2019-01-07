# -*- coding: utf-8 -*-
import json
import html
import os
from .. import db

class Common_props_mixin(object):

    @classmethod
    def get_param(cls, r_name):
        find_param = cls.query.filter(cls.name == r_name).first()
        if find_param:
            return json.dumps(find_param.value)
        else:
            return json.dumps('Параметр {} не найден'.format(r_name))