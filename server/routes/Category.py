# -*- coding: utf-8 -*-
from flask import Blueprint, request
from ..common import Category
category_api = Blueprint('category_api', __name__)

@category_api.route('/api/get-category_list/', methods=['GET','POST'])
def get_category_list():
    if request.method == 'GET':
      return Category.get_all_category()
