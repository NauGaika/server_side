# -*- coding: utf-8 -*-
from ..models import Common_props
from .. import db
from flask import abort

def check_pass(password):
    result = Common_props.check_pass(password)
    if result == 'ok':
        return
    abort(403)
