# -*- coding: utf-8 -*-
from flask import Blueprint, request
from ..models import Delivery
from ..common.Check_pass import check_pass
import json
delivery_api = Blueprint('delivery_api', __name__)

@delivery_api.route('/api/delivery/get-delivery-list/', methods=['GET','POST'])
def get_category_list():
    if request.method == 'GET':
      return json.dumps(Delivery.get_all_region())

@delivery_api.route('/api/delivery/set-delivery', methods=['GET','POST'])
def set_new_region():
    check_pass(password=request.form['pass'])
    if request.method == 'POST':
      return json.dumps(Delivery.set_new_region(request.form['region'], request.form['price']))

@delivery_api.route('/api/delivery/del-delivery', methods=['GET','POST'])
def del_region():
    if request.method == 'POST':
        check_pass(password=request.form['pass'])
        Delivery.del_region(request.form['id'])
        return 'OK'
